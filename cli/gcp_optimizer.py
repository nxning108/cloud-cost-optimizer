#!/usr/bin/env python3
"""Cloud Cost Optimizer — GCP Billing CSV Parser.

Parses GCP BigQuery billing export CSV files and generates
optimization recommendations.

Usage:
    python3 cli/gcp_optimizer.py analyze -i gcp-billing.csv
"""

import csv
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

OUTPUT_DIR = Path(__file__).parent.parent / "reports"


@dataclass
class GCPResource:
    account_id: str
    resource_type: str
    resource_id: str
    region: str
    total_cost: float
    total_usage: float
    usage_unit: str
    first_seen: str
    last_seen: str
    tags: dict = field(default_factory=dict)
    is_idle: bool = False
    idle_reason: str = ""


@dataclass
class Recommendation:
    resource_id: str
    resource_type: str
    action: str
    estimated_savings_monthly: float
    confidence: str
    description: str
    implementation_steps: list = field(default_factory=list)


class GCPCostAnalyzer:
    """Analyze GCP billing CSV exports for cost optimization."""

    CPU_IDLE_THRESHOLD = 5  # percent

    def __init__(self):
        self.resources: list[GCPResource] = []
        self.recommendations: list[Recommendation] = []

    def parse_gcp_csv(self, csv_path: str) -> list[GCPResource]:
        """Parse GCP BigQuery billing export CSV."""
        resources = []
        path = Path(csv_path)

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            grouped = {}

            for row in reader:
                try:
                    # GCP billing export fields
                    resource_id = (
                        row.get('resource.name', '') or
                        row.get('export.sub.resource.name', '') or
                        row.get('service.description', '')
                    )
                    if not resource_id:
                        continue

                    cost = float(row.get('cost', 0) or
                                  row.get('usage.amount', 0) or 0)
                    usage = float(row.get('usage.amount', 0) or
                                   row.get('usage.quantity', 0) or 0)

                    if resource_id not in grouped:
                        resource_type = self._infer_resource_type(
                            resource_id, row
                        )
                        grouped[resource_id] = {
                            'account_id': row.get('billing_account_id', ''),
                            'resource_type': resource_type,
                            'resource_id': resource_id,
                            'region': row.get('resource.location', '') or
                                       row.get('system_labels.goog-private-zone-region', ''),
                            'total_cost': 0,
                            'total_usage': 0,
                            'usage_unit': row.get('usage.unit', ''),
                            'first_seen': row.get('usage.start_time', ''),
                            'last_seen': row.get('usage.end_time', ''),
                            'tags': {},
                            'cost_per_day': [],
                            'usage_per_day': [],
                        }

                    entry = grouped[resource_id]
                    entry['total_cost'] += cost
                    entry['total_usage'] += usage
                    entry['cost_per_day'].append(cost)
                    entry['usage_per_day'].append(usage)

                    start = row.get('usage.start_time', '')
                    if start:
                        if start < entry['first_seen']:
                            entry['first_seen'] = start
                        if start > entry['last_seen']:
                            entry['last_seen'] = start

                except (ValueError, KeyError):
                    continue

            for rid, data in grouped.items():
                idle = False
                idle_reason = ""

                if data['usage_per_day']:
                    low_days = sum(
                        1 for u in data['usage_per_day']
                        if u < self.CPU_IDLE_THRESHOLD
                    )
                    if low_days > len(data['usage_per_day']) * 0.8:
                        idle = True
                        idle_reason = (
                            f"Usage below {self.CPU_IDLE_THRESHOLD} "
                            f"({low_days}/{len(data['usage_per_day'])} days)"
                        )

                resources.append(GCPResource(
                    account_id=data['account_id'],
                    resource_type=data['resource_type'],
                    resource_id=rid,
                    region=data['region'],
                    total_cost=round(data['total_cost'], 2),
                    total_usage=round(data['total_usage'], 2),
                    usage_unit=data['usage_unit'],
                    first_seen=data['first_seen'],
                    last_seen=data['last_seen'],
                    tags=data['tags'],
                    is_idle=idle,
                    idle_reason=idle_reason,
                ))

        self.resources.extend(resources)
        return resources

    def _infer_resource_type(self, resource_id: str, row: dict) -> str:
        """Infer GCP resource type from ID or row data."""
        service = row.get('service.description', '') or row.get('service.id', '')
        if 'Compute Engine' in service or 'N1' in resource_id or 'N2' in resource_id or 'N2D' in resource_id:
            return 'GCE'
        if 'Cloud SQL' in service or 'sql' in resource_id.lower():
            return 'CloudSQL'
        if 'Cloud Storage' in service or 'storage' in resource_id.lower():
            return 'GCS'
        if 'BigQuery' in service or 'bigquery' in resource_id.lower():
            return 'BigQuery'
        if 'Kubernetes' in service or 'GKE' in service:
            return 'GKE'
        if 'Cloud Functions' in service:
            return 'CloudFunctions'
        if 'Cloud Run' in service:
            return 'CloudRun'
        if 'Memorystore' in service or 'Redis' in service:
            return 'Memorystore'
        if 'DNS' in service:
            return 'DNS'
        if 'Network' in service or 'CDN' in service or 'Cloud Interconnect' in service:
            return 'Network'
        return 'Unknown'

    def generate_recommendations(self) -> list[Recommendation]:
        """Generate optimization recommendations."""
        recs = []

        for resource in self.resources:
            if resource.is_idle:
                if resource.resource_type == 'GCE':
                    recs.append(Recommendation(
                        resource_id=resource.resource_id,
                        resource_type=resource.resource_type,
                        action='stop-then-delete',
                        estimated_savings_monthly=resource.total_cost,
                        confidence='high',
                        description=f"Idle GCE VM — {resource.idle_reason}",
                        implementation_steps=[
                            "Verify no workloads are running",
                            "Take a snapshot of persistent disks",
                            "Stop the instance",
                            "Delete if confirmed unused after 7 days",
                        ],
                    ))
                elif resource.resource_type in ('GCS', 'Memorystore'):
                    recs.append(Recommendation(
                        resource_id=resource.resource_id,
                        resource_type=resource.resource_type,
                        action='review-and-downsize',
                        estimated_savings_monthly=resource.total_cost * 0.5,
                        confidence='medium',
                        description=f"Underutilized {resource.resource_type}",
                        implementation_steps=[
                            "Review access patterns",
                            "Consider Coldline or Archive storage class",
                            "Set up lifecycle policies",
                        ],
                    ))
                else:
                    recs.append(Recommendation(
                        resource_id=resource.resource_id,
                        resource_type=resource.resource_type,
                        action='review',
                        estimated_savings_monthly=resource.total_cost * 0.3,
                        confidence='low',
                        description=f"Low usage {resource.resource_type}",
                    ))

            # Committed Use Discounts
            elif resource.total_cost > 200 and resource.resource_type in ('GCE', 'CloudSQL', 'GKE'):
                recs.append(Recommendation(
                    resource_id=resource.resource_id,
                    resource_type=resource.resource_type,
                    action='committed-use-discount',
                    estimated_savings_monthly=resource.total_cost * 0.35,
                    confidence='high',
                    description=(
                        f"${resource.total_cost:.2f}/month — "
                        f"consider Committed Use Discounts (30-40% savings)"
                    ),
                    implementation_steps=[
                        "Review 12-month usage trends",
                        "Check if workload is stable",
                        "Purchase 1-year or 3-year commitment",
                        "1-year: ~30% savings, 3-year: ~40% savings",
                    ],
                ))

        self.recommendations.extend(
            sorted(recs, key=lambda r: r.estimated_savings_monthly, reverse=True)
        )
        return self.recommendations


def main():
    """CLI entry point for GCP billing analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Analyze GCP billing CSV for cost optimization'
    )
    parser.add_argument(
        'command', choices=['analyze', 'report'],
        help='Command to run'
    )
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-f', '--format', default='markdown',
                        choices=['markdown', 'json', 'csv'])
    parser.add_argument('-o', '--output', help='Output directory')

    args = parser.parse_args()
    analyzer = GCPCostAnalyzer()
    resources = analyzer.parse_gcp_csv(args.input)
    recs = analyzer.generate_recommendations()

    print(f"Parsed {len(resources)} GCP resources from {args.input}")
    print(f"Generated {len(recs)} recommendations")
    total = sum(r.estimated_savings_monthly for r in recs)
    print(f"Total potential savings: ${total:,.2f}/month")

    if recs:
        print(f"\n{'='*60}")
        print(f"Top Recommendations:")
        print(f"{'='*60}")
        for i, r in enumerate(recs[:10], 1):
            print(f"\n{i}. [{r.confidence.upper()}] {r.resource_type} {r.resource_id}")
            print(f"   Action: {r.action}")
            print(f"   Savings: ${r.estimated_savings_monthly:,.2f}/month")
            print(f"   {r.description}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Cloud Cost Optimizer — Azure Billing CSV Parser.

Parses Azure Cost Management exported CSV files and generates
optimization recommendations.

Usage:
    python3 cli/azure_optimizer.py analyze -i azure-billing.csv
"""

import csv
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

OUTPUT_DIR = Path(__file__).parent.parent / "reports"


@dataclass
class AzureResource:
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


class AzureCostAnalyzer:
    """Analyze Azure billing CSV exports for cost optimization."""

    CPU_IDLE_THRESHOLD = 5  # percent

    def __init__(self):
        self.resources: list[AzureResource] = []
        self.recommendations: list[Recommendation] = []

    def parse_azure_csv(self, csv_path: str) -> list[AzureResource]:
        """Parse Azure Cost Management CSV export."""
        resources = []
        path = Path(csv_path)

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            grouped = {}

            for row in reader:
                try:
                    # Azure CSV fields (varies by export format)
                    resource_id = (
                        row.get('ResourceId', '') or
                        row.get('resourceId', '') or
                        row.get('Resource group', '')
                    )
                    if not resource_id:
                        continue

                    cost = float(row.get('PreTaxCost', 0) or
                                  row.get('cost', 0) or
                                  row.get('Cost', 0) or 0)
                    usage = float(row.get('Quantity', 0) or
                                  row.get('usageQuantity', 0) or 0)

                    if resource_id not in grouped:
                        resource_type = self._infer_resource_type(
                            resource_id, row
                        )
                        grouped[resource_id] = {
                            'account_id': row.get('AccountID', ''),
                            'resource_type': resource_type,
                            'resource_id': resource_id,
                            'region': row.get('ResourceLocation', '') or
                                       row.get('resourceLocation', ''),
                            'total_cost': 0,
                            'total_usage': 0,
                            'usage_unit': row.get('UnitOfMeasure', ''),
                            'first_seen': row.get('Date', ''),
                            'last_seen': row.get('Date', ''),
                            'tags': {},
                            'cost_per_day': [],
                            'usage_per_day': [],
                        }

                    entry = grouped[resource_id]
                    entry['total_cost'] += cost
                    entry['total_usage'] += usage
                    entry['cost_per_day'].append(cost)
                    entry['usage_per_day'].append(usage)

                    date = row.get('Date', '')
                    if date:
                        if date < entry['first_seen']:
                            entry['first_seen'] = date
                        if date > entry['last_seen']:
                            entry['last_seen'] = date

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

                resources.append(AzureResource(
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
        """Infer Azure resource type from ID or row data."""
        provider = row.get('AzureService', '') or row.get('providerName', '')
        if 'VirtualMachine' in resource_id or 'Microsoft.Compute' in provider:
            return 'VM'
        if 'disk' in resource_id.lower() or 'Disk' in provider:
            return 'Disk'
        if 'sql' in resource_id.lower() or 'SqlServer' in provider:
            return 'SQL'
        if 'storage' in resource_id.lower() or 'Storage' in provider:
            return 'Storage'
        if 'cosmos' in resource_id.lower() or 'Cosmos' in provider:
            return 'CosmosDB'
        if 'aks' in resource_id.lower() or 'Kubernetes' in provider:
            return 'AKS'
        if 'function' in resource_id.lower() or 'Function' in provider:
            return 'Function'
        if 'appservice' in resource_id.lower() or 'AppService' in provider:
            return 'AppService'
        return 'Unknown'

    def generate_recommendations(self) -> list[Recommendation]:
        """Generate optimization recommendations."""
        recs = []

        for resource in self.resources:
            if resource.is_idle:
                if resource.resource_type in ('VM', 'AKS'):
                    recs.append(Recommendation(
                        resource_id=resource.resource_id,
                        resource_type=resource.resource_type,
                        action='terminate',
                        estimated_savings_monthly=resource.total_cost,
                        confidence='high',
                        description=(
                            f"Idle {resource.resource_type} - "
                            f"{resource.idle_reason}"
                        ),
                        implementation_steps=[
                            "Verify no workloads are running",
                            "Take a snapshot/backup",
                            "Deallocate the VM",
                            "Delete if confirmed unused after 7 days",
                        ],
                    ))
                elif resource.resource_type in ('Disk', 'Storage'):
                    recs.append(Recommendation(
                        resource_id=resource.resource_id,
                        resource_type=resource.resource_type,
                        action='snapshot-then-delete',
                        estimated_savings_monthly=resource.total_cost,
                        confidence='high',
                        description=(
                            f"Unused {resource.resource_type} - "
                            f"{resource.idle_reason}"
                        ),
                        implementation_steps=[
                            "Create a snapshot",
                            "Verify no mounts or attachments",
                            "Delete after 7-day grace period",
                        ],
                    ))
                else:
                    recs.append(Recommendation(
                        resource_id=resource.resource_id,
                        resource_type=resource.resource_type,
                        action='review',
                        estimated_savings_monthly=resource.total_cost * 0.5,
                        confidence='medium',
                        description=f"Underutilized {resource.resource_type}",
                    ))

            # Rightsizing recommendations
            elif resource.total_cost > 100:
                recs.append(Recommendation(
                    resource_id=resource.resource_id,
                    resource_type=resource.resource_type,
                    action='rightsize',
                    estimated_savings_monthly=resource.total_cost * 0.2,
                    confidence='medium',
                    description=(
                        f"${resource.total_cost:.2f}/month - "
                        f"consider reserved instances"
                    ),
                    implementation_steps=[
                        "Review usage patterns over 30 days",
                        "Check if Reserved Instances are available",
                        "Purchase 1-year RI for 30-40% savings",
                    ],
                ))

        self.recommendations.extend(
            sorted(recs, key=lambda r: r.estimated_savings_monthly, reverse=True)
        )
        return self.recommendations


def main():
    """CLI entry point for Azure billing analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Analyze Azure billing CSV for cost optimization'
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
    analyzer = AzureCostAnalyzer()
    resources = analyzer.parse_azure_csv(args.input)
    recs = analyzer.generate_recommendations()

    print(f"Parsed {len(resources)} Azure resources from {args.input}")
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

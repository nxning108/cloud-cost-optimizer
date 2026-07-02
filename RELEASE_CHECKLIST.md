# Release Checklist

## Pre-Release
- [ ] All tests passing (`python3 -m pytest tests/ -v`)
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in server.py
- [ ] README.md badges updated

## Release
- [ ] Tag release (`git tag -a v1.0.0 -m "Release v1.0.0"`)
- [ ] Push tags (`git push origin --tags`)
- [ ] Create GitHub release
- [ ] Upload binary artifacts (if applicable)

## Post-Release
- [ ] Update PyPI (if applicable)
- [ ] Update website
- [ ] Announce on Twitter/LinkedIn
- [ ] Submit to Product Hunt
- [ ] Monitor for issues

## Security
- [ ] Dependency audit (`pip audit`)
- [ ] No hardcoded secrets
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Input validation complete

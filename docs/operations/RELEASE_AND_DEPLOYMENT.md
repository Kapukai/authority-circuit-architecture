# Release and Deployment Operations

## Status

This procedure operationalizes delivery of the ACA working draft. It does not
change or approve normative ACA requirements.

## Authority and environments

- GitHub `main` is the canonical working source.
- Pull requests are the review and validation boundary.
- GitHub Actions produces candidate release artifacts.
- Sites may host a private concept demonstrator.
- Iceland staging is the production-equivalent acceptance environment.
- `kapukai.org` is the approved public library.
- Case-specific or non-public evidence must remain outside all public packages.

## Release gates

A candidate may advance only when:

1. canonical structure and state validation passes;
2. the standards PDF builds without error;
3. examples remain compatible with the Decision Proof Record schema;
4. the website visibly identifies its draft status;
5. generated caches, dependencies, backup files, and macOS metadata are absent;
6. the artifact manifest and outer checksums verify;
7. accessibility, privacy, security, and rights-impact review are recorded;
8. staging acceptance is recorded by an authorized maintainer.

## Build a candidate

From the repository root:

```bash
chmod +x scripts/package-release.sh
./scripts/package-release.sh
```

The `dist/` directory contains a ZIP, a tarball, and outer SHA-256 checksums.
The packaged directory contains `MANIFEST.sha256` for every included file.

## Verify a candidate

```bash
cd dist
sha256sum --check ACA-*.artifacts.sha256
tar -xzf ACA-*.tar.gz
cd ACA-*/
sha256sum --check MANIFEST.sha256
```

## Staging deployment

1. Record the source commit and artifact checksum.
2. Deploy only the clean candidate artifact to an isolated staging path.
3. Verify draft labels, routes, links, responsive behavior, and accessibility.
4. Confirm no private evidence or secrets are present.
5. Record acceptance, known limitations, and the intended production target.

Do not deploy directly from a developer Downloads folder, `.next`, or
`node_modules`. Do not treat a successful build as publication approval.

## Production promotion

Production promotion requires an immutable version tag and a recorded staging
acceptance. Deploy the exact verified artifact; do not rebuild it on the server.
After deployment, verify the production checksum and complete a smoke test.

## Rollback

Retain the previously accepted artifact and its checksums. If verification,
privacy, availability, or correctness fails:

1. stop promotion or remove the new route from service;
2. restore the immediately preceding verified artifact;
3. verify its checksum and smoke-test critical routes;
4. record the failure, affected version, time, and corrective action;
5. correct through a new pull request and versioned candidate.

Never overwrite or silently amend a published release.

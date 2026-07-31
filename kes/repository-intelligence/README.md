# KES-0003 — Repository Intelligence

A read-only repository observability system for Kapukai.

It inventories the repository, classifies components, maps imports and architecture references,
surfaces governance risks, and generates a human-readable critical-path dashboard.

## Run

```bash
python3 scripts/analyze.py /path/to/repository
```

## Outputs

`dist/latest/` contains JSON, Markdown, Graphviz DOT, HTML, and SHA-256 checksums.

KES-0003 observes. It does not move, delete, merge, publish, or repair repository content.

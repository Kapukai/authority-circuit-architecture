# Threat Model

| Risk | Control |
|---|---|
| Source modification | Writes only to the output directory |
| Report mistaken for truth | Labels inference and observation |
| Source execution | Repository code is parsed, never executed |
| Untracked work overlooked | Git worktree status is surfaced |
| Dependency graph overstated | Edges represent observed import syntax only |
| Generated directories dominate | Common generated directories are excluded |

KES-0003 does not preserve, commit, reorganize, or authorize repository content.

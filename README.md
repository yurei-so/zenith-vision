# Zenith Vision

Experiment-first perception and context fusion for Guild Wars 2.

Zenith Vision tests a strict observation boundary before any model or UI is
promoted into Zenith:

- MumbleLink is authoritative for live game state such as map, position,
  heading, character, combat state, and camera orientation.
- Vision contributes only observations that telemetry cannot provide.
- Conflicting visual guesses never overwrite authoritative telemetry.
- Stale or disconnected telemetry becomes unavailable rather than being
  guessed from pixels.
- Every fused field carries provenance suitable for evaluation and audit.

The first checked-in experiment is CPU-only. It validates the contract and the
fail-closed fusion policy without downloading a model or reading a screen.

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
python3 -m unittest discover -s tests -v
./scripts/run-experiment contract_smoke
```

The fixed runner prefers `.venv/bin/python` when present so Agent Runtime uses
the repository's declared dependencies rather than ambient system packages.

See [docs/architecture.md](docs/architecture.md),
[docs/data-policy.md](docs/data-policy.md), and
[docs/experiment-contract.md](docs/experiment-contract.md).

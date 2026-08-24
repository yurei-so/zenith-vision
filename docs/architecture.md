# Architecture

Zenith Vision is an experiment boundary, not a second game client and not yet a
Zenith module.

```text
MumbleLink relay -- authoritative state --+
                                            +-- observation fusion -- structured context
window-scoped frame -- vision findings ----+
                                                    |
GW2 API / wiki / patch notes -- retrieval ----------+
```

## Authority rules

MumbleLink owns map, position, heading, character, combat state, game build, and
camera pose. Vision may observe UI regions, icons, text, encounter cues, and
other facts unavailable in telemetry. Reserved visual kinds are rejected even
when telemetry is absent or stale: unavailable state must stay unavailable.

The current adapter accepts the `PlayerSnapshot` JSON shape already emitted by
Zenith's relay. Zenith Vision does not copy or control that relay.

## Experimental progression

1. Contract and fusion policy (current).
2. Offline fixture ingestion with redaction and dataset manifests.
3. UI-region and icon baselines with held-out evaluation.
4. Window-scoped live observation under an explicit operator gate.
5. Optional advice composition using structured context plus retrieval.
6. Only after measured success: publish a stable observation contract that
   Zenith may consume.

No phase grants input control. GPU experiments enter through Agent Runtime and
roostd; telemetry normalization and CPU preprocessing do not need an accelerator
lease.

Pixel handling follows the reverse-reveal boundary documented in
[`redaction-boundary.md`](redaction-boundary.md): a new frame begins fully
obscured and only independently approved regions are copied through.

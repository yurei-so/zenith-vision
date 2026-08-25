# Roadmap

## Foundation

- [x] Normalize the existing Zenith MumbleLink relay contract.
- [x] Enforce telemetry authority and fail closed when it is stale.
- [x] Add provenance-bearing visual observations.
- [x] Add the fixed Agent Runtime experiment entrypoint.
- [x] Add digest-bound dataset manifests and privacy intake checks.
- [x] Add an independently testable reverse-reveal pixel boundary.
- [x] Add a fail-closed local OCR verification contract.
- [x] Validate real Tesseract output after the operator installs the OS package.
- [x] Add exact selected-window identity verification for XWayland captures.
- [x] Run the ephemeral zero-reveal smoke against an operator-approved GW2 window.
- [x] Build a deterministic, digest-bound synthetic UI-region corpus.
- [x] Precommit the first semantic UI-state architecture and abstention behavior.
- [x] Reject broad default geometry as a detector on a verified real holdout.
- [ ] Collect and review a small varied real holdout before selecting a model.

## Perception experiments

- [x] Establish a deterministic UI-region baseline and overlap metrics.
- [x] Add an inspectable CPU baseline for `present` / `absent` / `uncertain` HUD states.
- [x] Add a chat-masked, allowlisted title recognizer for Inventory and Hero panels.
- [ ] Validate Inventory and Hero recognition on varied Small-UI live scenes.
- [x] Freeze a recognition-disabled Small-UI panel holdout before visual-model training.
- [x] Evaluate and reject a compact global visual baseline on the frozen holdout.
- [ ] Build localized Hero-header/icon-rail and Inventory-grid evidence.
- [ ] Freeze a new holdout before evaluating the localized detector.
- [x] Cross-validate a frozen-backbone MobileNet panel classifier through roostd.
- [x] Collect corrective Hero-negative and Inventory-only development scenes.
- [x] Reject the corrective frozen-backbone run after cross-batch confounding persisted.
- [ ] Add class-specific, visually diverse negative development scenes.
- [ ] Freeze a development-only calibration gate for localized panel evidence.
- [ ] Freeze a real-holdout promotion gate before tuning the UI-state baseline.
- [ ] Label varied present/absent examples for objectives, skill bar, and minimap.
- [ ] Evaluate the frozen UI-state baseline on the real holdout.
- [ ] Evaluate icon classification on held-out licensed/synthetic fixtures.
- [x] Add OCR after independently testing the redaction policy.
- [ ] Measure latency and accuracy on the single 4070 through roostd.

## Integration gates

- [ ] Publish a versioned observation schema only after held-out evaluation.
- [ ] Prototype retrieval-backed advice without training mutable game facts.
- [ ] Design an optional Zenith consumer; do not embed experimental internals.
- [ ] Consider a dedicated live service only after the experiment proves useful.

## Ownership guardrail

- Zenith App owns live telemetry, maps, APIs, UI, and service lifecycle.
- Zenith Vision owns experiments and versioned vision evidence only.
- The one-shot live runner and fusion helper remain lab harnesses, never daemons.

# Data policy

- Default to synthetic and licensed public fixtures.
- User screenshots or frames require an explicit collection session and remain
  private unless separately approved for release.
- Collect only the selected game window, never the full desktop.
- Store derived labels and bounded crops where possible instead of raw frames.
- Strip chat, account names, character names, guild text, and other identifiers
  before a frame may enter an experiment corpus.
- Teacher-generated labels are untrusted until verified by a human or a
  precommitted evaluation rule.
- High-frequency MumbleLink samples are ephemeral. Persist only experiment
  fixtures or meaningful, privacy-reviewed summaries.
- Dataset manifests record source class, consent, redaction status, license,
  split, and content digest. Train and evaluation splits are immutable per run.
- Experiment output must not contain screenshots, OCR text, character names,
  absolute paths, prompts, or private source material.

An operator-approved review candidate is not a dataset item. It is stored in an
owner-only local state directory with a content digest and a receipt containing
no OCR text. Admission requires a later explicit review decision; merely
creating or viewing the candidate grants no training or transfer permission.

Privacy approval admits the reviewed candidate only as an unlabeled private
holdout. It does not make the image training-ready. The admission is bound to
the candidate digest, original consent receipt, non-release license, structural
mask policy, and an explicit `labels_verified: false` record.

Geometry-seeded labels remain proposals until a human reviews a visual overlay.
Masked chat and party/squad regions are excluded from the current proposal;
privacy approval never implies annotation approval.

An approved proposal becomes a separate digest-bound label file. The dataset
manifest, admission record, and proposal status are updated to preserve the
review chain; training and evaluation code reads labels only through that
manifest reference.

Bounded collection sessions revalidate the exact window on every attempt,
apply structural masks before retention, discard perceptual near-duplicates,
and stop at both a candidate ceiling and a wall-clock deadline. A batch remains
outside every dataset until its private contact sheet is approved.

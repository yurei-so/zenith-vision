# Labnote 007: Small-UI panel recognition

## Question

Can Zenith Vision recognize a concrete open Guild Wars 2 UI panel in a messy live
scene without retaining the full frame or emitting unrelated screen text?

## Precommitted scope

- UI profile: Small at 1920x1080.
- Allowed panel kinds: `inventory` and `hero`.
- Output states: recognized panel kinds, none, or uncertain.
- Privacy boundary: exact GW2 window, complete chat and party/squad masks before
  recognition, ephemeral full frame, allowlisted output only.
- Method: local sparse-screen OCR research followed by a fixed central panel
  search area, grayscale autocontrast, 2x enlargement, and dense-block OCR.

## Live sample

The operator presented an Inventory panel while another game dialog overlapped
the scene and the world continued rendering behind both panels. The first
whole-frame OCR configuration did not find the clearly visible title and
correctly emitted no supported panel. Preprocessing and constraining the search
area corrected that failure without lowering the confidence gate.

| Check | Result |
| --- | --- |
| Exact game window | Pass |
| Active UI profile | Small |
| Chat and party/squad masked | Yes |
| Full frame retained | No |
| Supported panel recognized | `inventory` |
| Title confidence | 0.963 |
| Unrelated OCR text emitted | No |
| Unit suite | 79 passing |

## Decision

- Continue UI recognition research with real, varied Small-UI scenes.
- Preserve abstention for incomplete or low-confidence supported titles.
- Collect Hero, no-panel, and additional Inventory holdout examples before
  describing the recognizer as validated.
- Keep the scanner one-shot and experimental. Zenith App remains responsible
  for any future live lifecycle or presentation.

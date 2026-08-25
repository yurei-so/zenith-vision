# Localized panel frozen holdout

Evaluates one content-addressed localized panel candidate against four separately
frozen, balanced Small-UI holdout segments. It never trains, calibrates, changes
the threshold, or emits per-sample predictions.

The frozen promotion gate requires at least 87.5% aggregate exact accuracy,
at least 75% exact accuracy in each staged panel state, and no class above a
12.5% aggregate false-call-plus-miss rate. A failed gate is a preserved
scientific result, not permission to tune against the holdout.

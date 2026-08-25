# Localized panel transfer

Extracts frozen MobileNet V3 Small embeddings from a fixed set of Hero
header/icon-rail and Inventory-grid proposals. Independent multiple-instance
classifier heads learn from sample-level labels and score only their matching
region family.

The experiment performs leave-one-development-batch-out evaluation. Its
promotion gate is frozen at 80% aggregate exact accuracy, at least 70% exact
accuracy in every fold, and no class with more than 20% aggregate false calls
plus misses. It never reads a spent or future holdout and has no live capture or
input-control capability.

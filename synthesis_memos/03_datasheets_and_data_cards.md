# Synthesis Memo: Datasheets + Data Cards

## Paper focus

- *Datasheets for Datasets* (Gebru et al.)
- *Data Cards* (Pushkarna et al.)

## Practical takeaway

Dataset quality is not only about data values. It is about transparent documentation of motivation, composition, collection, preprocessing, intended use, and limits.

## What we applied

- created `datasheet.md` with seven core sections
- added layered reporting style (telescopic/periscopic/microscopic)
- documented proxy-trace substitutions where Week 10 artifacts were unavailable
- linked quality controls (contamination checks, inter-rater agreement)

## Disagreement / adaptation

The papers assume mature datasets with stable upstream sources. Our setting is interim and synthetic-heavy, so we prioritized reproducible scripts + explicit caveat logging over exhaustive provenance metadata that does not exist yet.

## Actionable rule

If a claim cannot be traced to an artifact, it should not appear in memo/blog. This is enforced through `evidence_graph.json`.

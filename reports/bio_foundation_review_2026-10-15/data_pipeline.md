# Processing recipe for biological training data

[Model and dataset comparison](README.md)

## Processing diagram

![Corpus preparation: papers, web URLs and existing datasets become structured records, then undergo cleaning and deduplication.](assets/corpus_preparation.svg)

![Scoring and mixing: audit the scorer, compare sources and token ratios, and select the recipe through controlled continued-pretraining experiments. OpenThoughts3 contributes the experiment design; its reasoning SFT methods require separate validation.](assets/scoring_and_mixing.svg)

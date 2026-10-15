# BioReason-Pro

[Shared literature catalog](../README.md)

Biological multimodal reasoning model

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

**Training stage:** Supervised adaptation on synthetic reasoning, followed by reinforcement learning

**Source material and units:** UniProt-curated protein records with GO annotations, InterPro domains, STRING interactions and structural context; the author release describes 133,492 curated proteins, not full papers.

**Acquisition and document processing:** Structured biological records and protein representations; no paper-PDF extraction budget established in the imported source metadata.

**Generated or augmented material:** Author release describes GPT-5 reasoning traces for supervised training, kept distinct from the underlying biological records.

**Disclosure gaps:** Protein counts are not token counts. Native held-out evaluation cases and local raw outputs remain in the evaluation workspace.

**Source sections:** Official author README; native contract audit already retained by bio-evaluation.

## Primary sources

- [Primary paper v1](https://www.biorxiv.org/content/10.64898/2026.03.19.712954v1)
- [Official repository](https://github.com/bowang-lab/BioReason-Pro)

## Related evaluation notes

- [Evaluation workspace and retained protocol provenance](https://github.com/Some-random/bio-evaluation)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.

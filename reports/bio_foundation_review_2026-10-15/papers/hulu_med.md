# Hulu-Med

[Shared literature catalog](../README.md)

Medical vision-language generalist

This page consolidates existing reviewed sources. Author-reported results have not been reproduced here.

Historical medical context. Clinical-note acquisition is outside the biological research corpus scope.

**Training stage:** Alignment, medical CPT, mixed-modality SFT

**Backbone:** Open LLM decoder with patch-based vision encoder

**Source material and units:** 16.7M samples: 9M medical multimodal, 4.9M medical text, 1.3M general multimodal and 1.5M general text.

**Acquisition and document processing:** Uses public medical datasets, including literature-derived resources; sample count is not a distinct-paper count.

**Cleaning and filtering:** Dataset-specific processing and synthetic enrichment; the counts describe mixed text, images, volumes and videos.

**Training unit and mixture:** 2D alignment and CPT precede joint text/2D/3D/video instruction tuning; general data are included.

**Generated or augmented material:** Expand captions, create new long captions/VQA, multilingual reasoning and surgical-video annotations.

**Author-reported evidence:** Tests 30 benchmarks and ablates long-caption and reasoning augmentation; does not compare PDF text extractors.

**Disclosure gaps:** Clinical breadth should not be treated as proof that every scientific figure interpretation is grounded.

**Source sections:** Results: data and training; Methods; Extended Tables 4-6

## Primary sources

- [Hulu-Med report](https://arxiv.org/html/2510.08668v1)
- [Author repository](https://github.com/ZJUI-AI4H/Hulu-Med)

Corpus tokens, consumed training tokens, words, examples, papers and image tokens are different units. NR means not reported, not zero. Source versions and unresolved discrepancies are retained.

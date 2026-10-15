# Supporting literature

[Biological pretraining review](README.md)

These references inform data preparation or other training objectives. Their budgets are not biological CPT budgets.

## Reusable source corpora

- [S2ORC](papers/s2orc.md): Structured research text, metadata and citation links extracted from source papers.
- [peS2o](papers/pes2o.md): Cleaned text derived from S2ORC and Semantic Scholar; its reported token count uses whitespace tokenization.
- [Dolma](papers/dolma.md): General text corpus and curation toolkit with an academic component, not a biology-only dataset.

## Extraction and general training pipelines

- [OLMo 3](papers/olmo3.md): General pretraining/midtraining recipe using olmOCR PDFs and web data; its full token pool is not a biology budget.
- [Ryze](papers/ryze.md): Document extraction and synthetic SFT/RL data preparation; a processing reference, not a biological CPT run.

## Other biological training approaches

- [BioT5 / BioT5+](papers/biot5plus.md): T5-style denoising and biomolecule/text translation; a different objective from causal decoder CPT.
- [TxGemma](papers/txgemma.md): Task instruction tuning from Gemma 2; its 67B-token exposure is SFT, not CPT.
- [Tx-LLM](papers/txllm.md): Therapeutic task instruction tuning rather than a disclosed domain CPT stage.
- [BioReason](papers/bioreason.md): DNA encoder alignment, supervised adaptation and selected reinforcement learning.
- [BiomedCLIP / PMC-15M](papers/biomedclip.md): Contrastive image/text representation learning from paper figure-caption pairs.
- [BioReason-Pro](papers/bioreason_pro.md): Supervised biological reasoning adaptation and reinforcement learning.
- [ProtST](papers/protst.md): Protein/text representation alignment rather than autoregressive literature CPT.
- [UniGenX](papers/unigenx.md): Scientific sequence/coordinate generation; reviewed version and later repository capabilities differ.
- [STRIDE](papers/stride.md): Biological sequence instruction tuning and reinforcement learning.

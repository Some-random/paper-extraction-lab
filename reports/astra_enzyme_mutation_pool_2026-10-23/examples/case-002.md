# case-002 — PTEN phosphatase: mutation activity vs abundance

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (P60484, full canonical wild-type backbone; coordinate reference only):

```text
MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNL
CAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLL
HRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGT
CNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFI
PGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKT
VEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV
```


All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.

Published variants: C124S.

Supplied experimental observations:
- In a published yeast growth-rescue assay that reports PTEN lipid-phosphatase-associated function, wild-type PTEN rescues growth whereas C124S does not.
- In a separate published VAMP-seq experiment in cultured human cells, C124S has a normalized abundance score of 1.14 and falls in the wild-type-like abundance class. This is an abundance score, not a catalytic rate or a fold-change.
- The two results come from different experimental systems; no same-system protein-normalized catalytic rate is supplied.

**Question:** Which interpretation best combines these two measurements?

- **A.** C124S has wild-type-like human-cell abundance but fails yeast rescue; normal accumulation and successful functional rescue are distinct outcomes across these assays.
- **B.** C124S retains functional rescue despite low abundance in human cells, indicating that improved catalytic performance compensates for reduced protein accumulation.
- **C.** C124S has a catalytic score of 1.14 in human cells, so the growth result measures a decrease in protein abundance rather than function.
- **D.** C124S has reduced human-cell abundance and reduced yeast rescue, making deficient protein accumulation the directly measured common outcome in both experimental systems.


## Astra’s worked solution

A best combines the measurements because abundance and functional rescue are distinct assay outcomes.

Observed evidence: In the yeast assay, wild-type PTEN rescues growth whereas C124S does not. This demonstrates failure of the mutant to support the lipid-phosphatase-associated rescue phenotype under those conditions; it is not a direct measurement of protein abundance or a protein-normalized catalytic rate. Separately, human-cell VAMP-seq assigns C124S a normalized abundance score of 1.14 and places it in the wild-type-like abundance class. The score therefore supports normal accumulation in that assay, not low abundance, enhanced catalysis, or a 1.14-fold catalytic rate.

Mechanistic interpretation: Reference residues 123–130 are HCKAGKGR, placing C124 in the phosphatase catalytic motif. PTEN uses this cysteine's thiolate as a nucleophile during phosphate removal. Replacing cysteine with serine changes that active-site chemistry, making an activity defect compatible with continued protein accumulation. This provides a mechanistic explanation consistent with the observations, but it does not convert either assay into a direct catalytic-rate measurement or establish normal abundance in yeast.

Discriminating the choices: A accurately states both observations while keeping their experimental contexts separate. B reverses both results: rescue fails, and human-cell abundance is not classified as low; improved catalytic performance is unsupported. C incorrectly treats an abundance score as a catalytic score and reinterprets a functional rescue readout as an abundance measurement. D contradicts the wild-type-like human-cell abundance classification and incorrectly claims that deficient accumulation was directly measured in yeast.

The reusable principle is that a protein can accumulate normally yet fail a functional assay, particularly when an essential catalytic residue is altered.

## Final answer

A

## Astra’s stated limitations

The measurements come from different experimental systems. No yeast abundance measurement or same-system, protein-normalized catalytic rate is supplied, so these data cannot quantify intrinsic catalytic activity or establish that failed rescue is caused exclusively by a catalytic defect. Wild-type-like human-cell abundance does not establish unchanged folding or stability.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **PTEN phosphatase** — [UniProt P60484](https://www.uniprot.org/uniprotkb/P60484/entry).

Source-supported reference answer: **A**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not the complete tagged assay construct.

- Correctly separates wild-type-like human-cell abundance from failed yeast rescue and does not turn score 1.14 into a fold-change or catalytic rate.
- Adds a correct catalytic-cysteine explanation and explicitly limits what cross-system comparisons establish.

Source support:

- Figure 1A; Results describing growth rescue
- Wild-type PTEN rescues the growth defect; C124S does not. Methods use a 403-aa NP_000305 reference.
- Results on wild-type-like abundance of inactive variants, near Figure 4
- C124S is among inactive variants with wild-type-like abundance; its reported abundance score is 1.14.

Source qualifications:

- Do not treat score 1.14 as a 1.14-fold protein concentration.
- Do not infer that human-cell abundance measured the amount in the yeast assay.
- Catalytic impairment has stronger primary support than a specific folding or degradation mechanism.
- All substitutions use one-based coordinates in the full reference sequence, including the initial methionine. The sequence is a canonical coordinate reference, not a claim that complete tagged assay constructs have been reconstructed.
- Mighell2018 Methods: NM_000314.6, corresponding 403-aa NP_000305; current canonical record cross-references NP_000305.3. Full paper-assay construct sequence still requires final replay before release.
- VAMP-seq is an abundance assay in a different cellular system, not a direct PTEN catalytic-rate measurement.

Primary references:

- [A Saturation Mutagenesis Approach to Understanding PTEN Lipid Phosphatase Activity and Genotype-Phenotype Relationships](https://pmc.ncbi.nlm.nih.gov/articles/PMC5986715/)

- [Multiplex assessment of protein variant abundance by massively parallel sequencing](https://pmc.ncbi.nlm.nih.gov/articles/PMC5980760/)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.

# case-017 — APEX peroxidase: published variant comparison

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MGKSYPTVSADYQKAVEKAKKKLRGFIAEKRCAPLMLRLAWHSAGTFDKGTKTGGPFGTIKHPAELAHSA
NNGLDIAVRLLEPLKAEFPILSYADFYQLAGVVAVEVTGGPEVPFHPGREDKPEPPPEGRLPDATKGSDH
LRDVFGKAMGLTDQDIVALSGGHTIGAAHKERSGFEGPWTSNPLIFDNSYFTELLSGEKEGLLQLPSDKA
LLSDPVFRPLVDKYAADEDAFFADYAEAHQKLSELGFADA
```


Reference: Q43758. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
APEX: substitutions K14D, W41F, E112K; deletions none.
APEX2: substitutions K14D, W41F, E112K, A134P; deletions none.
VPGAPEX: substitutions K14D, W41F, E112K, A19V, A134P, D222G; deletions none.

Supplied assay observations:
- APEX2 has one additional substitution relative to APEX; VPGAPEX has three additional substitutions relative to APEX.
- The reported follow-up assays did not distinguish APEX2 from VPGAPEX, while the evolved variants improved on APEX.

**Question:** Which genotype-to-phenotype summary is justified by this comparison?

- **A.** APEX2 and VPGAPEX have matching assay performance because they carry the same set of additional substitutions relative to APEX.
- **B.** APEX2 improves on APEX with one added substitution; the extra VPGAPEX substitutions produce no further improvement detected in these assays.
- **C.** APEX2 and VPGAPEX both retain parent-level performance, despite carrying different numbers of additional substitutions relative to APEX.
- **D.** VPGAPEX improves on APEX2, associating an additional activity gain with its two extra substitutions beyond the APEX2 sequence.


## Astra’s worked solution

The relevant comparison is against the APEX parent, not against canonical wild type. All three variants share K14D, W41F, and E112K. Subtracting these shared substitutions gives:

- APEX2 relative to APEX: A134P only.
- VPGAPEX relative to APEX: A19V, A134P, and D222G.
- VPGAPEX relative to APEX2: A19V and D222G.

There are no listed deletions. Thus, APEX2 and VPGAPEX share A134P but do not carry identical sets of additional substitutions.

The supplied assay observations state that the evolved variants improved on APEX, while follow-up assays did not distinguish APEX2 from VPGAPEX. Therefore, APEX2 shows improved performance with one added substitution in the APEX background. The two further substitutions present in VPGAPEX are not associated with any additional improvement detected in those assays. This is exactly choice B.

Choice A is incorrect because the additional mutation sets differ. Choice C contradicts the observed improvement over APEX. Choice D claims a further gain over APEX2 that the assays did not detect.

The reusable principle is that mutation count does not determine phenotype: additional substitutions need not produce additive gains. Here, the evidence supports a shared improved assay outcome despite different genotypes, without establishing the individual effects or molecular mechanisms of the extra VPGAPEX substitutions.

## Final answer

B

## Astra’s stated limitations

The observations establish a comparative assay outcome, not its molecular mechanism. They do not distinguish effects on intrinsic catalysis, expression, stability, or other assay-dependent factors. Failure to distinguish APEX2 from VPGAPEX does not prove biochemical equivalence or show that A19V and D222G are individually neutral. The supplied sequence defines canonical coordinates, not the complete tagged assay construct.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **APEX peroxidase** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

Source-supported reference answer: **B**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly subtracts shared substitutions against the APEX parent and distinguishes the two extra VPGAPEX changes.
- Connects that genotype comparison to the assay result without equating nondetection of a difference with biochemical equivalence or individual mutation neutrality.
- The explanation teaches why additional substitutions need not yield additive gains.

Source support:

- Figure 1a; first Results section identifying evolved clones; Figure 2a–b
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- Indistinguishable in reported assays does not mean identical under every conceivable condition.
- Use corrected Figure 2a symbols and Figure 2e axis labels; correction dated December 10, 2014.

Primary references:

- [Directed evolution of APEX2 for electron microscopy and proximity labeling](https://www.nature.com/articles/nmeth.3179)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.

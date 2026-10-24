# 5. Locating repeated sequence motifs

## Question

Protein sequence:

```text
MSRHSRLQRQVLSLYRDLLRAGRGKPGAEARVRAEFRQHAGLPRSDVLRIEYLYRRGRRQLQLLRSGHAT
AMGAFVRPRAPTGEPGGVGCQPDDGDSPRNPHDSTGAPETRPDGR
```


**Question:** At which two residue ranges does the exact tripeptide LYR occur in this sequence? Number the first amino acid as residue 1.

**Choices:**

- **A.** Residues 15–17 and 54–56
- **B.** Residues 14–16 and 53–55
- **C.** Residues 16–18 and 55–57
- **D.** Residues 13–15 and 52–54

## Answer

Number the initial M as residue 1 and search for consecutive L–Y–R residues (leucine–tyrosine–arginine).

Residues 11–20 are VLSLYRDLLR: L is at 14, Y at 15, and R at 16. Thus the first match is 14–16.

Residues 51–60 are EYLYRRGRRQ: L is at 53, Y at 54, and R at 55. Thus the second match is 53–55. There are no other exact LYR occurrences.

Therefore, B is correct. Relative to the correct ranges, A shifts both windows one residue forward, C shifts them two residues forward, and D shifts them one residue backward.

**Final answer: B**

<details>
<summary>Sources, evidence checks and limitations</summary>

### Evidence check

Primary Results/Figure 2 passages support both LYR motif positions, which can also be counted exactly in the sequence. This example mainly tests indexing rather than deep biological reasoning.

### Answer limitations

None for this exact sequence-matching task; no functional or structural inference is needed.

### References and source review

The following information was **not supplied to AI**.

Verified source identity: **Succinate dehydrogenase assembly factor 1, mitochondrial** — [UniProt A6NFY7](https://www.uniprot.org/uniprotkb/A6NFY7/entry).

[Frozen UniProt annotation](../../astra_sequence_only_nine_2026-10-23/artifacts/case-002/uniprot_record.json), withheld from AI.

Source-supported answer: **B**. AI’s selected answer matches it.

The displayed sequence contains LYR exactly twice, at residues 14–16 and 53–55 using one-based numbering. The primary paper independently discusses those same two motifs. Its interaction experiments show that the first motif helps recruit the HSC20 iron-sulfur transfer machinery.

Scientific review: Supported sequence-indexing control.

- Both LYR occurrences and all distractor offsets are correct. This teaches exact indexing, with little biological inference; it is not counted as a deep biological example.

Exact-indexing control; limited biological depth

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- Finding the two motif positions is directly checkable from the sequence. Assigning their biological roles requires additional knowledge.
- The two identical tripeptides are not functionally interchangeable: experiments distinguish the first motif from the second, and neighboring residues matter.
- The pilot motif-location question does not independently test whether the model understands mitochondrial assembly or protein interactions.

Papers and experimental references:

- [Disease-Causing SDHAF1 Mutations Impair Transfer of Fe-S Clusters to SDHB.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4749439/). The primary paper maps both LYR motifs and reports interaction assays distinguishing the HSC20-binding first motif from the second. Review scope: Primary abstract via Europe PMC and primary paper Results/Figure 2 text available in web search; exact motif positions independently replayed against the canonical sequence.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

[Original source records and unchanged AI output](../../astra_sequence_only_nine_2026-10-23/examples/case-002.md)

</details>

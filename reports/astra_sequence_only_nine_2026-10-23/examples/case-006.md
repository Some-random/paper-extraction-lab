# case-006 — transmembrane

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MSSDFEGYEQDFAVLTAEITSKIARVPRLPPDEKKQMVANVEKQLEEARELLEQMDLEVREIPPQSRGMY
SNRMRSYKQEMGKLETDFKRSRIAYSDEVRNELLGDAGNSSENQRAHLLDNTERLERSSRRLEAGYQIAV
ETEQIGQEMLENLSHDREKIQRARDRLRDADANLGKSSRILTGMLRRIIQNRILLVILGIIVVIAILTAI
AFFVKGH
```

Task: transmembrane

Which overall membrane-association architecture best fits this protein sequence?

- **A.** A soluble peripheral membrane protein with no membrane-spanning segment.
- **B.** A protein with a large cytosolic region and a single membrane anchor near its C terminus.
- **C.** A seven-pass membrane receptor with short loops connecting its membrane-spanning helices.
- **D.** A secreted soluble protein whose only hydrophobic segment is a cleaved N-terminal signal peptide.

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

B is the best-supported architecture: a large cytosolic region with a single membrane anchor near the C terminus.

The strongest evidence is residues 193–214, ILLVILGIIVVIAILTAIAFFV. This 22-residue stretch is strongly hydrophobic and contains no charged residues. Its length and composition are appropriate for an alpha helix spanning a lipid bilayer; such helices commonly contain roughly 18–25 predominantly hydrophobic residues. Only KGH at positions 215–217 follows it, so the candidate anchor lies very close to the protein's C terminus.

In contrast, residues 1–192 contain frequent charged and polar residues and no other comparably long hydrophobic stretch. They therefore support a large region outside the membrane rather than additional transmembrane helices. The N-terminal 30 residues also lack the sustained hydrophobic core expected in a classical cleavable signal peptide. Together, these features support a C-terminally anchored architecture. The basic flank RRIIQNR at residues 186–192 is consistent with the positive-inside tendency, in which positively charged flanks preferentially lie on the cytosolic side. This strengthens, but does not prove, the inference that the large upstream region is cytosolic.

Comparison of the choices:
- A is disfavored because the sequence contains a conspicuous membrane-length hydrophobic segment, rather than lacking a membrane anchor.
- B matches the large nonmembrane region, single near-terminal hydrophobic segment, and very short following tail.
- C would require seven separate membrane-spanning hydrophobic segments; that repeated pattern is absent.
- D requires an N-terminal signal peptide and a soluble mature protein. Here, the strong hydrophobic segment is at the C terminus, not the N terminus.

Thus, B best accounts for both the number and location of the candidate membrane-spanning segments.

## Final answer

B

## Astra’s stated limitations

Sequence strongly supports one C-terminal membrane anchor, but exact membrane-spanning boundaries and membrane orientation cannot be established conclusively. The cytosolic location of the large upstream region is a well-supported topology inference, not a direct observation.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Vesicle transport through interaction with t-SNAREs homolog 1A** — [UniProt O89116](https://www.uniprot.org/uniprotkb/O89116/entry).

[Frozen UniProt annotation](../artifacts/case-006/uniprot_record.json), withheld from Astra.

Source-supported answer: **B**. Astra’s selected answer matches it.

The original Vti1-rp2 paper describes a 217-residue protein with a hydrophobic membrane anchor at its C terminus and an accessible cytoplasmic region. Antibody-based experiments identify it as an integral membrane protein enriched at the Golgi. This supports a large cytosolic region followed by a single C-terminal membrane anchor.

Scientific review: Strong sequence-based explanation.

- The long C-terminal hydrophobic stretch, short following tail and charged upstream region directly support the architecture. Cytosolic orientation is a weaker inference and is appropriately qualified.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- The strongly hydrophobic C-terminal stretch supports an anchor, but sequence alone does not establish the precise Golgi or endosomal destination.
- Treat the annotated anchor at residues 193-213 as a sequence-analysis boundary, not a membrane boundary measured in that paper.
- Do not confuse the soluble N-terminal domain with the whole protein being soluble: a tail anchor still makes the full protein integral to a membrane.

Papers and experimental references:

- [A 29-kilodalton Golgi soluble N-ethylmaleimide-sensitive factor attachment protein receptor (Vti1-rp2) implicated in protein trafficking in the secretory pathway](https://pubmed.ncbi.nlm.nih.gov/9705316/). The primary abstract explicitly reports 217 residues, a C-terminal hydrophobic anchor, a cytoplasmic region, integral membrane behavior and Golgi enrichment. Review scope: Primary PubMed abstract retrieved in search results; direct page opening encountered a browser challenge.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

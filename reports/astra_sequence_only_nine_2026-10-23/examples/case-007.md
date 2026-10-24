# case-007 — domain feature

Astra received only the student question below and the shared system instructions. Protein identity, gold answer, annotations and papers were withheld.

## Student question

Protein sequence:

```text
MVHIPSDVTPPRLCVVEKLNGENEYGYNLHAEKGRGQFVGTVDPDSPAERGGLITGDRIFAVNGHSIIGE
NHKKVVERIKANPNRCEMLVISEEGAKWYNENNVQITLDLPNIERVSPMSKETPVFVPPPPPPTDAMPYL
PRLAELNKGTPDQEFGFNLHAERGRGHFIGTVDAGGIGEKAGLEAGQRIVGVNGQLIYPTTGHKEVVALI
KKDTMKTTLLVASEDVDKYHKDHNIAYSWDNVERVDTRPVINVETHHHHEEVSVPKSNGYDVPPLNPHSI
QVNEEREISKMTTTTRTETITNSNSAYQYKESSTAYDAYATPPVDSNDLMDEVFGRVNLPGVTMSSHTEV
LPPTDDISSVSSLSSHRESAVDVPVSHQYVPSYATESHQKHEQHSQTHHHHHQHQQPSPLSNGSSHGYAA
SSTSGYDDDDIYHLSAREARERLRMKNRKHHLHEMSLNEKYQLVSNM
```

Task: domain feature

Which protein-interaction domain architecture is most consistent with this sequence?

- **A.** A WD40-repeat beta-propeller that lacks PDZ domains.
- **B.** Two SH2 domains specialized for recognizing phosphotyrosine-containing peptides.
- **C.** Two PDZ domains capable of recognizing short peptide motifs on partner proteins.
- **D.** A single SH3 domain specialized for recognizing proline-rich peptides.

The sequence is line-wrapped for readability; the exact original prompt is retained in `questions.jsonl` and the request artifact.

## Astra’s worked solution

C. Two PDZ domains is the most consistent architecture.

Sequence evidence:
The N-terminal portion contains two related-looking regions. Residues 24–43, EYGYNLHAEKGRGQFVGTVD, closely resemble residues 154–173, EFGFNLHAERGRGHFIGTVD. Similarity also occurs farther downstream: residues 59–80, IFAVNGHSIIGENHKKVVERIK, resemble residues 189–211, IVGVNGQLIYPTTGHKEVVALIK. Thus, the repetition is not confined to one short motif or a low-complexity run.

These extended patterns are characteristic of PDZ-like domain sequences: aromatic/glycine-containing early segments are followed by similarly organized hydrophobic and polar regions, including the recurring VNG-containing segment. Together, they support two related PDZ-sized modules. This is a family-level inference from the broader sequence pattern, not a claimed exact GLGF-motif match; PDZ sequences are variable and need not contain that literal string.

Biological interpretation:
PDZ domains are compact, usually approximately 80–110-residue α/β interaction modules. They commonly recognize short peptides at a partner protein's C terminus, accommodating the terminal carboxylate and nearby side chains in a binding groove. Some PDZ domains also recognize internal peptide motifs. This general interaction mechanism matches choice C, although the precise preferences of these two candidate domains cannot be assigned here.

Comparison with the alternatives:
• A: A WD40 β-propeller normally contains several shorter WD-repeat units. The WD at residues 239–240 is insufficient evidence: a single dipeptide does not establish a repeated propeller architecture. The extended PDZ-like duplication is more informative.
• B: SH2 domains can also occur in tandem, so repeat number alone would not distinguish them. However, the sequence does not show a convincing common SH2 phosphotyrosine-binding signature, such as an FLVRES-like region. Absence of that exact motif is not conclusive by itself, but there is positive evidence for PDZ-like repeats instead.
• D: Residues 128–133 are PPPPPP. Proline-rich sequences can be ligands for SH3 domains, but they are not themselves SH3 domains. SH3 domains are folded interaction modules, typically about 60 residues long; a single SH3 model also fails to account for the two extended PDZ-like regions.

Therefore, the strongest supported choice is a tandem-PDZ interaction-domain architecture.

## Final answer

C

## Astra’s stated limitations

Confidence applies to choosing the best architecture among the supplied alternatives. Sequence inspection does not establish exact domain boundaries, confirm that both domains bind peptides, or identify their physiological partners, preferred peptide sequences, or affinities.

Confidence reported by Astra: high.

## Post-generation verification

The following information was **not supplied to Astra**.

Verified source identity: **Na(+)/H(+) exchange regulatory cofactor-like protein nrfl-1** — [UniProt G5EDM4](https://www.uniprot.org/uniprotkb/G5EDM4/entry).

[Frozen UniProt annotation](../artifacts/case-007/uniprot_record.json), withheld from Astra.

Source-supported answer: **C**. Astra’s selected answer matches it.

The primary study identifies the selected C. elegans NRFL-1 isoform as a two-PDZ-domain scaffold. It combines domain comparisons with direct binding experiments involving the end of the AAT-6 transporter. The results support recognition of short partner-protein peptide motifs by PDZ domains.

Scientific review: Strong sequence-based explanation.

- Extended similarity across two regions supports tandem domains. The explanation avoids inventing a literal GLGF motif and distinguishes a proline-rich SH3 ligand from an SH3 domain.
- PDZ-family recognition depends on learned family knowledge; neither precise domain boundaries nor physiological partners are demonstrated from sequence alone.

Strong biological inference among the supplied choices

Retain as an assistant-reviewed quality-pilot draft; preserve all qualifications. Training benefit is not measured.

Source qualifications:

- The literal motif GLGF occurs zero times in this selected sequence. A solution must not claim it found one or two exact GLGF motifs. PDZ loop sequences can differ.
- Some NRFL-1 splice variants contain only one PDZ domain; the answer here is specific to the selected two-domain sequence.
- The particular AAT-6 interaction and preference for PDZ2 require the paper. They are not proven by spotting two interaction domains.
- The Results text says mutation of PDZ2 impairs binding; a duplicated phrase in the Figure 2 caption is inconsistent. Prefer the Results text and source annotation rather than repeating the caption typo.

Papers and experimental references:

- [NRFL-1, the C. elegans NHERF orthologue, interacts with amino acid transporter 6 (AAT-6) for age-dependent maintenance of AAT-6 on the membrane](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043050). Figure 1 and Results describe double-PDZ NRFL-1 isoforms; the interaction section and Figure 2 test recognition of the AAT-6 C-terminal motif. Review scope: Full primary article, especially NRFL-1 identification, Figure 1 and the PDZ interaction Results section.

Source review was performed by assistants, not expert human reviewers. A matching answer and source support do not establish that every explanatory claim is sound or that training will improve a model.

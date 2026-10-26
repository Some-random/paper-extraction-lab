# 7. Distinguishing interaction domains from ligand motifs

## Question

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

**Question:** Which protein-interaction domain architecture is most consistent with this sequence?

**Choices:**

- **A.** A WD40-repeat beta-propeller interaction scaffold.
- **B.** Two SH2 interaction domains for phosphotyrosine-containing peptides.
- **C.** Two PDZ interaction domains for short partner-protein peptides.
- **D.** One SH3 interaction domain for proline-rich partner peptides.

## Answer

**Answer: C.**

A reasonable hypothesis is a tandem arrangement of two PDZ-like interaction modules. The clearest sequence evidence is extended similarity between two regions of the N-terminal portion, rather than one short conserved word or a low-complexity repeat.

For example, EYGYNLHAEKGRGQFVGTVD at residues 24–43 resembles EFGFNLHAERGRGHFIGTVD at residues 154–173. Both contain related aromatic/glycine-rich portions followed by a similar GTVD-containing segment. The similarity continues farther along the candidate modules: IFAVNGHSIIGENHKKVVERIK at residues 59–80 resembles IVGVNGQLIYPTTGHKEVVALIK at residues 189–211. Agreement across separated parts of each region is more informative than matching a single short motif. It supports two related modules with internal sequence complexity.

The broader pattern is compatible with PDZ domains, compact interaction modules whose folded binding grooves often recognize short peptides at the C termini of partner proteins. Recognition can involve the partner’s terminal carboxylate and nearby side chains; some PDZ domains also recognize internal motifs. This explains how a tandem-domain protein could participate in partner recognition without identifying any particular partner. The PDZ assignment requires family knowledge: duplication alone would establish related regions, not uniquely name their fold. There is no literal GLGF motif in this sequence, so that familiar PDZ motif cannot be claimed as observed evidence here.

The PPPPPP stretch at residues 128–133 illustrates a different kind of sequence feature. A proline-rich segment could serve as a ligand for an SH3-containing partner. It is not itself evidence for the SH3 domain proposed in D. A ligand motif is a short recognition sequence; a domain is a larger folded module that performs recognition. Confusing the two would substitute a potential partner-binding site for a domain-architecture assignment.

A would require a repeated WD40 architecture, not merely an isolated WD pair. SH2 domains can also occur in tandem, so repeat count alone does not distinguish B from C. The broader PDZ-like patterns across separated parts of both modules provide the more specific support for C.

The sequence therefore supports tandem related interaction modules, with PDZ-like domains as a reasonable leading interpretation. It does not determine exact domain boundaries, prove that both modules bind peptides, establish their affinities or identify their physiological partners.

<details>
<summary>Sources and qualifications</summary>

Source identity: the tandem-PDZ NRFL-1 isoform, [UniProt G5EDM4](https://www.uniprot.org/uniprotkb/G5EDM4/entry). Some NRFL-1 splice variants contain only one PDZ domain; this example concerns the supplied two-domain sequence.

Primary reference: [NRFL-1, the C. elegans NHERF orthologue, interacts with amino acid transporter 6 (AAT-6) for age-dependent maintenance of AAT-6 on the membrane](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043050), especially Figure 1 and the PDZ-interaction Results.

The study supports the selected architecture and examines AAT-6 binding. The specific partner and PDZ2 preference come from the interaction Results, not from recognizing two sequence repeats. Domain boundaries, binding preferences and affinities remain separate from the anonymous sequence-based assignment.

</details>

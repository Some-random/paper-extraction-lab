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

What interaction-domain architecture is a reasonable hypothesis for this sequence? Use repeated sequence regions to support your assessment. Explain whether the proline-rich stretch identifies a folded interaction domain or could instead be a partner-binding motif, and state which conclusions about binding partners remain unsupported.

## Answer

Two PDZ-like interaction modules are a reasonable family-level hypothesis. EYGYNLHAEKGRGQFVGTVD resembles EFGFNLHAERGRGHFIGTVD, with additional downstream similarity between IFAVNGHSIIGENHKKVVERIK and IVGVNGQLIYPTTGHKEVVALIK. Extended repetition supports two related modules more than a single short motif does, although repetition alone does not uniquely identify PDZ domains. The PPPPPP stretch could be an SH3-binding ligand motif; it is not evidence that this protein contains an SH3 fold. No literal GLGF motif occurs, so that cannot be cited. Sequence inspection does not establish precise domain boundaries, whether both modules bind peptides, their affinities or their physiological partners.

## Assessment rubric

- Identifies extended similarity in two regions using actual sequence segments; does not rely only on a low-complexity run.
- Treats tandem PDZ-like modules as a hypothesis requiring family knowledge, not a deduction from repeat count alone. A cautious tandem-module answer can receive full credit if it explains why exact family identification remains uncertain.
- Distinguishes a potential proline-rich ligand motif from a folded SH3 domain; does not invent a literal GLGF motif.
- Separates architecture from precise boundaries, partner identity, functional binding and affinity. Credit another family hypothesis if it explains the extended sequence evidence and acknowledges its limitations.

<details>
<summary>Sources and review notes</summary>

The existing review identifies the selected sequence as the tandem-PDZ NRFL-1 isoform, UniProt G5EDM4. Some splice variants have one PDZ domain. The primary study supports the selected two-domain architecture and examines AAT-6 binding; the specific partner and PDZ2 preference are not supplied in the student input. The prior review preferred the Results text over an inconsistent duplicated phrase in the Figure 2 caption.

Primary reference: [NRFL-1, the C. elegans NHERF orthologue, interacts with amino acid transporter 6 (AAT-6) for age-dependent maintenance of AAT-6 on the membrane](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043050), especially Figure 1 and the PDZ-interaction Results.

This is a source-aware assistant revision of the existing source-checked example into an open-response task. The original full sequence is unchanged. No new experiment, measurement or variant is proposed. The question uses only the anonymous sequence and standard family knowledge; the source identity and experimental findings remain in these review notes. No expert human validation or measured training benefit is claimed.

</details>

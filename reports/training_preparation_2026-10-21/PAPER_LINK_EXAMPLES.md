# Two complete protein questions, with supporting papers

These are two actual examples from the training dataset. Each shows the **full protein sequence, original question, all answer choices, full training explanation, and selected answer**. Each letter in a sequence represents one amino acid, a building block of the protein.

The training explanations were generated from UniProt annotations. The separate plain-English paper explanations below show the supporting experiments in the cited papers; they were added afterward.

## 1. Where is VCCN2 found in a plant cell?

**In plain English:** Where inside a plant cell is this protein located?

**Full protein sequence (410 amino acids)**

```text
MYQSMNLSFSSNFTNLSFLKPRLYSGISARAPKSLHFKFNPSCVSSGPKSDDSPLSEKLISLLKAVPNWS
DGIKERRMQQKRSLYTHENWVRHRSSLRHLRHVSSSPSSRVILSLIPPVFFFTTVAILIAGYNSAVDLDW
LPDFFPVLRASPLPYQLTAPALALLLVFRTEASYSRFEQGRKAWVKIISGTNDLARLVISSVHGSGDELI
IRDALLRYIVAFPVALKCHVIYGSDIASDLKNVIEVDDLSLILQSKHRPRCVIQFISQSLQLLNLDSTKI
DMLETKMMQLQEGIGVCEQLMGIPIPLSYTRLTSRFLVLWHLTLPVILWDDCHWNVVPATFISAASLFCI
EEVGVLIEEPFSMLALDELCAMVLSNSDEAVESKEVIRNRIIAKKRILEIKHSSNGWHKS
```

**Original training question**

For this protein’s cellular-component task, which location is most specifically associated with its role as a chloride channel contributing to proton-motive-force partitioning?

**Answer choices**

- **A.** Chloroplast thylakoid membrane
- **B.** Mitochondrial inner membrane
- **C.** Chloroplast outer envelope
- **D.** Vacuolar membrane

**Full explanation used in training**

The protein is a voltage-dependent chloride channel associated with the chloroplast thylakoid membrane. Its role in moving anions across that membrane is consistent with influencing proton-motive-force partitioning across the thylakoid. The sequence’s hydrophobic regions are compatible with a membrane protein, but sequence features alone do not establish this specific cellular location.

**Final answer: A — Chloroplast thylakoid membrane.**

**What the paper shows, in plain English**

Chloroplasts are the parts of plant cells that carry out photosynthesis. Inside them are membranes called **thylakoids**. The researchers attached a fluorescent label to VCCN2 and saw it inside chloroplasts. They then separated the chloroplast into its different parts and detected the labelled protein in the thylakoid membrane. That supports **answer A**.

[Herdean et al. (2016), Figure 1 — read the supporting experiment](https://pmc.ncbi.nlm.nih.gov/articles/PMC4890181/).

This experiment supports VCCN2’s location. The paper’s direct measurements of chloride-channel activity were on the related protein VCCN1, so they do not directly verify every functional claim in the training explanation.

## 2. Which protein interacts with TCL2?

**In plain English:** Which other protein does this protein interact with?

**Full protein sequence (100 amino acids)**

```text
MDNTNRLRHLRSRKQSKFTLGDTAEVNSVKWEFINMTEQEEDLIFRMHRLVGDRWDLIAGRVVGREAKDI
ERYWIMRNCDHCSHKRRRVHKFYRFSISPP
```

**Original training question**

Which protein is the interaction partner associated with this protein?

**Answer choices**

- **A.** GL1
- **B.** TTG1
- **C.** EGL3
- **D.** GL3

**Full explanation used in training**

The supported protein-subunit association is an interaction with GL3, so D is correct. This identifies a protein interaction, not something that can be established from the amino-acid sequence alone; the sequence does not by itself distinguish GL3 from the other plausible regulatory proteins listed.

**Final answer: D — GL3.**

**What the paper shows, in plain English**

TCL2 helps regulate the tiny hairs on a plant’s surface. Proteins often do their jobs by interacting with other proteins. The researchers tested TCL2 and GL3 in plant cells using a system that gives a measurable signal when the two proteins interact. The signal appeared when TCL2 and GL3 were present together, but not with TCL2 alone. That supports **answer D: GL3**.

[Gan et al. (2011), Figure 6A — read the supporting experiment](https://pmc.ncbi.nlm.nih.gov/articles/PMC3264604/).

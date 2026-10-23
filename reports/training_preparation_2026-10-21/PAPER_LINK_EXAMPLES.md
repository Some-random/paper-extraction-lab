# Protein properties, training questions, and the papers behind them

We are building a dataset that connects a **protein sequence** to its **biological properties** and the **research supporting those properties**. For example: where is a protein found in a cell, or which other protein does it interact with?

## How the dataset is made

1. **Get the protein and its properties from UniProt.** UniProt records protein sequences, annotations about what the proteins do, and references to relevant papers.
2. **Use GPT-6 Luna to create questions and answers.** Luna receives the UniProt annotations to write multiple-choice questions, explanations, and answers. These generation calls did not receive the full papers. A separate Luna call checks the generated example.
3. **Link the evidence back to the papers.** We follow the recorded references to the original articles. For the two examples below, we also read the relevant experiments and explain how they support the answer.

For this first dataset, the original training explanations were generated from UniProt annotations; the papers were attached afterward. Below, each example presents the question and choices, the supporting paper evidence, and then Luna’s original training explanation and final answer. Both original papers are linked.

Each letter in a protein sequence represents one amino acid, a building block of the protein.

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

**What the paper shows, in plain English**

Chloroplasts are the parts of plant cells that carry out photosynthesis. Inside them are membranes called **thylakoids**. The researchers attached a fluorescent label to VCCN2 and saw it inside chloroplasts. They then separated the chloroplast into its different parts and detected the labelled protein in the thylakoid membrane. That supports **answer A**.

[Herdean et al. (2016), Figure 1 — read the supporting experiment](https://pmc.ncbi.nlm.nih.gov/articles/PMC4890181/).

This experiment supports VCCN2’s location. The paper’s direct measurements of chloride-channel activity were on the related protein VCCN1, so they do not directly verify every functional claim in the training explanation.

**Luna’s full explanation used in training**

The protein is a voltage-dependent chloride channel associated with the chloroplast thylakoid membrane. Its role in moving anions across that membrane is consistent with influencing proton-motive-force partitioning across the thylakoid. The sequence’s hydrophobic regions are compatible with a membrane protein, but sequence features alone do not establish this specific cellular location.

**Final answer: A — Chloroplast thylakoid membrane.**

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

**What the paper shows, in plain English**

TCL2 helps regulate the tiny hairs on a plant’s surface. Proteins often do their jobs by interacting with other proteins. The researchers tested TCL2 and GL3 in plant cells using a system that gives a measurable signal when the two proteins interact. The signal appeared when TCL2 and GL3 were present together, but not with TCL2 alone. That supports **answer D: GL3**.

[Gan et al. (2011), Figure 6A — read the supporting experiment](https://pmc.ncbi.nlm.nih.gov/articles/PMC3264604/).

**Luna’s full explanation used in training**

The supported protein-subunit association is an interaction with GL3, so D is correct. This identifies a protein interaction, not something that can be established from the amino-acid sequence alone; the sequence does not by itself distinguish GL3 from the other plausible regulatory proteins listed.

**Final answer: D — GL3.**

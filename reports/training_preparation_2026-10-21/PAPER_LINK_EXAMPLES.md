# Two protein questions, explained using research papers

Here are plain-English versions of two questions from our protein dataset. Each explanation below uses evidence from the linked paper.

## 1. Where in a plant cell is this protein found?

**Protein:** VCCN2.

**Question:** Where in a plant cell is VCCN2 found?

**Explanation from the paper:** Chloroplasts are the parts of plant cells that carry out photosynthesis. Inside them are membranes called **thylakoids**. The researchers attached a fluorescent label to VCCN2 and saw it inside chloroplasts. They then separated the chloroplast into its different parts and found the labelled protein in the thylakoid membrane. These observations support that location.

**Answer: In the chloroplast's internal membrane, called the thylakoid membrane.**

**Source:** Herdean et al. (2016), Figure 1. [Read the paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4890181/) · [Original training example](examples/vccn2.txt).

## 2. Which other protein does this protein interact with?

**Protein:** TCL2, which helps control the tiny hairs on a plant’s surface.

**Question:** Which other protein does TCL2 interact with?

**Explanation from the paper:** Proteins often work by contacting other proteins. The researchers tested TCL2 and GL3 in plant cells using a system that produces a detectable signal when the proteins interact. The signal appeared when TCL2 and GL3 were supplied together, but not with TCL2 alone. That supports GL3 as an interaction partner.

**Answer: GL3.**

**Source:** Gan et al. (2011), Figure 6A. [Read the paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3264604/) · [Original training example](examples/tcl2.txt).

*These questions and explanations are simplified for readability. The original training answers were generated from UniProt annotations; the paper-based explanations shown here were written afterward for this page. The original training examples are unchanged.*

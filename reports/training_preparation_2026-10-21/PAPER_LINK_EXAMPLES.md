# Three actual training examples linked to original papers

These are existing rows from the public 10,000-example SFT dataset, not newly invented demonstrations. Each link below follows **the exact sequence → its frozen UniProt record → the specific annotation used for the question → an explicit PubMed citation → the included original article**. The full training sequence, prompt, generated explanation, annotation evidence and paper checks are also recorded in [the small JSON companion](paper_link_examples.json).

**The teachers used UniProt annotation packets, not full papers.** Original articles were retrieved afterward for provenance. Here we additionally read those articles and checked a specific supporting passage for each selected answer. These are assistant source reviews, not expert human ground truth or proof that the sequence alone determines the answer.

Links use the immutable Hugging Face revision `181c177733b15feac8abcafa6da652bf83dfbe4f`.

| Existing training example | Exact protein | Answer | Original article |
|---|---|---|---|
| [sequence-mcq-judge-009](#case-1) | O80952, PGP1 / PGPS1 | A. Phosphatidylglycerol biosynthetic process | [PMID 27047516](https://pmc.ncbi.nlm.nih.gov/articles/PMC4800280/) |
| [judge:sequence-mcq-expansion-v1-00489](#case-2) | O80832, VCCN2 / BEST2 | A. Chloroplast thylakoid membrane | [PMID 27216227](https://pmc.ncbi.nlm.nih.gov/articles/PMC4890181/) |
| [judge:sequence-mcq-expansion-v1-01324](#case-3) | B3H4X8, TCL2 | D. GL3 | [PMID 22168948](https://pmc.ncbi.nlm.nih.gov/articles/PMC3264604/) |

<a id="case-1"></a>
## 1. PGP1 / PGPS1: Phosphatidylglycerol biosynthetic process

**Training ID:** `sequence-mcq-judge-009`. **Task:** `GO_biological_process`. [Exact training row and full sequence](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/train.jsonl#L4).

**Protein:** *Arabidopsis thaliana*, UniProt [O80952](https://www.uniprot.org/uniprotkb/O80952/entry), sequence version 1, 296 amino acids; gene `PGPS1 (synonym PGP1)`, locus `At2g39290`. Sequence starts `MLRSGLASLIVDVNLRRTLR` and ends `GLSVWSLAVYMRKIWKVLMK`. Its exact SHA-256 is `efe422219bada00a67564e4dde5ebcb919cad9fe3c82abbbb42bd229eaf51d29`.

**Actual question and choices**

Which biological process most directly describes the catalytic role of this protein?

A. Phosphatidylglycerol biosynthetic process
B. Chloroplast organization
C. Photosynthetic electron transport in photosystem II
D. Regulation of embryonic development

**Stored final answer: A — Phosphatidylglycerol biosynthetic process.**

**Why this paper is linked:** the selected annotation `GO:0006655 — phosphatidylglycerol biosynthetic process` at `/record/uniProtKBCrossReferences/43` explicitly cites PMID `27047516` with **ECO:0000315; IMP:UniProtKB (mutant-phenotype evidence)**. This is an annotation-level citation, not merely another paper in the record bibliography.

**Original paper:** Kobayashi K. et al. (2016). Multiple Impacts of Loss of Plastidic Phosphatidylglycerol Biosynthesis on Photosynthesis during Seedling Growth of Arabidopsis. DOI [10.3389/fpls.2016.00336](https://doi.org/10.3389/fpls.2016.00336); [PMID 27047516](https://pubmed.ncbi.nlm.nih.gov/27047516/); [PMC4800280](https://pmc.ncbi.nlm.nih.gov/articles/PMC4800280/). [Read the actual included paper text on Hugging Face](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/papers/PMC4800280.1/PMC4800280.1.txt) (CC-BY, version 1; [license](http://creativecommons.org/licenses/by/4.0/)).

**Where to look:** Abstract; Introduction; PGP1-knockout mutant results. Short verbatim passage:

> In this study, we characterized the photosynthesis of an Arabidopsis thaliana T-DNA insertional mutant (pgp1-2), which lacks plastidic PG biosynthesis.

**What the paper supports:** The article names the Arabidopsis PGP1 knockout and directly studies the loss of plastidic phosphatidylglycerol biosynthesis and its photosynthetic consequences. This supports the chosen biological-process answer. It is mutant-phenotype support, not a new purified-enzyme assay of every reaction detail stated in the generated explanation.

**Limit of this check:** The teacher explanation adds the enzyme reaction. This specific paper supports the biological process and mutant phenotype; it does not independently verify each enzyme-reaction detail or establish that the answer can be inferred from sequence alone.

**Generated explanation actually stored for training:**

The protein catalyzes transfer of a phosphatidyl group from CDP-diacylglycerol to glycerol-3-phosphate, producing phosphatidylglycerophosphate, an intermediate in phosphatidylglycerol synthesis. Chloroplast organization, photosystem II function, and embryonic development are associated biological outcomes, but they do not describe this direct catalytic process. The sequence alone does not establish that function.

<a id="case-2"></a>
## 2. VCCN2 / BEST2: Chloroplast thylakoid membrane

**Training ID:** `judge:sequence-mcq-expansion-v1-00489`. **Task:** `GO_cellular_component`. [Exact training row and full sequence](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/train.jsonl#L1840).

**Protein:** *Arabidopsis thaliana*, UniProt [O80832](https://www.uniprot.org/uniprotkb/O80832/entry), sequence version 1, 410 amino acids; gene `VCCN2 (synonym BEST2)`, locus `At2g45870`. Sequence starts `MYQSMNLSFSSNFTNLSFLK` and ends `IIAKKRILEIKHSSNGWHKS`. Its exact SHA-256 is `9b88b557cc487cc3e925ed46c3f7b24e474274c64972e84852e8e0881d331b64`.

**Actual question and choices**

For this protein’s cellular-component task, which location is most specifically associated with its role as a chloride channel contributing to proton-motive-force partitioning?

A. Chloroplast thylakoid membrane
B. Mitochondrial inner membrane
C. Chloroplast outer envelope
D. Vacuolar membrane

**Stored final answer: A — Chloroplast thylakoid membrane.**

**Why this paper is linked:** the selected annotation `GO:0042651 — thylakoid membrane` at `/record/uniProtKBCrossReferences/31` explicitly cites PMID `27216227` with **ECO:0000314; IDA:TAIR (direct-assay evidence)**. This is an annotation-level citation, not merely another paper in the record bibliography.

**Original paper:** Herdean A. et al. (2016). A voltage-dependent chloride channel fine-tunes photosynthesis in plants. DOI [10.1038/ncomms11654](https://doi.org/10.1038/ncomms11654); [PMID 27216227](https://pubmed.ncbi.nlm.nih.gov/27216227/); [PMC4890181](https://pmc.ncbi.nlm.nih.gov/articles/PMC4890181/). [Read the actual included paper text on Hugging Face](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/papers/PMC4890181.1/PMC4890181.1.txt) (CC-BY, version 1; [license](http://creativecommons.org/licenses/by/4.0/)).

**Where to look:** Results → AtVCCNs are thylakoid members of a conserved channel family; Figure 1. Short verbatim passage:

> Immunoblotting of chloroplast subfractions isolated from leaves of transformed plants revealed a location for both AtVCCNs in the thylakoid membrane

**What the paper supports:** The paper identifies At2g45870 as AtVCCN2 and distinguishes it from the close paralogue AtVCCN1. It reports chloroplast colocalization and thylakoid-fraction immunoblots for both proteins. Those results support the selected thylakoid-membrane location for this exact protein.

**Limit of this check:** O80832 is VCCN2, not VCCN1. The paper focuses its physiological and electrophysiological characterization on VCCN1; the demonstrated VCCN2 localization should not be treated as proof of every VCCN1 functional claim. The training question and rationale include a chloride-channel/PMF premise; the narrower localization answer is what this example verifies.

**Generated explanation actually stored for training:**

The protein is a voltage-dependent chloride channel associated with the chloroplast thylakoid membrane. Its role in moving anions across that membrane is consistent with influencing proton-motive-force partitioning across the thylakoid. The sequence’s hydrophobic regions are compatible with a membrane protein, but sequence features alone do not establish this specific cellular location.

<a id="case-3"></a>
## 3. TCL2: GL3

**Training ID:** `judge:sequence-mcq-expansion-v1-01324`. **Task:** `protein_subunit`. [Exact training row and full sequence](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/train.jsonl#L6726).

**Protein:** *Arabidopsis thaliana*, UniProt [B3H4X8](https://www.uniprot.org/uniprotkb/B3H4X8/entry), sequence version 1, 100 amino acids; gene `TCL2 (synonym CPL4)`, locus `At2g30424`. Sequence starts `MDNTNRLRHLRSRKQSKFTL` and ends `HCSHKRRRVHKFYRFSISPP`. Its exact SHA-256 is `1c02181978a4c844cd934e419a43098fa7c92d906ad182dea3ab24f43b929872`.

**Actual question and choices**

Which protein is the interaction partner associated with this protein?

A. GL1
B. TTG1
C. EGL3
D. GL3

**Stored final answer: D — GL3.**

**Why this paper is linked:** the selected annotation `Interacts with GL3` at `/record/comments/1/texts/0` explicitly cites PMID `22168948` with **ECO:0000269 (experimental evidence)**. This is an annotation-level citation, not merely another paper in the record bibliography.

**Original paper:** Gan L. et al. (2011). Functional characterization of TRICHOMELESS2, a new single-repeat R3 MYB transcription factor in the regulation of trichome patterning in Arabidopsis. DOI [10.1186/1471-2229-11-176](https://doi.org/10.1186/1471-2229-11-176); [PMID 22168948](https://pubmed.ncbi.nlm.nih.gov/22168948/); [PMC3264604](https://pmc.ncbi.nlm.nih.gov/articles/PMC3264604/). [Read the actual included paper text on Hugging Face](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/papers/PMC3264604.1/PMC3264604.1.txt) (CC-BY, version 1; [license](http://creativecommons.org/licenses/by/2.0)).

**Where to look:** Results → TCL2 interacts with GL3; Figure 6A. Short verbatim passage:

> indicating that TCL2 interacts with GL3 in plant cells

**What the paper supports:** The article identifies Arabidopsis At2g30424 as TCL2 and reports a cell-based protein-interaction assay with controls. Its Results and Figure 6A support interaction with GL3, which is exactly the selected answer.

**Limit of this check:** The paper supports the stated interaction under the reported experimental conditions. It does not make GL3 inferable from the letters of the sequence alone or establish that GL3 is the only possible interaction partner.

**Generated explanation actually stored for training:**

The supported protein-subunit association is an interaction with GL3, so D is correct. This identifies a protein interaction, not something that can be established from the amino-acid sequence alone; the sequence does not by itself distinguish GL3 from the other plausible regulatory proteins listed.

## How these three links were selected

1. Start from the immutable training row and match the entire sequence and its SHA-256 to the frozen provenance row.
2. Identify the exact selected annotation field and retain only a citation explicitly present in that annotation.
3. Confirm that PMID/DOI/PMCID map to an original paper already included in the public dataset with a verified permissive license and file hash.
4. Read the paper, check the exact gene/protein identity, and identify a passage supporting the selected answer. Do not substitute a better-studied paralogue or treat a multi-claim annotation as though each citation supported every sentence.

These three are deliberately inspectable examples, not a random accuracy audit of the entire dataset. A UniProt citation can refer to a particular experiment, phenotype or annotation claim; it does not necessarily mean the whole paper is about only that protein. The Hugging Face [SOURCE_GUIDE.md](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/SOURCE_GUIDE.md) and [full link table](https://huggingface.co/datasets/jiangdongwei/protein-sequence-reasoning-10k/blob/181c177733b15feac8abcafa6da652bf83dfbe4f/provenance/sequence_paper_links.csv) cover the broader dataset.

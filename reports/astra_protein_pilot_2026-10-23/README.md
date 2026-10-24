# CorA: one paper-grounded protein reasoning example

We gave GPT-6 Astra a real protein question, the supporting paper text, its correction notice and a curated UniProt annotation. The aim is to create a useful training demonstration for Qwen3.5-4B: connect sequence features with protein architecture and distinguish competing biological functions. The student receives the sequence and question; the references are additional teacher evidence.

**Teacher:** GPT-6 Astra · **Reasoning:** maximum effort, pro mode · **Generation time:** 3 minutes 15 seconds · **Usage-based cost:** approximately **$1.76**.

## Protein and question

This is **CorA from *Thermotoga maritima*** ([UniProt Q9WZ31](https://www.uniprot.org/uniprotkb/Q9WZ31/entry)), a 351-amino-acid protein. The actual student question already identifies the CorA family.

```text
MEEKRLSAKKGLPPGTLVYTGKYREDFEIEVMNYSIEEFREFKTTDVESVLPFRDSSTPTWINITGIHRT
DVVQRVGEFFGIHPLVLEDILNVHQRPKVEFFENYVFIVLKMFTYDKNLHELESEQVSLILTKNCVLMFQ
EKIGDVFDPVRERIRYNRGIIRKKRADYLLYSLIDALVDDYFVLLEKIDDEIDVLEEEVLERPEKETVQR
THQLKRNLVELRKTIWPLREVLSSLYRDVPPLIEKETVPYFRDVYDHTIQIADTVETFRDIVSGLLDVYL
SSVSNKTNEVMKVLTIIATIFMPLTFIAGIYGMNFEYMPELRWKWGYPVVLAVMGVIAVIMVVYFKKKKW
L
```

What is the best-supported functional role of the first transmembrane domain in this CorA-family transporter?

- A. It contributes to the central ion permeation pathway, with one such domain from each subunit surrounding the pathway.
- B. It forms an external scaffold that anchors the transporter to the membrane but does not contribute to ion passage.
- C. It acts as an ATP-hydrolyzing domain that supplies energy for active ion pumping.
- D. It serves as a cytoplasmic metal-sensing domain that binds ions but does not form part of the permeation pathway.

## What the paper supports

[Nordin et al. (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3629940/) describes the CorA membrane pore and its conserved ion-entry region. The selected UniProt annotation explicitly states that the first transmembrane domain from each of five subunits forms the central ion pathway. The [published correction](https://pmc.ncbi.nlm.nih.gov/articles/PMC3871142/) concerns colour figures and a Figure 7 caption; it does not change the pore assignment used here.

Read the [full paper text supplied to Astra](sources/cora_paper.txt), [annotation excerpt](sources/uniprot_annotation.json) and [four supporting evidence quotes](EVIDENCE.md).

## Astra’s worked solution

The CorA-family assignment is already provided. The sequence supports the expected C-terminal membrane organization. Using 1-based residue numbering, two prominent hydrophobic stretches are:

- Residues 293–313: VLTIIATIFMPLTFIAGIYGM, in the TM1 region.
- Residues 325–345: WGYPVVLAVMGVIAVIMVVYF, in the TM2 region.

The GMN signature at residues 312–314 lies within YGMNF at 311–315, near the end of the first membrane-spanning region. It is followed by MPEL at 318–321 before TM2. In known CorA topology, the GMN-containing region lies at the extracellular ion entrance, adjoining the short loop connecting the two membrane helices. These features are consistent with CorA's two C-terminal transmembrane helices and much larger N-terminal cytoplasmic region.

The decisive functional information comes from established CorA structure, not from hydrophobicity alone. CorA has a characteristic homopentameric assembly in which one TM1 helix from each of the five subunits surrounds the shared central ion-permeation pathway. TM1 therefore contributes to the pore wall through which divalent cations pass when the channel is open. The sequence identifies relevant hydrophobic segments and motifs, but does not independently establish this five-subunit arrangement.

The alternatives can therefore be distinguished as follows:

- A correctly describes the pore-forming contribution of TM1 from each subunit.
- B is inconsistent with TM1's central, pore-lining position. TM1 is not merely an external membrane anchor that is excluded from ion passage.
- C assigns an ATPase function to the wrong type of structural element. CorA functions as an ion channel, not as an ATP-hydrolyzing ion pump.
- D confuses cytoplasmic regulation with membrane permeation. CorA has cytoplasmic metal-binding sites that help regulate channel function, but the membrane-spanning TM1 segment itself contributes to the ion pathway.

The best-supported answer is A.

## Final answer

**A**

## Review and scope

The answer matches the source annotation. All five reported sequence ranges and four evidence quotes were checked. A separate AI assistant source review found the explanation scientifically defensible. This is not expert human validation.

The example applies known CorA architecture to a domain-function question. The family name is supplied, and the exact membrane boundaries and five-subunit arrangement rely on annotation and structural knowledge. No new sequence alignment, hydropathy prediction or structural calculation was run. Training benefit has not been measured, and this pilot has not been added to the existing training dataset.

Only a duplicated question-and-choices preface was removed from the displayed solution. The [original generated solution](ASTRA_ORIGINAL_WORKED_SOLUTION.txt) is preserved.

## Complete package

| Material | File |
| --- | --- |
| Exact student question | [student_question.txt](student_question.txt) |
| Plain-text question and solution | [EXAMPLE.txt](EXAMPLE.txt) |
| Original generated scientific output | [generated_output.json](generated_output.json) |
| Student example: sequence/question → worked solution and final letter | [student_example.jsonl](student_example.jsonl) |
| Actual teacher instructions | [generation_system_prompt.txt](generation_system_prompt.txt) |
| Teacher evidence and public request copy | [teacher_packet.public.json](teacher_packet.public.json), [generation_request.public.json](generation_request.public.json) |
| Model settings and measured usage/cost | [generation_settings.json](generation_settings.json), [usage_cost.json](usage_cost.json) |
| Sequence and quote checks; assistant source review | [offline_checks.json](offline_checks.json), [review.json](review.json) |
| Protein–paper provenance and attribution | [source_provenance.json](source_provenance.json), [SOURCES_AND_LICENSES.md](SOURCES_AND_LICENSES.md) |

The public request retains the scientific inputs and settings, with the account identifier removed. The full correction XML is replaced by a source link because redistribution terms were not verified. [reconstruct_request.py](reconstruct_request.py) restores that reference locally and checks its recorded hash; it makes no model-generation request. The cost includes internal reasoning and cache writes, calculated from API usage at [published standard rates](https://developers.openai.com/api/docs/models/gpt-6-astra).

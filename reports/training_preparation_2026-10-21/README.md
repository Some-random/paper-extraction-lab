# Protein mid-training: data and mixing

We are continuing training on Qwen3.5-4B with protein-related material to study how data sources and mixtures affect the model.

## Source data

| Source or dataset | Documents or examples | Tokens | Average length |
|---|---:|---:|---:|
| **Swiss-Prot** | 575.7K records | 3.66B | 6.35K per record |
| **PMC** | 9.09M papers | 99.7B | 11K per paper |
| **BioCollection** | 36.6M records | 36.5B | 995 per record |
| **FineWeb-Edu (filtered for bio)** | 11.8M pages | 9.14B | 775 per page |
| **QA post-training datasets** | | | |
| 10K QA post-training | 10K questions | 22.34M | 2.24K per example |
| 124K QA post-training | 124K questions | 270.28M | 2.18K per example |

The Swiss-Prot total scales the measured average from 100K selected records to 575.7K. Source collection counts used different tokenizers. The QA token counts use the Qwen3.5-4B tokenizer and include each question, reasoning trace, and answer once; multiple training epochs process the data again.

## Selecting and rewriting the data

We use a strong model to label biological relevance, then train a fastText classifier to rank documents.

We use **Qwen3.6-35B-A3B** to rewrite source records into clear biology text. The model is instructed to preserve supported facts and uncertainty, copy protein sequences exactly, and remove administrative material. Rewrites with detected protein-sequence changes are excluded.

**The current mid-training run trains on the rewrites, not the original records.** The original records are inputs to the rewriting model.

<details>
<summary>Swiss-Prot example: swissprot-P42562</summary>

**Original**

<p>&lt;ns0:entry xmlns:ns0="https://uniprot.org/uniprot" dataset="Swiss-Prot" created="1995-11-01" modified="2026-09-02" version="39"&gt;<br />
    &lt;ns0:accession&gt;P42562&lt;/ns0:accession&gt;<br />
    &lt;ns0:name&gt;FAR3_HIRME&lt;/ns0:name&gt;<br />
    &lt;ns0:protein&gt;<br />
        &lt;ns0:recommendedName&gt;<br />
            &lt;ns0:fullName&gt;FMRFamide-like neuropeptide YLRF-amide&lt;/ns0:fullName&gt;<br />
        &lt;/ns0:recommendedName&gt;<br />
    &lt;/ns0:protein&gt;<br />
    &lt;ns0:organism&gt;<br />
        &lt;ns0:name type="scientific"&gt;Hirudo medicinalis&lt;/ns0:name&gt;<br />
        &lt;ns0:name type="common"&gt;Medicinal leech&lt;/ns0:name&gt;<br />
        &lt;ns0:dbReference type="NCBI Taxonomy" id="6421" /&gt;<br />
        &lt;ns0:lineage&gt;<br />
            &lt;ns0:taxon&gt;Eukaryota&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Metazoa&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Spiralia&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Lophotrochozoa&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Annelida&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Clitellata&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Hirudinea&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Hirudinida&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Hirudiniformes&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Hirudinidae&lt;/ns0:taxon&gt;<br />
            &lt;ns0:taxon&gt;Hirudo&lt;/ns0:taxon&gt;<br />
        &lt;/ns0:lineage&gt;<br />
    &lt;/ns0:organism&gt;<br />
    &lt;ns0:reference key="1"&gt;<br />
        &lt;ns0:citation type="journal article" date="1991" name="Peptides" volume="12" first="897" last="908"&gt;<br />
            &lt;ns0:title&gt;Identification of RFamide neuropeptides in the medicinal leech.&lt;/ns0:title&gt;<br />
            &lt;ns0:authorList&gt;<br />
                &lt;ns0:person name="Evans B.D." /&gt;<br />
                &lt;ns0:person name="Pohl J." /&gt;<br />
                &lt;ns0:person name="Kartsonis M.A." /&gt;<br />
                &lt;ns0:person name="Calabrese R.L." /&gt;<br />
            &lt;/ns0:authorList&gt;<br />
            &lt;ns0:dbReference type="PubMed" id="1686933" /&gt;<br />
            &lt;ns0:dbReference type="DOI" id="10.1016/0196-9781(91)90035-n" /&gt;<br />
        &lt;/ns0:citation&gt;<br />
        &lt;ns0:scope&gt;PROTEIN SEQUENCE&lt;/ns0:scope&gt;<br />
        &lt;ns0:scope&gt;AMIDATION AT PHE-4&lt;/ns0:scope&gt;<br />
    &lt;/ns0:reference&gt;<br />
    &lt;ns0:comment type="subcellular location"&gt;<br />
        &lt;ns0:subcellularLocation&gt;<br />
            &lt;ns0:location&gt;Secreted&lt;/ns0:location&gt;<br />
        &lt;/ns0:subcellularLocation&gt;<br />
    &lt;/ns0:comment&gt;<br />
    &lt;ns0:comment type="similarity"&gt;<br />
        &lt;ns0:text evidence="2"&gt;Belongs to the FARP (FMRFamide related peptide) family.&lt;/ns0:text&gt;<br />
    &lt;/ns0:comment&gt;<br />
    &lt;ns0:dbReference type="GO" id="GO:0005576"&gt;<br />
        &lt;ns0:property type="term" value="C:extracellular region" /&gt;<br />
        &lt;ns0:property type="evidence" value="ECO:0000501" /&gt;<br />
        &lt;ns0:property type="project" value="UniProtKB-SubCell" /&gt;<br />
    &lt;/ns0:dbReference&gt;<br />
    &lt;ns0:proteinExistence type="evidence at protein level" /&gt;<br />
    &lt;ns0:keyword id="KW-0027"&gt;Amidation&lt;/ns0:keyword&gt;<br />
    &lt;ns0:keyword id="KW-0903"&gt;Direct protein sequencing&lt;/ns0:keyword&gt;<br />
    &lt;ns0:keyword id="KW-0527"&gt;Neuropeptide&lt;/ns0:keyword&gt;<br />
    &lt;ns0:keyword id="KW-0964"&gt;Secreted&lt;/ns0:keyword&gt;<br />
    &lt;ns0:feature type="peptide" id="PRO_0000043679" description="FMRFamide-like neuropeptide YLRF-amide"&gt;<br />
        &lt;ns0:location&gt;<br />
            &lt;ns0:begin position="1" /&gt;<br />
            &lt;ns0:end position="4" /&gt;<br />
        &lt;/ns0:location&gt;<br />
    &lt;/ns0:feature&gt;<br />
    &lt;ns0:feature type="modified residue" description="Phenylalanine amide" evidence="1"&gt;<br />
        &lt;ns0:location&gt;<br />
            &lt;ns0:position position="4" /&gt;<br />
        &lt;/ns0:location&gt;<br />
    &lt;/ns0:feature&gt;<br />
    &lt;ns0:evidence type="ECO:0000269" key="1"&gt;<br />
        &lt;ns0:source&gt;<br />
            &lt;ns0:dbReference type="PubMed" id="1686933" /&gt;<br />
        &lt;/ns0:source&gt;<br />
    &lt;/ns0:evidence&gt;<br />
    &lt;ns0:evidence type="ECO:0000305" key="2" /&gt;<br />
    &lt;ns0:sequence length="4" mass="598" checksum="69D4073B30000000" modified="1995-11-01" version="1"&gt;YLRF&lt;/ns0:sequence&gt;<br />
&lt;/ns0:entry&gt;</p>

**Rewrite**

<p>In the medicinal leech (<em>Hirudo medicinalis</em>), the neuropeptide YLRF-amide (UniProtKB accession P42562) is a member of the FARP (FMRFamide-related peptide) family. This peptide is secreted and localized to the extracellular region.<br />
<br />
The primary sequence of the mature neuropeptide consists of four amino acids: Tyrosine-Leucine-Arginine-Phenylalanine (YLRF). The phenylalanine residue at position 4 undergoes C-terminal amidation. This modification and the protein sequence were determined via direct protein sequencing. The peptide has a molecular mass of 598 Da.<br />
<br />
Protein existence is confirmed at the protein level. The identification was reported by Evans B.D., Pohl J., Kartsonis M.A., and Calabrese R.L. in a 1991 study published in <em>Peptides</em> (PubMed ID 1686933).</p>

</details>

<details>
<summary>BioCollection example: biocollection-000001-000000001223</summary>

**Original**

<p>Magnetosome protein MamT from Paramagnetospirillum magneticum (strain ATCC 700264 / AMB-1) is a protein. The functional descriptions of this protein are as follows: May play a role in magnetite crystal maturation (Probable). May transfer electrons to balance the Fe(2+)-Fe(3+) ratio during magnetite formation (Probable). Gene Ontology (GO) information indicates that this protein has the following annotations: molecular function annotations describe roles in metal ion binding, oxidoreductase activity; cellular component annotations show localization to magnetosome membrane. It has a length of 176 amino acids. The protein sequence is &lt;protein&gt;MSMEAPRRGRRWVSLGMIALLAAIGLGLYWDQLSTPSGITPATSPRRAEGLLLGRLPLPMEPS<br />LLSPLERLLEPPLRYKLMTIRHIPPVKPGTGMPHPYVGDCIQCHLMVGGPAAGSQFKTPYGAVLENLSRVRK<br />LGPPILPTSRQPHPPAGRCIKCHDIVVKVPVDKKGGMRWQL&lt;/protein&gt;.</p>

**Rewrite**

<p>MamT is a magnetosome protein found in <em>Paramagnetospirillum magneticum</em> (strain ATCC 700264 / AMB-1). The protein consists of 176 amino acids. Its sequence is:<br />
<br />
MSMEAPRRGRRWVSLGMIALLAAIGLGLYWDQLSTPSGITPATSPRRAEGLLLGRLPLPMEPSLLSPLERLL<br />EPPLRYKLMTIRHIPPVKPGTGMPHPYVGDCIQCHLMVGGPAAGSQFKTPYGAVLENLSRVRKLGPPILPTS<br />RQPHPPAGRCIKCHDIVVKVPVDKKGGMRWQL<br />
<br />
Gene Ontology (GO) annotations indicate that MamT is localized to the magnetosome membrane. Its molecular function includes metal ion binding and oxidoreductase activity.<br />
<br />
Functional descriptions suggest probable roles in magnetite crystal maturation and in transferring electrons to balance the Fe(2+)-Fe(3+) ratio during magnetite formation.</p>

</details>

<details>
<summary>PMC example: pmc-PMC7079415</summary>

[Sun et al. (2020), original paper](https://doi.org/10.1186/s11658-020-00210-3), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The original below is extracted text; the rewrite is model-generated.

**Original**

<p>miR-144-3p inhibits cell proliferation of colorectal cancer cells by targeting BCL6 via inhibition of Wnt/β-catenin signaling<br />
<br />
Background It has been shown that miR-144-3p regulates cell proliferation, apoptosis, migration and invasion in various cancers. However, the function and expression of miR-144-3p in colorectal cancer (CRC) remained obscure. Methods Immunohistochemical (IHC) staining was performed to investigate the protein expression of BCL6 in CRC tissues. The effect of BCL6 and miR-144-3p on CRC cells was explored through methylthiazolyl tetrazolium (MTT) assay, colony formation and cell cycle assays. Luciferase reporter assays, reverse transcription quantitative polymerase chain reaction (RT-qPCR) and Western blot assay were carried out to determine that BCL6 is directly regulated by miR-144-3p. Results Our results showed that miR-144-3p is down-regulated in CRC and correlates with the tumor progression of CRC patients. miR-144-3p inhibits cell proliferation and delays G1/S phase transition of CRC cells. Moreover, we found that BCL6 is a new target of miR-144-3p. Furthermore, BCL6 is a mediator of miR-144-3p repression of cell proliferation and cell cycle arrest in CRC cells. miR-144-3p repression of Wnt/β-catenin signaling is mediated by BCL6 in CRC cells. Conclusions Overall, the effect of the miR-144-3p/BCL6 axis on regulating CRC carcinogenesis was demonstrated, and miR-144-3p was identified as a potential prognostic and therapeutic target in colorectal cancer.<br />
<br />
MicroRNAs (miRNAs) are a class of noncoding RNAs ranging from 18 to 24 nt in length with involvement in endogenous regulation of post-transcriptional gene expression, resulting in gene silencing generally [ [bib_ref]MicroRNAs: genomics, biogenesis, mechanism, and function — Bartel[/bib_ref] ]. More and more evidence has indicated that miRNAs exhibit dysregulation in the diverse developmental process of different types of human cancer, suggesting that miRNAs play a vital role in different biological processes including cell proliferation, development, metastasis, apoptosis, and cell cycle progress [ [bib_ref]Adult-specific functions of animal microRNAs — Sun et al.[/bib_ref] [bib_ref]The functions of animal microRNAs — Ambros[/bib_ref] [bib_ref]Small molecule with big role: MicroRNAs in cancer metastatic microenvironments — Su et al.[/bib_ref] [bib_ref]MicroRNAs: small RNAs with a big role in gene regulation — He et al.[/bib_ref] ].<br />
<br />
Recent reports show that abnormal expression of miR-144-3p plays either tumor suppressor or oncogene roles in various cancers. For instance, miR-144-3p targets and regulates the expression of connexin 43, leading to the suppression of bone formation in distraction osteogenesis [ [bib_ref]MicroRNA-144-3p inhibits bone formation in distraction osteogenesis through targeting Connexin 43 — Sun et al.[/bib_ref] ]. miR-144-3p represses epithelial-to-mesenchymal transition of gastric cancer by down-regulating PBX3 [ [bib_ref]MicroRNA-144-3p suppresses gastric cancer progression by inhibiting epithelial-to-mesenchymal transition through targeting PBX3 — Li et al.[/bib_ref] ]. miR-144-3p exerts the effect of a tumor suppressor on glioblastoma through regulating c-Met [ [bib_ref]miR-144-3p exerts anti-tumor effects in glioblastoma by targeting c-met — Lan et al.[/bib_ref] ]. Moreover, in hepatocellular carcinoma (HCC), miR-144-3p acts as a tumor suppressor microRNA to regulate the progression of HCC [ [bib_ref]MicroRNA-144-3p suppresses tumor growth and angiogenesis by targeting SGK3 in hepatocellular carcinoma — Wu et al.[/bib_ref] , [bib_ref]A comprehensive insight into the clinicopathologic significance of miR-144-3p in hepatocellular carcinoma — Liang et al.[/bib_ref] ]. In pancreatic cancer, MiR-144-3p inhibits cell proliferation, migration, and invasion through targeting AP-1 transcription factor subunit (FOSB) and promotes cell apoptosis and cell cycle arrest by targeting proline-rich protein 11 [ [bib_ref]Liu S, Luan J, Ding Y. MiR-144-3p targets FosB Protooncogene, AP-1 transcription factor subunit (FOSB) to suppress proliferation, migration, and invasion of PANC-1 pancreatic Cancer cells. Oncol Res. 2018;26:683–90.10.3727/096504017X14982585511252PMC784473628653602[/bib_r<br />ef] , [bib_ref]miR-144-3p induces cell cycle arrest and apoptosis in pancreatic Cancer cells by targeting Proline-rich protein 11 expression via the mitogen-activated protein kinase signaling pathway — Li et al.[/bib_ref] ]. Furthermore, miR-144-3p presents an oncogene role in clear cell renal cell carcinoma (ccRCC) by regulating ARID1A [ [bib_ref]Mir-144-3p promotes cell proliferation, metastasis, Sunitinib resistance in clear cell renal cell carcinoma by Downregulating ARID1A — Xiao et al.[/bib_ref] ]. However, the function of miR-144-3p in CRC remained unknown.<br />
<br />
The BCL6 gene encodes a 95-kD nuclear phosphor protein belonging to the BTB/POZ/zinc finger (ZF) family of transcription factors [ [bib_ref]Cloning of bcl-6, the locus involved in chromosome translocations affecting band 3q27 in B-cell lymphoma — Ye et al.[/bib_ref] ]. BCL6 has been shown to modulate the expression of genes involved in B cell activation, differentiation, cell cycle arrest, and apoptosis [ [bib_ref]BCL6 controls the expression of the B7-1/CD80 costimulatory receptor in germinal center B cells — Niu et al.[/bib_ref] [bib_ref]Specific peptide interference reveals BCL6 transcriptional and oncogenic mechanisms in B-cell lymphoma cells — Polo et al.[/bib_ref] [bib_ref]BCL-6 represses genes that function in lymphocyte differentiation, inflammation, and cell cycle control — Shaffer et al.[/bib_ref] [bib_ref]Direct repression of prdm1 by Bcl-6 inhibits plasmacytic differentiation — Tunyaplin et al.[/bib_ref] ]. In addition, BCL6 could target the transcription of two critical oncogenes, MYC and BCL2, leading to MYC deregulated expression to regulate cell growth [ [bib_ref]BCL6 suppression of BCL2 via Miz1 and its disruption in diffuse large B cell lymphoma — Saito et al.[/bib_ref] ]. A previous study showed that BCL6 targets many genes belonging to multiple functional pathways including toll-like receptors, INF-R, a variety of cytokines, TGF-R, and WNT signaling [ [bib_ref]Integrated biochemical and computational approach identifies BCL6 direct target genes controlling multiple pathways in normal germinal center B cells — Basso et al.[/bib_ref] ]. We found that miR-144-3p inhibited cell proliferation of colorectal cancer cells. Moreover, β-catenin as a therapeutic target for colon cancer led us to explore the role of miR-144-3p in the Wnt/β-catenin signaling pathway [ [bib_ref]Therapeutic potential of targeting Wnt/beta-catenin pathway in treatment of colorectal Cancer: rational and Progress — Bahrami et al.[/bib_ref] ]. However, the role of BCL6 in CRC remained unclear.<br />
<br />
Herein, we found that that miR-144-3p is down-regulated in CRC and correlated with the tumor progression of CRC patients. We demonstrated that miR-144-3p inhibits cell proliferation and delays G1/S phase transition of CRC cells. Moreover, we found that BCL6 is a new target of miR-144-3p. Furthermore, BCL6 is a mediator of miR-144-3p repression of cell proliferation and cell cycle arrest in CRC cells. miR-144-3p repression of Wnt/β-catenin signaling is mediated by BCL6 in CRC cells. Together, our findings may provide a new molecular biomarker and therapeutic target to shed light on the carcinogenic mechanism of colorectal cancer.<br />
<br />
Twenty pairs of CRC tissues and adjacent non-tumor tissues were collected from Tianjin Ninghe Hospital. This study was performed in accordance with the ethical standards of the institutional committee.<br />
<br />
HCT116 and SW480 cells were cultured in RPMI 1640 medium supplemented with 10% fetal bovine serum (FBS), 100 mg/mL streptomycin, and 100 IU/mL penicillin. HCT116 cells were maintained in a humidified incubator with 5% CO_(2) at 37 °C. All the transfection was performed with Lipofectamine 2000 transfection reagent (Invitrogen, Carlsbad, CA, USA) according to the manufacturer’s protocol.<br />
<br />
Total RNA was isolated from CRC tissues and cells with the mirVana miRNA Isolation Kit (Ambion, Austin, TX, USA) according to the manufacturer’s instructions. The RNAs were reversely transcribed into cDNAs with random primers and the miRNA inverse transcription primers: miR-144-3p RT: 5′-GTCGTATCCAGTGCAGGGTCCGAGGTGCACTGGATACGACAGTACA-3′; U6-RT: 5′-GTCGTATCCAGTGCAGGGTCCGAGGTGCACTGGATACGACAAAATATGG-3′. The following primers were designed for PCR detection: miR-144-3p-S, 5′-TGCGGTACAGTATAGATGAT-3′, miR-144-3p-AS, 5′-CCAGTGCAGGGTCCGAGGT-3′; U6-S, 5′-TGCGGGTGCTCGCTTCGGCAGC-3′, U6-AS,5′-CCAGTGCAGGGTCCGAGGT-3′; BCL6-S, 5′-TCCTCGGAAGATGAGATTGC-3′, BCL6-AS, 5′-GTTGAGCACGATGAACTTGTA-3′; β-actin-S, 5′-CTACGTCGCCCTGGACTTCGAGC-3′, β-actin-AS, 5′-GATGGAGCCGCCGATCCACACGG-3′. The detailed experimental protocol of RNA extraction and RT-qPCR can be found in ref. [ [bib_ref]MiR-98 inhibits malignant progression via targeting MTDH in squamous cell carcinoma of the head and neck — Tan et al.[/bib_ref] ].<br />
<br />
MiR-144-3p mimics, the miR control, the overexpression plasmid of BCL6, 3′UTR and 3′UTR mutant of BCL6 gene expression plasmids were purchased from Invitrogen (Carlsbad, CA).<br />
<br />
HCT116 cells were seeded on a 48-well plate and co-transfected with either miR-144-3p mimics or miR control together with the reporter plasmid including either wild-type or mutant 3′UTR of BCL6. The fluorescence detection used a Luciferase Assay System (Promega, USA) 48 h after transfection according to the manufacturer protocols.<br />
<br />
HCT116 and SW480 cells were transfected with miR-144-3p mimics or miR control, BCL6 overexpression or inhibition vector, with transfection after 24 h to perform MTT and colony formation assays. Details of the procedure of MTT and colony formation assays were described by Zhao et al. [ [bib_ref]miR-212/132 downregulates SMAD2 expression to suppress the G1/S phase transition of the cell cycle and the epithelial to mesenchymal transition in cervical cancer cells — Zhao et al.[/bib_ref] ].<br />
<br />
HCT116 cells were transfected with miR-144-3p mimics or miR control, co-transfected with either miR-144-3p mimics or miR control together with BCL6 overexpression vector, and 24 h after transfection, cell cycle distribution of HCT116 cells were examined by flow cytometry analyses, which were performed using annexin V and propidium iodide staining according to [ [bib_ref]miR-212/132 downregulates SMAD2 expression to suppress the G1/S phase transition of the cell cycle and the epithelial to mesenchymal transition in cervical cancer cells — Zhao et al.[/bib_ref] , [bib_ref]MicroRNA-324-3p regulates nasopharyngeal carcinoma radioresistance by directly targeting WNT2B — Li et al.[/bib_ref] ].<br />
<br />
Twenty pairs of CRC tissues and adjacent non-tumor tissues were fixed in 4% formaldehyde for 24 h and sent to Tianjin Saier Co. for immunohistochemistry.<br />
<br />
All statistical analyses were performed at least three times for independent experiments. Data are presented as mean ± SD and were analyzed with two-tailed unpaired Student’s t-test or ANOVA analysis to make the comparison. P ≤ 0.05 was considered statistically significant.<br />
<br />
To explore the potential role of miR-144-3p in the progression of CRC, we examined the level of miR-144-3p in 20 CRC tissues and non-tumor adjacent tissues using qRT-PCR. Figure 1a shows that miR-144-3p was significantly down-regulated in CRC tissues when compared to non-tumor adjacent tissues. Moreover, we analyzed miR-144-3p expression with clinicopathologic characteristics of patients in CRC tissues. As shown in Fig. 1b, higher miR-144-3p expression was associated with a lower stage of CRC. These results indicate that miR-144-3p is down-regulated in CRC and correlates with the tumor progression of CRC patients.<br />
<br />
Expression of miR-144-3p level in CRC tissues and related to the clinicopathologic characteristics of patients. a qRT-PCR showed the expression levels of miR-144-3p in 20 pairs of CRC tissues and adjacent non-tumor tissues, U6 snRNA was used as an internal control. b Correlation between miR-144-3p and clinicopathologic characteristics of patients with CRC<br />
<br />
To determine whether miR-144-3p plays a role in CRC cells, HCT116 and SW480 cells were transfected with miR-144-3p mimics, anti-miR-144-3p or the negative control accordingly. In further analyses, the efficiency of these vectors was validated by qRT-PCR (Fig. 2a). Then, MTT and colony formation assay were performed. The results showed that overexpression of miR-144-3p inhibited cell proliferation of CRC cells, while anti-miR-144-3p promoted CRC cell proliferation (Fig. 2b, c). In order to study the underlying mechanism, flow cytometry analysis was performed to detect the cell cycle progression. The results showed that miR-144-3p inhibited the G1/S transition of HCT116 cells (Fig. 2d). Taken together, the results indicate that miR-144-3p inhibits cell proliferation and delays G1/S phase transition in CRC cells.<br />
<br />
miR-144-3p inhibits cell proliferation and delays G1/S phase transition in CRC cells. (a) qRT-PCR showed the expression of miR-144-3p mimics in HCT116 and SW480 cells. MTT assay (b) and colony formation assay (c) were performed to detect the effect of miR-144-3p on cell proliferation activity in CRC cells. (d) Flow cytometry analysis was performed to determine the distribution of cells in the cell cycle of HCT116 cells<br />
<br />
Using bioinformatics analyses TargetScan 7.2, RNAhybrid (v2.2), PITA Catalog version 6 and miRanda (v1.9) to predict the target of miR-144-3p, among them, BCL6 was chosen for further study due to its high scores. We identified putative binding sites for miR-144-3p within the 3′UTR of BCL6 mRNA. In order to validate whether BCL6 is targeted by miR-144-3p, a human wild type or the mutant sites 3′UTR of the BCL6 fragment was cloned into luciferase reporter plasmids (Fig. 3a). HCT116 cells were co-transfected with either miR-144-3p mimic, anti-miR-144-3p or the negative control vector with the wild type or the mutant sites 3′UTR of the BCL6 overexpression vector, as shown in Fig. 3b. Compared with the negative control group, fluorescence intensity of the wild type BCL6 3′UTR was significantly reduced by overexpression of miR-144-3p, while it was increased by overexpressing the anti-miR-144-3p vector in HCT116 cells. However, the fluorescence intensity of the mutant BCL6 3′UTR was not changed by overexpression or inhibition of miR-144-3p. In addition, qRT-PCR and Western blot assay showed that ectopic expression of miR-144-3p reduced the mRNA and protein level of BCL6, while the opposite effects were observed in anti-miR-144-3p-transfected cells at both mRNA and protein levels (Fig. 3c, d).<br />
<br />
BCL6 is a target of miR-144-3p. (a) The predicted binding sites for miR-144-3p in the 3′UTR of BCL6 and the mutant 3′UTR of BCL6 are shown. (b) Luciferase reporter assay was performed in HCT116 cells co-transfected miR-144-3p mimics or the control vector with BCL6–3′UTR1, BCL6–3′UTR1-mut. qRT-PCR (c) and Western blot (d) were performed to detect the mRNA and protein levels of BCL6 in HCT116 cells transfected with miR-144-3p mimics or the control vector. (e) Immunohistochemical staining with BCL6 in CRC tissue samples and the representative graph of expression levels of BCL6. Original magnification: 400Χ. (f) qRT-PCR showed the expression levels of BCL6 in 20 pairs of CRC tissues and adjacent non-tumor tissues. β-actin was used as an internal control. (g) Pearson’s correlation analysis indicated a negative correlation between the expression level of miR-144-3p and BCL6 in 20 pairs of CRC tissues (R = − 0.827; **: P &lt; 0.01)<br />
<br />
Likewise, to explore whether miR-144-3p is relevant to endogenous BCL6 expression in human CRC, immunohistochemical staining and qRT-PCR assay were performed to determine the mRNA and protein level of BCL6 in 20 pairs of CRC tissues and non-tumor adjacent tissues. The results showed that the expression of BCL6 in CRC tissues was up-regulated at both protein and mRNA levels in comparison to the non-tumor adjacent tissues (Fig. 3e, f). Moreover, correlation analysis indicated that the expression of miR-144-3p and BCL6 had a negative correlation in the 20 pairs of CRC tissues (Fig. 3g). These results suggest that miR-144-3p negatively regulates BCL6.<br />
<br />
Furthermore, to confirm that the effect of miR-144-3p on cell proliferation and cell cycle progression of CRC cells is due to its regulation of BCL6, a series of rescue experiments were performed. Figure 4a shows that ectopic expression of miR-144-3p could reduce BCL6 protein expression in HCT116 cells, and re-expression of BCL6 overexpression plasmid was effective to restore the protein level of BCL6. In addition, the functional rescue experiments showed that miR-144-3p-mediated repression of cell proliferation and cell cycle progression in CRC cells was restored by ectopic expression of the BCL6 overexpression plasmid (Fig. 4b, c, d). These results show that BCL6 is a mediator of miR-144-3p repression of cell proliferation and cell cycle arrest in CRC cells.<br />
<br />
The miR-144-3p/BCL6 axis regulates malignant behavior of CRC cells. (a) HCT116 cells were co-transfected with miR-144-3p mimics and pcDNA3/BCL6 or the control vector. Western blot assay was carried out to detect the protein level of BCL6. CRC cells were co-transfected with miR-144-3p mimics and pcDNA3/BCL6 or the control vector. MTT assay (b), colony formation assay (c) and cell cycle assay (d) were performed to determine the malignant behavior of CRC cells<br />
<br />
Next, we investigated the functional relevance of the interaction between miR-144-3p and BCL6 by determining the effect of changes in their expression levels on the activity of the Wnt/β-catenin signaling pathway, then the important downstream target genes (β-catenin, c-myc, cyclin D1) of the Wnt/β-catenin pathway were examined using Western blot assay (Fig. 5a, b). The results showed that miR-144-3p caused a decrease in the protein level of β-catenin, c-myc, and cyclin D1, while ectopic expression of BCL6 could restore the protein level of β-catenin, c-myc, and cyclin D1. The results indicate that the role of miR-144-3p/BCL6 repression of cell proliferation may involve Wnt/β-catenin signaling.<br />
<br />
The miR-144-3p/BCL6 axis inhibited the Wnt/β-catenin signaling pathway. HCT116 cells were co-transfected with miR-144-3p mimics and pcDNA3/BCL6 or the control vector. Western blot analysis of β-catenin, C-myc and cyclin D1 protein levels in HCT116 cells<br />
<br />
Colorectal cancer (CRC) is one of the most common cancers worldwide. With 600 000 patients dying from colorectal cancer annually and with an unfavorable prognosis of advanced CRC [ [bib_ref]Colorectal cancer — Brenner et al.[/bib_ref] ], it is urgent to explore and identify new biomarkers for diagnosis and treatment in CRC. Recent reports indicate that miRNAs play a vital role in the development and progression of various cancers [ [bib_ref]MicroRNAs: genomics, biogenesis, mechanism, and function — Bartel[/bib_ref] ]. Herein, our findings indicated that miR-144-3p was down-regulated in CRC and correlated with the tumor progression of CRC patients. Furthermore, we showed that miR-144-3p inhibited cell proliferation and delayed G1/S phase transition of HCT116 cells. It may manifest the tumor suppressor of miR-144-3p in CRC.<br />
<br />
miRNA plays its role via regulating the expression of its target gene [ [bib_ref]MicroRNAs: target recognition and regulatory functions — Bartel[/bib_ref] ]. B-cell lymphoma 6 (BCL6), also known as BCL6A, LAZ3, or ZNF51, belonging to the BTB-POZ protein family, has been demonstrated to facilitate cell proliferation [ [bib_ref]BCL-6 represses genes that function in lymphocyte differentiation, inflammation, and cell cycle control — Shaffer et al.[/bib_ref] ]. Reports showed that BCL6 may be a novel diagnostic and treatment strategy for breast or ovarian cancer [ [bib_ref]High expressions of BCL6 and Lewis y antigen are correlated with high tumor burden and poor prognosis in epithelial ovarian cancer — Zhu et al.[/bib_ref] , [bib_ref]Expression of and correlation between BCL6 and ZEB family members in patients with breast cancer — Ang et al.[/bib_ref] ]. However, the role BCL6 plays in CRC remained unknown. In this study, we used bioinformatics analyses to determine that BCL6 is a potential target of miR-144-3p based on functional knowledge of miR-144-3p. Then we demonstrated that BCL6 was directly targeted by miR-144-3p using luciferase reporter assay. Immunohistochemical staining and qRT-PCR assays indicated that BCL6 was up-regulated in human CRC tissues compared with its adjacent non-tumor tissues. Additionally, there was a negative correlation between miR-144-3p and BCL6 in 20 pairs of CRC tissues. Furthermore, we found that BCL6 was a mediator of miR-144-3p repression of cell proliferation and cell cycle arrest in CRC cells.<br />
<br />
Wnt/β-catenin signaling is crucial for regulating growth-related pathologies in cancer, being closely related to the development of cancer [ [bib_ref]Wnt/beta-catenin signaling and disease — Clevers et al.[/bib_ref] , [bib_ref]Wnt/beta-catenin signaling, disease, and emerging therapeutic modalities — Nusse et al.[/bib_ref] ]. Recently, many reports have shown that the Wnt/β-catenin pathway is involved in the progression of CRC through multiple ways [ [bib_ref]Chen G, Gao C, Gao X, Zhang DH, Kuan SF, Burns TF, Hu J. Wnt/beta-catenin pathway activation mediates adaptive resistance to BRAF inhibition in colorectal cancer. Mol Cancer Ther. 2018;17:806–13.10.1158/1535-7163.MCT-17-0561PMC588254329167314[/bib_ref] [bib_ref]MicroRNA-494 promotes cancer progression and targets adenomatous polyposis coli in colorectal cancer — Zhang et al.[/bib_ref] [bib_ref]Role of Wnt/beta-catenin signaling regulatory microRNAs in the pathogenesis of colorectal cancer — Rahmani et al.[/bib_ref] ]. In our study, we found that miR-144-3p down-regulated the expression of β-catenin, c-Myc and cyclin D1, which are downstream targets of Wnt signaling in HCT116 cells. Moreover, the ectopic expression of BCL6 restored the inhibition of the expression of β-catenin, c-Myc and cyclin D1 in HCT116 cells, miR-144-3p/BCL6 repressed cell proliferation possibly through Wnt/β-catenin signaling, but the specific regulatory mechanism of miR-144-3p/BCL6 in Wnt/β-catenin signaling requires further study.<br />
<br />
In all, our data reveal that miR-144-3p inhibits malignant cell phenotype and Wnt/β-catenin signaling in CRC cells. We demonstrated that BCL6 is targeted and downregulated by miR-144-3p. miR-144-3p repression of malignant cell phenotype and Wnt/β-catenin signaling is mediated by BCL6 in CRC cells. These findings may draw attention to understanding the molecular mechanism of CRC progression and may improve the preventive and therapeutic strategies for CRC.<br />
<br />
Our results show that miR-144-3p is downregulated and related to the clinicopathologic characteristics of patients in CRC tissues. Moreover, miR-144-3p inhibits cell proliferation of colorectal cancer cells by targeting BCL6, possibly through inhibition of Wnt/β-catenin signaling. These findings provide further evidence for the miR-144-3p/BCL6 axis as a therapeutic molecular target for CRC.<br />
<br />
Three prime untranslated region<br />
<br />
B-cell lymphoma 6<br />
<br />
complementary DNA<br />
<br />
Colorectal cancer<br />
<br />
microRNA-144-3p<br />
<br />
microRNA<br />
<br />
3-(4,5-cimethylthiazol-2-yl)-2,5-diphenyl tetrazolium bromide</p>

**Rewrite**

<p><strong>miR-144-3p Inhibits Colorectal Cancer Cell Proliferation by Targeting BCL6 and Suppressing Wnt/β-catenin Signaling</strong><br />
<br />
<strong>Background and Context</strong><br />
MicroRNAs (miRNAs) are noncoding RNAs, typically 18–24 nucleotides in length, that regulate post-transcriptional gene expression, generally resulting in gene silencing. Dysregulation of miRNAs is associated with various biological processes in cancer, including cell proliferation, metastasis, apoptosis, and cell cycle progression. miR-144-3p has been reported to function as either a tumor suppressor or an oncogene depending on the cancer type. In bone, gastric, glioblastoma, hepatocellular, and pancreatic cancers, miR-144-3p acts as a tumor suppressor by targeting genes such as connexin 43, PBX3, c-Met, SGK3, FOSB, and proline-rich protein 11. Conversely, in clear cell renal cell carcinoma (ccRCC), miR-144-3p acts as an oncogene by regulating ARID1A. The specific role of miR-144-3p in colorectal cancer (CRC) was previously unknown.<br />
<br />
BCL6 is a 95-kD nuclear phosphoprotein belonging to the BTB/POZ/zinc finger (ZF) family of transcription factors. It modulates genes involved in B cell activation, differentiation, cell cycle arrest, and apoptosis, and targets oncogenes such as MYC and BCL2. BCL6 also influences multiple pathways, including Wnt signaling.<br />
<br />
<strong>Expression of miR-144-3p and BCL6 in Colorectal Cancer</strong><br />
Analysis of 20 pairs of CRC tissues and adjacent non-tumor tissues revealed that miR-144-3p is significantly down-regulated in CRC tissues compared to normal tissues. Higher expression levels of miR-144-3p were associated with lower tumor stages, indicating a correlation with tumor progression.<br />
<br />
Conversely, BCL6 was up-regulated at both mRNA and protein levels in CRC tissues compared to adjacent non-tumor tissues. Immunohistochemical staining confirmed elevated BCL6 protein expression in CRC samples. A negative correlation was observed between miR-144-3p and BCL6 expression in CRC tissues (Pearson’s correlation R = −0.827; P &lt; 0.01).<br />
<br />
<strong>miR-144-3p Inhibits Cell Proliferation and Delays G1/S Transition</strong><br />
In CRC cell lines HCT116 and SW480, overexpression of miR-144-3p (via mimics) inhibited cell proliferation, as measured by MTT and colony formation assays. Conversely, inhibition of miR-144-3p promoted proliferation. Flow cytometry analysis demonstrated that miR-144-3p delays the G1/S phase transition in HCT116 cells.<br />
<br />
<strong>BCL6 is a Direct Target of miR-144-3p</strong><br />
Bioinformatics predictions using TargetScan 7.2, RNAhybrid (v2.2), PITA Catalog version 6, and miRanda (v1.9) identified BCL6 as a potential target of miR-144-3p, with putative binding sites located in the 3′ untranslated region (3′UTR) of BCL6 mRNA.<br />
<br />
Luciferase reporter assays in HCT116 cells confirmed direct targeting:<br />
*   Co-transfection of miR-144-3p mimics with a reporter plasmid containing the wild-type BCL6 3′UTR significantly reduced fluorescence intensity.<br />
*   Co-transfection of anti-miR-144-3p increased fluorescence intensity.<br />
*   Mutations in the binding site of the BCL6 3′UTR abolished these effects.<br />
<br />
Additionally, ectopic expression of miR-144-3p reduced BCL6 mRNA and protein levels, while inhibition of miR-144-3p increased them.<br />
<br />
<strong>BCL6 Mediates the Effects of miR-144-3p on Proliferation and Cell Cycle</strong><br />
Rescue experiments demonstrated that BCL6 mediates the tumor-suppressive effects of miR-144-3p. While miR-144-3p mimics reduced BCL6 protein levels and inhibited proliferation/cell cycle progression, co-expression of a BCL6 overexpression plasmid restored BCL6 protein levels and reversed the inhibition of cell proliferation and G1/S arrest caused by miR-144-3p.<br />
<br />
<strong>miR-144-3p Suppresses Wnt/β-catenin Signaling via BCL6</strong><br />
The Wnt/β-catenin pathway is critical in CRC progression. Downstream targets of this pathway, including β-catenin, c-Myc, and cyclin D1, were examined. miR-144-3p overexpression decreased the protein levels of β-catenin, c-Myc, and cyclin D1. However, ectopic expression of BCL6 restored the protein levels of these downstream targets. This indicates that miR-144-3p represses Wnt/β-catenin signaling through the downregulation of BCL6.<br />
<br />
<strong>Conclusion</strong><br />
miR-144-3p is down-regulated in colorectal cancer and functions as a tumor suppressor by directly targeting BCL6. This interaction leads to the inhibition of cell proliferation, delay of G1/S phase transition, and suppression of Wnt/β-catenin signaling. These findings identify the miR-144-3p/BCL6 axis as a potential prognostic marker and therapeutic target for colorectal cancer.</p>

</details>

<details>
<summary>FineWeb-Edu example: fineweb-00090-000000169424</summary>

**Original**

<p>A gene that makes a protein called epidermal growth factor receptor (EGFR), which is involved in cell growth and cell survival. Mutated (changed) forms of the EGFR gene and protein have been found in some types of cancer, including non-small cell lung cancer. These changes may cause cancer cells to grow and spread in the body. Checking for changes in the EGFR gene in tumor tissue may help plan cancer treatment. Also called epidermal growth factor receptor gene, ERBB1 gene, and HER1 gene.</p>

**Rewrite**

<p>The epidermal growth factor receptor (EGFR) is a protein involved in cell growth and survival. The gene encoding this protein is also known as ERBB1 or HER1.<br />
<br />
Mutated forms of the EGFR gene and protein have been identified in certain types of cancer, including non-small cell lung cancer. These genetic alterations may promote the growth and spread of cancer cells. Detection of EGFR gene changes in tumor tissue may assist in planning cancer treatment.</p>

</details>

## Mixing experiments

We are testing how the proportions of the four sources affect mid-training.  We have prepared over 200M rewritten training tokens, with roughly 50M from each source

| Source | Mix 1 | Mix 2 | Mix 3 | Training tokens |
|---|---:| ---:| ---:| ---:|
| Swiss-Prot | 25% | 40% | 20% | 30M |
| PMC | 25% | 20% | 40% | 30M |
| BioCollection | 25% | 20%| 20% | 30M |
| FineWeb-Edu | 25% | 20% | 20% | 30M |
| **Results** | | | | **120M** |

The current model is **Qwen3.5-4B**, trained on this mixture with a LoRA adapter. We can compare other mixtures against this equal-source run.

We compare the original and mid-trained models on the same 200 synthetic protein questions by measuring the log probabilities assigned to the correct answer text.

<details>
<summary>How answer log probabilities work</summary>

Each of the 200 questions has four choices, A–D. Here is one of the actual questions:

<blockquote>
<p>Protein sequence:<br />
MSFLGFGGGQPQLSSQQKIQAAEAELDLVTDMFNKLVNNCYKKCINTSYSEGELNKNESSCLDRCVAKYFET<br />NVQVGENMQKMGQSFNAAGKF<br />
<br />
Task: GO_molecular_function<br />
<br />
Question: Which molecular function best describes this protein’s chaperone-like role?<br />
<br />
Choices:<br />
A. ATP-dependent protein-folding chaperone activity<br />
B. Peptidase activity<br />
C. Unfolded protein holdase activity<br />
D. GTPase activity</p>
</blockquote>

The saved correct choice is **C: Unfolded protein holdase activity**.

The correct-answer log-probability evaluation gives the model the question and choices, then scores the text of the correct choice—not the letter C—after the prompt <code>Answer:</code>. For a multi-token answer, it averages the log probabilities across the answer tokens. Higher average log probability means the model assigns more probability to that correct answer text; the corresponding loss is its negative, so lower is better.

A separate multiple-choice accuracy calculation scores the text of all four choices and selects the letter with the highest average score.

The 200 questions come from the earlier synthetic QA datasets; this is not a full LiveProteinBench evaluation.

</details>

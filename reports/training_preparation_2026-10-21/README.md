# Protein mid-training: data and mixing

We are continuing training on Qwen3.5-4B with protein-related material to study how data sources and mixtures affect the model.

## Source data

| Source or dataset | Documents or examples | Tokens | Average length |
|---|---:|---:|---:|
| **Swiss-Prot** | 575.7K records | ~3.66B | 6.35K per record |
| **PMC** | 9.09M papers | 99.7B | 11K per paper |
| **BioCollection** | 36.6M records | 36.5B | 995 per record |
| **FineWeb-Edu (filtered for bio)** | 11.8M pages | 9.14B | 775 per page |
| **QA post-training datasets** | | | |
| 10K QA post-training | 10K questions | 22.34M | 2.24K per example |
| 124K QA post-training | 124K questions | 270.28M | 2.18K per example |

The Swiss-Prot total scales the measured average from 100K selected records to 575.7K. Source collection counts used different tokenizers. The QA token counts use the Qwen3.5-4B tokenizer and include each question, reasoning trace, and answer once; multiple training epochs process the data again.

## Selecting and rewriting the data

The source collection counts above describe the broader collections. FineWeb-Edu is already filtered for biology. For PMC and FineWeb-Edu, Qwen3.5-4B labeled documents for protein relevance, and those labels were used to train a smaller classifier. The classifier ranks documents for selection before rewriting and before counting the rewritten training tokens. Swiss-Prot and BioCollection use their own selection processes.

We use **Qwen3.6-35B-A3B** to rewrite source records into clear biology text. The model is instructed to preserve supported facts and uncertainty, copy protein sequences exactly, and remove administrative material. Rewrites with detected protein-sequence changes are excluded.

**The current mid-training run trains on the rewrites, not the original records.** The original records are inputs to the rewriting model.

<details>
<summary>Swiss-Prot example: swissprot-P42562</summary>

**Original**

```xml
<ns0:entry xmlns:ns0="https://uniprot.org/uniprot" dataset="Swiss-Prot" created="1995-11-01" modified="2026-09-02" version="39">
    <ns0:accession>P42562</ns0:accession>
    <ns0:name>FAR3_HIRME</ns0:name>
    <ns0:protein>
        <ns0:recommendedName>
            <ns0:fullName>FMRFamide-like neuropeptide YLRF-amide</ns0:fullName>
        </ns0:recommendedName>
    </ns0:protein>
    <ns0:organism>
        <ns0:name type="scientific">Hirudo medicinalis</ns0:name>
        <ns0:name type="common">Medicinal leech</ns0:name>
        <ns0:dbReference type="NCBI Taxonomy" id="6421" />
        <ns0:lineage>
            <ns0:taxon>Eukaryota</ns0:taxon>
            <ns0:taxon>Metazoa</ns0:taxon>
            <ns0:taxon>Spiralia</ns0:taxon>
            <ns0:taxon>Lophotrochozoa</ns0:taxon>
            <ns0:taxon>Annelida</ns0:taxon>
            <ns0:taxon>Clitellata</ns0:taxon>
            <ns0:taxon>Hirudinea</ns0:taxon>
            <ns0:taxon>Hirudinida</ns0:taxon>
            <ns0:taxon>Hirudiniformes</ns0:taxon>
            <ns0:taxon>Hirudinidae</ns0:taxon>
            <ns0:taxon>Hirudo</ns0:taxon>
        </ns0:lineage>
    </ns0:organism>
    <ns0:reference key="1">
        <ns0:citation type="journal article" date="1991" name="Peptides" volume="12" first="897" last="908">
            <ns0:title>Identification of RFamide neuropeptides in the medicinal leech.</ns0:title>
            <ns0:authorList>
                <ns0:person name="Evans B.D." />
                <ns0:person name="Pohl J." />
                <ns0:person name="Kartsonis M.A." />
                <ns0:person name="Calabrese R.L." />
            </ns0:authorList>
            <ns0:dbReference type="PubMed" id="1686933" />
            <ns0:dbReference type="DOI" id="10.1016/0196-9781(91)90035-n" />
        </ns0:citation>
        <ns0:scope>PROTEIN SEQUENCE</ns0:scope>
        <ns0:scope>AMIDATION AT PHE-4</ns0:scope>
    </ns0:reference>
    <ns0:comment type="subcellular location">
        <ns0:subcellularLocation>
            <ns0:location>Secreted</ns0:location>
        </ns0:subcellularLocation>
    </ns0:comment>
    <ns0:comment type="similarity">
        <ns0:text evidence="2">Belongs to the FARP (FMRFamide related peptide) family.</ns0:text>
    </ns0:comment>
    <ns0:dbReference type="GO" id="GO:0005576">
        <ns0:property type="term" value="C:extracellular region" />
        <ns0:property type="evidence" value="ECO:0000501" />
        <ns0:property type="project" value="UniProtKB-SubCell" />
    </ns0:dbReference>
    <ns0:proteinExistence type="evidence at protein level" />
    <ns0:keyword id="KW-0027">Amidation</ns0:keyword>
    <ns0:keyword id="KW-0903">Direct protein sequencing</ns0:keyword>
    <ns0:keyword id="KW-0527">Neuropeptide</ns0:keyword>
    <ns0:keyword id="KW-0964">Secreted</ns0:keyword>
    <ns0:feature type="peptide" id="PRO_0000043679" description="FMRFamide-like neuropeptide YLRF-amide">
        <ns0:location>
            <ns0:begin position="1" />
            <ns0:end position="4" />
        </ns0:location>
    </ns0:feature>
    <ns0:feature type="modified residue" description="Phenylalanine amide" evidence="1">
        <ns0:location>
            <ns0:position position="4" />
        </ns0:location>
    </ns0:feature>
    <ns0:evidence type="ECO:0000269" key="1">
        <ns0:source>
            <ns0:dbReference type="PubMed" id="1686933" />
        </ns0:source>
    </ns0:evidence>
    <ns0:evidence type="ECO:0000305" key="2" />
    <ns0:sequence length="4" mass="598" checksum="69D4073B30000000" modified="1995-11-01" version="1">YLRF</ns0:sequence>
</ns0:entry>
```

**Rewrite**

```text
In the medicinal leech (*Hirudo medicinalis*), the neuropeptide YLRF-amide (UniProtKB accession P42562) is a member of the FARP (FMRFamide-related peptide) family. This peptide is secreted and localized to the extracellular region.

The primary sequence of the mature neuropeptide consists of four amino acids: Tyrosine-Leucine-Arginine-Phenylalanine (YLRF). The phenylalanine residue at position 4 undergoes C-terminal amidation. This modification and the protein sequence were determined via direct protein sequencing. The peptide has a molecular mass of 598 Da.

Protein existence is confirmed at the protein level. The identification was reported by Evans B.D., Pohl J., Kartsonis M.A., and Calabrese R.L. in a 1991 study published in *Peptides* (PubMed ID 1686933).
```

</details>

<details>
<summary>BioCollection example: biocollection-000001-000000001223</summary>

**Original**

```text
Magnetosome protein MamT from Paramagnetospirillum magneticum (strain ATCC 700264 / AMB-1) is a protein. The functional descriptions of this protein are as follows: May play a role in magnetite crystal maturation (Probable). May transfer electrons to balance the Fe(2+)-Fe(3+) ratio during magnetite formation (Probable). Gene Ontology (GO) information indicates that this protein has the following annotations: molecular function annotations describe roles in metal ion binding, oxidoreductase activity; cellular component annotations show localization to magnetosome membrane. It has a length of 176 amino acids. The protein sequence is <protein>MSMEAPRRGRRWVSLGMIALLAAIGLGLYWDQLSTPSGITPATSPRRAEGLLLGRLPLPMEPSLLSPLERLLEPPLRYKLMTIRHIPPVKPGTGMPHPYVGDCIQCHLMVGGPAAGSQFKTPYGAVLENLSRVRKLGPPILPTSRQPHPPAGRCIKCHDIVVKVPVDKKGGMRWQL</protein>.
```

**Rewrite**

```text
MamT is a magnetosome protein found in *Paramagnetospirillum magneticum* (strain ATCC 700264 / AMB-1). The protein consists of 176 amino acids. Its sequence is:

MSMEAPRRGRRWVSLGMIALLAAIGLGLYWDQLSTPSGITPATSPRRAEGLLLGRLPLPMEPSLLSPLERLLEPPLRYKLMTIRHIPPVKPGTGMPHPYVGDCIQCHLMVGGPAAGSQFKTPYGAVLENLSRVRKLGPPILPTSRQPHPPAGRCIKCHDIVVKVPVDKKGGMRWQL

Gene Ontology (GO) annotations indicate that MamT is localized to the magnetosome membrane. Its molecular function includes metal ion binding and oxidoreductase activity.

Functional descriptions suggest probable roles in magnetite crystal maturation and in transferring electrons to balance the Fe(2+)-Fe(3+) ratio during magnetite formation.
```

</details>

<details>
<summary>PMC example: pmc-PMC4215664</summary>

**Original**

```text
Re: New insights into SET protein during mouse spermatogenesis

We are thankful to Dr. Yeste for the encouraging comments. [bib_ref]New insights into SET protein during mouse spermatogenesis — Yeste[/bib_ref] In the previous study, we revealed a specific, SET-initiated, PP2A-mediated, pathway that leads to the increased lyase activity of P450c17 in ovarian theca cells, by which SET regulates testosterone biosynthesis. How to work SET protein in Leydig cells is our new research interesting. Secondly, SET protein is a multifunctional protein involved in histone binding, transcription control, nucleosome assembly, and cell apoptosis. Very interestingly, we found the changing SET expression in the seminiferous epithelium at different stages in this manuscript. The highest level of SET protein was mainly in haploid and tetraploid cells of the prepubertal and adult mice, suggesting that SET is involved in the regulation of the complex, unique process of spermatogenesis. Our group is working on this role of SET protein as you proposed. It will contribute our understanding about molecular mechanism of spermatogenesis.
```

**Rewrite**

```text
In mouse spermatogenesis, the SET protein exhibits stage-specific expression within the seminiferous epithelium. The highest levels of SET protein are observed in haploid and tetraploid cells of both prepubertal and adult mice. This distribution suggests that SET is involved in regulating the complex process of spermatogenesis.

SET is a multifunctional protein known to participate in histone binding, transcription control, nucleosome assembly, and cell apoptosis. In other contexts, such as ovarian theca cells, SET initiates a PP2A-mediated pathway that increases the lyase activity of P450c17, thereby regulating testosterone biosynthesis. Current research focuses on elucidating the specific role of SET in Leydig cells to further understand the molecular mechanisms of spermatogenesis.
```

</details>

<details>
<summary>FineWeb-Edu example: fineweb-00090-000000169424</summary>

**Original**

```text
A gene that makes a protein called epidermal growth factor receptor (EGFR), which is involved in cell growth and cell survival. Mutated (changed) forms of the EGFR gene and protein have been found in some types of cancer, including non-small cell lung cancer. These changes may cause cancer cells to grow and spread in the body. Checking for changes in the EGFR gene in tumor tissue may help plan cancer treatment. Also called epidermal growth factor receptor gene, ERBB1 gene, and HER1 gene.
```

**Rewrite**

```text
The epidermal growth factor receptor (EGFR) is a protein involved in cell growth and survival. The gene encoding this protein is also known as ERBB1 or HER1.

Mutated forms of the EGFR gene and protein have been identified in certain types of cancer, including non-small cell lung cancer. These genetic alterations may promote the growth and spread of cancer cells. Detection of EGFR gene changes in tumor tissue may assist in planning cancer treatment.
```

</details>

## Mixing experiments

We are testing how the proportions of the four sources affect mid-training. The first run uses approximately **30 million rewritten tokens per source**:

| Source | Share | Training tokens |
|---|---:|---:|
| Swiss-Prot | 25% | 30M |
| PMC | 25% | 30M |
| BioCollection | 25% | 30M |
| FineWeb-Edu | 25% | 30M |
| **Total** | **100%** | **120M** |

The current model is **Qwen3.5-4B**, trained on this mixture with a LoRA adapter. We can compare other mixtures against this equal-source run.

We compare the original and mid-trained models on the same 200 synthetic protein questions by measuring the log probabilities assigned to the correct answer text.

<details>
<summary>How answer log probabilities work</summary>

For each question, the model sees the question and its answer choices. We then provide the correct answer text and measure the probability the model assigns to each of its tokens. A token is a piece of text; it may be a whole word or part of one.

For a simplified example, suppose the correct answer is a single token, **“DNA”**:

| Model | Probability assigned to the correct answer | Log probability |
|---|---:|---:|
| Original model | 20% | −1.61 |
| Mid-trained model | 60% | −0.51 |

In this illustration, the mid-trained model assigns more probability to the correct answer. For longer answers, the score averages the log probabilities of the answer tokens. A higher average log probability is better; the corresponding loss is its negative, so a lower loss is better.

The 200 questions are sampled from the earlier synthetic QA datasets; this is not a full LiveProteinBench evaluation.

</details>

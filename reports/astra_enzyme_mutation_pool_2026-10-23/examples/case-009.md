# case-009 — APEX peroxidase: mutation effect mechanism evidence

**Assistant selection tier: strong.** Generation status: `completed`.

## Exact information supplied to Astra

The input may contain a reference sequence, published variant identities and explicitly supplied assay observations. Those observations are evidence available to the solver. This is not necessarily a sequence-only prediction task. The original unwrapped prompt is preserved in the request artifact and questions.jsonl.

Reference protein sequence (canonical wild-type backbone; coordinate reference only):

```text
MGKSYPTVSADYQKAVEKAKKKLRGFIAEKRCAPLMLRLAWHSAGTFDKGTKTGGPFGTIKHPAELAHSA
NNGLDIAVRLLEPLKAEFPILSYADFYQLAGVVAVEVTGGPEVPFHPGREDKPEPPPEGRLPDATKGSDH
LRDVFGKAMGLTDQDIVALSGGHTIGAAHKERSGFEGPWTSNPLIFDNSYFTELLSGEKEGLLQLPSDKA
LLSDPVFRPLVDKYAADEDAFFADYAEAHQKLSELGFADA
```


Reference: Q43758. All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded. The sequence is not the complete tagged assay construct.

Published variant identities:
APEX: substitutions K14D, W41F, E112K; deletions none.
APEX2: substitutions K14D, W41F, E112K, A134P; deletions none.
Dimeric APX-W41F comparator: substitutions W41F; deletions none.

Supplied assay observations:
- APEX2 is more active in cells than APEX and the dimeric APX-W41F comparator.
- Thermal stability and heme binding improve slightly over APEX, but remain below the dimeric comparator; purified assays show stronger peroxide-inhibition resistance for APEX2.

**Question:** Which mechanistic explanation best reconciles the cellular ranking with the independent biochemical comparisons?

- **A.** A heme-binding advantage over the dimeric comparator accounts for the stronger cellular signal observed with APEX2.
- **B.** Cellular activity follows the thermal-stability ranking across the variants, making the peroxide-tolerance comparison consistent with that same ranking.
- **C.** A thermal-stability advantage over the dimeric comparator accounts for the stronger cellular signal observed with APEX2.
- **D.** Peroxide-tolerance differences help explain the cellular advantage, whereas stability and heme-binding rankings alone do not match the cellular ranking.


## Astra’s worked solution

D best reconciles the observations.

Sequence comparison: APEX2 adds A134P to the K14D/W41F/E112K background of APEX. This identifies the listed sequence difference, but the presence of a proline substitution alone does not establish its effects on stability, heme binding or peroxide inhibition. Those effects must be interpreted from the supplied measurements.

Observed rankings: Cellular activity places APEX2 above both APEX and the dimeric APX-W41F comparator. In contrast, thermal stability and heme binding each rank the dimeric comparator above APEX2, with APEX2 only slightly improved over APEX. Therefore, neither thermal stability nor heme binding alone reproduces the cellular ranking.

Mechanistic interpretation: Peroxide is a catalytic cosubstrate for a heme peroxidase, but excessive peroxide exposure can also inhibit catalysis or cause oxidative inactivation. Resistance to peroxide inhibition is therefore distinct from resistance to thermal unfolding and from heme binding. If peroxide inhibition limits activity under the cellular assay conditions, APEX2's observed greater resistance can preserve catalytic activity despite its lower thermal stability and heme binding relative to the dimeric comparator. The purified-assay result supplies independent biochemical support for this explanation without requiring a particular structural mechanism.

Discriminating the alternatives: A incorrectly asserts a heme-binding advantage over the dimeric comparator, directly contradicting the observations. C makes the corresponding incorrect assertion about thermal stability. B incorrectly states that cellular activity follows the thermal-stability ranking and treats peroxide tolerance as though it necessarily follows that ranking. D correctly identifies peroxide tolerance as a plausible contributor while recognizing that stability and heme-binding rankings alone cannot explain the cellular advantage.

## Final answer

D

## Astra’s stated limitations

The observations support peroxide tolerance as a contributor, not necessarily the sole cause of higher cellular activity. Peroxide concentrations, cellular enzyme abundance and complete assay constructs are not supplied. Neither the sequence nor these comparisons establish the precise structural mechanism of A134P.

Confidence reported by Astra: high.

## Review and sources — checked after generation

The reference label and the following verification material are separate from the solver input. Any biological facts already supplied to Astra remain visible above.

Source identity: **APEX peroxidase** — [UniProt Q43758](https://www.uniprot.org/uniprotkb/Q43758/entry).

Source-supported reference answer: **D**. Selected answer matches.

Scientific review: Assistant-reviewed; no material errors found.

Reference-sequence scope: Canonical wild-type backbone for reference coordinates only; not claimed to be the complete tagged assay construct.

- Correctly contrasts the cellular ranking with the different stability and heme-binding rankings.
- Uses independent peroxide-tolerance evidence as a conditional contributing explanation, without claiming exclusive causality.
- Correctly identifies the shared substitutions and sole additional A134P difference.

Source support:

- Figure 2e; Supplementary Figures 8c and 9; accompanying Results
- Supplied assay observations in the exact student prompt are short paraphrases of the stated paper Results/caption/Methods; approximate numbers are explicitly labelled.

Source qualifications:

- All listed substitutions and deletions use the one-based canonical wild-type coordinates, including the initial methionine. Tags, linkers and targeting fusions are excluded.
- Published enzyme-core identity; complete assay fusion sequence, tag/linker boundaries and expression cassette are not supplied.
- The assays support a contributing explanation; they do not prove a uniquely sufficient mechanism.
- Use corrected Figure 2a symbols and Figure 2e axis labels; correction dated December 10, 2014.

Primary references:

- [Directed evolution of APEX2 for electron microscopy and proximity labeling](https://www.nature.com/articles/nmeth.3179)

This is assistant review, not expert human ground truth. Matching a label does not validate every explanatory claim. Student training benefit has not been measured.

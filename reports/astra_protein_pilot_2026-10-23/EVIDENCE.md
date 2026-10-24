# Evidence behind the CorA answer

These are the evidence excerpts returned by Astra and matched against the supplied reference text. The full protein question and solution are in [the pilot](README.md).

## 1. Established CorA architecture directly supports A: each of five subunits contributes its first transmembrane domain to the shared central ion pathway.

Source: [UniProt Q9WZ31](https://www.uniprot.org/uniprotkb/Q9WZ31/entry)

> The central ion permeation pathway is formed by the first transmembrane domain from each of the five subunits.

## 2. The conserved GMN motif belongs to the polar ion-entry region of CorA.

Source: [Nordin et al. (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3629940/)

> The universally conserved GMN motif is arranged in an almost exact way as that of MjCorA, creating a polar entry made of the Asn314 side chain with the underlying ring of the carbonyl group from Gly312 (Figure 1C).

## 3. MPEL is a second CorA signature motif in the extracellular connecting-loop region.

Source: [Nordin et al. (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3629940/)

> In MjCorA, this stretch is composed of SYLPLA (which is also less conserved within the family), whereas TmCorA contains the conserved region EYMPEL (where MPEL is the second signature motif of the CorA family).

## 4. Intracellular metal-binding sites have regulatory and stabilizing functions, distinct from TM1's membrane pore-forming role.

Source: [Nordin et al. (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3629940/)

> Finally, the roles of the intracellular metal-binding sites have been assigned to increased thermostability and regulation of the gating.

## Sequence observations

Coordinates use 1-based numbering in the supplied 351-residue sequence. The exact residue strings were checked; membrane boundaries use the source annotation.

| Feature | Residues | Sequence |
| --- | --- | --- |
| UniProt-annotated TM1 | 293–313 | `VLTIIATIFMPLTFIAGIYGM` |
| UniProt-annotated TM2 | 325–345 | `WGYPVVLAVMGVIAVIMVVYF` |
| CorA signature | 312–314 | `GMN` |
| extended motif | 311–315 | `YGMNF` |
| second signature | 318–321 | `MPEL` |

Source attributions and licenses are listed in [SOURCES_AND_LICENSES.md](SOURCES_AND_LICENSES.md). These checks are not expert human validation.

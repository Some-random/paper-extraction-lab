"""Consolidate named biological inputs without treating reused sources as new data."""
GROUPS = {
    'papers': 'Paper text', 'web': 'Web text', 'records': 'Biological database records',
    'raw': 'Raw sequences and structures', 'general': 'General replay / other sciences',
}
# id | group | display name | overlap / counting treatment | explicit aliases
_DEFINITIONS = '''
pmc|papers|PubMed Central|Count the current PMC scenario once; older PMC imports overlap.|PMC;PMC full text;PMC-OA XML;The Pile: PubMed Central
pubmed|papers|PubMed / MEDLINE abstracts|Abstracts overlap PMC and multiple imported corpora; incremental amount unmeasured.|PubMed;PubMed abstracts;PubMed titles/abstracts;PubMed/MEDLINE;The Pile: PubMed Abstracts
pile_pubmed|papers|The Pile PubMed components|Older repackaging of PMC and PubMed; not an additional copy of the corpus.|The Pile PubMed components
biorxiv|papers|bioRxiv|Partly overlaps published versions and imported scientific corpora; incremental amount unmeasured.|bioRxiv
medrxiv|papers|medRxiv|Research-biology subset and incremental overlap unresolved.|medRxiv
arxiv|papers|arXiv|Biological subset and overlap with paper imports unresolved.|arXiv
chemrxiv|papers|ChemRxiv|Biologically relevant subset and overlap unresolved.|ChemRxiv
osf|papers|OSF|Biologically relevant subset and overlap unresolved.|OSF
acl|papers|ACL Anthology|Biological subset unresolved; mostly other research fields.|ACL
pubag|papers|PubAg|Agricultural research; incremental overlap unresolved.|PubAg abstracts
s2orc|papers|S2ORC / Semantic Scholar|Overlaps PMC, preprints, peS2o and the OLMo PDF collection.|S2ORC;Semantic Scholar full text;Semantic Scholar abstracts
pes2o|papers|peS2o|Derived from Semantic Scholar/S2ORC; not additive to its full parent corpus.|peS2o
biomedica|papers|BIOMEDICA|PMC-derived text and image-caption records; text overlaps PMC.|BIOMEDICA
olmo_pdfs|papers|OLMo 3 / olmOCR science PDFs|972B total across subjects; biology-only and incremental tokens unmeasured.|OLMo 3 PDF pool
patents|papers|USPTO patent applications|Biological subset unresolved; reaction datasets below are derived records.|USPTO-Applications
finefineweb|web|FineFineWeb biology|Count the biology-labelled collection once; do not add its parent FineWeb again.|FineFineWeb
biocollection|records|TheBioCollection free-text stream|Count the free-text release once, excluding its separate instruction stream.|TheBioCollection
pubchem|records|PubChem|Contributes to TheBioCollection and many model corpora; extra coverage beyond the bundle unmeasured.|PubChem
uniprot|records|UniProt / UniRef|Swiss-Prot, TrEMBL and UniRef clusterings overlap; contributes to TheBioCollection.|UniProt;UniProt/Swiss-Prot;UniProt/TrEMBL;UniRef50;UniRef90;UniRef50/90
pdb|records|Protein Data Bank|PDB/RCSB are the same source family; contributes to TheBioCollection.|PDB;RCSB PDB
alphafold|records|AlphaFold DB|Contributes to TheBioCollection; predicted structures overlap UniProt entities.|AlphaFold DB
bindingdb|records|BindingDB|Contributes to TheBioCollection; extra coverage beyond the bundle unmeasured.|BindingDB
drugbank|records|DrugBank|Contributes to TheBioCollection; access and reusable subset may differ.|DrugBank
chembl|records|ChEMBL|Contributes to TheBioCollection; overlaps other molecular sources.|ChEMBL
uspto50k|records|USPTO-50K reactions|Contributes to TheBioCollection; derived from patents.|USPTO-50K
gencode|records|GENCODE|Contributes to TheBioCollection; annotations are distinct from raw genome strings.|GENCODE
encode|records|ENCODE|Contributes to TheBioCollection; assay records may overlap other resources.|ENCODE
rnacentral|records|RNAcentral|Contributes to TheBioCollection and OpenGenome2; avoid counting both complete exports.|RNAcentral
rfam|records|Rfam|Contributes to TheBioCollection and OpenGenome2.|Rfam
l1000|records|LINCS L1000|Contributes to TheBioCollection.|L1000
hpa|records|Human Protein Atlas|Contributes to TheBioCollection.|Human Protein Atlas
 generif|records|GeneRIF|Contributes to TheBioCollection; linked to NCBI Gene.|GeneRIF
ncbi_gene|records|NCBI Gene|Contributes to TheBioCollection.|NCBI Gene
go|records|Gene Ontology / GOA|Contributes to TheBioCollection and protein annotation corpora.|Gene Ontology;GOA
cell_ontology|records|Cell Ontology|Contributes to TheBioCollection.|Cell Ontology
cellxgene|records|CELLxGENE|Contributes to TheBioCollection.|CELLxGENE
jump|records|JUMP Cell Painting|Contributes to TheBioCollection.|JUMP Cell Painting
hubmap|records|HuBMAP|Contributes to TheBioCollection.|HuBMAP
hetionet|records|Hetionet|Contributes to TheBioCollection.|Hetionet
drkg|records|DRKG|Contributes to TheBioCollection.|DRKG
dgidb|records|DGIdb|Contributes to TheBioCollection.|DGIdb
string|records|STRING|Contributes to TheBioCollection and BioReason-Pro.|STRING
omnipath|records|OmniPath|Contributes to TheBioCollection.|OmniPath
reactome|records|Reactome|Contributes to TheBioCollection.|Reactome
moltextnet|records|MolTextNet|Molecule-description pairs; overlap with PubChem unresolved.|MolTextNet
pcqm4mv2|records|PCQM4Mv2|Molecular-property records; PubChem-derived entities and additional labels.|PCQM4Mv2
pubchemqc|records|PubChemQC|PubChem-derived quantum-chemistry records; extra coverage unmeasured.|PubChemQC
stitch|records|STITCH|Interaction records; overlap with other interaction sources unresolved.|STITCH
glaser|records|J. Glaser binding-affinity dataset|Binding records; overlap with BindingDB and structural sources unresolved.|jglaser binding affinity
crossdocked|records|CrossDocked2020|Protein-ligand complex records; relation to PDB-based sources unresolved.|CrossDocked2020
alphaseq|records|Open-AlphaSeq|Protein interaction measurements; incremental token count unmeasured.|AlphaSeq
ppiref|records|PPIRef|Protein-interface records; overlaps PDB entities.|PPIRef
ncbi_unspecified|records|Other NCBI resources|The model report does not enumerate a precise reusable release.|NCBI resources
zinc|records|ZINC20|Molecule records used in BioT5; overlap with other molecular sources unresolved.|ZINC20
kegg|records|KEGG|Pathway records used in BioReason; reusable subset and token count unresolved.|KEGG
clinvar|records|ClinVar|Variant records used in BioReason; scope and overlap unresolved.|ClinVar
omim|records|OMIM|Variant/gene records used in BioReason; reusable subset and token count unresolved.|OMIM
dbsnp|records|dbSNP|Variant records used in BioReason.|dbSNP
cosmic|records|COSMIC|Variant records used in BioReason; reusable subset and token count unresolved.|COSMIC
gnomad|records|gnomAD|Variant-frequency records used in BioReason.|gnomAD
interpro|records|InterPro|Protein-domain annotations used in BioReason-Pro.|InterPro
protdescribe|records|ProtDescribe|Swiss-Prot-derived protein descriptions used in ProtST; overlaps UniProt.|ProtDescribe
tdc|records|Therapeutics Data Commons|Task collections used in Tx-LLM/TxGemma; repeated training tokens are not source size.|Therapeutics Data Commons
qm9|records|QM9 / GEOM-QM9|Molecular conformers and properties; QM9 and its GEOM views overlap.|QM9;GEOM-QM9
geomdrugs|records|GEOM-Drugs|Molecular conformers; do not count each representation as a new molecule.|GEOM-Drugs
misato|records|MISATO|Molecular-dynamics and protein-ligand records in later UniGenX repository support.|MISATO
gfp|records|TAPE GFP fluorescence|Sequence/function measurements used by STRIDE.|TAPE GFP
moledit|records|Mega-MolEdit|Molecular-edit training examples used by STRIDE; derivative task data.|Mega-MolEdit
molopt|records|MolOpt-Instructions|Test reference in STRIDE; excluded from the training inventory total.|MolOpt-Instructions
opengenome2|raw|OpenGenome2|8.8T biological nucleotide positions; not a count in the text tokenizer.|OpenGenome2
 gtdb|raw|GTDB|An upstream component of OpenGenome2; not additive to its complete release.|GTDB
imgpr|raw|IMG/PR|An upstream component of OpenGenome2.|IMG/PR
imgvr|raw|IMG/VR|An upstream component of OpenGenome2.|IMG/VR
mgddb|raw|MGD metagenomes|An upstream component of OpenGenome2.|MGD DB
ncbi_genomes|raw|NCBI genome assemblies|An upstream component of OpenGenome2.|NCBI genome assemblies
ensembl|raw|Ensembl|An upstream component of OpenGenome2.|Ensembl
epd|raw|EPDnew|An upstream component of OpenGenome2.|EPDnew
oas|raw|Observed Antibody Space|Antibody sequence pool; no common-tokenizer total established.|OAS
c4|general|C4|General web replay; the biological fraction is unmeasured.|C4
finewebedu|general|FineWeb-Edu|General educational text, overlapping the parent FineWeb collection.|FineWeb-Edu
wikipedia|general|English Wikipedia|General replay; biological subset unmeasured.|English Wikipedia
dclmcc|general|DCLM-CC|General web replay, overlapping other Common Crawl derivatives.|DCLM-CC
eaidclm|general|EAI-DCLM|General web replay; biological fraction unmeasured.|EAI-DCLM
dolma|general|Dolma|Mixed-domain corpus; academic component overlaps peS2o.|Dolma
materials|general|Materials Project|Materials science outside the biological corpus.|Materials Project
crystals|general|MP-20 / Carbon-24 / MPTS-52|Crystal/materials tasks in UniGenX; outside the biological total.|MP-20;Carbon-24;MPTS-52
paperswithcode|general|Papers with Code|General ML resource; biological subset unmeasured.|Papers with Code
'''

# Named upstream inputs confirmed in the cited construction papers, not inferred token totals.
_BUNDLE_INPUTS = {
    'biocollection': ['pubchem','uniprot','pdb','alphafold','bindingdb','drugbank','chembl','uspto50k',
        'gencode','encode','rnacentral','rfam','l1000','hpa','generif','ncbi_gene','go','cell_ontology',
        'cellxgene','jump','hubmap','hetionet','drkg','dgidb','string','omnipath','reactome'],
    'opengenome2': ['gtdb','imgpr','imgvr','mgddb','ncbi_genomes','ensembl','epd','rnacentral','rfam'],
}
_OTHER_INPUTS = {
    'biot5plus': ['ZINC20','PMC','PubMed','bioRxiv','C4','PubChem','UniRef50'],
    'bioreason': ['KEGG','ClinVar','OMIM','dbSNP','COSMIC','gnomAD'],
    'bioreason_pro': ['UniProt','Gene Ontology','InterPro','STRING'],
    'txgemma': ['Therapeutics Data Commons'], 'txllm': ['Therapeutics Data Commons'],
    'protst': ['UniProt', 'ProtDescribe'], 'biomedclip': ['PMC'],
    'unigenx': ['QM9','GEOM-QM9','GEOM-Drugs','MP-20','Carbon-24','MPTS-52','MISATO'],
    'stride': ['TAPE GFP','Mega-MolEdit','MolOpt-Instructions'],
}


def build_source_inventory(data, estimate):
    families = {}
    aliases = {}
    for line in _DEFINITIONS.strip().splitlines():
        sid, group, name, treatment, labels = [v.strip() for v in line.split('|')]
        if group not in GROUPS:
            raise ValueError('Unknown source group: ' + group)
        family = dict(id=sid, group=group, name=name, treatment=treatment,
                      aliases=labels.split(';'), used_by=[], evidence=[], upstream_of=[])
        families[sid] = family
        for label in family['aliases']:
            if label in aliases:
                raise ValueError('Duplicate source alias: ' + label)
            aliases[label] = sid

    all_entries = [e for kind in ('models','training_studies','method_references','corpora')
                   for e in data.get(kind, [])]
    selected = [e for e in all_entries if e['presentation']['section'] in
                {'cpt', 'from_scratch', 'corpora', 'other'}]
    covered_mentions = set()
    unresolved_studies = []
    for entry in selected:
        origins = entry.get('paper_text_origins', {})
        labels = set(entry.get('dataset_sources', {}).get('names', []))
        labels.update(origins.get('direct', [])); labels.update(origins.get('reused', []))
        labels.update(_OTHER_INPUTS.get(entry['id'], []))
        if entry['presentation']['section'] == 'corpora':
            labels.add({'s2orc':'S2ORC','pes2o':'peS2o','dolma':'Dolma'}[entry['id']])
        if not labels:
            unresolved_studies.append(entry['id'])
        for label in labels:
            if label not in aliases:
                raise ValueError('Unmapped named source: ' + label)
            covered_mentions.add(label)
            row = families[aliases[label]]
            row['used_by'].append(entry['id'])
            row['evidence'].extend(s['url'] for s in entry['sources'])

    families['biocollection']['used_by'].append('gravity_bio')
    families['biocollection']['evidence'].append('https://huggingface.co/datasets/trillionlabs/TheBioCollection')
    families['finefineweb']['evidence'].append('https://huggingface.co/datasets/m-a-p/FineFineWeb')
    families['olmo_pdfs']['used_by'].append('olmo3')
    families['olmo_pdfs']['evidence'].append('https://arxiv.org/html/2512.13961v2#S3.SS4')
    families['opengenome2']['used_by'].append('evo2_reference')
    families['opengenome2']['evidence'].append('https://huggingface.co/datasets/arcinstitute/opengenome2')
    for bundle, children in _BUNDLE_INPUTS.items():
        evidence = ('https://arxiv.org/html/2607.08803v1#S2' if bundle == 'biocollection'
                    else 'https://huggingface.co/datasets/arcinstitute/opengenome2')
        for sid in children:
            families[sid]['upstream_of'].append(bundle)
            families[sid]['evidence'].append(evidence)

    for row in families.values():
        for field in ('used_by', 'evidence', 'upstream_of'):
            row[field] = sorted(set(row[field]))
        row['counted_component'] = row['id'] if row['id'] in {'pmc','finefineweb','biocollection'} else None
        row['additional_unique_tokens'] = None
    active = [row for row in families.values() if row['used_by'] or row['upstream_of']]

    raw = estimate['current_web_and_record_inventory']
    paper_range = estimate['paper_text_scenarios']['gross_text_tokens']
    components = [
        dict(id='pmc', group='papers', low=paper_range[0], high=paper_range[-1],
             status='scenario_before_biology_filter', note='All candidate PMC text; not a biology-only amount.'),
        dict(id='finefineweb', group='web', low=raw['web_tokens_local_tokenizer_proxy'],
             high=raw['web_tokens_local_tokenizer_proxy'], status='tokenizer_conversion_proxy',
             note='Biology-labelled web source, before research selection and additional deduplication.'),
        dict(id='biocollection', group='records', low=raw['record_tokens_local_tokenizer_proxy'],
             high=raw['record_tokens_local_tokenizer_proxy'], status='tokenizer_conversion_proxy',
             note='Free-text stream only, including sequence and molecular representations.'),
    ]
    return dict(
        status='complete_named_source_census_incomplete_token_measurement',
        scope='All non-archived biological studies and source corpora in the review, plus documented upstream inputs of TheBioCollection and OpenGenome2.',
        families=active, family_count=len(active), named_labels_mapped=len(covered_mentions),
        unresolved_study_source_details=unresolved_studies,
        components=components,
        quantified_candidate_subtotal_low=sum(c['low'] for c in components),
        quantified_candidate_subtotal_high=sum(c['high'] for c in components),
        complete_biology_only_unique_total=None,
        subtotal_definition='Gross candidate text/record token equivalents for three measurable source families; not a full unique biological total. Other families have unresolved additional contributions.',
        raw_sequence_nucleotide_positions=8_800_000_000_000,
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
w1_build.py  --  Phase W1 deterministic site generator (Disease Mechanisms volume).

VP-SPEC v1.8 discipline:
  * Principle 1: code is the agent of conversion (the model does not free-type the body;
    the body is authored as data-bound templates filled from curated, graded artifacts).
  * C1 reproducibility: EVERY analytical number shown on a page (burden axes O/P/S/M/D,
    raw_burden, efficacy offset e, R_treat, residual burden_score, residual rank) is read
    from the curated CSVs at build time -- never hard-coded in prose. Same inputs -> same
    HTML (2x sha256 identical; verified by w1_gate.py).
  * C1 observed vs reproduced (C-D1): clinical facts (gene function, inheritance, symptoms,
    onset, definitions) are OBSERVED inputs, cited to their source, never "reproduced".
    The reproducible contribution is the analysis layer (classification + burden + residual).
  * C2: canonical material is HTML; no TeX bundled.
  * C3 + provisional-[H]: the burden/residual order is carried as a provisional [H]-grade
    prioritisation device on every page that shows it. Five registry passes have now run
    (R5 treatment accession-dating → [L] 33/35; R6 Orphanet natural-history → onset [L]
    28/35, +1 mortality; R7 open-source natural-history → disability [L] 13/35 from the
    GBD 2013 disability-weights table + 2 mortality axes independently corroborated from
    PMC survival literature; R8 open-source severity → the HPO clinical-modifier Severity
    subtree (HP:0012824) via a cited dominant-sequela join lifts severity to [L] for the
    one disease whose defining sequela is annotated; R9 curated severity/progression →
    progression lifts to [L] from cited PMC open-access literature via a dominant-sequela
    join whose tier is DERIVED by the frozen R3 tier function (Niemann-Pick type A → a 3rd
    order_locked disease; Duchenne MD corroborated, not locked — its severity stays [H]),
    order_locked 3/35). The remaining lift (the rest of severity — feature-level in the
    open HPO annotations, a category error if used as a disease tier — and most
    progression) is named, never guessed; the OMIM clinical-synopsis path is removed (its
    API key is unobtainable for an individual researcher), not deferred. A read-only
    unmet-need / treatment-gap surface (data/curated/unmet_need_surface.*) re-presents the
    same registry as a graded research-prioritisation signal — never clinical advice.
  * C4 retrieval-readiness / Google discoverability: ONE standalone HTML per disease at a
    unique URL, disease-name-leading <title> + meta description, answer-first <p class=answer>
    (40-60 words), self-contained vp-cards, JSON-LD (MedicalCondition + ScholarlyArticle +
    BreadcrumbList), sitemap + crawler-allowing robots + llms.txt.

This is living code (post-dates the R2 engine freeze); it is NOT in MANIFEST_governed.sha256.
"""
import json, csv, os, html, hashlib, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR  = os.path.join(ROOT, "data", "curated")
DOSS = os.path.join(CUR, "dossiers")
DOCS = os.path.join(ROOT, "docs")
VOLDIR = os.path.join(DOCS, "disease")

SITE = "https://jamming-physics.org"
VOL_SHORT = "Disease Mechanisms"
VOL_TITLE = "Systemic Genetic & Rare Disease Mechanisms"
AUTHOR = "Young Jae Lee"
ORCID = "https://orcid.org/0009-0002-7535-8245"
PARENT_REPO = "https://github.com/rego093-sketch/jamming-physics"
PHYSICS_DOI = "https://doi.org/10.5281/zenodo.17932566"
VOLUME_DOI  = "10.5281/zenodo.20763842"   # concept DOI (registered, VP-SPEC §2)
BUILD_DATE = "2026-06-18"
HPOA_VER = "phenotype.hpoa v2026-06-06"

# ----------------------------------------------------------------------------- load curated data
def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

# Prefer the R5 registry artifacts (treatment grades accession-dated [H]->[L]; burden grades
# corroborated by GeneReviews; order_locked flag) when present; fall back to the R3/R4 banked
# files. The registry CSVs preserve every R3/R4 column, so existing field reads are unchanged;
# the lift shows through as tr["grade"]==[L] and per-axis [L] grades.
def _pick(*names):
    for n in names:
        p = os.path.join(CUR, n)
        if os.path.exists(p):
            return p
    return os.path.join(CUR, names[-1])

residual = {r["cui"]: r for r in load_csv(_pick("burden_residual_registry.csv", "burden_residual.csv"))}
scores   = {r["cui"]: r for r in load_csv(_pick("burden_scores_registry.csv", "burden_scores.csv"))}
treats   = {r["cui"]: r for r in load_csv(_pick("treatments_registry.csv", "treatments.csv"))}
REGISTRY = os.path.exists(os.path.join(CUR, "treatments_registry.csv"))

def _locked_n_names():
    """(count, 'Name A, Name B, ...') of order_locked diseases — read live from the registry."""
    names = sorted(scores[c]["entity"] for c in scores if scores[c].get("order_locked") == "yes")
    return len(names), (", ".join(names) or "none")

dossiers = {}
for fn in os.listdir(DOSS):
    if fn.endswith(".json") and not fn.startswith("_"):
        d = json.load(open(os.path.join(DOSS, fn)))
        dossiers[d["identity"]["medgen_cui"]] = (fn[:-5], d)

# placed (rankable) cohort, ordered by residual rank
placed = sorted([r for r in residual.values() if r["rankable"] == "yes"],
                key=lambda r: int(r["residual_rank"]))
RANK_TOTAL = len(placed)  # 17

# ----------------------------------------------------------------------------- authored per-disease prose
# Each value is OBSERVED-grounded narrative (from the cited MedGen clinical_definition + the
# curated mechanism class). Numbers are never placed here -- only {placeholders} the generator
# fills from the curated CSVs (so the gate can re-verify drift 0).
#   mech     : protein function + what the variant does (consistent with the curated mech class)
#   clinical : in-scope organ involvement, plain words
#   xref     : (optional) excluded-organ feature owned by sibling neuro/mind, named + linked
#   emergence: (optional) which normal-development engine quantity the disease perturbs
A = {
 "C0220685": {  # Achondrogenesis type II
  "mech": "COL2A1 encodes type II collagen, the principal structural collagen of cartilage. A defective allele degrades the cartilage template on which endochondral bone is laid down, so the skeleton fails to ossify normally.",
  "clinical": "The result is severe micromelic (short-limbed) dwarfism with a small chest, prominent abdomen, incomplete ossification of the vertebral bodies, and a disorganised costochondral junction. The disorder is perinatal-lethal.",
  "emergence": "Achondrogenesis type II perturbs the cartilage-to-bone (endochondral) growth programme that the carried morphogenesis engine forward-simulates as its normal-development baseline.",
 },
 "C0268242": {  # Niemann-Pick disease, type A
  "mech": "SMPD1 encodes acid sphingomyelinase. Biallelic loss of its activity lets sphingomyelin accumulate in lysosomes throughout the viscera and the nervous system (acid sphingomyelinase deficiency, ASMD).",
  "clinical": "Infantile neurovisceral ASMD presents with hepatosplenomegaly, failure to thrive, a cherry-red macula, and a rapidly progressive, fatal neurodegeneration in the first years of life.",
  "xref": ("the neuronopathic central-nervous-system course of infantile ASMD", "neuro"),
 },
 "C0002312": {  # alpha Thalassemia
  "mech": "The duplicated alpha-globin genes HBA1 and HBA2 encode alpha-globin. Deletion or inactivation of alpha-globin alleles lowers alpha-globin output and imbalances the alpha/beta globin-synthesis ratio.",
  "clinical": "Two clinically significant forms result: hemoglobin H disease (a hypochromic microcytic haemolytic anaemia, usually from loss of three alleles) and, with loss of all four alleles, the in-utero-lethal Hb Bart hydrops fetalis syndrome.",
 },
 "C0917713": {  # Becker muscular dystrophy
  "mech": "DMD encodes dystrophin, the cytoskeletal protein that anchors the muscle-fibre membrane to the contractile apparatus. In-frame variants leave a shortened but partly functional dystrophin, milder than the frame-disrupting loss seen in Duchenne dystrophy.",
  "clinical": "Becker dystrophy presents later than Duchenne, with slowly progressive proximal weakness and calf pseudohypertrophy, and a more preserved ambulation.",
  "xref": ("DMD-associated dilated cardiomyopathy", "neuro"),
 },
 "C0029434": {  # Osteogenesis imperfecta
  "mech": "COL1A1 and COL1A2 encode the two chains of type I collagen, the dominant protein of bone matrix. Glycine substitutions poison the collagen triple helix (a dominant-negative effect), while null alleles simply reduce collagen output (haploinsufficiency).",
  "clinical": "The phenotype is recurrent fractures with minimal trauma, together with variable dentinogenesis imperfecta, blue sclerae, and adult-onset hearing loss, ranging from a perinatal-lethal end to a mild form.",
  "emergence": "Osteogenesis imperfecta perturbs bone-matrix formation, part of the normal-development baseline the carried morphogenesis engine simulates.",
 },
 "C0013264": {  # Duchenne muscular dystrophy
  "mech": "DMD encodes dystrophin; frame-disrupting variants abolish the protein, leaving muscle fibres mechanically fragile and progressively degenerating. It is the severe pole of the X-linked dystrophinopathy spectrum.",
  "clinical": "Boys present in early childhood with proximal weakness, calf hypertrophy, and delayed motor milestones, progressing to loss of ambulation and respiratory decline.",
  "xref": ("the DMD-associated dilated cardiomyopathy", "neuro"),
 },
 "C0002986": {  # Fabry disease
  "mech": "GLA encodes the lysosomal enzyme alpha-galactosidase A. Deficient activity causes progressive lysosomal deposition of globotriaosylceramide (Gb3) in vascular endothelium, kidney, and heart.",
  "clinical": "Manifestations include acroparaesthesia and angiokeratomas, proteinuria progressing to renal insufficiency, and left-ventricular hypertrophy. As an X-linked disorder it is fully expressed in males and variably in heterozygous females.",
 },
 "C0268490": {  # Tyrosinemia type I
  "mech": "FAH encodes fumarylacetoacetate hydrolase, the terminal enzyme of tyrosine catabolism. Its loss diverts the pathway into the toxic intermediate succinylacetone, which damages liver and kidney.",
  "clinical": "Untreated disease presents in infancy with severe liver involvement or, later in the first year, with hepatic and renal-tubular dysfunction, growth failure, and rickets; hepatocellular carcinoma is a long-term risk.",
 },
 "C2751306": {  # Polycystic kidney disease 2
  "mech": "PKD2 encodes polycystin-2, a calcium-permeable channel of the renal primary cilium. Reduced function raises cyst-driving intracellular cAMP, so fluid-filled cysts expand in both kidneys over decades.",
  "clinical": "The cited definition characterises this as autosomal dominant polycystic kidney disease: bilateral kidney cysts with progressive loss of renal function, liver cysts, and an increased risk of intracranial aneurysm. (The structured MedGen mode-of-inheritance field is unpopulated for this concept.)",
 },
 "C0751202": {  # Classic homocystinuria
  "mech": "CBS encodes cystathionine beta-synthase, which clears homocysteine by committing it to cystathionine. Its deficiency raises plasma homocysteine, which damages the lens zonules, skeleton, and vascular endothelium.",
  "clinical": "Four systems are involved: the eye (ectopia lentis, severe myopia), the skeleton (tall stature, long limbs, osteoporosis, scoliosis), the vasculature (thromboembolism), and the central nervous system.",
  "xref": ("the cognitive / central-nervous-system involvement", "neuro"),
 },
 "C0010674": {  # Cystic fibrosis
  "mech": "CFTR encodes an epithelial chloride and bicarbonate channel. Loss of function -- for the common p.Phe508del allele, a protein folding and trafficking defect -- dehydrates secretions across many epithelia.",
  "clinical": "The disease affects the respiratory tract, exocrine pancreas, intestine, hepatobiliary system, and sweat glands, with bronchiectasis, recurrent sinusitis, pancreatic insufficiency, and a diagnostically elevated sweat chloride.",
 },
 "C1961835": {  # Gaucher disease type I
  "mech": "GBA1 encodes the lysosomal enzyme glucocerebrosidase. Its deficiency loads macrophages with glucosylceramide; type 1, the non-neuronopathic form, spares the central nervous system.",
  "clinical": "Type 1 Gaucher disease produces hepatosplenomegaly, thrombocytopenia and anaemia, and bone disease (pain, infarcts, osteopenia), with a markedly elevated glucosylsphingosine biomarker.",
 },
 "C0086795": {  # Hurler syndrome
  "mech": "IDUA encodes alpha-L-iduronidase. Its deficiency stores the glycosaminoglycans dermatan and heparan sulfate in lysosomes throughout the body (mucopolysaccharidosis type I), of which Hurler syndrome is the severe pole.",
  "clinical": "Features include coarse facies, organomegaly, skeletal dysostosis multiplex, corneal clouding, hearing loss, and -- at the severe Hurler end -- progressive neurodegeneration.",
  "xref": ("the severe-end central-nervous-system involvement", "neuro"),
 },
 "C0017921": {  # Glycogen storage disease, type II (Pompe)
  "mech": "GAA encodes acid alpha-glucosidase, the lysosomal enzyme that degrades glycogen. Its deficiency traps glycogen in the lysosomes of cardiac and skeletal muscle (Pompe disease).",
  "clinical": "Infantile-onset disease combines a hypertrophic cardiomyopathy with profound hypotonia; late-onset disease presents as a slowly progressive limb-girdle and respiratory-muscle weakness.",
  "xref": ("the infantile-onset hypertrophic cardiomyopathy", "neuro"),
 },
 "C0017205": {  # Gaucher disease (aggregate)
  "mech": "Gaucher disease is glucocerebrosidase deficiency spanning a continuum from a perinatal-lethal form to an asymptomatic type. The causative gene is not annotated at this MedGen aggregate concept, so gene-level fields here are open and point to the gene-resolved type I section.",
  "clinical": "The systemic (type 1) picture is hepatosplenomegaly, cytopenias, and bone disease; the neuronopathic types 2 and 3 add a central-nervous-system course.",
  "xref": ("the neuronopathic (type 2 / type 3) central-nervous-system course", "neuro"),
 },
 "C0268487": {  # Tyrosinemia type II
  "mech": "TAT encodes hepatic tyrosine aminotransferase, the first enzyme of tyrosine breakdown. Its deficiency raises plasma tyrosine, which crystallises in the cornea and skin.",
  "clinical": "The disease is defined by corneal dystrophy, painful palmoplantar hyperkeratosis, and variable intellectual disability; individuals treated from early infancy may remain nearly asymptomatic.",
 },
 "C0024796": {  # Marfan syndrome
  "mech": "FBN1 encodes fibrillin-1, the scaffold protein of connective-tissue microfibrils. Defective fibrillin-1 weakens the extracellular matrix and dysregulates TGF-beta signalling, acting through dominant-negative and haploinsufficiency modes.",
  "clinical": "In-scope features are skeletal (tall marfanoid habitus, long limbs, scoliosis), ocular (ectopia lentis), and dural (dural ectasia); clinical variability is high.",
  "xref": ("the aortic-root dilatation and dissection risk", "neuro"),
  "emergence": "Marfan syndrome perturbs connective-tissue patterning, relevant to the morphogenetic baseline the carried engine simulates.",
 },

 # ---- not-placed cohort (axes_scored < 3 of 5; rank null) ----
 "C2936858": {  # 21-Hydroxylase-deficient CAH
  "mech": "CYP21A2 encodes 21-hydroxylase, an adrenal cytochrome-P450 enzyme of cortisol and aldosterone synthesis. Biallelic deficiency blocks cortisol production; the lost negative feedback drives ACTH-stimulated adrenal hyperplasia and shunts steroid precursors into androgens.",
  "clinical": "Classic 21-hydroxylase deficiency presents as salt-wasting or simple-virilising congenital adrenal hyperplasia: prenatal virilisation of affected females, and life-threatening neonatal salt-wasting crises in the salt-wasting form; a milder non-classic form presents later.",
 },
 "C0001080": {  # Achondroplasia
  "mech": "FGFR3 encodes fibroblast growth factor receptor 3, a negative regulator of bone growth. A recurrent gain-of-function variant leaves the receptor constitutively active, suppressing chondrocyte proliferation at the growth plate.",
  "clinical": "Achondroplasia is the most common skeletal dysplasia: disproportionate short stature with rhizomelic limb shortening, macrocephaly with frontal bossing, midface hypoplasia, and trident hands.",
  "xref": ("the cervicomedullary (foramen-magnum) compression risk", "neuro"),
  "emergence": "Achondroplasia perturbs the growth-plate length scale that the carried morphogenesis engine forward-simulates as its normal-development baseline.",
 },
 "C0162565": {  # Acute intermittent porphyria
  "mech": "HMBS encodes hydroxymethylbilane synthase, the third enzyme of haem biosynthesis. Haploinsufficiency lets the neurotoxic precursors delta-aminolevulinic acid and porphobilinogen accumulate when haem demand rises.",
  "clinical": "Acute neurovisceral attacks bring severe abdominal pain, autonomic instability, hyponatraemia, peripheral neuropathy, and neuropsychiatric features, typically provoked by certain drugs, fasting, or hormonal cycles.",
  "xref": ("the central and peripheral neuropsychiatric attack features", "neuro"),
 },
 "C0002066": {  # Alkaptonuria
  "mech": "HGD encodes homogentisate 1,2-dioxygenase in the tyrosine-degradation pathway. Its deficiency lets homogentisic acid accumulate and polymerise, depositing an ochronotic pigment in connective tissue.",
  "clinical": "Urine darkens on standing from infancy; in adulthood ochronotic pigment accumulates in cartilage and a degenerative ochronotic arthropathy of the spine and large joints develops, with cardiac-valve and renal-stone involvement.",
 },
 "C0221757": {  # Alpha-1-antitrypsin deficiency
  "mech": "SERPINA1 encodes alpha-1 antitrypsin, the principal serum inhibitor of neutrophil elastase. The Z allele misfolds and polymerises within hepatocytes, causing both a loss of antiprotease lung protection and a toxic hepatic accumulation.",
  "clinical": "Two organs are affected across the lifespan: early-onset panacinar emphysema and chronic obstructive lung disease (accelerated by smoking), and liver disease ranging from neonatal cholestasis to adult cirrhosis.",
 },
 "CN322236": {  # Beta-thalassemia
  "mech": "HBB encodes beta-globin. Absent or reduced beta-globin synthesis imbalances the alpha/beta-globin ratio, so excess alpha-globin precipitates and drives ineffective erythropoiesis and haemolysis.",
  "clinical": "Beta-thalassemia major presents in infancy with transfusion-dependent anaemia, extramedullary haematopoiesis and skeletal change, and transfusional iron overload; beta-thalassemia intermedia is a milder, later-presenting form.",
 },
 "C4316899": {  # Cystinosis
  "mech": "CTNS encodes cystinosin, the lysosomal cystine transporter. Its loss traps cystine inside lysosomes, where it crystallises and progressively damages cells in the kidney and other organs.",
  "clinical": "Nephropathic (infantile) cystinosis presents with a renal Fanconi syndrome from infancy progressing to renal failure, with corneal cystine crystals, hypothyroidism, and a later distal myopathy.",
 },
 "C0010691": {  # Cystinuria
  "mech": "SLC3A1 and SLC7A9 encode the two subunits of the renal and intestinal dibasic-amino-acid transporter. Defective cystine reabsorption raises urinary cystine above its solubility, so it crystallises into stones.",
  "clinical": "Recurrent cystine kidney stones present from childhood, bringing renal colic, obstruction, infection, and a cumulative threat to renal function.",
 },
 "C0268335": {  # EDS classic
  "mech": "COL5A1 encodes a chain of type V collagen, which templates type I collagen fibril assembly. Haploinsufficiency yields disorganised dermal collagen fibrils.",
  "clinical": "Classic Ehlers-Danlos syndrome combines skin hyperextensibility, atrophic cigarette-paper scarring, and generalised joint hypermobility with recurrent dislocations and easy bruising.",
  "emergence": "Classic EDS perturbs collagen fibrillogenesis within the connective-tissue patterning the carried morphogenesis engine treats as baseline.",
 },
 "C0268338": {  # EDS vascular
  "mech": "COL3A1 encodes type III collagen, a major collagen of arterial and hollow-organ walls. A dominant-negative or null defect weakens those walls.",
  "clinical": "Vascular Ehlers-Danlos syndrome presents with thin translucent skin, easy bruising, and characteristic facies, and is defined by the risk of spontaneous arterial, intestinal, or uterine rupture.",
  "emergence": "Vascular EDS perturbs the vessel-wall collagen substrate of the morphogenetic baseline the carried engine simulates.",
 },
 "C0002895": {  # Hb SS / sickle cell
  "mech": "A single HBB variant produces sickle haemoglobin (HbS) that polymerises when deoxygenated, deforming the red cell into the sickle shape.",
  "clinical": "Sickle cell disease brings chronic haemolytic anaemia and recurrent vaso-occlusive events causing ischaemic pain crises, acute chest syndrome, splenic and renal injury, and cumulative organ damage.",
  "xref": ("the cerebral vaso-occlusive stroke risk", "neuro"),
 },
 "C3469186": {  # Hemochromatosis type 1
  "mech": "HFE regulates hepcidin, the master iron-regulatory hormone. Loss of HFE function lowers hepcidin, so intestinal iron absorption is inappropriately high and iron deposits in parenchymal organs.",
  "clinical": "Progressive iron overload in mid-adult life causes hepatic cirrhosis, diabetes mellitus, cardiomyopathy, arthropathy, and skin pigmentation.",
 },
 "C0008533": {  # Hemophilia B / factor IX
  "mech": "F9 encodes coagulation factor IX. Deficient factor IX activity impairs the intrinsic coagulation cascade, so thrombin generation is reduced.",
  "clinical": "This X-linked bleeding disorder causes haemarthroses, deep-tissue bleeds, and prolonged bleeding after trauma, dental work, or surgery, graded by the residual factor IX level.",
 },
 "C0019069": {  # Hemophilia A / factor VIII
  "mech": "F8 encodes coagulation factor VIII. Its deficiency impairs the intrinsic clotting pathway.",
  "clinical": "This X-linked bleeding disorder causes recurrent joint and muscle bleeds and prolonged surgical or traumatic bleeding, with severity set by the residual factor VIII level.",
 },
 "C0024776": {  # Maple syrup urine disease
  "mech": "The branched-chain alpha-ketoacid dehydrogenase complex (BCKDHA and BCKDHB subunits) decarboxylates the branched-chain amino acids. Its deficiency lets leucine and its ketoacid accumulate to neurotoxic levels.",
  "clinical": "Classic maple syrup urine disease presents in the neonate with the characteristic maple-syrup odour, feeding difficulty, and encephalopathy, progressing without treatment to fatal cerebral oedema.",
  "xref": ("the acute and chronic encephalopathy", "neuro"),
 },
 "C0031485": {  # Phenylketonuria
  "mech": "PAH encodes phenylalanine hydroxylase, which converts phenylalanine to tyrosine. Its deficiency lets phenylalanine accumulate to levels toxic to the developing brain.",
  "clinical": "Untreated phenylalanine-hydroxylase deficiency causes intellectual disability, seizures, and behavioural disturbance; treated from birth by dietary phenylalanine restriction, cognitive outcome is preserved.",
  "xref": ("the intellectual-disability and seizure phenotype of untreated disease", "neuro"),
 },
 "C0019202": {  # Wilson disease
  "mech": "ATP7B encodes a copper-transporting ATPase that exports hepatic copper into bile. Its loss causes copper to accumulate first in the liver and then in the brain and other organs.",
  "clinical": "Wilson disease presents with hepatic disease (hepatitis, cirrhosis), and the in-scope features extend to Kayser-Fleischer corneal rings and a Coombs-negative haemolytic anaemia.",
  "xref": ("the neurologic movement disorder and psychiatric features", "neuro"),
 },
 "C1264039": {  # von Willebrand disease type 1
  "mech": "VWF encodes von Willebrand factor, which mediates platelet adhesion and carries factor VIII in plasma. Type 1 disease is a partial quantitative deficiency of von Willebrand factor.",
  "clinical": "Type 1 von Willebrand disease causes mucocutaneous bleeding — epistaxis, menorrhagia, easy bruising — and excessive bleeding with trauma or surgical procedures.",
 },
}

INH_SHORT = {
 "Autosomal recessive inheritance": "autosomal recessive",
 "Autosomal dominant inheritance": "autosomal dominant",
 "X-linked recessive inheritance": "X-linked recessive",
 "X-linked dominant inheritance; X-linked recessive inheritance": "X-linked",
 "Autosomal dominant inheritance; Autosomal recessive inheritance; X-linked recessive inheritance":
     "mostly autosomal dominant (also recessive forms)",
 "not_stated": "mode of inheritance not populated in the structured source",
}
MECH_ANS = {  # compact mechanism phrase for the answer-first sentence only (full value stays in the body)
 "C0029434": "dominant-negative and haploinsufficiency mechanisms",  # osteogenesis imperfecta
 "C0024796": "dominant-negative and haploinsufficiency mechanisms",  # Marfan
 "C0010674": "loss of function (a folding/trafficking defect for p.Phe508del)",  # cystic fibrosis
}
STATUS_CLAUSE = {
 "none": "no disease-directed therapy alters its course",
 "symptomatic": "only symptomatic / supportive care is established",
 "disease-modifying (partial)": "established therapy is partially disease-modifying",
 "disease-modifying (substantial)": "established therapy is substantially disease-modifying",
}

# ----------------------------------------------------------------------------- helpers
def esc(s): return html.escape(str(s), quote=True)

def slugify(entity, num):
    s = entity.lower()
    out = []
    for ch in s:
        if ch.isalnum(): out.append(ch)
        else: out.append("-")
    s = "-".join(t for t in "".join(out).split("-") if t)
    stop = {"the","a","an","of","and","as","its","for","to","in","on","with","from"}
    words = [w for w in s.split("-") if w not in stop]
    s = "-".join(words[:5])
    return f"{num:02d}-{s}"

def gi(grade):
    """inline grade chip e.g. [L] -> coloured span"""
    g = grade.strip("[]")
    return f'<span class="grade-inline gi-{esc(g)}">{esc(grade)}</span>'

def num(x, places=4):
    if x is None or x == "": return None
    try: return f"{float(x):.{places}f}"
    except ValueError: return str(x)

def page_skeleton(title, desc, canonical, jsonld_blocks, body, prev_lnk, next_lnk):
    blocks = "\n".join(jsonld_blocks)
    pn = ['<nav class="pn">']
    pn.append(f'<a rel="prev" href="{prev_lnk[0]}">&larr; {esc(prev_lnk[1])}</a>' if prev_lnk
              else '<span></span>')
    pn.append('<a href="/disease/">Volume contents</a>')
    pn.append(f'<a rel="next" href="{next_lnk[0]}">{esc(next_lnk[1])} &rarr;</a>' if next_lnk
              else '<span></span>')
    pn.append('</nav>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/assets/css/site.css">
<meta name="author" content="{esc(AUTHOR)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
{blocks}
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="/disease/">{esc(VOL_SHORT)}</a></nav></header>
<main>
{body}
{''.join(pn)}
</main>
<footer>
<p>{esc(VOL_TITLE)} &middot; author <a href="{ORCID}">{esc(AUTHOR)}</a> &middot;
   part of the <a href="/">Jamming Physics</a> programme (jamming branch &rarr; <a href="/physics/">VP Theory</a>).</p>
<p>Research whitepaper, not clinical guidance: mechanisms and population-level facts only; no dosing, diagnosis, or individualised advice. Licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
<p class="note">Volume DOI: <a href="https://doi.org/10.5281/zenodo.20763842">10.5281/zenodo.20763842</a>. Reproduction: in-package deterministic pipeline at <a href="{PARENT_REPO}">{esc(PARENT_REPO.replace('https://',''))}</a>.</p>
</footer>
</body>
</html>
"""

def jsonld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            + '</script>')

def breadcrumb_ld(section_name, url):
    return jsonld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":VOL_SHORT,"item":SITE+"/disease/"},
        {"@type":"ListItem","position":3,"name":section_name,"item":url}]})

# ----------------------------------------------------------------------------- per-disease page
def build_disease(idx, r):
    cui = r["cui"]
    slug, d = dossiers[cui]
    sc = scores[cui]; tr = treats[cui]
    num_sec = idx + 2                     # framework is section 1; diseases start at 2
    page_slug = slugify(r["entity"], num_sec)
    url = f"{SITE}/disease/{page_slug}/"
    ent = r["entity"]
    idn = d["identity"]
    genes = idn.get("genes", [])
    gene_str = ", ".join(genes) if genes else "(gene not annotated at this aggregate concept)"
    system = idn.get("system_class", r["system_class"])
    inh = d["inheritance"]; mech = d["molecular_mechanism"]
    a = A[cui]

    # ---- data-bound analytical values (READ FROM CSV; the C1 contract) ----
    rrank = r["residual_rank"]; rawrank = r["raw_rank"]; shift = r["rank_shift_vs_raw"]
    raw = num(r["raw_burden"]); bscore = num(r["burden_score"])
    e = num(tr["efficacy_offset_e"]); rtreat = num(tr["R_treat"])
    status = r["evidence_status"]
    axisvals = {ax: (num(sc[ax+"_value"]), sc[ax+"_grade"]) for ax in ["O","P","S","M","D"]}
    axes_scored = sc["axes_scored"]

    # ---- title + description (disease name leads -- Google exact-match) ----
    title = f"{ent} \u2014 {VOL_SHORT} \u00a7{num_sec} | Jamming Physics"
    inh_sd = INH_SHORT.get(inh["value"], inh["value"])
    primary_gene = genes[0] if genes else "gene not annotated at this aggregate concept"
    gene_clause = f"gene {primary_gene}" if genes else primary_gene
    desc = (f"{ent}: a {system} genetic disease ({gene_clause}). "
            f"Mechanism, inheritance, a reproducible burden rank, and treatment \u2014 each graded.")
    if len(desc) > 160:  # word-boundary safety net
        desc = desc[:159].rsplit(" ", 1)[0]

    # ---- answer-first (40-60 words, self-contained) ----
    sc_clause = STATUS_CLAUSE[status]
    if cui == "C2751306":
        inh_ans = "variants in PKD2 (structured inheritance unpopulated, graded open; the definition describes autosomal dominant disease)"
    elif not genes:
        inh_ans = "glucocerebrosidase deficiency (the gene is not annotated at this aggregate concept)"
    else:
        inh_ans = f"{inh_sd} variants in {gene_str}"
    mech_ans = MECH_ANS.get(cui, mech["value"])
    answer = (f"{ent} is a {system} genetic disease caused by {inh_ans}, acting through "
              f"{mech_ans}. Within this volume's rankable burden cohort it sits at residual rank "
              f"{rrank} of {RANK_TOTAL}, where {sc_clause}. That order is a provisional "
              f"[H]-grade prioritisation device, not a registry-locked ranking.")

    # ---- abstract (<=3 sentences, carries the residual figure) ----
    abstract = (f"{ent} is inherited as {inh_sd} and acts by {mech['value']} "
                f"({gi(mech['grade'])}). Its pre-treatment burden proxy is {raw} and, after the established "
                f"therapy's efficacy offset e = {e} is applied, its residual burden score is {bscore} "
                f"({gi(r['burden_score_grade'])}), placing it at residual rank {rrank} of {RANK_TOTAL}.")

    # ---- JSON-LD: MedicalCondition (SEO/medical) + ScholarlyArticle + Breadcrumb ----
    anatomy = []
    for o in d["clinical"].get("organ_systems", {}).get("value", [])[:6]:
        nm = o.get("system","").replace("Abnormality of the ","").replace("Abnormality of ","")
        if nm: anatomy.append({"@type":"AnatomicalSystem","name":nm})
    symptoms = []
    for s in d["clinical"].get("cardinal_symptoms", {}).get("value", [])[:5]:
        if s.get("name"): symptoms.append({"@type":"MedicalSignOrSymptom","name":s["name"]})
    codes = [{"@type":"MedicalCode","codeValue":cui,"codingSystem":"MedGen"}]
    for omim in idn.get("omim_codes", [])[:3]:
        codes.append({"@type":"MedicalCode","codeValue":str(omim),"codingSystem":"OMIM"})
    mc = {"@context":"https://schema.org","@type":"MedicalCondition","name":ent,
          "code":codes,"associatedAnatomy":anatomy,"signOrSymptom":symptoms,
          "possibleTreatment":{"@type":"MedicalTherapy","name":tr["modality"]},
          "epidemiology":"genetic / rare disease",
          "url":url}
    if genes:
        mc["cause"]={"@type":"MedicalCause","name":f"pathogenic variants in {gene_str}"}
    sa = {"@context":"https://schema.org","@type":"ScholarlyArticle","headline":ent,
          "isPartOf":{"@type":"CreativeWorkSeries","name":VOL_SHORT},
          "position":num_sec,
          "author":{"@type":"Person","name":AUTHOR,"sameAs":ORCID},
          "datePublished":BUILD_DATE,"dateModified":BUILD_DATE,
          "isBasedOn":PARENT_REPO,
          "license":"https://creativecommons.org/licenses/by/4.0/",
          "about":{"@type":"MedicalCondition","name":ent},
          "url":url}
    blocks = [jsonld(sa), jsonld(mc), breadcrumb_ld(ent, url)]

    # ---- claim strip ----
    claim = (f'<aside class="claim-strip">'
             f'<span class="grade g-hypothesis">[H] provisional order</span>'
             f'<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
             f'<a href="/disease/01-classification-burden-treatment-framework/#burden">Burden method &sect;1</a>'
             f'<a href="{PARENT_REPO}">Reproduce (pipeline)</a>'
             f'<span class="doi">DOI <a href="https://doi.org/10.5281/zenodo.20763842">10.5281/zenodo.20763842</a></span>'
             f'</aside>')

    # ---- burden vp-card (self-contained, links to canonical derivation) ----
    burden_card = (f'<aside class="vp-card" data-locked="burden-{esc(cui)}">'
                   f'<b>Residual burden score = {bscore}</b> <span class="g">{gi(r["burden_score_grade"])}</span> '
                   f'&mdash; the renormalised-mean burden proxy over {axes_scored} scored axes '
                   f'(raw {raw}) reduced by the treatment efficacy offset e = {e}, i.e. '
                   f'burden_score = raw_burden &middot; (1 &minus; e). Residual rank {rrank} of {RANK_TOTAL}. '
                   f'<a href="/disease/01-classification-burden-treatment-framework/#burden">Canonical derivation &sect;1</a>.'
                   f'</aside>')

    # ---- emergence vp-card (developmental diseases) ----
    emergence_card = ""
    if a.get("emergence"):
        emergence_card = (f'<aside class="vp-card" data-locked="emergence-lambda">'
                          f'<b>Normal-development baseline</b> <span class="g">{gi("[L]")}</span> '
                          f'&mdash; the carried morphogenesis engine forward-simulates normal development from '
                          f'measured, cited biophysics (e.g. the length band &lambda; = &radic;(D&middot;&tau;)) and '
                          f'never reads disease data (NON-FIT). This disease is read as a perturbation of that baseline. '
                          f'<a href="/disease/01-classification-burden-treatment-framework/#emergence">Engine baseline &sect;1</a>.'
                          f'</aside>')

    # ---- cross-reference (excluded organ owned by sibling) ----
    xref = ""
    if a.get("xref"):
        feat, sib = a["xref"]
        xref = (f'<div class="xref">Scope boundary: {feat} is owned by the sibling '
                f'<a href="/{sib}/">neuro/mind whitepaper</a> and is cross-referenced here, not duplicated '
                f'(SCOPE.md primary-system rule).</div>')

    # ---- body sections ----
    # mechanism
    body = [f'<h1>{esc(ent)}</h1>',
            f'<p class="answer">{answer}</p>',
            f'<p class="abstract">{abstract}</p>',
            claim]

    body.append('<h2 id="mechanism">Gene, inheritance, and molecular mechanism</h2>')
    body.append(f'<p>{esc(ent)} is inherited as <b>{esc(inh["value"])}</b> {gi(inh["grade"])} and is '
                f'classified mechanistically as <b>{esc(mech["value"])}</b> {gi(mech["grade"])}. '
                f'{esc(a["mech"])}</p>')
    body.append(f'<p class="note">Inheritance source: {esc(inh.get("source","(structured MedGen field)"))}. '
                f'Mechanism source: {esc(mech.get("source",""))}. These are observed, cited inputs; the '
                f'inheritance and mechanism <i>classification</i> is the reproducible analysis layer (C-D1).</p>')

    body.append('<h2 id="clinical">In-scope clinical involvement</h2>')
    body.append(f'<p>{esc(a["clinical"])}</p>')
    # organ-system table from HPO
    orgs = d["clinical"].get("organ_systems", {})
    org_vals = orgs.get("value", [])[:6]
    if org_vals:
        rows = "".join(
            f'<tr><td>{esc(o.get("system","").replace("Abnormality of the ","").replace("Abnormality of ",""))}</td>'
            f'<td class="num">{esc(o.get("supporting_term_count",""))}</td></tr>'
            for o in org_vals)
        body.append('<table><thead><tr><th>Organ system (HPO rollup)</th><th>terms</th></tr></thead>'
                    f'<tbody>{rows}</tbody></table>')
        body.append(f'<p class="note">Organ systems {gi(orgs.get("grade","[L]"))} from {esc(orgs.get("source", HPOA_VER))}.</p>')
    if xref: body.append(xref)

    body.append('<h2 id="burden">Reproducible burden position</h2>')
    body.append(burden_card)
    # axis table
    axrows = ""
    axis_names = {"O":"Onset earliness","P":"Progression","S":"Symptom severity",
                  "M":"Mortality","D":"Disability"}
    for ax in ["O","P","S","M","D"]:
        v,g = axisvals[ax]
        axrows += (f'<tr><td>{axis_names[ax]} ({ax})</td>'
                   f'<td class="num">{v if v is not None else "&mdash;"}</td>'
                   f'<td>{gi(g)}</td></tr>')
    body.append('<table><thead><tr><th>Burden axis</th><th>value</th><th>grade</th></tr></thead>'
                f'<tbody>{axrows}</tbody></table>')
    scored_ax = [ax for ax in ["O", "P", "S", "M", "D"] if axisvals[ax][0] is not None]
    L_ax = [ax for ax in scored_ax if axisvals[ax][1] in ("[L]", "[V]")]
    H_ax = [ax for ax in scored_ax if axisvals[ax][1] == "[H]"]
    nm = {"O": "onset", "P": "progression", "S": "severity", "M": "mortality", "D": "disability"}
    def axlist(xs):
        names = [nm[x] for x in xs]
        if not names:
            return ""
        return names[0] if len(names) == 1 else (" and ".join(names) if len(names) == 2
                                                 else ", ".join(names[:-1]) + ", and " + names[-1])
    o_is_L = axisvals["O"][1] in ("[L]", "[V]")
    d_is_L = axisvals["D"][1] in ("[L]", "[V]")
    reg_clause = ""
    if L_ax:
        src_bits = []
        if o_is_L:
            src_bits.append("onset from the Orphanet AverageAgeOfOnset register / HPO")
        if d_is_L:
            src_bits.append("disability from the GBD 2013 disability-weights table")
        reg_clause = (f'The registry-grade {gi("[L]")} {"axes" if len(L_ax) > 1 else "axis"} here '
                      f'{"are" if len(L_ax) > 1 else "is"} {axlist(L_ax)}'
                      + (' (' + '; '.join(src_bits) + ')' if src_bits else '')
                      + '. ')
    if H_ax:
        reg_clause += (f'{axlist(H_ax)[:1].upper()}{axlist(H_ax)[1:]} '
                       f'remain{"" if len(H_ax) > 1 else "s"} an {gi("[H]")} inference from the cited '
                       f'clinical definition. ')
    body.append(f'<p>Of the five axes, {axes_scored} are scored (the rankability cut is &ge; 3 of 5); the '
                f'pre-treatment composite is the renormalised mean over the scored axes, raw_burden = {raw}. '
                f'{reg_clause}</p>')
    if r["order_locked"] == "yes":
        body.append(f'<p>All {len(scored_ax)} scored axes for this disease are registry-grade {gi("[L]")}/'
                    f'{gi("[V]")}: its burden <b>value is registry-locked</b> (order_locked) and no longer rests '
                    f'on definition-only inference. The cohort <i>order</i> overall is still a <b>provisional '
                    f'{gi("[H]")} prioritisation device, not a registry-locked ranking</b> &mdash; this '
                    f'disease&rsquo;s absolute rank depends on neighbours whose axes remain {gi("[H]")}.</p>')
    else:
        body.append(f'<p>Because {"those axes carry" if H_ax else "the scored axes include"} {gi("[H]")} '
                    f'inferences, this position is a <b>provisional {gi("[H]")} prioritisation device, not a '
                    f'registry-locked ranking</b>.</p>')
    body.append(f'<p class="note">The natural-history registry passes have been run against '
                f'<a href="https://www.orphadata.com/">Orphanet/Orphadata</a> (CC BY 4.0, R6) and the openly '
                f'published <a href="https://doi.org/10.1016/S2214-109X(15)00069-8">GBD 2013 disability-weights '
                f'table</a> (Salomon et al., CC BY, R7). R6 lifts onset to registry-grade {gi("[L]")} across most '
                f'of the cohort (earliest AverageAgeOfOnset category, entity-anchored per ORPHAcode, Exact '
                f'OMIM&harr;ORPHA only); R7 lifts disability to {gi("[L]")} where one dominant untreated sequela '
                f'maps to a named GBD health state (published disability weight binned by declared cut-points), '
                f'and independently corroborates a mortality axis from PMC survival literature where a quantitative '
                f'disease-typical figure exists. Severity now lifts to registry {gi("[L]")} for the one disease whose '
                f'dominant sequela carries a cited HPO Severity-modifier annotation (the HP:0012824 subtree, R8); for '
                f'the rest the open HPO severity annotations are feature-level (using one feature as the disease tier '
                f'would be a category error), so severity stays {gi("[H]")}/{gi("[O]")} with the obstacle named. '
                f'Progression lifts to registry {gi("[L]")} where a cited PMC open-access source states a disease-level '
                f'magnitude for the dominant untreated sequela and the frozen R3 tier function derives the tier from '
                f'that verbatim sentence (R9, curated dominant-sequela join, non-spectrum); for the rest progression '
                f'stays {gi("[H]")}/{gi("[O]")}. The OMIM clinical synopsis (the disease-level '
                f'alternative) is API-key-gated and the key is unobtainable for an individual researcher &mdash; that '
                f'path is removed, not guessed.</p>')
    if emergence_card:
        body.append(emergence_card)
        body.append(f'<p>{esc(a["emergence"])}</p>')

    body.append('<h2 id="treatment">Established treatment and residual burden</h2>')
    body.append(f'<p>The established disease-directed approach is <b>{esc(tr["modality"])}</b>. '
                f'Mechanistically: {esc(tr["mechanism"])} {gi(tr["grade"])}.</p>')
    body.append(f'<p>Its effect on natural history is classified <b>{esc(status)}</b>, mapping to an efficacy '
                f'offset e = {e} and a residual factor R_treat = {rtreat}. Applied to the pre-treatment proxy this '
                f'gives the residual burden score {bscore}, moving the disease from raw rank {rawrank} to residual '
                f'rank {rrank} (shift {shift}).</p>')
    # treatment evidence-tier honesty
    if tr["grade"] == "[L]":
        nbk = tr.get("nbk", ""); post = tr.get("accession_initial_posting", "")
        rev = tr.get("accession_last_revision", ""); cterms = tr.get("mgmt_corroboration_terms", "")
        body.append(f'<p class="note">Evidence tier: accession-dated to the GeneReviews '
                    f'<a href="https://www.ncbi.nlm.nih.gov/books/{esc(nbk)}/">{esc(nbk)}</a> Management '
                    f'section {gi("[L]")} (initial posting {esc(post)}; last revision {esc(rev)}; retrieved '
                    f'{BUILD_DATE}'
                    + (f'; corroborating term(s): &ldquo;{esc(cterms)}&rdquo;' if cterms else '')
                    + f'). The natural-history axis grades remain a mix of {gi("[L]")} (GeneReviews-corroborated) '
                    f'and {gi("[H]")} (definition-only), so the burden <i>order</i> is still provisional.</p>')
    elif tr["definition_corroborated"] == "yes":
        body.append(f'<p class="note">Evidence tier: in-package cited MedGen clinical_definition {gi("[H]")} '
                    f'(matched treatment phrase: &ldquo;{esc(tr["definition_phrase"])}&rdquo;). '
                    f'Accession-dated {gi("[L]")} verification (FDA label / GeneReviews Management / OMIM / Orphanet) is deferred.</p>')
    else:
        body.append(f'<p class="note">Evidence tier: established standard of care {gi("[H]")} '
                    f'(source class: {esc(tr["source_class"])}; no accession fabricated). '
                    f'Accession-dated {gi("[L]")} verification is deferred &mdash; {esc(tr["obstacle_for_L"])}.</p>')
    if status == "none":
        body.append(f'<p>An <b>evidence_status of none</b> (e = 0) is a positive {gi("[H]")} finding that no '
                    f'disease-directed therapy alters the course &mdash; distinct from an open {gi("[O]")} gap. '
                    f'No cure is implied (constitution C-D3).</p>')

    body_html = "\n".join(body)
    prev_lnk = (f"/disease/{slugify(placed[idx-1]['entity'], idx+1)}/", placed[idx-1]['entity']) if idx>0 else \
               ("/disease/01-classification-burden-treatment-framework/", "Framework")
    next_lnk = (f"/disease/{slugify(placed[idx+1]['entity'], idx+3)}/", placed[idx+1]['entity']) if idx+1<len(placed) else None
    page = page_skeleton(title, desc, url, blocks, body_html, prev_lnk, next_lnk)
    return page_slug, page, {
        "no": num_sec, "slug": page_slug, "title": ent, "cui": cui,
        "one_liner": f"{system} disease in {gene_str}; residual burden rank {rrank}/{RANK_TOTAL}",
        "grade": "[H]", "residual_rank": rrank, "burden_score": bscore,
    }

# ----------------------------------------------------------------------------- not-placed disease page
def build_disease_notplaced(num_sec, cui, prev_lnk, next_lnk):
    slug, d = dossiers[cui]
    sc = scores[cui]; tr = treats[cui]; r = residual.get(cui, {})
    ent = sc["entity"]
    page_slug = slugify(ent, num_sec)
    url = f"{SITE}/disease/{page_slug}/"
    idn = d["identity"]
    genes = idn.get("genes", [])
    gene_str = ", ".join(genes) if genes else "(gene not annotated at this aggregate concept)"
    system = idn.get("system_class", sc["system_class"])
    inh = d["inheritance"]; mech = d["molecular_mechanism"]
    a = A[cui]

    # data-bound values (read from CSV)
    raw = num(sc["raw_burden"]); e = num(tr["efficacy_offset_e"]); rtreat = num(tr["R_treat"])
    status = tr["evidence_status"]
    axisvals = {ax: (num(sc[ax+"_value"]), sc[ax+"_grade"]) for ax in ["O","P","S","M","D"]}
    axes_scored = int(sc["axes_scored"])
    scored_ax = [ax for ax in ["O","P","S","M","D"] if axisvals[ax][0] is not None]
    open_ax = [ax for ax in ["O","P","S","M","D"] if axisvals[ax][0] is None]
    axis_full = {"O":"onset","P":"progression","S":"severity","M":"mortality","D":"disability"}
    open_names = ", ".join(axis_full[ax] for ax in open_ax)

    title = f"{ent} \u2014 {VOL_SHORT} \u00a7{num_sec} | Jamming Physics"
    inh_sd = INH_SHORT.get(inh["value"], inh["value"])
    primary_gene = genes[0] if genes else "gene not annotated at this aggregate concept"
    gene_clause = f"gene {primary_gene}" if genes else primary_gene
    desc = (f"{ent}: a {system} genetic disease ({gene_clause}). Graded mechanism and treatment; "
            f"not placed in the burden order ({axes_scored}/5 axes scored) \u2014 each value graded.")
    if len(desc) > 160:
        desc = desc[:159].rsplit(" ", 1)[0]

    # answer-first (40-60 words), honest not-placed framing
    if cui == "C2751306":
        inh_ans = "variants in PKD2"
    elif not genes:
        inh_ans = "an enzyme deficiency (gene not annotated at this aggregate concept)"
    else:
        inh_ans = f"{inh_sd} variants in {gene_str}"
    mech_ans = MECH_ANS.get(cui, mech["value"])
    n_open = len(open_ax)
    answer = (f"{ent} is a {system} genetic disease caused by {inh_ans}. It is <b>not placed</b> in the "
              f"rankable burden order: only {axes_scored} of five axes are scored (cut: three of five), so the "
              f"remaining {n_open} stay open [O], not guessed. Mechanism, scored axes, and treatment follow below.")

    abstract = (f"{ent} is inherited as {inh_sd} and acts by {mech['value']} ({gi(mech['grade'])}). "
                f"Of the five burden axes, {axes_scored} are scored ({', '.join(scored_ax) or 'none'}) and "
                f"{len(open_ax)} are open [O] ({', '.join(open_ax)}); because fewer than three are scored the "
                f"disease is reported as \u201cnot placed \u2014 insufficient axis coverage\u201d (rank null), not "
                f"ranked on partial data.")

    # JSON-LD (same surface as placed pages)
    anatomy = []
    for o in d["clinical"].get("organ_systems", {}).get("value", [])[:6]:
        nm = o.get("system","").replace("Abnormality of the ","").replace("Abnormality of ","")
        if nm: anatomy.append({"@type":"AnatomicalSystem","name":nm})
    symptoms = []
    for s in d["clinical"].get("cardinal_symptoms", {}).get("value", [])[:5]:
        if s.get("name"): symptoms.append({"@type":"MedicalSignOrSymptom","name":s["name"]})
    codes = [{"@type":"MedicalCode","codeValue":cui,"codingSystem":"MedGen"}]
    for omim in idn.get("omim_codes", [])[:3]:
        codes.append({"@type":"MedicalCode","codeValue":str(omim),"codingSystem":"OMIM"})
    mc = {"@context":"https://schema.org","@type":"MedicalCondition","name":ent,
          "code":codes,"associatedAnatomy":anatomy,"signOrSymptom":symptoms,
          "possibleTreatment":{"@type":"MedicalTherapy","name":tr["modality"]},
          "epidemiology":"genetic / rare disease","url":url}
    if genes:
        mc["cause"]={"@type":"MedicalCause","name":f"pathogenic variants in {gene_str}"}
    sa = {"@context":"https://schema.org","@type":"ScholarlyArticle","headline":ent,
          "isPartOf":{"@type":"CreativeWorkSeries","name":VOL_SHORT},"position":num_sec,
          "author":{"@type":"Person","name":AUTHOR,"sameAs":ORCID},
          "datePublished":BUILD_DATE,"dateModified":BUILD_DATE,"isBasedOn":PARENT_REPO,
          "license":"https://creativecommons.org/licenses/by/4.0/",
          "about":{"@type":"MedicalCondition","name":ent},"url":url}
    blocks = [jsonld(sa), jsonld(mc), breadcrumb_ld(ent, url)]

    claim = (f'<aside class="claim-strip">'
             f'<span class="grade g-open">[O] not placed</span>'
             f'<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
             f'<a href="/disease/01-classification-burden-treatment-framework/#burden">Burden method &sect;1</a>'
             f'<a href="{PARENT_REPO}">Reproduce (pipeline)</a>'
             f'<span class="doi">DOI <a href="https://doi.org/10.5281/zenodo.20763842">10.5281/zenodo.20763842</a></span>'
             f'</aside>')

    xref = ""
    if a.get("xref"):
        feat, sib = a["xref"]
        xref = (f'<div class="xref">Scope boundary: {feat} is owned by the sibling '
                f'<a href="/{sib}/">neuro/mind whitepaper</a> and is cross-referenced here, not duplicated '
                f'(SCOPE.md primary-system rule).</div>')

    body = [f'<h1>{esc(ent)}</h1>',
            f'<p class="answer">{answer}</p>',
            f'<p class="abstract">{abstract}</p>',
            claim]

    body.append('<h2 id="mechanism">Gene, inheritance, and molecular mechanism</h2>')
    body.append(f'<p>{esc(ent)} is inherited as <b>{esc(inh["value"])}</b> {gi(inh["grade"])} and is '
                f'classified mechanistically as <b>{esc(mech["value"])}</b> {gi(mech["grade"])}. {esc(a["mech"])}</p>')
    body.append(f'<p class="note">Inheritance source: {esc(inh.get("source","(structured MedGen field)"))}. '
                f'Mechanism source: {esc(mech.get("source",""))}. These are observed, cited inputs; the '
                f'classification is the reproducible analysis layer (C-D1).</p>')

    body.append('<h2 id="clinical">In-scope clinical involvement</h2>')
    body.append(f'<p>{esc(a["clinical"])}</p>')
    orgs = d["clinical"].get("organ_systems", {})
    org_vals = orgs.get("value", [])[:6]
    if org_vals:
        rows = "".join(
            f'<tr><td>{esc(o.get("system","").replace("Abnormality of the ","").replace("Abnormality of ",""))}</td>'
            f'<td class="num">{esc(o.get("supporting_term_count",""))}</td></tr>' for o in org_vals)
        body.append('<table><thead><tr><th>Organ system (HPO rollup)</th><th>terms</th></tr></thead>'
                    f'<tbody>{rows}</tbody></table>')
        body.append(f'<p class="note">Organ systems {gi(orgs.get("grade","[L]"))} from {esc(orgs.get("source", HPOA_VER))}.</p>')
    if xref: body.append(xref)

    body.append('<h2 id="burden">Burden axes and why this disease is not placed</h2>')
    body.append(f'<aside class="vp-card" data-locked="burden-{esc(cui)}">'
                f'<b>Not placed in the rankable order</b> <span class="g">{gi("[O]")}</span> &mdash; '
                f'{axes_scored} of 5 burden axes are scored; the rankability cut is &ge; 3 of 5. A renormalised '
                f'mean over fewer than three axes is not a stable aggregate, so this disease is listed as '
                f'\u201cnot placed\u201d (rank null) rather than ranked on partial data. '
                f'<a href="/disease/01-classification-burden-treatment-framework/#burden">Rankability rule &sect;1</a>.'
                f'</aside>')
    axrows = ""
    axis_names = {"O":"Onset earliness","P":"Progression","S":"Symptom severity","M":"Mortality","D":"Disability"}
    for ax in ["O","P","S","M","D"]:
        v,g = axisvals[ax]
        axrows += (f'<tr><td>{axis_names[ax]} ({ax})</td>'
                   f'<td class="num">{v if v is not None else "&mdash;"}</td><td>{gi(g)}</td></tr>')
    body.append('<table><thead><tr><th>Burden axis</th><th>value</th><th>grade</th></tr></thead>'
                f'<tbody>{axrows}</tbody></table>')
    if raw is not None:
        body.append(f'<p>For transparency the partial composite over the {axes_scored} scored '
                    f'axis/axes is raw_burden = {raw}, but it is <b>not</b> used to rank the disease '
                    f'(below the &ge; 3-axis cut). The open axes ({esc(open_names)}) are graded {gi("[O]")} '
                    f'with a named obstacle, never imputed.</p>')
    else:
        body.append(f'<p>Too few axes are scored to form even a partial composite; the open axes '
                    f'({esc(open_names)}) are graded {gi("[O]")} with a named obstacle, never imputed.</p>')
    body.append(f'<p>The natural-history registry passes lift onset (Orphanet, R6) and disability (GBD 2013 '
                f'disability weights, R7) to registry {gi("[L]")} where an entity-anchored mapping exists, lift '
                f'severity (HPO Severity-modifier subtree, R8) where the dominant sequela is annotated, and lift '
                f'progression (curated PMC open-access literature with a frozen-R3-derived tier, R9) where a cited '
                f'disease-level magnitude for the dominant untreated sequela exists. '
                f'For some diseases the added disability axis was enough to cross the &ge; 3-axis cut and enter '
                f'the placed residual order; for this one it was not &mdash; and its dominant sequela carries no '
                f'open HPO severity annotation, so no registry severity tier is available (the open HPO severity '
                f'annotations elsewhere are feature-level; the OMIM clinical synopsis, the disease-level alternative, '
                f'is API-key-gated and the key is unobtainable for an individual researcher). '
                f'Scoring three or more axes at registry grade (via published functional &amp; survival literature) '
                f'would let this disease enter the rankable residual order; until '
                f'then it is reported here, never imputed.</p>')

    body.append('<h2 id="treatment">Established treatment</h2>')
    body.append(f'<p>The established disease-directed approach is <b>{esc(tr["modality"])}</b>. '
                f'Mechanistically: {esc(tr["mechanism"])} {gi(tr["grade"])}. Its effect on natural history is '
                f'classified <b>{esc(status)}</b> (efficacy offset e = {e}, residual factor R_treat = {rtreat}); '
                f'this offset would apply to the burden score once the disease is placed.</p>')
    if tr["grade"] == "[L]":
        nbk = tr.get("nbk",""); post = tr.get("accession_initial_posting",""); rev = tr.get("accession_last_revision","")
        cterms = tr.get("mgmt_corroboration_terms","")
        body.append(f'<p class="note">Evidence tier: accession-dated to the GeneReviews '
                    f'<a href="https://www.ncbi.nlm.nih.gov/books/{esc(nbk)}/">{esc(nbk)}</a> Management section '
                    f'{gi("[L]")} (initial posting {esc(post)}; last revision {esc(rev)}; retrieved {BUILD_DATE}'
                    + (f'; corroborating term(s): &ldquo;{esc(cterms)}&rdquo;' if cterms else '') + f').</p>')
    elif status == "none":
        body.append(f'<p>An <b>evidence_status of none</b> (e = 0) is a positive {gi("[H]")} finding that no '
                    f'disease-directed therapy alters the course &mdash; distinct from an open {gi("[O]")} gap. '
                    f'No cure is implied (constitution C-D3).</p>')
    else:
        body.append(f'<p class="note">Evidence tier: established standard of care {gi("[H]")} '
                    f'(source class: {esc(tr["source_class"])}; no accession fabricated).</p>')

    body_html = "\n".join(body)
    page = page_skeleton(title, desc, url, blocks, body_html, prev_lnk, next_lnk)
    return page_slug, page, {
        "no": num_sec, "slug": page_slug, "title": ent, "cui": cui,
        "one_liner": f"{system} disease in {gene_str}; not placed ({axes_scored}/5 axes scored)",
        "grade": "[O]", "residual_rank": None, "burden_score": None,
    }

# ----------------------------------------------------------------------------- cross-cutting class chapter
# A class chapter LINKS the individual disease pages that share one molecular mechanism; it does
# NOT absorb their content (each disease keeps its own canonical page). Membership is taken from
# the curated dossiers' gene/mechanism, so a class with no cohort members is simply not authored
# (the systemic cohort has no repeat-expansion disease -- those are neurological, owned by the
# sibling neuro volume -- so collagenopathy is the second class instead of repeat-expansion).
CLASSES = [
 {"key":"lysosomal",
  "name":"Lysosomal storage and transport disorders",
  "members":["C0268242","C0086795","C0017921","C1961835","C0017205","C0002986","C4316899"],
  "snippet":"a disabled lysosomal enzyme or transporter, so an undegraded substrate accumulates and poisons the cell",
  "lede":("These diseases each disable a single lysosomal protein, so an undegraded substrate "
          "accumulates inside the lysosome and progressively poisons the cell. The shared mechanism "
          "is why enzyme-replacement and substrate-reduction strategies recur across the class."),
  "mech":("The disabled protein is either a degradative enzyme \u2014 acid sphingomyelinase "
          "(Niemann-Pick A), \u03b1-L-iduronidase (Hurler), acid \u03b1-glucosidase (Pompe), acid "
          "\u03b2-glucosidase (Gaucher), \u03b1-galactosidase A (Fabry) \u2014 or a lysosomal membrane "
          "transporter, cystinosin (cystinosis). In every case the lysosome is the point of failure, "
          "which is why the class shares treatment logic (enzyme replacement, substrate reduction) and "
          "a common progressive multi-organ storage phenotype.")},
 {"key":"collagenopathy",
  "name":"Fibrillar collagenopathies",
  "members":["C0029434","C0220685","C0268338","C0268335"],
  "snippet":"a defective fibrillar collagen of the extracellular matrix, acting by dominant-negative or haploinsufficiency",
  "lede":("These diseases each corrupt a fibrillar collagen of the extracellular matrix, so a "
          "structural-matrix protein is defective. They share dominant-negative and haploinsufficiency "
          "mechanisms and, for three of the four, the same morphogenetic patterning baseline."),
  "mech":("The affected collagen is type I in osteogenesis imperfecta (bone matrix), type II in "
          "achondrogenesis type II (cartilage), type III in vascular Ehlers-Danlos syndrome (vessel and "
          "hollow-organ walls), and type V in classic Ehlers-Danlos syndrome (regulation of dermal type I "
          "fibrillogenesis). The shared lesion is a structural-matrix protein defect acting through a "
          "dominant-negative poisoned triple helix or through haploinsufficiency; three of the four are read "
          "by the carried morphogenesis engine as perturbations of the same connective-tissue patterning "
          "baseline (the length band \u03bb = \u221a(D\u00b7\u03c4)).")},
]

def build_class_chapter(num_sec, cdef, page_index):
    name = cdef["name"]
    page_slug = slugify(name, num_sec)
    url = f"{SITE}/disease/{page_slug}/"
    members = [m for m in cdef["members"] if m in page_index]
    title = f"{name} (mechanism class) \u2014 {VOL_SHORT} \u00a7{num_sec} | Jamming Physics"
    desc = (f"{name}: the cohort diseases that share this molecular mechanism, each linked to its own "
            f"page \u2014 a cross-cutting reference, not a re-description.")
    if len(desc) > 160:
        desc = desc[:159].rsplit(" ", 1)[0]
    answer = (f"{name} is a mechanism class of {len(members)} diseases in this volume that share "
              f"{esc(cdef['snippet'])}. This chapter links each member to its own canonical page rather than "
              f"restating it; the graded burden values live on those pages and in the framework.")

    items = [{"@type":"ListItem","position":i+1,
              "url":f"{SITE}/disease/{page_index[m]['slug']}/","name":page_index[m]["title"]}
             for i,m in enumerate(members)]
    sa = {"@context":"https://schema.org","@type":"ScholarlyArticle","headline":name,
          "isPartOf":{"@type":"CreativeWorkSeries","name":VOL_SHORT},"position":num_sec,
          "author":{"@type":"Person","name":AUTHOR,"sameAs":ORCID},
          "datePublished":BUILD_DATE,"dateModified":BUILD_DATE,"isBasedOn":PARENT_REPO,
          "license":"https://creativecommons.org/licenses/by/4.0/","url":url}
    il = {"@context":"https://schema.org","@type":"ItemList","name":name,"numberOfItems":len(members),
          "itemListElement":items}
    blocks = [jsonld(sa), jsonld(il), breadcrumb_ld(name, url)]

    claim = (f'<aside class="claim-strip">'
             f'<span class="grade g-feature">[F] mechanism class</span>'
             f'<span class="gate">links member pages</span>'
             f'<a href="/disease/01-classification-burden-treatment-framework/#mechanism">Mechanism axis &sect;1</a>'
             f'<span class="doi">DOI <a href="https://doi.org/10.5281/zenodo.20763842">10.5281/zenodo.20763842</a></span>'
             f'</aside>')

    body = [f'<h1>{esc(name)}</h1>',
            f'<p class="answer">{answer}</p>',
            claim,
            '<h2 id="mechanism">The shared mechanism</h2>',
            f'<p>{esc(cdef["mech"])}</p>',
            '<h2 id="members">Member diseases (each on its own page)</h2>',
            '<ul class="sectlist">']
    for m in members:
        pi = page_index[m]
        if pi["placed"]:
            badge = f'<span class="rank-badge">#{pi["residual_rank"]}</span>'
            note = f'residual burden rank {pi["residual_rank"]}/{RANK_TOTAL}'
        else:
            badge = '<span class="rank-badge">&mdash;</span>'
            note = 'not placed (insufficient axis coverage)'
        body.append(f'<li>{badge}<a href="/disease/{pi["slug"]}/">{esc(pi["title"])}</a>'
                    f'<span class="meta">{esc(pi["system"])} &middot; {esc(", ".join(pi["genes"]) or "aggregate concept")} &middot; {note}</span></li>')
    body.append('</ul>')
    body.append(f'<p class="note">This chapter is a cross-reference: the burden order and all graded values live '
                f'on the individual disease pages and in the framework (&sect;1). Membership is read from the curated '
                f'dossiers\u2019 gene and mechanism fields, so the class list is reproducible, not hand-picked.</p>')
    body_html = "\n".join(body)
    page = page_skeleton(title, desc, url, blocks, body_html,
                         ("/disease/", "Volume contents"), None)
    return page_slug, page, {
        "no": num_sec, "slug": page_slug, "title": name, "cui": None,
        "one_liner": f"mechanism class linking {len(members)} member disease pages",
        "grade": "[F]", "residual_rank": None, "burden_score": None,
    }

# ----------------------------------------------------------------------------- framework chapter
def build_framework(meta_chapters):
    url = f"{SITE}/disease/01-classification-burden-treatment-framework/"
    title = f"Classification, burden, and treatment framework \u2014 {VOL_SHORT} \u00a71 | Jamming Physics"
    desc = ("How this volume classifies systemic genetic diseases, scores a reproducible burden order, "
            "and grades evidence: observed inputs vs the analysis layer.")
    answer = ("This volume orders systemic genetic and rare diseases by a deterministic burden proxy built "
              "from five graded axes -- onset, progression, severity, mortality, disability -- then offset by "
              "the established therapy's efficacy. Clinical facts are observed, cited inputs; the classification "
              "and the burden order are the reproducible contribution. The order is a provisional prioritisation "
              "device, not a registry-locked ranking.")
    abstract = ("Each disease is placed on three orthogonal axes (inheritance, molecular mechanism, organ system) "
                "and scored on a fixed a-priori burden scale whose composite is burden_score = raw_burden \u00b7 (1 \u2212 e). "
                "Every value carries a grade: [V] law, [L] registry/measured, [H] cited-text inference, [O] open with a named obstacle.")
    sa = {"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"Classification, burden, and treatment framework",
          "isPartOf":{"@type":"CreativeWorkSeries","name":VOL_SHORT},"position":1,
          "author":{"@type":"Person","name":AUTHOR,"sameAs":ORCID},
          "datePublished":BUILD_DATE,"dateModified":BUILD_DATE,"isBasedOn":PARENT_REPO,
          "license":"https://creativecommons.org/licenses/by/4.0/","url":url}
    blocks=[jsonld(sa), breadcrumb_ld("Classification, burden, and treatment framework", url)]
    claim = (f'<aside class="claim-strip">'
             f'<span class="grade g-hypothesis">[H] provisional order</span>'
             f'<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
             f'<a href="{PARENT_REPO}">Reproduce (pipeline)</a>'
             f'<span class="doi">DOI <a href="https://doi.org/10.5281/zenodo.20763842">10.5281/zenodo.20763842</a></span></aside>')
    b=[f'<h1>Classification, burden, and treatment framework</h1>',
       f'<p class="answer">{answer}</p>',
       f'<p class="abstract">{abstract}</p>', claim]

    b.append('<h2 id="observed">Observed inputs vs the reproducible layer</h2>')
    b.append('<p>Clinical and epidemiologic facts here are <b>observed inputs</b> from NCBI (MedGen, OMIM, Gene, '
             'ClinVar) and HPO: respected and cited, never asserted as &ldquo;reproduced&rdquo;. The volume\u2019s '
             'reproducible contribution is the <b>analysis layer</b> &mdash; the inheritance / mechanism '
             'classification, the deterministic burden index, the residual-treatment offset, and the normal-development '
             'engine annotation.</p>')
    b.append(f'<p>Reproducibility is bit-for-bit: the burden order is regenerated by an in-package pipeline '
             f'(<code>r3_burden_index.py</code> &rarr; <code>r4_burden_residual.py</code>) and a gate re-runs the '
             f'builders and asserts an identical digest (2&times; sha256). Every number on every disease page is read '
             f'from that pipeline\u2019s output, not typed into prose.</p>')

    b.append('<h2 id="axes">Three classification axes</h2>')
    b.append('<p>Each entity is placed on three orthogonal axes so that &ldquo;how it is inherited&rdquo; is never '
             'confused with &ldquo;what the variant does to the protein&rdquo;.</p>')
    b.append('<table><thead><tr><th>Axis</th><th>values</th></tr></thead><tbody>'
             '<tr><td>Inheritance</td><td>autosomal dominant / recessive; X-linked dominant / recessive; '
             'mitochondrial; imprinting; chromosomal; CNV; mosaic</td></tr>'
             '<tr><td>Molecular mechanism</td><td>loss-of-function; haploinsufficiency; gain-of-function; '
             'dominant-negative; dosage; repeat-expansion; imprinting; splicing; trafficking/folding</td></tr>'
             '<tr><td>Organ system (in scope)</td><td>metabolic; lysosomal/peroxisomal; connective-tissue/skeletal; '
             'hematologic; immunologic; renal; hepatic; GI; pulmonary/exocrine; endocrine/growth; dermatologic</td></tr>'
             '</tbody></table>')
    b.append('<p>The sibling neuro/mind whitepapers own the brain, nerve, heart, and affect. A multi-system disease '
             'is classified by its primary in-scope system; its excluded-organ features are named and cross-referenced, '
             'not re-described (SCOPE.md).</p>')

    b.append('<h2 id="burden">The deterministic burden index</h2>')
    b.append('<p>Subjective suffering is individual and not directly measurable, so this volume does not rank suffering. '
             'It defines a transparent <b>burden proxy</b> from observable, published clinical attributes &mdash; a '
             'prioritisation device for coverage and triage, explicitly not a value judgement about any patient.</p>')
    b.append('<p>Five axes are each binned to [0,1] by fixed a-priori clinical meaning (tier values are not chosen to '
             'produce any ordering):</p>')
    b.append('<table><thead><tr><th>Axis</th><th>bins &rarr; value</th></tr></thead><tbody>'
             '<tr><td>O onset earliness</td><td>congenital 1.0 &middot; infantile 0.85 &middot; childhood 0.7 &middot; '
             'juvenile 0.55 &middot; adult 0.35 &middot; late-adult 0.2</td></tr>'
             '<tr><td>P progression</td><td>static 0.2 &middot; slow 0.5 &middot; rapid 0.8 &middot; lethal 1.0 &middot; '
             'variable 0.5</td></tr>'
             '<tr><td>S severity</td><td>mild 0.25 &middot; moderate 0.5 &middot; severe 0.75 &middot; profound 1.0 &middot; '
             'variable 0.5</td></tr>'
             '<tr><td>M mortality</td><td>normal 0.0 &middot; near-normal+risk 0.4 &middot; premature 0.7 &middot; '
             'early-lethal 1.0</td></tr>'
             '<tr><td>D disability</td><td>independent 0.2 &middot; partial 0.5 &middot; high support 0.75 &middot; '
             'fully dependent 1.0</td></tr></tbody></table>')
    b.append('<p>The composite is a renormalised mean over the axes actually scored (a missing axis is excluded, never '
             'imputed): raw_burden = mean(scored axes), and burden_score = raw_burden \u00b7 R_treat. Equal weights of '
             '0.20 are declared and recorded.</p>')
    b.append(f'<p><b>Honest limitation, front and centre.</b> <b>Onset</b> is registry-grade {gi("[L]")} for '
             f'most of the cohort, taken from the <a href="https://www.orphadata.com/">Orphanet</a> '
             f'AverageAgeOfOnset register (earliest typical category, entity-anchored per ORPHAcode, Exact '
             f'OMIM&harr;ORPHA only) cross-checked with HPO (R6). <b>Disability</b> is now registry-grade '
             f'{gi("[L]")} for the diseases whose one dominant untreated sequela maps to a named '
             f'<a href="https://doi.org/10.1016/S2214-109X(15)00069-8">GBD 2013</a> health state, the published '
             f'disability weight binned by declared cut-points (R7); two mortality axes are independently '
             f'corroborated from PMC survival literature. <b>Severity</b> now lifts to registry {gi("[L]")} for the '
             f'one disease whose dominant sequela carries a cited annotation in the HPO clinical-modifier Severity '
             f'subtree (HP:0012824, R8); for the rest of the cohort the open HPO severity annotations are '
             f'feature-level (a category error if read as a disease tier) and the OMIM clinical synopsis is '
             f'API-key-gated with the key unobtainable for an individual researcher, so severity stays largely '
             f'{gi("[H]")}/{gi("[O]")}. <b>Progression</b> lifts to registry {gi("[L]")} where a cited PMC '
             f'open-access source states a disease-level magnitude for the dominant untreated sequela and the '
             f'<i>frozen R3 tier function</i> derives the tier from that verbatim sentence (R9, non-spectrum, '
             f'non-comparative dominant-sequela join); for the rest progression stays {gi("[H]")} inferences from '
             f'the cited definition. '
             f'The whole order is therefore a <b>provisional {gi("[H]")} prioritisation device, not a '
             f'registry-locked ranking</b>. {_locked_n_names()[0]} diseases ({_locked_n_names()[1]}) now have '
             f'every one of their scored axes at registry {gi("[L]")} (order_locked, {_locked_n_names()[0]} of 35): '
             f'their burden '
             f'<i>value</i> is registry-grade, though the cohort order overall stays provisional until severity and '
             f'progression lift further via published functional &amp; survival literature &mdash; not guessed.</p>')
    b.append('<h3>Rankability</h3>')
    b.append(f'<p>A mean over fewer than a majority of the five axes is not a meaningful aggregate, so one fixed declared '
             f'cut applies: <code>rankable = (axes_scored &ge; 3)</code>. Of the cohort, {RANK_TOTAL} diseases are placed in '
             f'the contiguous order on this page; the rest are reported as &ldquo;not placed &mdash; insufficient axis '
             f'coverage&rdquo;. This is a declared coverage cut, not a tuned parameter.</p>')

    b.append('<h2 id="treatment">Treatment evidence and the residual offset</h2>')
    b.append('<p>The clinically relevant quantity is <i>residual</i> burden &mdash; what remains after the best '
             'established therapy. Each disease\u2019s established disease-directed therapy is surveyed, its mechanism stated '
             'only where mechanistically established (C-D3), and an evidence status mapped to a fixed efficacy offset e.</p>')
    b.append('<table><thead><tr><th>evidence status</th><th>offset e</th><th>R_treat = 1 &minus; e</th></tr></thead><tbody>'
             '<tr><td>curative</td><td class="num">0.85</td><td class="num">0.15</td></tr>'
             '<tr><td>disease-modifying (substantial)</td><td class="num">0.55</td><td class="num">0.45</td></tr>'
             '<tr><td>disease-modifying (partial)</td><td class="num">0.30</td><td class="num">0.70</td></tr>'
             '<tr><td>symptomatic</td><td class="num">0.10</td><td class="num">0.90</td></tr>'
             '<tr><td>none</td><td class="num">0.00</td><td class="num">1.00</td></tr></tbody></table>')
    b.append(f'<p>Under the grading rule the treatment modality itself is never assigned a fabricated cure: its '
             f'mechanism is stated only where mechanistically established (C-D3). The natural-history <i>effect</i> '
             f'of each established therapy has been accession-dated to the GeneReviews Management section '
             f'{gi("[L]")} for 33 of 35 diseases (the R5 pass; initial-posting and last-revision dates recorded '
             f'per page); the two without a current GeneReviews chapter stay {gi("[H]")}. Cross-dating the same '
             f'effect against the FDA label / OMIM clinical management is the deferred extension. The residual '
             f'<i>order</i> remains provisional because the burden <i>axes</i> &mdash; not the treatments &mdash; '
             f'are still a mix of {gi("[L]")} and {gi("[H]")}.</p>')

    b.append('<h2 id="emergence">The carried normal-development engine</h2>')
    b.append('<p>Many developmental diseases are perturbations of a morphogenetic programme. This volume carries, '
             'read-only, a DB-grounded morphogenesis engine that forward-simulates normal development from measured, '
             'cited biophysics and grades every quantity honestly.</p>')
    b.append(f'<aside class="vp-card" data-locked="emergence-engine"><b>NON-FIT baseline</b> '
             f'<span class="g">{gi("[L]")}</span> &mdash; the engine never reads disease data; developmental diseases are '
             f'<i>annotated</i> against it (which quantity they shift: the length band &lambda; = &radic;(D&middot;&tau;), '
             f'Layer-2 dosage &phi;, or the spinodal switch). Pin verified drift 0.</aside>')

    b.append('<h2 id="grades">Grade legend</h2>')
    b.append('<table><thead><tr><th>grade</th><th>meaning</th></tr></thead><tbody>'
             f'<tr><td>{gi("[V]")}</td><td>derived from a law / proof, or a quantitative published distribution</td></tr>'
             f'<tr><td>{gi("[L]")}</td><td>registry-stated and cited (an observed input, e.g. an HPO annotation)</td></tr>'
             f'<tr><td>{gi("[H]")}</td><td>inference from cited text / established science; the basis is recorded</td></tr>'
             f'<tr><td>{gi("[O]")}</td><td>open / unavailable; the obstacle is named; never guessed</td></tr>'
             f'<tr><td>{gi("[F]")}</td><td>forced by a structural/geometric rule (used in sibling physics volumes)</td></tr>'
             '</tbody></table>')

    # ordered ledger of the placed cohort -> links to each disease page (internal linking, crawl)
    b.append('<h2 id="order">The rankable burden order</h2>')
    b.append('<p>The placed cohort, by residual burden (each disease is its own page):</p>')
    rows=""
    for i,r in enumerate(placed):
        ps = slugify(r["entity"], i+2)
        rows += (f'<tr><td class="num">{r["residual_rank"]}</td>'
                 f'<td><a href="/disease/{ps}/">{esc(r["entity"])}</a></td>'
                 f'<td>{esc(r["system_class"])}</td>'
                 f'<td class="num">{num(r["burden_score"])}</td>'
                 f'<td>{esc(r["evidence_status"])}</td></tr>')
    b.append('<table class="ledger"><thead><tr><th>rank</th><th>disease</th><th>system</th>'
             '<th>residual</th><th>treatment status</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    b.append(f'<p class="note">All {RANK_TOTAL} residual figures are {gi("[H]")} provisional. Diseases with 1&ndash;2 '
             f'scored axes are not placed and are authored separately in later sections.</p>')

    # ---- forward plan + completion criteria (carried in the whitepaper until completion) ----
    _nL = lambda ax: sum(1 for c in scores if scores[c].get(ax + "_grade") == "[L]")
    _ntx_L = sum(1 for c in scores if treats[c]["grade"] == "[L]")
    _nlk, _lknames = _locked_n_names()
    _nshl = sum(1 for r in placed if any(scores[r["cui"]][ax + "_grade"] == "[H]"
                                         for ax in ["O", "P", "S", "M", "D"]))
    b.append('<h2 id="forward">Forward plan and completion criteria</h2>')
    b.append('<p>This volume is built in <b>versioned, gated passes</b>, and the forward plan is carried '
             '<b>inside the whitepaper itself</b> — in every version — until an explicit completion '
             'declaration replaces it. Each pass either lifts a burden axis to registry grade through a '
             'cited, gate-enforced rule, or records, per disease, the precise obstacle that prevents it. '
             'No value is ever guessed to advance the plan.</p>')
    b.append(f'<p><b>Landed so far.</b> Treatments accession-dated {gi("[L]")} ({_ntx_L} of {len(scores)}); '
             f'onset {gi("[L]")} ({_nL("O")} of {len(scores)}, Orphanet, R6); disability {gi("[L]")} '
             f'({_nL("D")} of {len(scores)}, GBD 2013, R7); mortality {gi("[L]")} ({_nL("M")} of {len(scores)}, '
             f'PMC survival literature, R7); severity {gi("[L]")} ({_nL("S")} of {len(scores)}, HPO Severity '
             f'subtree HP:0012824 R8 + curated PMC open-access R11+R12+R14, frozen-R3-derived tier); progression {gi("[L]")} ({_nL("P")} of {len(scores)}, curated PMC '
             f'open-access literature with a frozen-R3-derived tier, R9+R10+R13+R14). <b>order_locked {_nlk} of '
             f'{len(scores)}</b> ({esc(_lknames)}). A read-only unmet-need / treatment-gap surface '
             f'(residual&nbsp;=&nbsp;raw_burden&nbsp;&middot;&nbsp;(1&minus;e)) re-presents the same registry '
             f'as a graded research-prioritisation signal.</p>')
    b.append(f'<p><b>Next task (R16).</b> R9&ndash;R15 took the curated-PMC-OA frontier through the '
             f'clearly defensible disease-level joins reached so far: R9&rsquo;s progression lifts (NPD-A '
             f'locking), R10&rsquo;s two grade-only progression corroborations (Fabry and Marfan, '
             f'{gi("[H]")}&rarr;{gi("[L]")} value unchanged, neither locking), R11&rsquo;s single '
             f'<b>severity</b> lift (Marfan syndrome {gi("[H]")}&rarr;{gi("[L]")}, completing the 4th '
             f'order-lock), and R12&rsquo;s two <b>severity</b> lifts &mdash; Duchenne muscular dystrophy '
             f'severity {gi("[H]")}&rarr;{gi("[L]")} (0.50&rarr;0.75, tier <b>derived</b> by the frozen R3 '
             f'function via &lsquo;severe&rsquo; from the disease-defining sentence) which, because '
             f'Duchenne&rsquo;s onset, progression, mortality and disability were already {gi("[L]")}, '
             f'<b>completes its order-lock</b> (the 5th), plus Tyrosinemia&nbsp;type&nbsp;I severity '
             f'{gi("[H]")}&rarr;{gi("[L]")} (value 0.75 unchanged, a grade-only lift that does not lock, '
             f'two {gi("[H]")} axes remaining). R12 also recorded two declines, each a cited open-access '
             f'sentence found and verbatim-pinned but not a clean disease-level magnitude: Hurler syndrome '
             f'severity (<b>comparative</b> &mdash; &lsquo;the severe phenotype&rsquo; of MPS&nbsp;I in '
             f'contrast to the attenuated forms) and the beta-thalassemia umbrella severity '
             f'(<b>umbrella spectrum</b> &mdash; silent/minor&nbsp;&rarr;&nbsp;intermedia&nbsp;&rarr;&nbsp;major, '
             f'tripping the R3 spectrum override). A frontier observation is recorded for hemophilia&nbsp;A: '
             f'its only retrievable open-access &lsquo;severe&rsquo; framing is &lsquo;severe hemophilia&nbsp;A '
             f'(FVIII&lt;1%)&rsquo;, a factor-activity <b>sub-phenotype</b> of an entity spanning '
             f'mild/moderate/severe, so no disease-level severity tier is isolable and severity is left '
             f'{gi("[H]")}, not forced. R13 then added three lifts &mdash; Maple syrup urine disease '
             f'severity {gi("[H]")}&rarr;{gi("[L]")} (via &lsquo;life-threatening&rsquo;) plus Cystic '
             f'fibrosis and Pompe progression grade-only &mdash; and R14 added three more &mdash; Classic '
             f'homocystinuria and Fabry disease severity 0.50&rarr;0.75 (via &lsquo;life-threatening&rsquo; / '
             f'&lsquo;severe&rsquo;) plus Becker muscular dystrophy progression grade-only (via '
             f'&lsquo;progressive&rsquo;, advancing the R13 BMD frontier on a different axis from a clean '
             f'BMD-specific sentence) &mdash; <b>none completing a new order-lock</b> (each lifted disease '
             f'retains another {gi("[H]")} axis, so the lock set stayed 5). R14 also declined Polycystic '
             f'kidney disease 2 severity (<b>comparative</b>, PKD1-vs-PKD2) and Osteogenesis imperfecta '
             f'progression (<b>spectrum</b>, moderate-to-mild across a 17-patient cohort). '
             f'R15 then added three <b>severity</b> lifts &mdash; Acute intermittent porphyria '
             f'{gi("[H]")}&rarr;{gi("[L]")} (0.50&rarr;0.75, via &lsquo;severe&rsquo; from the disease-defining '
             f'neurovisceral-attack sentence; stays sub-rankable at 2 scored axes, so no lock), Achondroplasia '
             f'{gi("[O]")}&rarr;{gi("[L]")} (0.75, via &lsquo;severe disproportionate short stature&rsquo;; '
             f'becomes rankable but retains mortality {gi("[H]")}, so no lock), and Phenylketonuria '
             f'{gi("[O]")}&rarr;{gi("[L]")} (0.75, via &lsquo;severe intellectual disability and irreversible '
             f'brain damage&rsquo; in the untreated-classical-PKU sentence) which, because PKU&rsquo;s onset and '
             f'disability were already {gi("[L]")}, <b>completes the 6th order-lock</b>. That lock is '
             f'<b>disclosed as an honest consequence</b>, not lock-fishing: PKU&rsquo;s severity and '
             f'disability axes are orthogonal by construction (disease-severity magnitude vs the GBD '
             f'functional-dependence weight), the sources differ, and the cited sentence passes every '
             f'inclusion criterion independently &mdash; so the lock set moves 5&rarr;6 with the delta '
             f'<b>exactly +Phenylketonuria</b> (the gate asserts this). R15 also declined '
             f'21-hydroxylase-deficient congenital adrenal hyperplasia severity (<b>form-specific</b> &mdash; '
             f'&lsquo;life-threatening salt-wasting&rsquo; attaches to the severest classic form, not the '
             f'entity that also spans the mild non-classic form) and Hemochromatosis&nbsp;type&nbsp;1 severity '
             f'(<b>comparative</b> &mdash; &lsquo;severe clinical outcomes&rsquo; framed only as a '
             f'high-vs-low-TSAT between-stratum contrast). With <b>{_nshl} placed diseases still carrying an {gi("[H]")} '
             f'axis</b> &mdash; overwhelmingly severity &mdash; R16 continues the <b>same</b> rule on the '
             f'placed cohort&rsquo;s remaining {gi("[H]")}/{gi("[O]")} <b>severity</b> and <b>progression</b> '
             f'axes (and any further <b>mortality</b> axis): a disease-level magnitude for the dominant '
             f'untreated sequela, with the tier <b>derived by the frozen R3 tier function</b> over the '
             f'verbatim cited sentence &mdash; non-spectrum, non-comparative, non-treated-cohort, '
             f'non-sub-phenotype. '
             f'The cut-points are <b>never widened</b>; every lift is gated and every decline is recorded '
             f'with its reason; the pass ships as a <b>new cumulative stage</b> that leaves all prior '
             f'artifacts byte-identical. Mortality lifts only where a quantitative disease-typical survival '
             f'figure exists (free text does not fill an open mortality axis). The OMIM clinical-synopsis '
             f'path stays <b>removed</b> (its key is unobtainable for an individual researcher), not '
             f'deferred.</p>')
    b.append(f'<p><b>Completion declaration (the criterion).</b> This volume will be declared '
             f'<b>complete</b> when, for <b>every placed disease</b>, either <b>(a)</b> all scored axes are '
             f'registry grade {gi("[L]")}/{gi("[V]")} (the disease is <code>order_locked</code> and its burden '
             f'<i>value</i> is registry-locked), or <b>(b)</b> every remaining open axis carries a '
             f'<b>permanent, named obstacle that is irreducible from open data</b> (e.g. a magnitude that '
             f'exists only behind an unobtainable licensed source). At that point the burden order is either '
             f'<b>fully registry-locked</b> or <b>provably as locked as open data allows</b>, the residual '
             f'{gi("[H]")} openness is itemised in <code>IRREPRODUCIBILITY_LEDGER.md</code> with each '
             f'obstacle, and a dated completion declaration replaces this forward plan. Until then, this '
             f'section is part of the whitepaper in every version.</p>')

    body_html="\n".join(b)
    next_lnk=(f"/disease/{slugify(placed[0]['entity'],2)}/", placed[0]['entity'])
    page=page_skeleton(title,desc,url,blocks,body_html,
                       ("/disease/","Volume contents"), next_lnk)
    meta_chapters.insert(0, {"no":1,"slug":"01-classification-burden-treatment-framework",
        "title":"Classification, burden, and treatment framework","cui":None,
        "one_liner":"three axes + deterministic burden index + residual offset + grade legend",
        "grade":"[H]"})
    return "01-classification-burden-treatment-framework", page

# ----------------------------------------------------------------------------- hub
def build_hub(meta_chapters):
    url=f"{SITE}/disease/"
    title=f"{VOL_TITLE} \u2014 {VOL_SHORT} | Jamming Physics"
    desc=("Systemic genetic and rare diseases, one page each: a graded molecular mechanism, a reproducible "
          "burden order, and established treatment for every disease.")
    lede=("This volume covers systemic-body genetic and rare diseases &mdash; one standalone page per disease &mdash; "
          "giving each a graded molecular mechanism, a reproducible burden position, and its established treatment. "
          "It is the jamming branch of the Jamming Physics programme.")
    series_ld={"@context":"https://schema.org","@type":"CreativeWorkSeries","name":VOL_SHORT,
        "alternateName":VOL_TITLE,"author":{"@type":"Person","name":AUTHOR,"sameAs":ORCID},
        "url":url,"inLanguage":"en","license":"https://creativecommons.org/licenses/by/4.0/",
        "isPartOf":{"@type":"CreativeWork","name":"Jamming Physics","url":SITE+"/"},
        "hasPart":[{"@type":"ScholarlyArticle","name":c["title"],
                    "url":f"{SITE}/disease/{c['slug']}/","position":c["no"]} for c in meta_chapters]}
    bc=jsonld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":VOL_SHORT,"item":url}]})
    blocks=[jsonld(series_ld),bc]
    b=[f'<h1>{esc(VOL_TITLE)}</h1>',
       f'<div class="hub-lede">{lede}</div>',
       '<p>This is the jamming branch of the programme &rarr; <a href="/physics/">VP Theory (foundation)</a>. '
       'The brain, nervous system, heart, and affect are owned by the sibling '
       '<a href="/neuro/">neuro</a> and <a href="/mind/">mind</a> whitepapers and are cross-referenced, not duplicated.</p>']
    b.append(f'<p><b>Reading order.</b> The framework (&sect;1) defines the classification, the deterministic burden '
             f'index, and the grade legend. Each placed disease then has its own page (&sect;2 onward), ordered by '
             f'residual burden; the not-placed diseases and the mechanism-class cross-references follow, each disease '
             f'still on its own page. The burden order is a provisional {gi("[H]")} prioritisation device, not a '
             f'registry-locked ranking &mdash; treatments are accession-dated {gi("[L]")} (33 of 35), onset is '
             f'lifted to registry {gi("[L]")} (Orphanet, 28 of 35) and disability to registry {gi("[L]")} (GBD 2013 '
             f'disability weights, 13 of 35; order_locked {_locked_n_names()[0]} of 35); severity lifts to registry '
             f'{gi("[L]")} where a dominant sequela carries a cited HPO Severity-modifier annotation (R8), and '
             f'progression lifts to registry {gi("[L]")} where cited PMC open-access literature gives a disease-level '
             f'magnitude with a frozen-R3-derived tier (R9), with the rest of severity/progression the remaining '
             f'lift.</p>')
    b.append('<h2>Sections</h2><ul class="sectlist">')
    for c in meta_chapters:
        kind=c.get("kind","placed")
        if kind=="framework":      rb='<span class="rank-badge">&sect;1</span>'
        elif kind=="placed":       rb=f'<span class="rank-badge">#{c.get("residual_rank","")}</span>'
        elif kind=="notplaced":    rb='<span class="rank-badge np">np</span>'
        else:                      rb='<span class="rank-badge cls">[F]</span>'
        b.append(f'<li>{rb}<a href="/disease/{c["slug"]}/">{esc(c["title"])}</a>'
                 f'<span class="meta">{esc(c["one_liner"])} &middot; grade {esc(c["grade"])}</span></li>')
    b.append('</ul>')
    n_np=sum(1 for c in meta_chapters if c.get("kind")=="notplaced")
    n_cls=sum(1 for c in meta_chapters if c.get("kind")=="class")
    b.append(f'<p class="note">{RANK_TOTAL} diseases are placed in the rankable order (&ge; 3 of 5 burden axes scored); '
             f'{n_np} further diseases are listed as <b>not placed</b> (fewer than three axes scored, rank null, open axes '
             f'graded {gi("[O]")} not guessed), each still on its own page. {n_cls} cross-cutting mechanism chapters '
             f'(lysosomal storage; fibrillar collagenopathies) link their member disease pages without restating them. '
             f'The systemic cohort has no repeat-expansion disease &mdash; those are neurological, owned by the sibling '
             f'<a href="/neuro/">neuro</a> volume.</p>')
    body_html="\n".join(b)
    page=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="/assets/css/site.css">
<meta name="author" content="{esc(AUTHOR)}">
<meta name="robots" content="index,follow,max-snippet:-1">
{''.join(blocks)}
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; {esc(VOL_SHORT)}</nav></header>
<main>
{body_html}
</main>
<footer>
<p>{esc(VOL_TITLE)} &middot; author <a href="{ORCID}">{esc(AUTHOR)}</a> &middot; jamming branch of <a href="/">Jamming Physics</a>.</p>
<p>Research whitepaper, not clinical guidance. Licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
   Volume DOI: <a href="https://doi.org/10.5281/zenodo.20763842">10.5281/zenodo.20763842</a>.</p>
</footer>
</body>
</html>
"""
    return page

# ----------------------------------------------------------------------------- emit everything
def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8") as f: f.write(text)

def main():
    os.makedirs(VOLDIR, exist_ok=True)
    # Reproducible output: remove stale per-disease/class page directories from any prior
    # build (rank prefixes change when the burden order changes, e.g. after the R6 registry
    # pass, so old <rank>-<slug>/ dirs would otherwise linger as orphans). Files in VOLDIR
    # (hub index.html, _meta.json) are regenerated below; only subdirectories are pruned.
    import shutil
    for name in os.listdir(VOLDIR):
        sub = os.path.join(VOLDIR, name)
        if os.path.isdir(sub):
            shutil.rmtree(sub)
    emitted=[]
    page_index={}   # cui -> {slug,num,placed,residual_rank,system,genes,title}

    # ---- placed disease pages (sections 2..N) ----
    disease_meta=[]
    for i,r in enumerate(placed):
        ps,page,m = build_disease(i,r)
        write(os.path.join(VOLDIR,ps,"index.html"), page)
        emitted.append(("disease/"+ps+"/index.html",page))
        disease_meta.append(m)
        cui=r["cui"]; slug2,d=dossiers[cui]
        page_index[cui]={"slug":ps,"num":m["no"],"placed":True,
            "residual_rank":m["residual_rank"],"system":d["identity"].get("system_class",r["system_class"]),
            "genes":d["identity"].get("genes",[]),"title":m["title"]}

    # ---- not-placed disease pages (continue numbering), ordered by axis coverage then name ----
    notplaced_cuis=[c for c,s in scores.items() if s["rankable"]!="yes"]
    notplaced_cuis.sort(key=lambda c:(-int(scores[c]["axes_scored"]), scores[c]["entity"]))
    np_meta=[]
    base=len(placed)+2   # framework=1, placed=2..(len+1); not-placed start here
    for j,cui in enumerate(notplaced_cuis):
        num_sec=base+j
        prev_lnk=(f"/disease/{slugify(placed[-1]['entity'],len(placed)+1)}/", placed[-1]['entity']) if j==0 \
                 else (f"/disease/{slugify(scores[notplaced_cuis[j-1]]['entity'],num_sec-1)}/", scores[notplaced_cuis[j-1]]['entity'])
        next_lnk=(f"/disease/{slugify(scores[notplaced_cuis[j+1]]['entity'],num_sec+1)}/", scores[notplaced_cuis[j+1]]['entity']) \
                 if j+1<len(notplaced_cuis) else None
        ps,page,m = build_disease_notplaced(num_sec, cui, prev_lnk, next_lnk)
        write(os.path.join(VOLDIR,ps,"index.html"), page)
        emitted.append(("disease/"+ps+"/index.html",page))
        np_meta.append(m)
        slug2,d=dossiers[cui]
        page_index[cui]={"slug":ps,"num":num_sec,"placed":False,"residual_rank":None,
            "system":d["identity"].get("system_class",scores[cui]["system_class"]),
            "genes":d["identity"].get("genes",[]),"title":m["title"]}

    # ---- cross-cutting class chapters (after the diseases) ----
    class_meta=[]
    cbase=base+len(notplaced_cuis)
    for k,cdef in enumerate(CLASSES):
        num_sec=cbase+k
        ps,page,m = build_class_chapter(num_sec, cdef, page_index)
        write(os.path.join(VOLDIR,ps,"index.html"), page)
        emitted.append(("disease/"+ps+"/index.html",page))
        class_meta.append(m)

    # ---- framework (prepends itself; built with the placed order table) ----
    meta_for_fw = list(disease_meta)
    fwslug,fwpage = build_framework(meta_for_fw)
    write(os.path.join(VOLDIR,fwslug,"index.html"), fwpage)
    emitted.append(("disease/"+fwslug+"/index.html",fwpage))

    # ---- full ordered chapter list ----
    meta_chapters=[{"no":1,"slug":fwslug,"kind":"framework",
        "title":"Classification, burden, and treatment framework",
        "one_liner":"three axes + deterministic burden index + residual offset + grade legend",
        "grade":"[H]","residual_rank":None}]
    for m in disease_meta:
        meta_chapters.append({"no":m["no"],"slug":m["slug"],"kind":"placed","title":m["title"],
            "one_liner":m["one_liner"],"grade":m["grade"],"residual_rank":m["residual_rank"]})
    for m in np_meta:
        meta_chapters.append({"no":m["no"],"slug":m["slug"],"kind":"notplaced","title":m["title"],
            "one_liner":m["one_liner"],"grade":m["grade"],"residual_rank":None})
    for m in class_meta:
        meta_chapters.append({"no":m["no"],"slug":m["slug"],"kind":"class","title":m["title"],
            "one_liner":m["one_liner"],"grade":m["grade"],"residual_rank":None})

    # ---- hub ----
    hub=build_hub(meta_chapters)
    write(os.path.join(VOLDIR,"index.html"), hub)
    emitted.append(("disease/index.html",hub))

    # ---- _meta.json ----
    meta={"paper_id":"disease","code":"dis","title":VOL_TITLE,"short":VOL_SHORT,
          "doi":"10.5281/zenodo.20763842","doi_status":"registered (VP-SPEC §2)","hub_url":"/disease/",
          "branch":"jamming","build_date":BUILD_DATE,
          "abstract":"Systemic genetic and rare diseases, one page per disease: a graded molecular mechanism, a "
                     "reproducible burden order (provisional [H]), and the established treatment mechanism "
                     "(accession-dated [L] for 33 of 35). Onset is registry-graded [L] from Orphanet (28/35), "
                     "disability [L] from the GBD 2013 disability-weights table (13/35), severity [L] from the "
                     "HPO clinical-modifier Severity subtree (HP:0012824) for the one disease whose dominant sequela "
                     "is annotated, and progression [L] from curated PMC open-access literature with a "
                     f"frozen-R3-derived tier (order_locked {_locked_n_names()[0]}/35).",
          "headline_results":["burden_score = raw_burden · (1 − e)","rankable = axes_scored ≥ 3 of 5",
                              "treatments accession-dated to GeneReviews Management: 33 [L], 2 [H] (no therapy)",
                              "disability [L] 13/35 from GBD 2013 disability weights; 2 mortality axes corroborated from PMC survival literature (R7)",
                              "severity [L] via the HPO Severity-modifier subtree (HP:0012824) dominant-sequela join (R8): 1 disease lifted",
                              f"progression [L] via curated PMC-OA literature with a frozen-R3-derived tier (R9+R10): Niemann-Pick type A &rarr; tier 1.0 (3rd order_locked, R9), Duchenne MD (R9) plus Fabry &amp; Marfan progression (R10 round 2) corroborated (not locked); order_locked {_locked_n_names()[0]}/35",
                              "unmet-need / treatment-gap surface: a read-only graded research-prioritisation view (residual = raw_burden·(1−e)); headline = burden [L] + no disease-directed therapy"],
          "provisional_order":True,
          "registry_passes":["R5 treatment accession-dating (GeneReviews Management → [L], 33/35)",
                             "R6 Orphanet natural-history (onset → registry [L], 28/35; +1 mortality)",
                             "R7 open-source natural-history (GBD 2013 disability weights → disability [L], 13/35; "
                             "+2 mortality axes corroborated from PMC survival literature; OMIM clinical synopsis "
                             "clean-skipped, no key)",
                             "R8 open-source severity (HPO clinical-modifier Severity subtree HP:0012824 → severity "
                             "[L] via a cited dominant-sequela join, 1 disease)",
                             "R9 curated severity/progression (cited PMC open-access dominant-sequela join; tier "
                             "DERIVED by the frozen R3 tier function over the verbatim sentence, non-spectrum → "
                             f"progression [L]; Niemann-Pick type A is a 3rd order_locked disease, Duchenne MD "
                             f"corroborated not locked; order_locked {_locked_n_names()[0]}/35)"],
          "order_locked":sum(1 for c in scores if scores[c].get("order_locked")=="yes"),
          "deferred_L_passes":["the rest of severity (feature-level in the open HPO annotations — a category error if "
                               "read as a disease tier), the rest of progression, and remaining mortality [H]→[L]/[V] via "
                               "published functional & survival literature — remaining lift. The OMIM clinical-synopsis "
                               "path is removed (API key unobtainable for an individual researcher), not deferred"],
          "chapters":meta_chapters,
          "totals":{"sections":len(meta_chapters),"diseases_total":len(scores),
                    "diseases_placed":RANK_TOTAL,"diseases_not_placed":len(notplaced_cuis),
                    "class_chapters":len(class_meta)}}
    write(os.path.join(VOLDIR,"_meta.json"), json.dumps(meta,ensure_ascii=False,indent=2))

    # ---- sitemap.xml (hub + every section) ----
    urls=[f"{SITE}/disease/"] + [f"{SITE}/disease/{c['slug']}/" for c in meta_chapters]
    sm=['<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f'  <url><loc>{u}</loc><lastmod>{BUILD_DATE}</lastmod><changefreq>monthly</changefreq></url>')
    sm.append('</urlset>')
    write(os.path.join(DOCS,"sitemap.xml"), "\n".join(sm)+"\n")

    # ---- robots.txt ----
    robots=("# Disease Mechanisms volume — allow search and AI crawlers (VP-SPEC §6-R.5)\n"
            "User-agent: Googlebot\nAllow: /\n"
            "User-agent: Bingbot\nAllow: /\n"
            "User-agent: OAI-SearchBot\nAllow: /\n"
            "User-agent: GPTBot\nAllow: /\n"
            "User-agent: PerplexityBot\nAllow: /\n"
            "User-agent: ClaudeBot\nAllow: /\n"
            "User-agent: Google-Extended\nAllow: /\n"
            "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {SITE}/sitemap.xml\n")
    write(os.path.join(DOCS,"robots.txt"), robots)

    # ---- llms.txt ----
    llms=[f"# {VOL_TITLE} ({VOL_SHORT})","",
          "> Systemic-body genetic and rare diseases, one standalone page per disease: each gives a graded molecular",
          "> mechanism, a reproducible burden position, and the established treatment mechanism. Clinical facts are",
          "> observed, cited inputs; the classification and burden order are the reproducible analysis layer. The",
          "> burden order is a provisional [H]-grade prioritisation device, not a registry-locked ranking.","",
          "## Core",
          f"- [Framework: classification, burden index, grades](/disease/01-classification-burden-treatment-framework/)",
          f"- [Volume hub](/disease/)","",
          "## Placed diseases (one page each, residual-burden order)"]
    for m in disease_meta:
        llms.append(f"- [{m['title']}](/disease/{m['slug']}/) — residual rank {m['residual_rank']}/{RANK_TOTAL} [H]")
    llms += ["","## Not-placed diseases (own page; <3 of 5 burden axes scored, rank null)"]
    for m in np_meta:
        llms.append(f"- [{m['title']}](/disease/{m['slug']}/) — not placed [O]")
    llms += ["","## Mechanism-class cross-references (link member pages, do not restate them)"]
    for m in class_meta:
        llms.append(f"- [{m['title']}](/disease/{m['slug']}/) — {m['one_liner']} [F]")
    llms += ["","## Policy",
             "- Research whitepaper, not clinical guidance (no dosing/diagnosis).",
             "- Treatments accession-dated to GeneReviews Management (33 [L]); 2 have no disease-directed therapy ([H]).",
             f"- Registry passes: onset [L] (Orphanet, 28/35)+1 mortality (R6); disability [L] (GBD 2013, 13/35)+2 mortality from PMC (R7); severity & progression [L] via curated PMC-OA literature, frozen-R3 tier (R8-R15, 12+12/35); locked {_locked_n_names()[0]}/35.",
             "- Unmet-need surface (unmet_need_surface.*): read-only graded view; residual=raw_burden·(1−e); headline=burden [L]+no therapy.",
             "- Remaining [L] lift: rest of severity/progression/mortality via published literature. OMIM removed (no key); [O] axes carry an obstacle."]
    write(os.path.join(DOCS,"llms.txt"), "\n".join(llms)+"\n")

    # ---- IRREPRODUCIBILITY_LEDGER.md ----
    n_tx_L=sum(1 for c in scores if treats[c]["grade"]=="[L]")
    n_tx_H=sum(1 for c in scores if treats[c]["grade"]=="[H]")
    n_open_axes=sum(1 for c in scores for ax in ["O","P","S","M","D"] if scores[c][ax+"_grade"]=="[O]")
    n_onset_L=sum(1 for c in scores if scores[c]["O_grade"]=="[L]")
    n_mort_L=sum(1 for c in scores if scores[c]["M_grade"]=="[L]")
    n_disab_L=sum(1 for c in scores if scores[c]["D_grade"]=="[L]")
    n_locked=sum(1 for c in scores if scores[c].get("order_locked")=="yes")
    n_sev_L=sum(1 for c in scores if scores[c]["S_grade"]=="[L]")
    n_prog_L=sum(1 for c in scores if scores[c]["P_grade"]=="[L]")
    locked_names=", ".join(sorted(scores[c]["entity"] for c in scores if scores[c].get("order_locked")=="yes")) or "none"
    led=["# IRREPRODUCIBILITY_LEDGER — Disease Mechanisms volume (W1)","",
         "Every `[O]` grade carries a named obstacle (VP-SPEC C3). This ledger aggregates the open items the",
         "W1 prose exposes, plus the volume-level provisional-`[H]` condition.","",
         "## Volume-level provisional grade (the W1-entry condition)","",
         "| item | grade | obstacle / upgrade path |","|---|---|---|",
         f"| Burden / residual ORDER (all placed diseases) | [H] | the natural-history registry passes have lifted onset to registry [L] (Orphanet/Orphadata, R6: {n_onset_L}/35, entity-anchored AverageAgeOfOnset, Exact OMIM↔ORPHA), disability to registry [L] (GBD 2013 disability weights, R7: {n_disab_L}/35, one dominant untreated sequela → named GBD health state, published weight binned by declared cut-points), with {n_mort_L}×[L] mortality (2 independently corroborated from PMC survival literature, R7), severity to registry [L] (cited dominant-sequela joins, tier DERIVED by the frozen R3 tier function: R8 HPO Severity subtree HP:0012824 + R11/R12/R14 curated PMC open-access + R3 clinical-definition/GeneReviews corroboration, {n_sev_L}/35), and progression to registry [L] (curated PMC open-access literature, R9+R10+R13+R14: {n_prog_L}/35, dominant-sequela join whose tier is DERIVED by the frozen R3 tier function over the verbatim sentence, non-spectrum); order_locked = {n_locked}/35 ({locked_names} — every scored axis registry [L]). The order overall stays [H] because the rest of severity (feature-level in the open HPO annotations — a category error if read as a disease tier) and the rest of progression remain definition-grade inferences for the other placed diseases; remaining lift via published functional & survival literature. The OMIM clinical-synopsis path is removed (its API key is unobtainable for an individual researcher), not deferred |",
         f"| Treatment evidence | {n_tx_L}×[L] / {n_tx_H}×[H] | {n_tx_L} accession-dated to GeneReviews Management/Summary (NBK + initial-posting/last-revision dates, drug-term corroborated); the {n_tx_H} retained [H] are evidence_status=none (achondrogenesis II, Niemann-Pick A) — no disease-directed therapy exists to accession-date |",
         f"| Open burden axes (cohort-wide) | [O] | {n_open_axes} axis cells are [O]; R6's entity-anchored Orphanet read lifted onset where an Exact mapping existed (incl. one [O]→[L] onset), R7's GBD 2013 disability-weights join lifted disability to [L] for {n_disab_L}/35 (promoting 4 diseases into the placed order), R8's HPO Severity-modifier join (HP:0012824) lifted severity to [L] for the one disease whose dominant sequela is annotated and R11's curated PMC open-access join lifted Marfan's severity to [L] (completing its order-lock), and R9+R10's curated PMC open-access literature join lifted progression to [L] for {n_prog_L}/35 (tier DERIVED by the frozen R3 tier function over the verbatim cited sentence, non-spectrum); the remaining open severity is feature-level in the open HPO annotations (a category error if read as a disease tier) and the OMIM clinical synopsis (the disease-level alternative) has an API key that is unobtainable for an individual researcher, so the remaining [O]/[H] severity/progression cells stay open/definition-grade, deferred to published functional & survival literature (the OMIM path is removed, not deferred); PMC survival literature corroborates mortality only where a quantitative disease-typical figure exists (free text does not fill an [O] mortality axis — over-trigger risk); GeneReviews [O]-fill stays WITHHELD (a single first-match over a ~6 kB chapter over-triggers and would move raw_burden) |",
         "| Volume DOI | 10.5281/zenodo.20763842 | registered concept DOI (VP-SPEC §2) |","",
         "## Per-field open items surfaced on disease pages","",
         "| disease | field | grade | obstacle |","|---|---|---|---|"]
    allcuis=[r["cui"] for r in placed]+notplaced_cuis
    for cui in allcuis:
        slug,d=dossiers[cui]; ent=scores[cui]["entity"]; inh=d["inheritance"]
        if inh["grade"]=="[O]":
            led.append(f"| {ent} | inheritance (structured) | [O] | {inh.get('obstacle','mode-of-inheritance field unpopulated; cited definition characterises it')} |")
        opens=[ax for ax in ["O","P","S","M","D"] if scores[cui][ax+"_grade"]=="[O]"]
        if opens:
            led.append(f"| {ent} | burden axes {','.join(opens)} | [O] | no HPO annotation and no definition phrase for these axes; not guessed (GeneReviews [O]-fill withheld, see volume-level row) |")
    if not dossiers["C0017205"][1]["identity"].get("genes"):
        led.append("| Gaucher disease (aggregate) | gene_function, variant_spectrum | [O] | causative gene not annotated at this MedGen aggregate concept; see the gene-resolved Gaucher type I page |")
    # ---- Round-2 literature-curation declines (R10): why a retrievable OA sentence did NOT lift the axis ----
    _r10x = os.path.join(ROOT, "methodology", "severity_litcurate2_excluded.csv")
    if os.path.exists(_r10x):
        with open(_r10x, newline="", encoding="utf-8") as _fh:
            _rows = list(csv.DictReader(_fh))
        if _rows:
            led += ["", "## Round-2 literature-curation declines (R10) — OA sentence retrievable but disqualified",
                    "", "These cohort entities stay **not-placed / open** on the named axis even though a cited PMC "
                    "open-access sentence was found and verbatim-pinned: the sentence is scope-disqualified under the "
                    "frozen R9 rule (disease-level magnitude for the dominant untreated sequela, non-spectrum), so no "
                    "tier is asserted. Recorded in `methodology/severity_litcurate2_excluded.csv`.", "",
                    "| disease | axis | decline class | obstacle (why the OA sentence does not lift) | source |",
                    "|---|---|---|---|---|"]
            _axname = {"P": "progression", "S": "severity", "M": "mortality", "O": "onset", "D": "disability"}
            for _r in _rows:
                _ax = _axname.get(_r["axis"].strip(), _r["axis"].strip())
                _src = f"{_r['considered_pmcid'].strip()}" + (f" / PMID {_r['considered_pmid'].strip()}" if _r.get("considered_pmid", "").strip() else "")
                led.append(f"| {_r['entity'].strip()} | {_ax} | {_r['decline_class'].strip()} | {_r['exclusion_reason'].strip()} | {_src} |")
    # ---- Round-3 literature-curation declines (R11): why a retrievable OA sentence did NOT lift the axis ----
    _r11x = os.path.join(ROOT, "methodology", "severity_litcurate3_excluded.csv")
    if os.path.exists(_r11x):
        with open(_r11x, newline="", encoding="utf-8") as _fh:
            _rows3 = list(csv.DictReader(_fh))
        if _rows3:
            led += ["", "## Round-3 literature-curation declines (R11) — OA sentence retrievable but disqualified",
                    "", "These cohort entities stay **open** on the named axis even though a cited PMC "
                    "open-access sentence was found and verbatim-pinned: the sentence is scope-disqualified under the "
                    "frozen R9 rule (disease-level magnitude for the dominant untreated sequela, non-spectrum), so no "
                    "tier is asserted. Recorded in `methodology/severity_litcurate3_excluded.csv`.", "",
                    "| disease | axis | decline class | obstacle (why the OA sentence does not lift) | source |",
                    "|---|---|---|---|---|"]
            _axname3 = {"P": "progression", "S": "severity", "M": "mortality", "O": "onset", "D": "disability"}
            for _r in _rows3:
                _ax = _axname3.get(_r["axis"].strip(), _r["axis"].strip())
                _src = f"{_r['considered_pmcid'].strip()}" + (f" / PMID {_r['considered_pmid'].strip()}" if _r.get("considered_pmid", "").strip() else "")
                led.append(f"| {_r['entity'].strip()} | {_ax} | {_r['decline_class'].strip()} | {_r['exclusion_reason'].strip()} | {_src} |")
    # ---- Round-4 literature-curation declines (R12): why a retrievable OA sentence did NOT lift the axis ----
    _r12x = os.path.join(ROOT, "methodology", "severity_litcurate4_excluded.csv")
    if os.path.exists(_r12x):
        with open(_r12x, newline="", encoding="utf-8") as _fh:
            _rows4 = list(csv.DictReader(_fh))
        if _rows4:
            led += ["", "## Round-4 literature-curation declines (R12) — OA sentence retrievable but disqualified",
                    "", "These cohort entities stay **open** on the named axis even though a cited PMC "
                    "open-access sentence was found and verbatim-pinned: the sentence is scope-disqualified under the "
                    "frozen R9 rule (disease-level magnitude for the dominant untreated sequela, non-spectrum, "
                    "non-comparative, non-sub-phenotype), so no tier is asserted. Recorded in "
                    "`methodology/severity_litcurate4_excluded.csv`.", "",
                    "| disease | axis | decline class | obstacle (why the OA sentence does not lift) | source |",
                    "|---|---|---|---|---|"]
            _axname4 = {"P": "progression", "S": "severity", "M": "mortality", "O": "onset", "D": "disability"}
            for _r in _rows4:
                _ax = _axname4.get(_r["axis"].strip(), _r["axis"].strip())
                _src = f"{_r['considered_pmcid'].strip()}" + (f" / PMID {_r['considered_pmid'].strip()}" if _r.get("considered_pmid", "").strip() else "")
                led.append(f"| {_r['entity'].strip()} | {_ax} | {_r['decline_class'].strip()} | {_r['exclusion_reason'].strip()} | {_src} |")
    # ---- Round-5 literature-curation declines (R13): why a retrievable OA sentence did NOT lift the axis ----
    _r13x = os.path.join(ROOT, "methodology", "severity_litcurate5_excluded.csv")
    if os.path.exists(_r13x):
        with open(_r13x, newline="", encoding="utf-8") as _fh:
            _rows5 = list(csv.DictReader(_fh))
        if _rows5:
            led += ["", "## Round-5 literature-curation declines (R13) — OA sentence retrievable but disqualified",
                    "", "These cohort entities stay **open** on the named axis even though a cited PMC "
                    "open-access sentence was found and verbatim-pinned: the sentence is scope-disqualified under the "
                    "frozen R9 rule (disease-level magnitude for the dominant untreated sequela, non-spectrum, "
                    "non-comparative, non-sub-phenotype), so no tier is asserted. Recorded in "
                    "`methodology/severity_litcurate5_excluded.csv`.", "",
                    "| disease | axis | decline class | obstacle (why the OA sentence does not lift) | source |",
                    "|---|---|---|---|---|"]
            _axname5 = {"P": "progression", "S": "severity", "M": "mortality", "O": "onset", "D": "disability"}
            for _r in _rows5:
                _ax = _axname5.get(_r["axis"].strip(), _r["axis"].strip())
                _src = f"{_r['considered_pmcid'].strip()}" + (f" / PMID {_r['considered_pmid'].strip()}" if _r.get("considered_pmid", "").strip() else "")
                led.append(f"| {_r['entity'].strip()} | {_ax} | {_r['decline_class'].strip()} | {_r['exclusion_reason'].strip()} | {_src} |")
    # ---- Round-6 literature-curation declines (R14): why a retrievable OA sentence did NOT lift the axis ----
    _r14x = os.path.join(ROOT, "methodology", "severity_litcurate6_excluded.csv")
    if os.path.exists(_r14x):
        with open(_r14x, newline="", encoding="utf-8") as _fh:
            _rows6 = list(csv.DictReader(_fh))
        if _rows6:
            led += ["", "## Round-6 literature-curation declines (R14) — OA sentence retrievable but disqualified",
                    "", "These cohort entities stay **open** on the named axis even though a cited PMC "
                    "open-access sentence was found and verbatim-pinned: the sentence is scope-disqualified under the "
                    "frozen R9 rule (disease-level magnitude for the dominant untreated sequela, non-spectrum, "
                    "non-comparative, non-sub-phenotype), so no tier is asserted. Recorded in "
                    "`methodology/severity_litcurate6_excluded.csv`.", "",
                    "| disease | axis | decline class | obstacle (why the OA sentence does not lift) | source |",
                    "|---|---|---|---|---|"]
            _axname6 = {"P": "progression", "S": "severity", "M": "mortality", "O": "onset", "D": "disability"}
            for _r in _rows6:
                _ax = _axname6.get(_r["axis"].strip(), _r["axis"].strip())
                _src = f"{_r['considered_pmcid'].strip()}" + (f" / PMID {_r['considered_pmid'].strip()}" if _r.get("considered_pmid", "").strip() else "")
                led.append(f"| {_r['entity'].strip()} | {_ax} | {_r['decline_class'].strip()} | {_r['exclusion_reason'].strip()} | {_src} |")
    # ---- Round-7 literature-curation declines (R15): why a retrievable OA sentence did NOT lift the axis ----
    _r15x = os.path.join(ROOT, "methodology", "severity_litcurate7_excluded.csv")
    if os.path.exists(_r15x):
        with open(_r15x, newline="", encoding="utf-8") as _fh:
            _rows7 = list(csv.DictReader(_fh))
        if _rows7:
            led += ["", "## Round-7 literature-curation declines (R15) — OA sentence retrievable but disqualified",
                    "", "These cohort entities stay **open**/**[H]** on the named axis even though a cited PMC "
                    "open-access sentence was found and verbatim-pinned: the sentence is scope-disqualified under the "
                    "frozen R9 rule (disease-level magnitude for the dominant untreated sequela, non-spectrum, "
                    "non-comparative, non-sub-phenotype), so no tier is asserted. Recorded in "
                    "`methodology/severity_litcurate7_excluded.csv`.", "",
                    "| disease | axis | decline class | obstacle (why the OA sentence does not lift) | source |",
                    "|---|---|---|---|---|"]
            _axname7 = {"P": "progression", "S": "severity", "M": "mortality", "O": "onset", "D": "disability"}
            for _r in _rows7:
                _ax = _axname7.get(_r["axis"].strip(), _r["axis"].strip())
                _src = f"{_r['considered_pmcid'].strip()}" + (f" / PMID {_r['considered_pmid'].strip()}" if _r.get("considered_pmid", "").strip() else "")
                led.append(f"| {_r['entity'].strip()} | {_ax} | {_r['decline_class'].strip()} | {_r['exclusion_reason'].strip()} | {_src} |")
    write(os.path.join(ROOT,"IRREPRODUCIBILITY_LEDGER.md"), "\n".join(led)+"\n")

    # ---- deterministic-build digest ----
    h=hashlib.sha256()
    for name,page in sorted(emitted):
        h.update(name.encode()); h.update(page.encode())
    digest=h.hexdigest()[:12]
    print(f"W1 build OK — {len(emitted)} HTML pages "
          f"(1 hub + 1 framework + {RANK_TOTAL} placed + {len(notplaced_cuis)} not-placed + {len(class_meta)} class)")
    print(f"site-set sha256(12) = {digest}")
    return digest

if __name__=="__main__":
    main()

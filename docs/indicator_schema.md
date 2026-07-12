# ICAID Indicator Schema — Month 1 Dataset Plan

Derived from Section X ("Reproducibility and Open-Science Roadmap") and
Section III-B (dimension formulas) of the ICAID paper. This is the
concrete list of indicators needed to replace `data/synthetic/` with a
real, source-verified `data/processed/icaid_real_panel.csv`.

**Target scope:** 36 states/UTs × 2020–2025 × ~100–150 indicators,
aggregated into the 6 ICAID dimensions (CE, DF, CA, SI, IR, IP).

**Status legend:** `pending` (not started) · `in_progress` · `collected`
(raw data downloaded, not yet verified) · `verified` (cross-checked,
ready for `build_real_panel.py`)

---

## Dimension → Indicator → Source map

### IR — Infrastructure Readiness
Formula (Section III-B, fully specified — usable as-is once sub-indicators exist):
`IR(s) = 0.30·Connectivity(s) + 0.25·PowerReliability(s) + 0.25·DeviceAccess(s) + 0.20·DigitalLiteracy(s)`

| Sub-indicator | Proposed source | Access | Status |
|---|---|---|---|
| Connectivity (teledensity, broadband penetration) | TRAI | Telecom Subscription Data Reports (quarterly PDF/Excel, trai.gov.in) | pending |
| Power reliability | MOSPI / state power utility reports | Varies by state, often PDF | pending |
| Device access (smartphone/PC penetration) | NSSO periodic surveys | Survey microdata / summary tables | pending |
| Digital literacy | NSSO periodic surveys | Survey microdata / summary tables | pending |

### CE — Causal Explainability
No direct government statistic — paper defines this as a property of
*deployed AI systems being audited* (ACE of causal XAI methods vs. SHAP/LIME).
Requires a primary audit protocol (Section III-H), not a scraped indicator.
**This dimension cannot be populated from open government data alone —
needs a defined case-study audit methodology before Month 1 numbers exist.**

| Sub-indicator | Proposed source | Access | Status |
|---|---|---|---|
| AI system inventory per state (health/agri/judicial) | AIKosh, ABDM, AgriStack, e-Courts | AIKosh has a catalog API; others vary | pending |
| Causal-XAI usage flag per system | Manual audit (Section III-H protocol) | N/A — primary research | pending |

### DF — Demographic Fairness
Requires outcome data broken out by SC/ST/OBC/General/Minority — this is
the hardest dimension to source at state-aggregate, non-personal level
per the DPDP constraint in Section IX-A.

| Sub-indicator | Proposed source | Access | Status |
|---|---|---|---|
| Demographic composition | Census of India | Census tables (2011 base + NSSO updates) | pending |
| Outcome disparity by group, per AI system | Sector-specific (ABDM, e-Courts) | Requires case-study-level audit | pending |

### CA — Constitutional Alignment
9 sub-criteria (Justice, Liberty, Equality, ... per Section III-B table).
Largely qualitative/audit-based, not a single open dataset.

| Sub-indicator | Proposed source | Access | Status |
|---|---|---|---|
| Judicial AI bias by group | e-Courts Mission Mode Project | Case-outcome data, needs audit | pending |
| Data localization compliance | MeitY / IndiaAI Mission policy docs | AIKosh policy-document catalog | pending |

### SI — Societal Impact
| Sub-indicator | Proposed source | Access | Status |
|---|---|---|---|
| AI adoption in health | ABDM (Ayushman Bharat Digital Mission) | ABDM dashboard/API | pending |
| AI adoption in agriculture | ICAR, Bharat-VISTAAR / AgriStack | AgriStack data portal | pending |
| State population (for normalization, N_s) | Census of India / MOSPI | Public tables | pending |

### IP — Innovation Potential
`IP(s) = Patents_AI(s)/Population(s) · StartupDensity(s) · TalentIndex(s)`

| Sub-indicator | Proposed source | Access | Status |
|---|---|---|---|
| AI-related patents by state | Indian Patent Office (IPO India) | IPO India search/annual reports | pending |
| AI startup count by state | DPIIT Startup India registry | Startup India open data | pending |
| Talent index (AI-skilled workforce) | NASSCOM reports, AICTE | Industry reports (secondary) | pending |

---

## Next concrete step (Month 1, Week 1)
Pick **one indicator with a real, testable API/download** (candidates:
DPIIT Startup India registry, AIKosh dataset catalog) and get it flowing
end-to-end through `fetch_indicator.py` → `data/raw/` → verified. That
becomes the template for the rest. Don't try to parallelize across all
10 sources at once — one clean, verified pipeline beats ten broken ones.

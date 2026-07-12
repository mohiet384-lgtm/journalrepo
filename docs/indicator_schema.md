# ICAID Indicator Schema — Month 1 Deliverable

Status: **SCAFFOLD**. This lists candidate indicators mapped to real,
publicly verifiable Indian government/institutional sources. Nothing in
this file is data — it is the *plan* for what to collect and from where.
Each row must be manually verified (URL, exact table/dataset name, access
method, and licence) before `src/data_collection/` scripts are pointed at it.

Coverage target: 36 states/UTs × 2020–2025 × ~120 indicators across the
6 ICAID dimensions (CE, DF, CA, SI, IR, IP).

## How to use this file
1. For each indicator, verify the source is still live and note the exact
   dataset/API/report name (sources move; data.gov.in datasets get
   deprecated and replaced often).
2. Fill in `data_collection/sources.yaml` (machine-readable version of this
   table) only after verification — do not hallucinate a URL.
3. Where a real per-state, per-year source does not exist for an indicator,
   either (a) drop the indicator, (b) proxy it with a related indicator that
   *does* have real data, or (c) mark it explicitly as "not collectible" —
   never fabricate.

## Dimension 1: Causal Explainability (CE) — proxy indicators
| # | Indicator | Candidate real source | Granularity | Notes |
|---|---|---|---|---|
| 1 | # of state-run AI systems with published model cards | State IT dept portals, RTI responses | State-year | Needs manual audit; no central registry exists yet |
| 2 | AI incidents reported / grievances filed re: automated decisions | State e-governance grievance portals (CPGRAMS) | State-year | CPGRAMS has an API; filter by keyword |
| 3 | # of empanelled AI vendors requiring explainability clauses | GeM (Government e-Marketplace) tender text | State-year | Requires text-mining tender documents |

## Dimension 2: Demographic Fairness (DF)
| # | Indicator | Candidate real source | Granularity | Notes |
|---|---|---|---|---|
| 4 | Gender Parity Index (education/digital access) | NFHS-5, UDISE+ (education dept) | State-year | UDISE+ has open dashboards |
| 5 | Rural-urban digital divide (internet access %) | TRAI + NSS 75th/78th round (MoSPI) | State | NSS rounds are periodic, not annual — interpolate & flag |
| 6 | SC/ST/OBC representation in AI/IT workforce | Periodic Labour Force Survey (PLFS), MoSPI | State-year | PLFS unit-level data on MoSPI website |

## Dimension 3: Constitutional Alignment (CA)
| # | Indicator | Candidate real source | Granularity | Notes |
|---|---|---|---|---|
| 7 | # of AI-related RTI/PIL cases | Indian Kanoon (case search), High Court portals | State-year | Legal text-mining required |
| 8 | Data Protection Board orders re: state AI use | MeitY / Data Protection Board notifications | National-year | DPDP Act 2023 enforcement is recent — sparse data pre-2024 |

## Dimension 4: Societal Impact (SI)
| # | Indicator | Candidate real source | Granularity | Notes |
|---|---|---|---|---|
| 9 | AI-enabled health diagnoses volume | Ayushman Bharat Digital Mission (ABDM) dashboards | State-year | ABDM has public dashboards |
| 10 | AI-assisted agri-advisory reach | Kisan Call Centre / e-NAM / PM-Kisan AI chatbot logs | State-year | Some data via IndiaAI Mission reports |

## Dimension 5: Infrastructure Readiness (IR)
| # | Indicator | Candidate real source | Granularity | Notes |
|---|---|---|---|---|
| 11 | Data centre capacity (MW) | Invest India / MeitY infra reports | State-year | Coarse, updated irregularly |
| 12 | Broadband penetration (BharatNet coverage %) | BharatNet / DoT dashboards | State-year | DoT publishes gram panchayat-level connectivity |
| 13 | Compute access (empanelled AI cloud/GPU credits disbursed) | IndiaAI Mission compute portal | State-year | New (2024+), limited history |

## Dimension 6: Innovation Potential (IP)
| # | Indicator | Candidate real source | Granularity | Notes |
|---|---|---|---|---|
| 14 | AI patent filings | Indian Patent Office (IPO) annual reports, IP India search | State-year | IPO has bulk search; state inferred from applicant address |
| 15 | AI startup funding/count | Startup India portal, Tracxn/Crunchbase (paid) | State-year | Free tier limited — may need manual curation |
| 16 | AI research output (papers w/ Indian-state affiliation) | Scopus/Web of Science (institutional access) or OpenAlex API (free) | State-year | OpenAlex is free & scriptable — prefer this |

## Honest gaps to flag in the paper
- No indicator here has annual, state-level, machine-readable coverage for
  all 36 states 2020–2025 out of the box. Real work = reconciling different
  update cadences (some annual, some quinquennial like NSS/Census) and
  documenting imputation choices.
- This table currently has 16 illustrative rows, not 100–150. Reaching
  100–150 real, sourced indicators is itself a multi-week literature +
  data-audit task — expand this table indicator by indicator, each with a
  verified live source, rather than padding the count with unverifiable rows.

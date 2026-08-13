# eSVD-2026 — methodology notes

**[نسخه فارسی](methodology.fa.md)**

This document expands on the rationale and precise operational definitions used
in the eSVD-2026 score. See the main [README](../README.md) for a quick summary
and usage examples.

## 1. Background

The Total SVD Score (Staals et al., 2014, *Neurology*) summarizes four
neuroimaging markers of cerebral small vessel disease into a single 0–4 ordinal
scale:

1. Lacunes of presumed vascular origin
2. White matter hyperintensities (WMH), graded with the Fazekas scale
3. Cerebral microbleeds
4. Enlarged perivascular spaces (EPVS) in the basal ganglia

Each marker contributes at most one point, based on evidence that these four
features frequently co-occur and jointly predict cognitive and functional
decline better than any single marker alone.

## 2. Rationale for the eSVD-2026 extension

Since 2014, two additional markers have accumulated substantial evidence of
mechanistic and prognostic relevance to small vessel disease, but were not part
of the original score:

### 2.1 Cortical superficial siderosis (cSS)

cSS is deposition of hemosiderin in the subarachnoid space over the cerebral
convexities, best seen on susceptibility-weighted or T2\*-weighted MRI. It is a
core diagnostic feature of **cerebral amyloid angiopathy (CAA)** — a form of
small vessel disease affecting cortical and leptomeningeal vessels — and is
one of the strongest known predictors of future lobar intracerebral
hemorrhage (Charidimou et al., 2022; Boston Criteria v2.0).

### 2.2 Cortical atrophy

Chronic small vessel disease is increasingly recognized as intertwined with
neurodegeneration and cortical volume loss, above and beyond what is expected
from normal aging. The **Global Cortical Atrophy (GCA)** scale (Pasquier et
al., 1996) offers a simple, visually-rated 0–3 measure of cortical atrophy that
is widely used in clinical radiology reporting and correlates with cognitive
outcomes in SVD cohorts.

Both additions are consistent with the STRIVE-2 consensus statement (Duering
et al., 2023) call for broadening SVD imaging assessment beyond the original
four markers.

## 3. Operational point rules

| Marker | Point rule |
|---|---|
| Lacunes | `lacunes == True` (≥ 1 lacune present) |
| WMH | `periventricular_fazekas == 3 OR deep_fazekas >= 2` |
| Microbleeds | `microbleeds == True` (≥ 1 microbleed present) |
| EPVS | `evps_basal_ganglia_grade >= 2` (≥ 11 EPVS) |
| Cortical superficial siderosis | `cortical_superficial_siderosis == True` |
| Cortical atrophy | `global_cortical_atrophy_grade >= 2` |

Total score = sum of the six binary indicators, range 0–6. Setting the two new
indicators to `False`/`0` reproduces the original Staals et al. (2014) score
exactly, preserving backward compatibility with prior research using the
classic instrument.

## 4. What eSVD-2026 is **not**

- It is **not** a peer-reviewed, externally validated clinical score. The
  combination of six markers into a single unified 0–6 index is a proposal
  made in this repository, built from markers each individually supported by
  the literature.
- It does **not** replace formal neuroradiology reporting or established
  scores such as the CAA-specific Boston Criteria v2.0, the ARWMC scale, or
  the STRIVE-2 reporting standards — it is a complementary, simplified summary
  measure for research and teaching.
- It is **not** a diagnostic device.

Contributions proposing formal external validation studies, alternative
weighting schemes, or additional markers (e.g. brain volume, cortical
microinfarcts) are very welcome via GitHub issues/PRs.

"""
Core scoring logic for the eSVD-2026 score.

References
----------
1. Staals J, Makin SD, Doubal FN, Dennis MS, Wardlaw JM. Total MRI load of
   cerebral small vessel disease and cognitive ability in older people.
   Neurology. 2014;83(14):1228-1234.
2. Fazekas F, Chawluk JB, Alavi A, et al. MR signal abnormalities at 1.5 T
   in Alzheimer's dementia and normal aging. AJR. 1987;149(2):351-356.
3. Greenberg SM, Vernooij MW, Cordonnier C, et al. Cerebral microbleeds: a
   guide to detection and interpretation. Lancet Neurol. 2009;8(2):165-174.
4. Doubal FN, MacLullich AM, Ferguson KJ, Dennis MS, Wardlaw JM. Enlarged
   perivascular spaces on MRI are a feature of cerebral small vessel
   disease. Stroke. 2010;41(3):450-454.
5. Charidimou A, Boulouis G, Frosch MP, et al. The Boston criteria version
   2.0 for cerebral amyloid angiopathy: a multicentre, retrospective,
   MRI-neuropathology diagnostic accuracy study. Lancet Neurol.
   2022;21(8):714-725. (cortical superficial siderosis)
6. Pasquier F, Leys D, Weerts JG, Mounier-Vehier F, Barkhof F, Scheltens P.
   Inter- and intraobserver reproducibility of cerebral atrophy assessment
   on MRI scans with hemispheric infarcts. Eur Neurol. 1996;36(5):268-272.
   (Global Cortical Atrophy, GCA, scale)
7. Duering M, Biessels GJ, Brodtmann A, et al. Neuroimaging standards for
   research into small vessel disease-advances since 2013. Lancet Neurol.
   2023;22(7):602-618. (rationale for extending the classic score)
8. Wardlaw JM, Smith EE, Biessels GJ, et al. Neuroimaging standards for
   research into small vessel disease and its contribution to ageing and
   neurodegeneration (STRIVE-2). Lancet Neurol. 2013;12(8):822-838.

Disclaimer
----------
This software is provided for research and educational purposes only.
It is NOT a certified medical device and must NOT be used as the sole
basis for clinical decision-making. Always correlate with a qualified
neuroradiologist's or neurologist's assessment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

__version__ = "1.0.0"


# --------------------------------------------------------------------------- #
# Input container
# --------------------------------------------------------------------------- #
@dataclass
class SVDFindings:
    """Structured MRI findings required to compute the SVD scores.

    Classic Total SVD Score (Staals 2014) markers
    -----------------------------------------------
    lacunes : bool
        True if >= 1 lacune of presumed vascular origin is present.
    microbleeds : bool
        True if >= 1 cerebral microbleed is present (any location).
    periventricular_fazekas : int (0-3)
        Fazekas periventricular white matter hyperintensity grade.
    deep_fazekas : int (0-3)
        Fazekas deep white matter hyperintensity grade.
    evps_basal_ganglia_grade : int (0-4)
        Enlarged perivascular spaces count grade in the basal ganglia
        (0 = none, 1 = 1-10, 2 = 11-20, 3 = 21-40, 4 = >40). A grade
        >= 2 (i.e. >=11 EPVS) scores a point, per the original score.

    eSVD-2026 extension markers
    ----------------------------
    cortical_superficial_siderosis : bool
        True if cortical superficial siderosis is present on
        susceptibility-weighted / T2*-weighted imaging (any extent).
    global_cortical_atrophy_grade : int (0-3)
        Global Cortical Atrophy (GCA) scale grade (Pasquier et al.
        1996). A grade >= 2 scores a point in eSVD-2026, reflecting
        moderate-to-severe cortical atrophy out of proportion to age.

    Optional metadata (not used in scoring, useful for reporting)
    ---------------------------------------------------------------
    patient_id, age, notes
    """

    lacunes: bool
    microbleeds: bool
    periventricular_fazekas: int
    deep_fazekas: int
    evps_basal_ganglia_grade: int
    cortical_superficial_siderosis: bool = False
    global_cortical_atrophy_grade: int = 0

    patient_id: Optional[str] = None
    age: Optional[float] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        _validate_range("periventricular_fazekas", self.periventricular_fazekas, 0, 3)
        _validate_range("deep_fazekas", self.deep_fazekas, 0, 3)
        _validate_range("evps_basal_ganglia_grade", self.evps_basal_ganglia_grade, 0, 4)
        _validate_range(
            "global_cortical_atrophy_grade", self.global_cortical_atrophy_grade, 0, 3
        )
        if self.age is not None and self.age < 0:
            raise ValueError("age must be non-negative")


def _validate_range(name: str, value: int, low: int, high: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if not (low <= value <= high):
        raise ValueError(f"{name} must be between {low} and {high}, got {value}")


# --------------------------------------------------------------------------- #
# Result container
# --------------------------------------------------------------------------- #
@dataclass
class ScoreResult:
    total: int
    max_score: int
    components: dict = field(default_factory=dict)
    risk_band: str = ""

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "max_score": self.max_score,
            "components": self.components,
            "risk_band": self.risk_band,
        }


# --------------------------------------------------------------------------- #
# Component point rules
# --------------------------------------------------------------------------- #
def _has_moderate_severe_wmh(f: SVDFindings) -> bool:
    """A point is awarded for WMH if periventricular Fazekas == 3 OR
    deep Fazekas >= 2 (Staals 2014 definition)."""
    return f.periventricular_fazekas == 3 or f.deep_fazekas >= 2


def _has_significant_evps(f: SVDFindings) -> bool:
    """A point is awarded when basal ganglia EPVS grade >= 2 (i.e. >= 11
    perivascular spaces), per the original Total SVD Score."""
    return f.evps_basal_ganglia_grade >= 2


def _has_significant_atrophy(f: SVDFindings) -> bool:
    """eSVD-2026 extension: a point is awarded when GCA grade >= 2
    (moderate to severe cortical atrophy)."""
    return f.global_cortical_atrophy_grade >= 2


# --------------------------------------------------------------------------- #
# Public scoring functions
# --------------------------------------------------------------------------- #
def score_svd(findings: SVDFindings) -> ScoreResult:
    """Compute the classic Total SVD Score (Staals et al., 2014), range 0-4."""
    components = {
        "lacunes": int(bool(findings.lacunes)),
        "white_matter_hyperintensities": int(_has_moderate_severe_wmh(findings)),
        "microbleeds": int(bool(findings.microbleeds)),
        "enlarged_perivascular_spaces": int(_has_significant_evps(findings)),
    }
    total = sum(components.values())
    return ScoreResult(
        total=total,
        max_score=4,
        components=components,
        risk_band=interpret(total, max_score=4),
    )


def score_esvd(findings: SVDFindings) -> ScoreResult:
    """Compute the eSVD-2026 score, range 0-6.

    Adds two markers to the classic Total SVD Score:
      * cortical superficial siderosis (marker of amyloid-related /
        hemorrhage-prone small vessel disease)
      * cortical atrophy (GCA >= 2), reflecting the neurodegenerative
        component increasingly linked to SVD burden.
    """
    base = score_svd(findings)
    components = dict(base.components)
    components["cortical_superficial_siderosis"] = int(
        bool(findings.cortical_superficial_siderosis)
    )
    components["cortical_atrophy"] = int(_has_significant_atrophy(findings))
    total = sum(components.values())
    return ScoreResult(
        total=total,
        max_score=6,
        components=components,
        risk_band=interpret(total, max_score=6),
    )


def interpret(total: int, max_score: int = 6) -> str:
    """Map a raw score to a qualitative burden band.

    The bands are proportional cut points (not yet independently
    validated for the 0-6 eSVD-2026 range) intended for descriptive,
    research-oriented reporting only.
    """
    if max_score <= 0:
        raise ValueError("max_score must be positive")
    ratio = total / max_score
    if ratio == 0:
        return "No detectable SVD burden"
    if ratio <= 1 / 3:
        return "Mild SVD burden"
    if ratio <= 2 / 3:
        return "Moderate SVD burden"
    return "Severe SVD burden"

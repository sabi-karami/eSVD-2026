"""
eSVD-2026: Extended Total Cerebral Small Vessel Disease (SVD) Score
====================================================================

A modernized, evidence-based extension of the ordinal Total SVD Score
introduced by Staals et al. (Neurology, 2014), incorporating two
additional MRI markers of cerebral small vessel disease that have
gained strong evidence support since the original score was published:
cortical superficial siderosis and cortical atrophy.

Public API
----------
- ``SVDFindings``      : structured input container for the four
  classic markers plus the two 2026-extension markers.
- ``score_svd()``      : compute the classic 0-4 Total SVD Score.
- ``score_esvd()``     : compute the extended 0-6 eSVD-2026 score.
- ``interpret()``      : map a score to a qualitative risk band.
"""

from .score import (
    SVDFindings,
    ScoreResult,
    score_svd,
    score_esvd,
    interpret,
    __version__,
)

__all__ = [
    "SVDFindings",
    "ScoreResult",
    "score_svd",
    "score_esvd",
    "interpret",
    "__version__",
]

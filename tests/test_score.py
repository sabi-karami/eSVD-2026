import pytest

from esvd import SVDFindings, score_svd, score_esvd, interpret


def make_findings(**overrides):
    base = dict(
        lacunes=False,
        microbleeds=False,
        periventricular_fazekas=0,
        deep_fazekas=0,
        evps_basal_ganglia_grade=0,
        cortical_superficial_siderosis=False,
        global_cortical_atrophy_grade=0,
    )
    base.update(overrides)
    return SVDFindings(**base)


def test_zero_score_when_no_markers_present():
    f = make_findings()
    result = score_esvd(f)
    assert result.total == 0
    assert result.max_score == 6
    assert result.risk_band == "No detectable SVD burden"


def test_classic_score_matches_staals_definition():
    f = make_findings(
        lacunes=True,
        microbleeds=True,
        periventricular_fazekas=3,
        deep_fazekas=1,
        evps_basal_ganglia_grade=2,
    )
    result = score_svd(f)
    assert result.total == 4
    assert result.max_score == 4
    assert result.components == {
        "lacunes": 1,
        "white_matter_hyperintensities": 1,
        "microbleeds": 1,
        "enlarged_perivascular_spaces": 1,
    }


def test_wmh_point_awarded_via_deep_fazekas_alone():
    f = make_findings(periventricular_fazekas=1, deep_fazekas=2)
    result = score_svd(f)
    assert result.components["white_matter_hyperintensities"] == 1


def test_wmh_point_not_awarded_below_threshold():
    f = make_findings(periventricular_fazekas=2, deep_fazekas=1)
    result = score_svd(f)
    assert result.components["white_matter_hyperintensities"] == 0


def test_esvd_extension_adds_two_points_max():
    f = make_findings(
        cortical_superficial_siderosis=True, global_cortical_atrophy_grade=2
    )
    result = score_esvd(f)
    assert result.total == 2
    assert result.components["cortical_superficial_siderosis"] == 1
    assert result.components["cortical_atrophy"] == 1


def test_full_house_scores_maximum_six():
    f = make_findings(
        lacunes=True,
        microbleeds=True,
        periventricular_fazekas=3,
        deep_fazekas=3,
        evps_basal_ganglia_grade=4,
        cortical_superficial_siderosis=True,
        global_cortical_atrophy_grade=3,
    )
    result = score_esvd(f)
    assert result.total == 6
    assert result.risk_band == "Severe SVD burden"


def test_interpret_bands():
    assert interpret(0, 6) == "No detectable SVD burden"
    assert interpret(1, 6) == "Mild SVD burden"
    assert interpret(3, 6) == "Moderate SVD burden"
    assert interpret(5, 6) == "Severe SVD burden"


def test_invalid_fazekas_grade_raises():
    with pytest.raises(ValueError):
        make_findings(periventricular_fazekas=5)


def test_invalid_type_raises_type_error():
    with pytest.raises(TypeError):
        make_findings(evps_basal_ganglia_grade="high")

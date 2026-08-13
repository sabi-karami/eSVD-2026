"""Example usage of the esvd2026 package.

Run with:
    python examples/example_usage.py
"""

from esvd import SVDFindings, score_svd, score_esvd

# Example patient with moderate-to-severe small vessel disease burden
findings = SVDFindings(
    patient_id="demo-001",
    age=72,
    lacunes=True,
    microbleeds=True,
    periventricular_fazekas=3,
    deep_fazekas=1,
    evps_basal_ganglia_grade=2,
    cortical_superficial_siderosis=False,
    global_cortical_atrophy_grade=1,
)

classic = score_svd(findings)
extended = score_esvd(findings)

print("Classic Total SVD Score (Staals 2014):")
print(f"  {classic.total} / {classic.max_score} — {classic.risk_band}")
for name, value in classic.components.items():
    print(f"    - {name}: {value}")

print()
print("eSVD-2026 Score:")
print(f"  {extended.total} / {extended.max_score} — {extended.risk_band}")
for name, value in extended.components.items():
    print(f"    - {name}: {value}")

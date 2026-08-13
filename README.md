# eSVD-2026

**🌐 Languages: [English](#english) | [فارسی](README.fa.md)**

[![CI](https://github.com/sabi-karami/eSVD-2026/actions/workflows/ci.yml/badge.svg)](https://github.com/sabi-karami/eSVD-2026/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live calculator](https://img.shields.io/badge/live-calculator-4fb0ff)](https://sabi-karami.github.io/eSVD-2026/)

> An updated, evidence-based extension of the classic **Total SVD Score** (Staals et al., 2014) for cerebral small vessel disease — now with two modern imaging markers and a bilingual (EN/FA) web calculator.

---

## English

### What is eSVD-2026?

The **Total SVD Score** (Staals et al., 2014, *Neurology*) is a well-known 0–4 ordinal
scale that summarizes four MRI markers of cerebral small vessel disease (SVD):
lacunes, white matter hyperintensities (WMH), microbleeds, and enlarged perivascular
spaces (EPVS).

**eSVD-2026** extends it to a **0–6 scale** by adding two markers with strong evidence
accumulated since 2014:

| # | Marker | Status |
|---|---|---|
| 1 | Lacunes of presumed vascular origin | classic |
| 2 | White matter hyperintensities (Fazekas) | classic |
| 3 | Cerebral microbleeds | classic |
| 4 | Enlarged perivascular spaces (EPVS) | classic |
| 5 | **Cortical superficial siderosis (cSS)** | 🆕 new in eSVD-2026 |
| 6 | **Cortical atrophy (GCA ≥ 2)** | 🆕 new in eSVD-2026 |

Setting the two new markers to `False` reproduces the original Staals et al. (2014)
score exactly, so eSVD-2026 stays fully backward-compatible.

See [`docs/methodology.md`](docs/methodology.md) for the full rationale, literature
references, and operational point rules.

### 🔴 Live calculator (bilingual EN/FA)

**[https://sabi-karami.github.io/eSVD-2026/](https://sabi-karami.github.io/eSVD-2026/)**

A self-contained, no-backend web panel to enter MRI findings and get the score
instantly, switchable between Classic (0–4) and eSVD-2026 (0–6) modes, and fully
translated into **English** and **Persian (فارسی)** with automatic RTL layout — use the
language switch in the top-right corner.

### Installation

```bash
git clone https://github.com/sabi-karami/eSVD-2026.git
cd eSVD-2026
pip install -e .
```

### Python usage

```python
from esvd import SVDFindings, score_esvd, score_svd

findings = SVDFindings(
    lacunes=True,
    microbleeds=False,
    periventricular_fazekas=3,
    deep_fazekas=1,
    evps_basal_ganglia_grade=2,
    cortical_superficial_siderosis=True,
    global_cortical_atrophy_grade=2,
)

classic = score_svd(findings)      # backward-compatible 0-4 score
extended = score_esvd(findings)    # new 0-6 eSVD-2026 score

print(extended.total, extended.max_score, extended.risk_band)
print(extended.components)
```

### Command-line interface

```bash
esvd-score --lacunes --microbleeds \
  --pv-fazekas 3 --deep-fazekas 1 \
  --evps-grade 2 \
  --css --gca-grade 2
```

See [`examples/example_usage.py`](examples/example_usage.py) for more usage patterns.

### Repository layout

```
src/esvd/          Core Python package (score.py, cli.py)
tests/             Unit tests (pytest)
docs/              GitHub Pages site (index.html) + methodology notes
examples/          Usage examples
.github/workflows/ CI (GitHub Actions)
```

### Testing

```bash
pip install -e ".[dev]"
pytest -v
```

### Disclaimer

This project is for **research and educational purposes only**. It is **not** a
certified medical device and must **not** replace the judgement of a qualified
neuroradiologist or neurologist. Always correlate with the full clinical and
imaging context.

### Contributing

Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md)
([فارسی](CONTRIBUTING.fa.md)).

### License

[MIT](LICENSE)

### Citation

See [`CITATION.cff`](CITATION.cff).

---

📖 **راهنمای کامل فارسی این پروژه را اینجا بخوانید: [README.fa.md](README.fa.md)**

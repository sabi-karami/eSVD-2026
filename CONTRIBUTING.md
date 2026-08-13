# Contributing to eSVD-2026

Thanks for your interest in improving eSVD-2026! Contributions of all kinds are
welcome: bug reports, documentation improvements, new tests, and proposals for
methodological refinement.

## Getting started

```bash
git clone https://github.com/sabi-karami/eSVD-2026.git
cd eSVD-2026
pip install -e ".[dev]"
pytest -v
```

## Making a change

1. Open an issue describing the bug or proposed enhancement before starting
   significant work, so we can discuss the approach.
2. Create a branch from `main`.
3. Make your change, and add/update tests in `tests/test_score.py` to cover it.
4. Ensure `pytest -v` passes locally.
5. Open a pull request describing the change and its motivation. Link the
   relevant issue.

## Code style

- Keep functions small and documented (docstrings for public functions).
- Prefer explicit, validated inputs (see `SVDFindings.__post_init__`) over
  silent coercion.
- Cite literature in docstrings/comments when introducing or modifying a
  clinical scoring rule.

## Reporting issues

Please include:
- A clear description of the problem or proposal
- Steps to reproduce (for bugs), or references (for methodological proposals)
- Your Python version and OS, if relevant

## Code of conduct

Be respectful and constructive. This project supports research and clinical
education; please keep discussions professional and evidence-based.

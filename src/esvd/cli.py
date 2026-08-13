"""Command-line interface for the eSVD-2026 score.

Usage examples
--------------
    esvd --lacunes --microbleeds --pv-fazekas 3 --deep-fazekas 1 \\
         --evps-grade 2 --css --gca-grade 2

    esvd --lacunes --pv-fazekas 1 --deep-fazekas 0 --evps-grade 0 --json
"""

from __future__ import annotations

import argparse
import json
import sys

from .score import SVDFindings, score_esvd, score_svd, __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="esvd",
        description="Compute the classic Total SVD Score and the "
        "eSVD-2026 extended score from structured MRI findings.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--lacunes", action="store_true", help="Presence of >=1 lacune"
    )
    parser.add_argument(
        "--microbleeds", action="store_true", help="Presence of >=1 cerebral microbleed"
    )
    parser.add_argument(
        "--pv-fazekas",
        type=int,
        required=True,
        metavar="0-3",
        help="Periventricular Fazekas WMH grade (0-3)",
    )
    parser.add_argument(
        "--deep-fazekas",
        type=int,
        required=True,
        metavar="0-3",
        help="Deep white matter Fazekas grade (0-3)",
    )
    parser.add_argument(
        "--evps-grade",
        type=int,
        required=True,
        metavar="0-4",
        help="Basal ganglia enlarged perivascular spaces grade (0-4)",
    )
    parser.add_argument(
        "--css",
        action="store_true",
        help="Presence of cortical superficial siderosis (eSVD-2026 extension)",
    )
    parser.add_argument(
        "--gca-grade",
        type=int,
        default=0,
        metavar="0-3",
        help="Global Cortical Atrophy (GCA) grade (0-3, eSVD-2026 extension)",
    )
    parser.add_argument(
        "--classic-only",
        action="store_true",
        help="Only compute/print the classic 0-4 Total SVD Score",
    )
    parser.add_argument(
        "--json", action="store_true", help="Print machine-readable JSON output"
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        findings = SVDFindings(
            lacunes=args.lacunes,
            microbleeds=args.microbleeds,
            periventricular_fazekas=args.pv_fazekas,
            deep_fazekas=args.deep_fazekas,
            evps_basal_ganglia_grade=args.evps_grade,
            cortical_superficial_siderosis=args.css,
            global_cortical_atrophy_grade=args.gca_grade,
        )
    except (ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    classic = score_svd(findings)
    result = classic if args.classic_only else score_esvd(findings)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        label = "Total SVD Score" if args.classic_only else "eSVD-2026 Score"
        print(f"{label}: {result.total} / {result.max_score}")
        print(f"Risk band: {result.risk_band}")
        print("Components:")
        for name, value in result.components.items():
            print(f"  - {name.replace('_', ' ')}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

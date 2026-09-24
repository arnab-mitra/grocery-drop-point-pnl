"""
run_all.py — reproduce the entire project in one command.

    python src/run_all.py

Each stage is loaded by file path rather than by import, because the numbered
script names are not valid Python module names. They are numbered to make the
order of execution obvious to a reader, which matters more here than
importability.
"""

import importlib.util
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent

STAGES = [
    "01_market_sizing.py",
    "02_cost_model.py",
    "03_pnl_model.py",
    "04_sensitivity.py",
    "05_charts.py",
]


def run_stage(script: str) -> None:
    path = HERE / script
    spec = importlib.util.spec_from_file_location(script[:-3], path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.main()


def main() -> None:
    print(f"Project root: {HERE.parent}")
    for script in STAGES:
        print()
        print("=" * 90)
        print(f"  {script}")
        print("=" * 90)
        try:
            run_stage(script)
        except Exception:
            print(f"  FAILED in {script}", file=sys.stderr)
            traceback.print_exc()
            raise SystemExit(1)
    print()
    print("=" * 90)
    print("  All stages completed. See outputs/ for CSVs and outputs/charts/ for exhibits.")
    print("=" * 90)


if __name__ == "__main__":
    main()

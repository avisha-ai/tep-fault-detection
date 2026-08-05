from pathlib import Path

import pandas as pd
import pyreadr


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data"
FAULT_FREE_FILE = DATA_DIR / "TEP_FaultFree_Training.RData"
FAULTY_FILE = DATA_DIR / "TEP_Faulty_Training.RData"


def load_rdata(path: Path) -> pd.DataFrame:
    result = pyreadr.read_r(path)
    if len(result) != 1:
        raise ValueError(f"Expected exactly one object in {path.name}, found {len(result)}")
    return next(iter(result.values()))


def main() -> None:
    fault_free_df = load_rdata(FAULT_FREE_FILE)
    faulty_df = load_rdata(FAULTY_FILE)

    print("=== Fault-free dataset ===")
    print(f"Shape: {fault_free_df.shape}")
    print("Columns:")
    for col in fault_free_df.columns:
        print(f"- {col}")
    print("\nFirst 5 rows:")
    print(fault_free_df.head().to_string())

    print("\n=== Faulty dataset ===")
    print(f"Shape: {faulty_df.shape}")
    fault_counts = faulty_df["faultNumber"].nunique()
    print(f"Distinct fault types in 'faultNumber': {fault_counts}")


if __name__ == "__main__":
    main()

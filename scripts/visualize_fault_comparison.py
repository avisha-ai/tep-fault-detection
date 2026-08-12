from pathlib import Path

import matplotlib.pyplot as plt
import pyreadr

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data"
FIG_DIR = ROOT.parent / "figures"
FAULT_FREE_FILE = DATA_DIR / "TEP_FaultFree_Training.RData"
FAULTY_FILE = DATA_DIR / "TEP_Faulty_Training.RData"
OUTPUT_FILE = FIG_DIR / "fault6_xmeas_16.png"

SENSOR = "xmeas_16"
FAULT_NUMBER = 6
RUN_ID = 1
FAULT_ONSET = 20


def load_df(path: Path, key: str):
    result = pyreadr.read_r(path)
    return result[key]


if __name__ == "__main__":
    fault_free = load_df(FAULT_FREE_FILE, "fault_free_training")
    faulty = load_df(FAULTY_FILE, "faulty_training")

    healthy_run = fault_free[
        (fault_free["simulationRun"] == RUN_ID)
    ].sort_values("sample")
    fault_run = faulty[
        (faulty["faultNumber"] == FAULT_NUMBER)
        & (faulty["simulationRun"] == RUN_ID)
    ].sort_values("sample")

    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
    })

    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200, facecolor="white")
    ax.set_facecolor("white")

    ax.plot(
        healthy_run["sample"],
        healthy_run[SENSOR],
        color="#1f77b4",
        linewidth=1.6,
        label="Healthy operation",
    )
    ax.plot(
        fault_run["sample"],
        fault_run[SENSOR],
        color="#d62728",
        linewidth=1.6,
        label="Fault 6 (A-feed loss)",
    )

    ax.axvline(
        FAULT_ONSET,
        color="0.4",
        linestyle=(0, (5, 5)),
        linewidth=1.0,
    )

    ymax = max(healthy_run[SENSOR].max(), fault_run[SENSOR].max())
    ax.text(
        FAULT_ONSET + 1,
        ymax * 0.98,
        "fault onset",
        color="0.2",
        fontsize=10,
        va="top",
        ha="left",
    )

    ax.set_xlabel("Sample (3-min intervals)")
    ax.set_ylabel("Stripper Pressure (xmeas_16)")
    ax.legend(frameon=False, loc="best")
    ax.grid(False)
    ax.set_xlim(healthy_run["sample"].min(), healthy_run["sample"].max())

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_FILE,
        dpi=200,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )
    plt.close(fig)

    print(f"Saved plot to: {OUTPUT_FILE}")

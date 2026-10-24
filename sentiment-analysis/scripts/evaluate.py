"""Run: python -m scripts.evaluate. Writes measured outputs, figures and provenance."""
import csv
import hashlib
from importlib.metadata import version
import json
import platform
from datetime import datetime, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sentiment_lab.engine import THRESHOLD
from sentiment_lab.evaluation import DATASET, ROOT, evaluate, load_dataset, summary


def main():
    output = ROOT / "results"
    figures = ROOT / "reports" / "figures"
    output.mkdir(exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    rows = evaluate(load_dataset())
    report = summary(rows)
    (output / "predictions.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "comparison.csv").open("w", newline="", encoding="utf-8-sig") as target:
        writer = csv.DictWriter(target, fieldnames=[key for key in rows[0] if key != "textblob_assessments"])
        writer.writeheader()
        writer.writerows({k: v for k, v in row.items() if k != "textblob_assessments"} for row in rows)
    (output / "metrics.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "packages": {name: version(name) for name in ("vaderSentiment", "textblob", "streamlit", "pandas", "matplotlib")},
        "dataset_sha256": hashlib.sha256(DATASET.read_bytes()).hexdigest(),
        "sample_count": len(rows),
        "threshold": THRESHOLD,
        "textblob_threshold_origin": "project-defined symmetric cutoff, not an official TextBlob default",
        "preprocessing": "Outer whitespace stripping only; no translation or language adaptation",
        "labels": "Project-authored reference labels without independent annotation",
        "training": "None; distributed English lexicons and rules",
    }
    (output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)
    for ax, tool, title in zip(axes, ("vader", "textblob"), ("VADER", "TextBlob")):
        values = report["overall"][tool]
        matrix = values["confusion_matrix"]
        ax.imshow(matrix, cmap="Greens", vmin=0, vmax=max(max(row) for row in matrix))
        ax.set(xticks=range(3), yticks=range(3), xticklabels=values["labels"], yticklabels=values["labels"], xlabel="Predicted label", ylabel="Reference label", title=title)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, str(matrix[i][j]), ha="center", va="center", fontsize=17,
                        color="white" if matrix[i][j] > 4 else "#222e29")
    fig.savefig(figures / "confusion_matrices.png", dpi=190, facecolor="#faf9f5")
    plt.close(fig)

    groups = list(report["by_category"])
    fig, ax = plt.subplots(figsize=(9, 3.6), constrained_layout=True)
    positions = list(range(len(groups)))
    for offset, tool, label, color in [(-0.18, "vader", "VADER", "#23644e"), (0.18, "textblob", "TextBlob", "#a76b35")]:
        ax.bar([i + offset for i in positions], [report["by_category"][g][tool]["accuracy"] * 100 for g in groups],
               width=0.34, label=label, color=color)
    ax.set(xticks=positions, xticklabels=groups, ylim=(0, 115), ylabel="Accuracy (%)", title="Measured accuracy on six examples per category")
    ax.legend(frameon=False, ncols=2, loc="upper right")
    fig.savefig(figures / "category_accuracy.png", dpi=190, facecolor="#faf9f5")
    plt.close(fig)
    print(f"Evaluated {len(rows)} inputs; disagreements: {report['disagreements']}.")
    for tool, values in report["overall"].items():
        print(f"{tool}: accuracy={values['accuracy']:.4f}; macro F1={values['macro_f1']:.4f}")


if __name__ == "__main__":
    main()

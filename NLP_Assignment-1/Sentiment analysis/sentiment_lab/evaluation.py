"""Metrics computed against declared author-assigned reference labels."""
import csv
from pathlib import Path
from .engine import LABELS, analyze, validate_text

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "challenge_set.csv"
REQUIRED = {"id", "text", "gold_label", "category", "language", "meaning", "challenge"}


def load_dataset(path: Path = DATASET) -> list[dict]:
    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError(f"Required columns: {', '.join(sorted(REQUIRED))}")
        rows = list(reader)
    if not rows:
        raise ValueError("Dataset is empty.")
    ids = set()
    for row in rows:
        if not all(row.get(k, "").strip() for k in REQUIRED):
            raise ValueError("Dataset cells must not be empty.")
        if row["id"] in ids or row["gold_label"] not in LABELS:
            raise ValueError("IDs must be unique and labels negative, neutral or positive.")
        if validate_text(row["text"]) != row["text"]:
            raise ValueError("Dataset text must not have outer whitespace.")
        ids.add(row["id"])
    return rows


def evaluate(rows: list[dict]) -> list[dict]:
    results = []
    for row in rows:
        result = {**row, **analyze(row["text"])}
        for tool in ("vader", "textblob"):
            result[f"{tool}_correct"] = result[f"{tool}_label"] == row["gold_label"]
        results.append(result)
    return results


def metrics(results: list[dict], tool: str) -> dict:
    if tool not in ("vader", "textblob"):
        raise ValueError("Unknown tool.")
    matrix = [[0 for _ in LABELS] for _ in LABELS]
    for row in results:
        matrix[LABELS.index(row["gold_label"])][LABELS.index(row[f"{tool}_label"]) ] += 1
    per_class = {}
    for i, label in enumerate(LABELS):
        tp = matrix[i][i]
        support = sum(matrix[i])
        predicted = sum(r[i] for r in matrix)
        precision = tp / predicted if predicted else 0.0
        recall = tp / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[label] = dict(precision=precision, recall=recall, f1=f1, support=support)
    return {
        "n": len(results),
        "accuracy": sum(matrix[i][i] for i in range(3)) / len(results) if results else 0.0,
        "macro_f1": sum(v["f1"] for v in per_class.values()) / len(LABELS),
        "labels": list(LABELS),
        "confusion_matrix": matrix,
        "per_class": per_class,
    }


def summary(results: list[dict]) -> dict:
    groups = sorted({r["category"] for r in results})
    return {
        "overall": {tool: metrics(results, tool) for tool in ("vader", "textblob")},
        "by_category": {
            group: {tool: metrics([r for r in results if r["category"] == group], tool)
                    for tool in ("vader", "textblob")}
            for group in groups
        },
        "disagreements": sum(not r["tools_agree"] for r in results),
    }

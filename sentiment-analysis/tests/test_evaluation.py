import csv
import json
import pytest
from sentiment_lab.evaluation import ROOT, evaluate, load_dataset, metrics, summary


def test_confusion_matrix_and_macro_f1_on_hand_computed_fixture():
    rows = [
        {"gold_label": "negative", "vader_label": "negative"},
        {"gold_label": "positive", "vader_label": "neutral"},
        {"gold_label": "neutral", "vader_label": "neutral"},
        {"gold_label": "positive", "vader_label": "positive"},
    ]
    m = metrics(rows, "vader")
    assert m["confusion_matrix"] == [[1, 0, 0], [0, 1, 0], [0, 1, 1]]
    assert m["accuracy"] == 0.75
    assert m["macro_f1"] == pytest.approx(7 / 9)


def test_empty_metrics_and_unknown_tool():
    assert metrics([], "vader")["accuracy"] == 0
    with pytest.raises(ValueError):
        metrics([], "unknown")


def test_duplicate_ids_are_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    rows = load_dataset()[:1] * 2
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="unique"):
        load_dataset(path)


def test_committed_measurements_reproduce():
    rows = evaluate(load_dataset())
    assert len(rows) == 36
    assert summary(rows) == json.loads((ROOT / "results" / "metrics.json").read_text())
    assert rows == json.loads((ROOT / "results" / "predictions.json").read_text(encoding="utf-8"))

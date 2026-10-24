"""Evaluate the Hindi adapter separately from the unchanged two-tool benchmark."""
import hashlib
import json
from sentiment_lab.hindi import analyze_hindi
from sentiment_lab.evaluation import ROOT, load_dataset, metrics


def main():
    results = []
    for row in load_dataset():
        if row["category"] in ("Hindi", "Hinglish"):
            output = analyze_hindi(row["text"])
            results.append({**row, "hindi_label": output["label"], "hindi_score": output["score"], "matches": output["matches"]})
    # Reuse the same class order and metric implementation without altering the original predictions.
    score_rows = [{"gold_label": row["gold_label"], "vader_label": row["hindi_label"]} for row in results]
    payload = {
        "method": "Hindi lexicon + negation", "n": len(results), "metrics": metrics(score_rows, "vader"),
        "lexicon_sha256": hashlib.sha256((ROOT / "data/hindi_lexicon.json").read_bytes()).hexdigest(),
        "scope": "Illustrative checks on coursework examples whose vocabulary was available during adapter development; not an independent test set.",
        "predictions": results,
    }
    (ROOT / "results/hindi_adapter.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Hindi adapter: {payload['metrics']['accuracy']:.1%} on {len(results)} illustrative checks.")


if __name__ == "__main__":
    main()

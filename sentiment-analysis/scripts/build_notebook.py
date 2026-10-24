"""Create and execute the coursework notebook using the current environment."""
import nbformat as nbf
from nbclient import NotebookClient
from sentiment_lab.evaluation import ROOT


def main():
    md = nbf.v4.new_markdown_cell
    code = nbf.v4.new_code_cell
    notebook = nbf.v4.new_notebook(cells=[
        md("# Sentiment analysis in context\n\n**ANSARI JAFEERA JAMIL AHMED | UIN: 231A022 | Roll number: 03**\n\nNLP application study: compare VADER and TextBlob on the same 36 inputs, identify linguistic failures, and propose adaptation for Hindi.\n\nThis executed notebook records actual local inference. The examples and reference labels are project-authored with AI assistance, not a published benchmark or independently annotated corpus."),
        md("## Method\n\nBoth tools use their distributed English lexicons. Preserve original text, punctuation, case and script. The original comparison uses the packages' distributed lexicons and fixed thresholds, without translation. Positive is score >= 0.05; negative is score <= -0.05; otherwise neutral. The symmetric TextBlob threshold is a project choice. Scores and subjectivity are not confidence probabilities."),
        code("from pathlib import Path\nimport json\nimport pandas as pd\nfrom IPython.display import display, Image, Markdown\nfrom sentiment_lab.engine import analyze\nfrom sentiment_lab.evaluation import ROOT, load_dataset, evaluate, summary\n\nrows = load_dataset()\nresults = evaluate(rows)\nreport = summary(results)\npd.Series(sorted({r['gold_label'] for r in rows}), name='Reference label vocabulary')\nprint(f'{len(rows)} inputs; {len(report[\"by_category\"])} categories')\ndisplay(pd.Series([r['gold_label'] for r in rows]).value_counts().rename('Reference support'))"),
        md("## Try the tools with identical input\n\nThe second sentence is Hindi praise meaning 'This phone is very good.' A neutral prediction is an error against its positive reference label."),
        code("for text in ['I love this phone. The camera is excellent!', 'यह फोन बहुत अच्छा है।']:\n    output = analyze(text)\n    print(json.dumps(output, ensure_ascii=False, indent=2))"),
        md("## All measured predictions\n\nReference labels express the intended reading. See the meaning and challenge columns for annotation decisions."),
        code("frame = pd.DataFrame(results)\nwith pd.option_context('display.max_rows', 50, 'display.max_colwidth', 100):\n    display(frame[['id', 'text', 'gold_label', 'vader_label', 'vader_compound', 'textblob_label', 'textblob_polarity']])"),
        md("## Aggregate comparison\n\nAccuracy is the fraction of labels matching the references. Macro F1 is the arithmetic mean of negative, neutral and positive F1, with undefined values set to zero. The overall scores describe this deliberately difficult, small set. An always-negative predictor scores 17/36 = 47.2%."),
        code("display(pd.DataFrame({tool: {'n': m['n'], 'accuracy': m['accuracy'], 'macro_f1': m['macro_f1']} for tool, m in report['overall'].items()}).T)\nprint('Different labels:', report['disagreements'])\ndisplay(pd.DataFrame([{ 'category': cat, 'n': values['vader']['n'], 'vader_accuracy': values['vader']['accuracy'], 'textblob_accuracy': values['textblob']['accuracy']} for cat, values in report['by_category'].items()]))"),
        code("for tool in ['vader', 'textblob']:\n    m = report['overall'][tool]\n    print(tool, 'confusion matrix: reference rows, predicted columns')\n    display(pd.DataFrame(m['confusion_matrix'], index=m['labels'], columns=m['labels']))\ndisplay(Image(filename=str(ROOT / 'reports/figures/confusion_matrices.png')))"),
        md("## Errors and cultural context\n\nSA03 has a floating-point threshold effect: TextBlob returns 0.04999999999999999, which is below 0.05 even though it displays as 0.0500. Labels use full precision. Either label misses the negative reference.\n\nBoth tools succeed on straightforward English and these negation cases. Both miss all sarcastic complaints. 'Paisa vasool' and 'third class' expose regional expression gaps. Every Hindi and Hinglish input returns neutral, including praise and criticism. Correct neutral predictions for factual Hindi do not prove language comprehension. VADER's positive output for the neutral Diwali schedule is consistent with an English holiday-word association; the output alone does not establish a causal cultural misunderstanding."),
        code("errors = frame[~(frame.vader_correct & frame.textblob_correct)]\ndisplay(errors[['id', 'text', 'gold_label', 'vader_label', 'textblob_label', 'challenge']])\ndisplay(frame[~frame.tools_agree][['id','text','vader_label','textblob_label']])"),
        md("## Implemented Hindi adapter and extension plan\n\nThe original VADER/TextBlob comparison remains unchanged. The updated app adds a separate Hindi dictionary with negation and intensity rules."),
        code("from sentiment_lab.hindi import analyze_hindi\nfor text in ['यह सामान बहुत खराब है।', 'यह फोन अच्छा नहीं है।', 'Camera bahut badhiya hai']:\n    print(json.dumps(analyze_hindi(text), ensure_ascii=False, indent=2))\ndisplay(Markdown((ROOT / 'docs/hindi_adaptation.md').read_text(encoding='utf-8')))"),
        md("## Limits and reproduction\n\nThe 36 examples have no independent annotators; native-speaker review is pending. NG04 can reasonably be neutral; mixed-aspect NG05 and NG06 use an overall-label convention. Sarcasm has only negative references. No random sampling, external validation or broad ranking of tools is claimed.\n\nRun `python -m scripts.evaluate` before this notebook to reproduce CSV, JSON and figures. `results/provenance.json` records versions and the dataset SHA-256.\n\nSources: [VADER](https://github.com/cjhutto/vaderSentiment), [TextBlob](https://textblob.readthedocs.io/en/stable/quickstart.html#sentiment-analysis), [IndicBERT](https://indicnlp.ai4bharat.org/pages/indic-bert/), [IndicXlit](https://github.com/AI4Bharat/IndicXlit), [IndicTrans2](https://github.com/AI4Bharat/IndicTrans2)."),
    ])
    notebook.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    NotebookClient(notebook, timeout=120, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}}).execute()
    path = ROOT / "Sentiment_analysis_experiment.ipynb"
    nbf.write(notebook, path)
    print(f"Executed {sum(c.cell_type == 'code' for c in notebook.cells)} notebook cells: {path.name}")


if __name__ == "__main__":
    main()

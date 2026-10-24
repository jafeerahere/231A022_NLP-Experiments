# Natural Language Processing experiments and sentiment analysis

**Rizvi College of Engineering**

Department of Artificial Intelligence & Data Science

| Student | Details |
|---|---|
| Name | ANSARI JAFEERA JAMIL AHMED |
| UIN | 231A022 |
| Roll number | 03 |
| Subject | Natural Language Processing |

This repository contains the NLP experiment notebooks and a sentiment analysis application for English, Hindi and Hinglish product reviews and social posts.

## Sentiment analysis project

The Streamlit application compares VADER and TextBlob on the same 36 inputs. A separate Hindi/Hinglish adapter recognizes sentiment words, negation and intensity. The submission includes measured results, confusion matrices, an executed notebook, screenshots and a report with the college name and logo.

- [Read the project report](sentiment-analysis/reports/sentiment_analysis_report.pdf)
- [Open the executed project notebook](sentiment-analysis/Sentiment_analysis_experiment.ipynb)
- [Read the project documentation](sentiment-analysis/README.md)
- [Inspect all input/output comparisons](sentiment-analysis/results/comparison.csv)
- [Read the Hindi implementation and extension plan](sentiment-analysis/docs/hindi_adaptation.md)

### What the app does

| View | Function |
|---|---|
| Try the tools | Analyze custom text or a supplied example; inspect scores and matched words |
| Compare 36 inputs | Compare the original VADER/TextBlob outputs, filter errors and inspect confusion matrices |
| Hindi sentiment | Explain the implemented Hindi dictionary, negation rules and language resources |
| Project & report | View assignment coverage and download the PDF |

English inputs use VADER and TextBlob. Automatic language routing selects the Hindi adapter for Hindi/Hinglish inputs, and a language selector allows manual selection. For example, `यह सामान बहुत खराब है।` receives a negative Hindi score of `-0.7579`.

### Run locally

Use Python 3.12. From a terminal:

```bash
git clone https://github.com/jafeerahere/231A022_NLP-Experiments.git
cd 231A022_NLP-Experiments/sentiment-analysis
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

On macOS or Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Open [the local application](http://127.0.0.1:8501). Run the command from `sentiment-analysis` so Streamlit loads the project theme. Sentiment inference runs locally and needs no API key.

### Results and verification

| Original tool comparison | Correct inputs | Accuracy | Macro F1 |
|---|---:|---:|---:|
| VADER | 18/36 | 50.0% | 0.498 |
| TextBlob, PatternAnalyzer | 20/36 | 55.6% | 0.555 |

The original comparison includes English, negation, sarcasm, Indian English, Hindi and Hinglish examples. The separate Hindi adapter passes all 12 illustrative Hindi/Hinglish checks. These examples were available during dictionary development; the results describe this coursework set rather than general accuracy. See [dataset notes](sentiment-analysis/data/README.md) and [measured Hindi outputs](sentiment-analysis/results/hindi_adapter.json).

The project has 33 automated checks. To reproduce the results and documents, install `requirements-dev.txt` and follow the [verification commands](sentiment-analysis/README.md#reproduce-and-verify). The [GitHub Actions workflow](.github/workflows/sentiment-analysis.yml) runs the test suite on Python 3.12.

![Hindi sentiment result](sentiment-analysis/reports/screenshots/06_hindi_adapter.png)

## NLP experiment notebooks

| Experiment | Notebook or document |
|---|---|
| 1 | [Notebook](AIDS_Sem7_NLP_Experiment01.ipynb) · [Experiment documentation](AIDS_Sem7_NLP_Experiment01/README.md) |
| 2 | [Notebook](AIDS_NLP_Experiments2.ipynb) |
| 3 | [Notebook](AIDS_Sem7_NLP_Experiment03.ipynb) |
| 4 | [Notebook](AIDS_Sem7_NLP_Experiment04.ipynb) |
| 5 | [Notebook](AIDS_SEM7_NLP_EXPERIMENT5.ipynb) |
| 6 | [Notebook](AIDS_SEM7_NLP_EXPERIMENT06_ipynb.ipynb) |
| 7 | [Part 1](AIDS_Sem7_NLP_Experiment07_Part1.ipynb) · [Part 2](AIDS_Sem7_NLP_Experiment07_Part2.ipynb) |
| 8 | [Notebook](AIDS_Sem7_NLP_Experiment08.ipynb) |
| 9 | [Notebook](AIDS_Sem7_NLP_Experiment09.ipynb) |
| 10 | [Notebook](AIDS_Sem7_NLP_Experiment10.ipynb) |

The original experiment files are retained. The sentiment analysis application and its submission materials are under [`sentiment-analysis/`](sentiment-analysis/README.md).

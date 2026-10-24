"""Build PDF and Markdown from measured results and actual UI captures."""
from html import escape
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

from sentiment_lab.evaluation import ROOT

GREEN = colors.HexColor("#23644e")
INK = colors.HexColor("#222e29")
MUTED = colors.HexColor("#617064")
CREAM = colors.HexColor("#faf9f5")
WIDTH = A4[0] - 88


def md_table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"] +
                     ["| " + " | ".join(str(x).replace("|", "/") for x in row) + " |" for row in rows])


def main():
    out = ROOT / "reports"
    rows = json.loads((ROOT / "results/predictions.json").read_text(encoding="utf-8"))
    metrics = json.loads((ROOT / "results/metrics.json").read_text())
    provenance = json.loads((ROOT / "results/provenance.json").read_text())
    cases = {row["id"]: row for row in rows}
    differing = [r for r in rows if not r["tools_agree"]]
    scores = [["VADER", "18/36", "50.0%", "0.498"], ["TextBlob", "20/36", "55.6%", "0.555"]]
    category_rows = [[cat, values["vader"]["n"], f"{values['vader']['accuracy']:.1%}", f"{values['textblob']['accuracy']:.1%}"]
                     for cat, values in metrics["by_category"].items()]
    diff_rows = [[r["id"], r["text"], r["gold_label"], f"{r['vader_label']} / {r['vader_compound']:+.4f}",
                  f"{r['textblob_label']} / {r['textblob_polarity']:+.4f}"] for r in differing]
    source_links = [
        ("VADER implementation, paper and scoring", "https://github.com/cjhutto/vaderSentiment"),
        ("TextBlob sentiment and API documentation", "https://textblob.readthedocs.io/en/stable/quickstart.html#sentiment-analysis"),
        ("AI4Bharat IndicBERT", "https://indicnlp.ai4bharat.org/pages/indic-bert/"),
        ("AI4Bharat IndicXlit", "https://github.com/AI4Bharat/IndicXlit"),
        ("AI4Bharat IndicTrans2", "https://github.com/AI4Bharat/IndicTrans2"),
    ]
    overview = "This study tests sentiment analysis for product feedback and social posts using two existing tools, VADER and TextBlob. It compares their actual local outputs on the same 36 project-authored inputs and implements a separate Hindi/Hinglish lexicon adapter. The original tools succeed on simple English cases but miss sarcastic complaints and Hindi sentiment. The adapter adds Hindi vocabulary, negation and intensity rules."
    method = "The two tools receive the original text field, with no translation, transliteration, spelling correction, lowercasing or stopword removal. Only outer whitespace is stripped for custom inputs. VADER uses its distributed lexicon and rules; TextBlob uses its default English PatternAnalyzer. The original comparison uses the distributed package versions and declared fixed thresholds."
    thresholds = "Positive means score >= +0.05, negative means score <= -0.05, and neutral falls between. The cutoffs follow VADER's documented recommendation. Applying the same cutoffs to TextBlob is an explicit project choice. VADER compound and TextBlob polarity have different scoring semantics, so their magnitudes are not directly calibrated. Subjectivity is not certainty; token sentiment proportions are not class probabilities."
    dataset_note = "The set contains six inputs in each of English, Negation, Sarcasm, Indian English, Hinglish and Hindi. Its reference distribution is 17 negative, 8 neutral and 11 positive. Examples and intended labels were prepared with AI assistance before inference, without independent annotation or native-speaker validation. The set deliberately stresses failure modes and is not representative of social-media traffic."
    success = "Both tools correctly label all six straightforward English inputs and all six negation examples under the declared references. For EN01, 'I love this phone. The camera is excellent!', VADER returns positive at +0.8478 and TextBlob returns positive at +0.7500. Preserving words such as 'not' allows both tools to label NG01, 'This phone is not good.', negative."
    regional = "Both tools return neutral for IN01, 'The food was simply paisa vasool.', although the intended reading is positive value for money. Both return neutral for IN03, 'The service is third class.', although the regional judgement is negative. IN02 includes 'I enjoyed it', and both tools succeed; that success alone does not demonstrate that they understood 'timepass'."
    sarcasm = "Both tools miss all six sarcastic complaints. SA01 says 'Great! The app crashed again and deleted my work.' The intended negative judgement conflicts with the surface praise. The observed outputs show a pragmatic/context error. They do not establish that either tool can infer the speaker's intent from isolated positive words."
    hindi = "All six Hindi inputs and all six Hinglish inputs receive neutral from both tools. Four references in each group are positive or negative, so each tool gets only the two factual inputs right, or 2/6. Correct factual labels here do not show Hindi comprehension. DV01 means 'This phone is very good.' Both scores are zero despite the positive reference. HI04, 'Product accha nahi hai.', means the product is not good, yet both tools return neutral."
    uncertainty = "NG04, 'I do not hate this movie.', has a weak-positive reference, but a neutral reading is defensible. NG05 and NG06 contain mixed aspects and use the final product-related clause for the overall label. Sarcasm references are all negative. These annotation choices limit interpretation. The results were not used to revise labels or remove examples."
    interpretation = "TextBlob gets two more inputs correct on this set. Both exceed an always-negative baseline of 17/36, or 47.2%, by a small margin. Four output labels differ. This is a descriptive classroom experiment; the sample size and construction do not support a general ranking of the tools. Accuracy is correct labels divided by inputs. Macro F1 averages the three class F1 values, with undefined values set to zero."

    md = ["# RIZVI COLLEGE OF ENGINEERING", "## Department of Artificial Intelligence & Data Science", "![Rizvi College of Engineering logo](assets/rizvi_logo.png)", "## Project report: Sentiment analysis", "Natural Language Processing (CSDO7011)", "**ANSARI JAFEERA JAMIL AHMED | UIN: 231A022 | Roll number: 03**\n\nNLP application study | 24 October 2026", "## Aim and scope", overview,
          "The report covers all requirements visible in the uploaded assignment: a real tool trial with input/output snapshots, a same-input comparison of two tools, an error matrix, cultural/regional analysis, and a Hindi adaptation proposal addressing linguistic resources and socio-linguistic challenges. The supplied image ends after the socio-linguistic subpart; unseen continuation text was not available.",
          "## Tools, inputs and procedure", method, thresholds, dataset_note, "See [all inputs and meanings](../data/challenge_set.csv) and [annotation notes](../data/README.md).",
          "## Tool trial and snapshots", success, "![EN01 input](screenshots/01_english_input.png)", "![Actual EN01 output](screenshots/02_english_output.png)",
          "## Measured comparison", md_table(["Tool", "Correct", "Accuracy", "Macro F1"], scores), interpretation,
          md_table(["Category", "Inputs", "VADER accuracy", "TextBlob accuracy"], category_rows),
          "![Measured confusion matrices](figures/confusion_matrices.png)", "Matrix rows are reference labels; columns are predictions, ordered negative, neutral, positive.",
          "## Every disagreement", md_table(["ID", "Unchanged input", "Reference", "VADER / score", "TextBlob / score"], diff_rows),
          "SA03 and SA04 are sarcasm/context errors for both tools, although their incorrect labels differ. SA03 also has a floating-point boundary effect: the raw TextBlob polarity is 0.04999999999999999, just below 0.05. It is classified neutral using full precision, despite displaying as 0.0500 after rounding. Treat that disagreement cautiously. IN04 is a domain-vocabulary error for VADER. IN06 is a false positive for a factual Diwali schedule. A holiday-word association is a plausible explanation for IN06; the output by itself does not prove cultural reasoning or its cause.",
          "## Successes, errors and regional context", success, sarcasm, regional, hindi,
          "Translation errors were not measured because no translation system was used. None of these examples diagnoses grammatical parsing by itself. The observed errors concern lexical coverage, idioms, pragmatics and context.",
          "![Original Hindi input DV01](screenshots/03_hindi_input.png)", "![Actual DV01 neutral predictions](screenshots/04_hindi_output.png)",
          "## Hindi implementation and extension plan", (ROOT / "docs/hindi_adaptation.md").read_text(encoding="utf-8"),
          "## Limitations", uncertainty, "The demonstration uses synthetic examples rather than scraped Twitter/Facebook data. It is a working application of existing NLP tools, a comparison of distributed English tools plus a local Hindi lexicon adapter. Scores should not be reported as confidence percentages.",
          "## Reproduce the work", "```bash\npython -m pip install -r requirements-dev.txt\npython -m scripts.evaluate\npython -m pytest -q\npython -m scripts.build_notebook\npython -m scripts.build_report\npython -m streamlit run app.py\n```",
          f"Python {provenance['python']}; VADER {provenance['packages']['vaderSentiment']}; TextBlob {provenance['packages']['textblob']}. Actual run time in UTC: {provenance['run_at_utc']}. Dataset SHA-256: `{provenance['dataset_sha256']}`.",
          "The CSV and predictions JSON preserve every output. Screenshots are actual captures from the running app. The notebook was executed, not populated with invented results. Implementation, illustrative data and documentation were prepared with AI assistance.",
          "## Sources", "\n".join(f"- [{label}]({url})" for label, url in source_links), "Sources consulted 24 October 2026."]
    (out / "report.md").write_text("\n\n".join(md) + "\n", encoding="utf-8")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BodyLab", fontName="Helvetica", fontSize=10, leading=14, textColor=INK, spaceAfter=9))
    styles.add(ParagraphStyle(name="SmallLab", fontName="Helvetica", fontSize=8, leading=10.5, textColor=MUTED, spaceAfter=7))
    styles.add(ParagraphStyle(name="LabelLab", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=GREEN, spaceAfter=14))
    styles.add(ParagraphStyle(name="TitleLab", fontName="Times-Bold", fontSize=32, leading=35, textColor=GREEN, spaceAfter=17))
    styles.add(ParagraphStyle(name="HeadingLab", fontName="Times-Bold", fontSize=22, leading=26, textColor=GREEN, spaceAfter=13))
    styles.add(ParagraphStyle(name="SubLab", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=7, spaceAfter=8))
    styles.add(ParagraphStyle(name="CellLab", fontName="Helvetica", fontSize=8.2, leading=11, textColor=INK))
    styles.add(ParagraphStyle(name="CollegeCover", fontName="Times-Bold", fontSize=22.5, leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#b91f23"), spaceAfter=4))
    styles.add(ParagraphStyle(name="DepartmentCover", fontName="Helvetica-Bold", fontSize=11.5, leading=17, alignment=TA_CENTER, textColor=colors.HexColor("#203b69"), spaceAfter=12))
    styles.add(ParagraphStyle(name="TitleCover", fontName="Helvetica-Bold", fontSize=25, leading=32, alignment=TA_CENTER, textColor=INK, spaceAfter=8))
    styles.add(ParagraphStyle(name="LabelCover", fontName="Helvetica-Bold", fontSize=11, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#203b69"), spaceAfter=10))
    styles.add(ParagraphStyle(name="MetaCover", fontName="Times-Roman", fontSize=12, leading=19, alignment=TA_CENTER, textColor=INK, spaceAfter=7))
    styles.add(ParagraphStyle(name="NameCover", fontName="Helvetica-Bold", fontSize=12, leading=19, alignment=TA_CENTER, textColor=INK, spaceAfter=7))
    story = []

    def p(text, kind="BodyLab"):
        return Paragraph(escape(str(text)).replace("\n", "<br/>"), styles[kind])

    def add(text, kind="BodyLab"):
        story.append(p(text, kind))

    def heading(number, title):
        add(f"NLP APPLICATION STUDY / {number:02d}", "LabelLab")
        add(title, "HeadingLab")

    def table(headers, data, widths):
        grid = [[p(x, "CellLab") for x in row] for row in [headers] + data]
        tab = Table(grid, colWidths=widths, repeatRows=1, hAlign="LEFT")
        tab.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5eee7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, 0), 0.7, GREEN),
            ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#d7ddd4")),
        ]))
        story.extend([tab, Spacer(1, 12)])

    def image(name, width):
        path = out / name
        from PIL import Image as PILImage
        with PILImage.open(path) as source:
            w, h = source.size
        return Image(str(path), width=width, height=width * h / w)

    def screenshot_pair(a, b):
        images = Table([[image(f"screenshots/{a}", 239), image(f"screenshots/{b}", 239)]], colWidths=[WIDTH / 2] * 2)
        images.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOX", (0, 0), (0, 0), 0.5, colors.HexColor("#d7ddd4")), ("BOX", (1, 0), (1, 0), 0.5, colors.HexColor("#d7ddd4"))]))
        story.append(images)
        story.append(Spacer(1, 10))

    # Institutional cover, styled after the supplied reference.
    story.append(Spacer(1, 8))
    add("RIZVI COLLEGE OF ENGINEERING", "CollegeCover")
    add("Department of Artificial Intelligence & Data Science", "DepartmentCover")
    story.append(Spacer(1, 14))
    story.append(image("assets/rizvi_logo.png", 94))
    story.append(Spacer(1, 31))
    add("PROJECT REPORT", "LabelCover")
    add("Sentiment analysis", "TitleCover")
    add("VADER, TextBlob and Hindi/Hinglish sentiment", "MetaCover")
    story.append(Spacer(1, 18))
    add("Natural Language Processing (CSDO7011)", "MetaCover")
    story.append(Spacer(1, 68))
    add("Submitted by", "MetaCover")
    add("ANSARI JAFEERA JAMIL AHMED", "NameCover")
    add("UIN: 231A022", "MetaCover")
    add("Roll number: 03", "MetaCover")
    story.append(Spacer(1, 31))
    add("24 October 2026", "MetaCover")
    story.append(PageBreak())

    # Study purpose, method and design.
    add("NLP APPLICATION STUDY / 231A022", "LabelLab")
    add("Sentiment analysis\nin context", "TitleLab")
    add("ANSARI JAFEERA JAMIL AHMED", "SubLab")
    add("UIN: 231A022 | Roll number: 03 | 24 October 2026", "SmallLab")
    add(overview)
    table(["Application", "Implemented study"], [["Product and social-post sentiment", "VADER + TextBlob; 36 unchanged test inputs"], ["Indian language", "Hindi/Hinglish dictionary, negation rules and an extension plan"]], [180, WIDTH - 180])
    add("How the experiment was run", "SubLab")
    add(method)
    add(thresholds)
    add("Input design", "SubLab")
    add(dataset_note)
    add("Scope follows the visible assignment image, which ends after the socio-linguistic challenges subpart. No unseen continuation was available.", "SmallLab")
    story.append(PageBreak())

    # Page 2: direct evidence of the existing tools in use.
    heading(2, "One input, two real tool responses")
    add("Requirement i: data supplied, observed response and success/failure analysis.", "SmallLab")
    add(success)
    screenshot_pair("01_english_input.png", "02_english_output.png")
    add("Figure 1. Actual app captures: EN01 entered in the interface, then both tool responses. The same sentence was passed to both packages.", "SmallLab")
    table(["Input ID", "Tool response", "Interpretation"], [["EN01", "VADER positive, +0.8478", "Matches the positive reference."], ["EN01", "TextBlob positive, +0.7500", "Matches the positive reference."], ["NG01", "Both negative for 'not good'", "Negation is handled in this example."]], [60, 210, WIDTH - 270])
    add("A successful English example establishes that inference runs and that the tools can recognize explicit praise. It does not establish accuracy on sarcasm, unfamiliar idioms or another language.")
    story.append(PageBreak())

    # Page 3: quantitative comparison.
    heading(3, "Measured comparison on 36 inputs")
    add("Requirement ii: same inputs in two tools and a comparison/error matrix.", "SmallLab")
    table(["Tool", "Correct", "Accuracy", "Macro F1"], scores, [160, 110, 115, WIDTH - 385])
    add(interpretation)
    table(["Category", "n", "VADER accuracy", "TextBlob accuracy"], category_rows, [170, 40, 145, WIDTH - 355])
    story.append(image("figures/confusion_matrices.png", WIDTH))
    add("Figure 2. Confusion matrices from the actual predictions. Rows are references; columns are predictions. Class order is negative, neutral, positive. All 36 observations are counted for each tool.", "SmallLab")
    add("Full-precision scores and all input IDs are preserved in results/comparison.csv and results/predictions.json.", "SmallLab")
    story.append(PageBreak())

    # Page 4: concrete disagreements and error interpretation.
    heading(4, "Output differences and error types")
    add("All four disagreements are shown below. A different output is not automatically a correct output.")
    table(["ID and unchanged input", "Reference", "VADER / score", "TextBlob / score"],
          [[f"{r['id']}\n{r['text']}", r['gold_label'], f"{r['vader_label']}\n{r['vader_compound']:+.4f}", f"{r['textblob_label']}\n{r['textblob_polarity']:+.4f}"] for r in differing],
          [238, 67, 100, WIDTH - 405])
    add("Scores above are rounded. SA03's raw TextBlob polarity is 0.04999999999999999, just below 0.05. Full-precision classification is neutral although the display reads 0.0500. This disagreement includes a floating-point boundary effect.", "SmallLab")
    add("Semantic and pragmatic errors", "SubLab")
    add(sarcasm)
    add("SA03 and SA04 have positive VADER outputs and neutral TextBlob outputs; both are incorrect against their negative references. This is context loss rather than a measured translation error.")
    add("Cultural and regional expressions", "SubLab")
    add(regional)
    add("IN04 is a negative restaurant complaint. TextBlob labels it negative while VADER labels it neutral. IN06 is a factual Diwali schedule; TextBlob labels it neutral while VADER labels it positive. An English holiday-word association is a plausible explanation, but the output alone does not prove the cause.")
    add("No translation system or grammatical parser was evaluated, so the study does not claim measured translation or grammar errors. The evidence supports vocabulary, idiom, pragmatics and context failures.", "SmallLab")
    story.append(PageBreak())

    # Page 5: Hindi and Hinglish evidence, with native script in real screenshots.
    heading(5, "Hindi and Hinglish expose the gap")
    add(hindi)
    screenshot_pair("03_hindi_input.png", "04_hindi_output.png")
    add("Figure 3. Actual DV01 input and observed neutral outputs. The native-script sentence is praise. Both tools return zero; agreement is not correctness.", "SmallLab")
    table(["Failure type", "Concrete evidence"], [["Script and vocabulary coverage", "DV01 and DV03 express opposite sentiment in Hindi; both tools return neutral for each."], ["Romanization and code-switching", "HI04, 'Product accha nahi hai.', includes Hindi negation over a product opinion. Both tools return neutral."], ["False appearance of success", "The two factual inputs in each group are correctly neutral, despite identical zero outputs on the opinion inputs."]], [150, WIDTH - 150])
    add("These observations motivate Hindi adaptation. The current app adds the Hindi adapter documented on the next page, while preserving these original tool measurements.")
    story.append(PageBreak())

    # Updated app: separately labeled Hindi adapter, preserving the original comparison.
    heading(6, "Hindi sentiment in the updated app")
    add("Hindi and Hinglish inputs now use a project-authored sentiment dictionary with negation and intensity rules. The original English tools remain available in a collapsed comparison panel.")
    story.append(image("screenshots/06_hindi_adapter.png", 265))
    story.append(Spacer(1, 12))
    add("Figure 4. Current app response to the supplied Hindi complaint: negative at -0.7579. The matched term is kharab, strengthened by bahut.", "SmallLab")
    add("The adapter sums matched word valences and normalizes the sum s as s / sqrt(s*s + 15). Nearby negation reverses a term with a 0.74 factor, while intensity words multiply its strength by 1.5. Hindi spelling variants and common Romanized forms share dictionary entries. Mixed-language English words use VADER's word lexicon.")
    add("All 12 coursework Hindi/Hinglish checks pass. Their vocabulary was available during development, so this is an illustrative check rather than an independent accuracy estimate. The full rules and measurements are stored in sentiment_lab/hindi.py and results/hindi_adapter.json.")
    story.append(PageBreak())

    # Extension resources and socio-linguistics.
    heading(7, "Extending the tool for Hindi")
    add("Requirement iii: linguistic resources and socio-linguistic challenges. The app implements a Hindi sentiment dictionary with negation and intensity rules; the steps below describe further extension.", "SmallLab")
    table(["Resource", "Specific use"], [
        ["Labeled Hindi/Hinglish corpus", "Collect a proposed 3,000-review pilot: 1,000 Devanagari, 1,000 Romanized Hindi and 1,000 mixed-language reviews."],
        ["Hindi sentiment lexicon", "Native-speaker valence ratings and negation rules as an interpretable baseline."],
        ["IndicBERT and Hindi corpora", "Fine-tune a pretrained encoder with sentiment labels. Pretraining alone is not sentiment classification."],
        ["Unicode tokenization and language ID", "Preserve Hindi/English tokens, emoji and negation. Optional Hindi POS/dependency tagging helps inspect scope errors."],
        ["IndicXlit; optional IndicTrans2", "Compare transliteration and translation as separate pipelines while retaining original input and checking meaning loss."],
    ], [160, WIDTH - 160])
    add("Implementation and evaluation steps", "SubLab")
    add("1. Collect consented reviews across products, delivery, food and social posts. Remove identifying information and group duplicates or shared conversations.")
    add("2. Have two Hindi speakers independently label each example. A third adjudicates disagreements. Record sarcasm, mixed aspects and regional phrases; measure agreement before adjudication.")
    add("3. Normalize Unicode to NFC while retaining negation, emoji, punctuation and repeated letters. Store original and normalized text. Cover accha/achha/acha and nahi/nahin variants.")
    add("4. Split grouped data into 70% training, 15% validation and 15% test with script/domain balance. Fine-tune using training data and select settings using validation only. Keep the 36 demonstration examples out of training.")
    add("5. Compare a Hindi lexicon baseline and fine-tuned encoder on the same untouched test IDs. Report macro F1, per-class recall, confusion matrices, subgroup sizes and confidence intervals by script, dialect, domain and code-switching level.")
    add("Regional Hindi varieties, politeness, sarcasm and code-switching need speaker/context coverage. Avoid treating Latin script as proof of English. Mixed-aspect reviews may need aspect labels or human review. Add abstention only after validation; no improvement numbers are claimed.")
    story.append(PageBreak())

    # Page 7: limitations, reproduction and sources.
    heading(8, "Limits, evidence and reproduction")
    add(uncertainty)
    add("The app uses synthetic examples rather than scraped Twitter or Facebook data. It combines the original two-tool study with an implemented Hindi sentiment dictionary and negation rules. The Hindi checks use illustrative vocabulary available during development; broader validation requires a new corpus.")
    add("Reproduce the project", "SubLab")
    add("Use Python 3.12 in the sentiment-analysis directory. Install requirements-dev.txt, then run these commands:")
    for command in ["python -m scripts.evaluate", "python -m scripts.evaluate_hindi", "python -m pytest -q", "python -m scripts.build_notebook", "python -m scripts.build_report", "python -m streamlit run app.py"]:
        add(command, "SmallLab")
    add(f"Verified runtime: Python {provenance['python']}, VADER {provenance['packages']['vaderSentiment']}, TextBlob {provenance['packages']['textblob']}. The provenance JSON records the UTC run time, package versions, threshold and dataset SHA-256.")
    add("Submission evidence", "SubLab")
    add("The executed notebook contains actual tool outputs. The CSV contains all 36 paired predictions, reference labels and challenge notes. The app supplies input/output JSON downloads, filters and error matrices. Actual screenshots are stored in reports/screenshots. The full Hindi resource and socio-linguistic plan is in docs/hindi_adaptation.md.")
    add("Implementation, illustrative examples and documentation were prepared with AI assistance. Reported measurements were produced by the named tools; screenshots came from the running application.", "SmallLab")
    add("Sources consulted 24 October 2026", "SubLab")
    for label, url in source_links:
        story.append(Paragraph(f'<a href="{escape(url, quote=True)}" color="#23644e">{escape(label)}</a><br/>{escape(url)}', styles["SmallLab"]))

    def chrome(canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(colors.white if doc.page == 1 else CREAM)
        canvas.rect(0, 0, w, h, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor("#d7ddd4"))
        if doc.page != 1:
            canvas.line(44, h - 30, w - 44, h - 30)
        canvas.line(44, 35, w - 44, 35)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        if doc.page != 1:
            canvas.drawString(44, h - 23, "RIZVI COLLEGE OF ENGINEERING")
            canvas.drawRightString(w - 44, h - 23, "231A022 / SENTIMENT ANALYSIS")
        canvas.drawString(44, 22, "ANSARI JAFEERA JAMIL AHMED | NLP application study")
        canvas.drawRightString(w - 44, 22, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(str(out / "sentiment_analysis_report.pdf"), pagesize=A4, leftMargin=44, rightMargin=44,
                            topMargin=49, bottomMargin=49, title="Sentiment analysis in context | 231A022",
                            author="ANSARI JAFEERA JAMIL AHMED", subject="VADER and TextBlob comparison; Hindi adaptation proposal")
    doc.build(story, onFirstPage=chrome, onLaterPages=chrome)
    print("Built reports/report.md and reports/sentiment_analysis_report.pdf")


if __name__ == "__main__":
    main()

import streamlit as st
from sentiment_lab.evaluation import ROOT

st.caption("04 / SUBMISSION GUIDE")
st.title("The project behind the scores.")
st.markdown("**ANSARI JAFEERA JAMIL AHMED · UIN: 231A022 · Roll number: 03**\n\nAssigned NLP application: sentiment analysis of social posts and product feedback.")
st.markdown("| Visible assignment requirement | Evidence in this project |\n|---|---|\n| Try one real-world NLP tool | Live VADER and TextBlob inference |\n| Inputs and responses with snapshots | Report and actual app screenshots |\n| Successes and failures | Full labeled comparisons and error case analysis |\n| Same inputs in at least two tools | 36 unchanged inputs processed by both tools |\n| Output differences and error matrix | Comparison CSV, accuracy, macro F1 and confusion matrices |\n| Indian cultural or regional issues | Paisa vasool, third class, Diwali, Hindi and Hinglish cases |\n| Adapt to one Indian language | Hindi dictionary and negation rules, plus resources for extension |\n| Socio-linguistic challenges | Code-switching, dialects and script variation |")
st.subheader("Reproduce the experiment")
st.code("python -m pip install -r requirements-dev.txt\npython -m scripts.evaluate\npython -m scripts.evaluate_hindi\npython -m pytest -q\npython -m streamlit run app.py", language="bash")
st.markdown("The executed notebook is `Sentiment_analysis_experiment.ipynb`. The Markdown report and PDF explain the method, measured outcomes and proposed adaptation. The CSV preserves all 36 reference labels and their intended meanings.")
pdf = ROOT / "reports" / "sentiment_analysis_report.pdf"
if pdf.exists():
    st.download_button("Download the assignment report", pdf.read_bytes(), pdf.name, "application/pdf", icon=":material/download:")
st.subheader("Tools and sources")
st.markdown("- [VADER source and scoring documentation](https://github.com/cjhutto/vaderSentiment)\n- [TextBlob sentiment documentation](https://textblob.readthedocs.io/en/stable/quickstart.html#sentiment-analysis)\n- [AI4Bharat IndicBERT](https://indicnlp.ai4bharat.org/pages/indic-bert/)\n- [IndicXlit transliteration](https://github.com/AI4Bharat/IndicXlit)\n- [IndicTrans2 translation](https://github.com/AI4Bharat/IndicTrans2)")
st.caption("Assignment scope follows the visible uploaded images. The last image ends after the socio-linguistic challenges subpart; any additional unseen subparts are outside this evidence.")

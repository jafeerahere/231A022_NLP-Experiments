import json
import pandas as pd
import streamlit as st
from sentiment_lab.engine import MAX_TEXT_LENGTH, analyze
from sentiment_lab.hindi import analyze_hindi, looks_hindi
from sentiment_lab.evaluation import load_dataset
from sentiment_lab.ui import score_chart


def english_results(result):
    left, right = st.columns(2, border=True)
    with left:
        st.caption("TOOL 01 / VADER")
        st.metric(result["vader_label"].capitalize(), f"{result['vader_compound']:+.4f}", help="Compound sentiment on a -1 to +1 scale.")
        st.caption("Lexicon + rules for social text")
        st.markdown(f"Positive {result['vader_positive']:.3f} · Neutral {result['vader_neutral']:.3f} · Negative {result['vader_negative']:.3f}")
    with right:
        st.caption("TOOL 02 / TEXTBLOB")
        st.metric(result["textblob_label"].capitalize(), f"{result['textblob_polarity']:+.4f}", help="PatternAnalyzer polarity on a -1 to +1 scale.")
        st.caption("PatternAnalyzer English sentiment")
        st.markdown(f"Subjectivity {result['textblob_subjectivity']:.3f}")
    score_chart(result)


st.caption("01 / INTERACTIVE EXPERIMENT")
st.title("Sentiment, in context.")
st.markdown("Analyze English, Hindi and Hinglish reviews, then explore the words behind each score.")
samples = {row["id"]: row for row in load_dataset()}
selected = st.selectbox("Choose a test input", list(samples),
    format_func=lambda key: f"{key} · {samples[key]['category']} · {samples[key]['text']}", key="sample")
sample = samples[selected]
with st.form("analysis", border=True):
    text = st.text_area("Your review or social post", value=sample["text"], height=110,
                        max_chars=MAX_TEXT_LENGTH, key=f"input_{selected}")
    language = st.segmented_control("Analysis language", ["Automatic", "English", "Hindi / Hinglish"], default="Automatic", key="analysis_language")
    st.caption("Local analysis · No API key required")
    submitted = st.form_submit_button("Analyze sentiment", type="primary", icon=":material/compare_arrows:")

if submitted or "analysis_result" not in st.session_state:
    try:
        result = analyze(text)
        use_hindi = language == "Hindi / Hinglish" or (language == "Automatic" and looks_hindi(text))
        if use_hindi:
            result["hindi"] = analyze_hindi(text)
        st.session_state["analysis_result"] = result
    except ValueError as exc:
        st.session_state.pop("analysis_result", None)
        st.error(str(exc))

result = st.session_state.get("analysis_result")
if result:
    st.subheader("Sentiment result")
    st.caption(f"Analyzed input: {result['text']}")
    if result["text"] != text.strip():
        st.caption("Press Analyze sentiment to update the result for your current input.")
    if "hindi" in result:
        hindi = result["hindi"]
        with st.container(border=True):
            st.caption("HINDI / HINGLISH · LEXICON + NEGATION")
            st.metric(hindi["label"].capitalize(), f"{hindi['score']:+.4f}")
            if hindi["matches"]:
                st.markdown("Matched words: " + ", ".join(f"**{m['token']}**" for m in hindi["matches"]))
                details = []
                if any(m["intensified"] for m in hindi["matches"]):
                    details.append("Intensity words strengthen the sentiment.")
                if any(m["negated"] for m in hindi["matches"]):
                    details.append("Negation reverses the affected sentiment words.")
                if details:
                    st.caption(" ".join(details))
            else:
                st.caption("No sentiment words matched in this input.")
        with st.expander("Compare original English tools"):
            english_results(result)
    else:
        english_results(result)
    if result["text"] == sample["text"]:
        st.caption(f"Expected sentiment: {sample['gold_label']} · {sample['meaning']}")
    with st.expander("Score details"):
        if "hindi" in result and result["hindi"]["matches"]:
            st.dataframe(pd.DataFrame(result["hindi"]["matches"]), hide_index=True, alt="Matched sentiment words and negation adjustments")
        st.json(result)
    st.download_button("Download this result", json.dumps(result, ensure_ascii=False, indent=2),
                       "sentiment_result.json", "application/json", icon=":material/download:")

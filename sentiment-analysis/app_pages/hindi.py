import streamlit as st
from sentiment_lab.evaluation import ROOT

st.caption("03 / INDIAN LANGUAGE ADAPTATION")
st.title("Sentiment analysis for Hindi.")
st.markdown("Hindi and Hinglish inputs use a local sentiment dictionary with negation and intensity rules. Explore the implementation and the steps for extending its coverage.")
st.markdown((ROOT / "docs" / "hindi_adaptation.md").read_text(encoding="utf-8"))

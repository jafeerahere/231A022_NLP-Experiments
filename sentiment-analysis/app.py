"""Run from this folder with: python -m streamlit run app.py."""
import streamlit as st

st.set_page_config(page_title="Sentiment lab | 231A022", page_icon=":material/forum:", layout="wide")

with st.sidebar:
    st.title("Sentiment lab")
    st.caption("NLP APPLICATION STUDY / 231A022")
    st.divider()

page = st.navigation([
    st.Page("app_pages/explorer.py", title="Try the tools", icon=":material/chat_bubble:", default=True),
    st.Page("app_pages/benchmark.py", title="Compare 36 inputs", icon=":material/analytics:", url_path="benchmark"),
    st.Page("app_pages/hindi.py", title="Hindi sentiment", icon=":material/translate:", url_path="hindi"),
    st.Page("app_pages/guide.py", title="Project & report", icon=":material/article:", url_path="guide"),
])
with st.sidebar:
    st.divider()
    st.markdown("Two tools. The same words.\n\nExplore where sentiment scores match the meaning, and where they miss it.")
    st.caption("ANSARI JAFEERA JAMIL AHMED\n\nVADER + TextBlob · Local inference")
page.run()

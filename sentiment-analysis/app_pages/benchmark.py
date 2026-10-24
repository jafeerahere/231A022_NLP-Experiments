import json
import altair as alt
import pandas as pd
import streamlit as st
from sentiment_lab.evaluation import metrics
from sentiment_lab.ui import confusion_chart, get_benchmark

st.caption("02 / CONTROLLED COMPARISON")
st.title("Same inputs. Different readings.")
st.markdown("36 project-authored examples across six categories. Every input runs through both tools without translation.")
results, report = get_benchmark()
v, t = report["overall"]["vader"], report["overall"]["textblob"]
with st.container(horizontal=True):
    st.metric("VADER accuracy", f"{v['accuracy']:.1%}", border=True)
    st.metric("TextBlob accuracy", f"{t['accuracy']:.1%}", border=True)
    st.metric("Different labels", f"{report['disagreements']} / {len(results)}", border=True)
    st.metric("Test categories", "6", border=True)
st.caption(f"Overall macro F1: VADER {v['macro_f1']:.3f} · TextBlob {t['macro_f1']:.3f}. These are challenge-set results, not population performance estimates.")

chart_rows = [{"Category": cat, "Tool": tool, "Accuracy": values[tool]["accuracy"]}
              for cat, values in report["by_category"].items() for tool in ("vader", "textblob")]
chart = alt.Chart(pd.DataFrame(chart_rows)).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
    x=alt.X("Category:N", axis=alt.Axis(labelAngle=0)), y=alt.Y("Accuracy:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format="%")),
    xOffset="Tool:N", color=alt.Color("Tool:N", scale=alt.Scale(range=["#a76b35", "#23644e"])),
    tooltip=["Category", "Tool", alt.Tooltip("Accuracy:Q", format=".1%")],
).properties(height=240)
st.altair_chart(chart, alt="Accuracy for each of the six challenge categories, comparing the two tools")

st.subheader("Inspect the evidence")
a, b, c = st.columns([2, 2, 3])
category = a.selectbox("Category", ["All categories"] + sorted(report["by_category"]), key="category")
view = b.selectbox("Show", ["All inputs", "Any tool incorrect", "Tools disagree"], key="view")
search = c.text_input("Search the input text", key="search")
filtered = [r for r in results if (category == "All categories" or r["category"] == category)
            and search.casefold() in r["text"].casefold()
            and (view == "All inputs" or (view == "Any tool incorrect" and not (r["vader_correct"] and r["textblob_correct"]))
                 or (view == "Tools disagree" and not r["tools_agree"]))]
columns = ["id", "text", "gold_label", "vader_label", "vader_compound", "textblob_label", "textblob_polarity", "challenge"]
st.caption(f"Showing {len(filtered)} of {len(results)} inputs. Metrics above always describe the complete test set.")
st.caption("Scores are rounded for display. SA03's raw TextBlob polarity is 0.04999999999999999, below 0.05, so its label is neutral even though the displayed score rounds to 0.0500.")
if filtered:
    st.dataframe(pd.DataFrame(filtered)[columns], hide_index=True, height=320,
                 column_config={"text": st.column_config.TextColumn("Input", width="large"),
                                "vader_compound": st.column_config.NumberColumn("VADER score", format="%.4f"),
                                "textblob_polarity": st.column_config.NumberColumn("TextBlob score", format="%.4f")},
                 alt="Filtered inputs with reference labels, both measured predictions and error challenges")
else:
    st.info("No inputs match these filters.")

st.subheader("Where predictions went")
st.caption("These matrices use all 36 inputs. Rows are reference labels; columns are predicted labels.")
for col, tool in zip(st.columns(2), ("vader", "textblob")):
    with col:
        st.markdown(f"**{'VADER' if tool == 'vader' else 'TextBlob'}**")
        m = metrics(results, tool)
        st.altair_chart(confusion_chart(m["confusion_matrix"], m["labels"]), alt=f"Full dataset confusion matrix for {tool}")

with st.expander("How to interpret this comparison"):
    st.markdown("The reference labels describe intended overall sentiment. They were authored for this project and have not had independent native-speaker validation. Sarcasm, mixed aspects and negated dislike can admit different readings.\n\nAccuracy is correct predictions divided by inputs. Macro F1 averages F1 across negative, neutral and positive. A class with zero support or zero predictions receives zero F1 in our implementation.\n\nThe comparison uses the distributed package lexicons and the declared fixed thresholds. The set intentionally includes failure cases and has 17 negative, 8 neutral and 11 positive labels. A majority-negative predictor would score 47.2% accuracy.")
with st.container(horizontal=True):
    st.download_button("Download all comparisons", pd.DataFrame(results).drop(columns="textblob_assessments").to_csv(index=False).encode("utf-8-sig"), "comparison.csv", "text/csv")
    st.download_button("Download metrics", json.dumps(report, indent=2), "metrics.json", "application/json")

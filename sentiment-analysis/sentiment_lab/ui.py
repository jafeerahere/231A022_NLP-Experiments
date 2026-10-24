"""Shared presentation helpers; NLP and metrics remain independent of Streamlit."""
import altair as alt
import pandas as pd
import streamlit as st
from .evaluation import DATASET, evaluate, load_dataset, summary


@st.cache_data(max_entries=4, show_spinner=False)
def benchmark_data(dataset_mtime: int) -> tuple[list[dict], dict]:
    results = evaluate(load_dataset())
    return results, summary(results)


def get_benchmark():
    return benchmark_data(DATASET.stat().st_mtime_ns)


def score_chart(result: dict):
    data = pd.DataFrame([
        {"Tool": "VADER", "Score": result["vader_compound"]},
        {"Tool": "TextBlob", "Score": result["textblob_polarity"]},
    ])
    chart = alt.Chart(data).mark_bar(cornerRadius=4, size=30).encode(
        x=alt.X("Score:Q", scale=alt.Scale(domain=[-1, 1]), title="Sentiment score, -1 to +1"),
        y=alt.Y("Tool:N", sort=["VADER", "TextBlob"], title=None),
        color=alt.Color("Tool:N", scale=alt.Scale(domain=["VADER", "TextBlob"], range=["#23644e", "#a76b35"]), legend=None),
        tooltip=["Tool", alt.Tooltip("Score:Q", format=".4f")],
    ).properties(height=130)
    st.altair_chart(chart, alt="VADER compound and TextBlob polarity on their native minus one to one scales")


def confusion_chart(matrix: list[list[int]], labels: list[str]):
    cells = pd.DataFrame([
        {"Reference": labels[i], "Predicted": labels[j], "Count": count}
        for i, row in enumerate(matrix) for j, count in enumerate(row)
    ])
    base = alt.Chart(cells).encode(
        x=alt.X("Predicted:N", sort=labels), y=alt.Y("Reference:N", sort=labels),
        tooltip=["Reference", "Predicted", "Count"],
    )
    tiles = base.mark_rect().encode(color=alt.Color("Count:Q", scale=alt.Scale(scheme="greens"), legend=None))
    numbers = base.mark_text(fontSize=20).encode(
        text="Count:Q", color=alt.condition(alt.datum.Count >= max(1, cells.Count.max() / 2), alt.value("white"), alt.value("#222e29"))
    )
    return (tiles + numbers).properties(height=240)

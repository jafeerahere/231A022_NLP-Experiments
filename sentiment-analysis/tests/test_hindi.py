import pytest
from sentiment_lab.hindi import analyze_hindi, looks_hindi


@pytest.mark.parametrize("text,label", [
    ("यह सामान बहुत खराब है।", "negative"),
    ("यह फिल्म बहुत अच्छी है।", "positive"),
    ("मुझे यह सेवा पसंद नहीं आई।", "negative"),
    ("यह खराब नहीं है।", "positive"),
    ("Product achha nahi hai", "negative"),
    ("Camera bahut badhiya hai", "positive"),
    ("Delivery bekar thi", "negative"),
    ("Kal phone kharida", "neutral"),
    ("पार्सल मंगलवार को आया।", "neutral"),
    ("Product accha nahi hai lekin camera zabardast hai", "positive"),
])
def test_hindi_meanings_and_negation(text, label):
    assert analyze_hindi(text)["label"] == label


def test_intensifier_strengthens_negative_score():
    assert analyze_hindi("यह बहुत खराब है")["score"] < analyze_hindi("यह खराब है")["score"] < 0


def test_hindi_auto_routing_and_english_fallback():
    assert looks_hindi("यह सामान खराब है")
    assert looks_hindi("Product achha hai")
    assert not looks_hindi("The camera is excellent")


def test_original_text_and_explanation_are_preserved():
    text = "यह सामान बहुत खराब है।"
    result = analyze_hindi(text)
    assert result["text"] == text
    assert result["matches"][0]["token"] == "खराब"
    assert result["matches"][0]["intensified"]
    assert -1 <= result["score"] < 0

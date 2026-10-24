from streamlit.testing.v1 import AppTest
from sentiment_lab.evaluation import ROOT


def test_user_can_analyze_custom_text_and_reject_blank_input():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()
    assert not app.exception
    app.text_area[0].set_value("I hate this terrible product.")
    app.form_submit_button[0].click().run()
    assert not app.exception
    assert app.session_state["analysis_result"]["vader_label"] == "negative"
    assert app.session_state["analysis_result"]["textblob_label"] == "negative"
    app.text_area[0].set_value("   ")
    app.form_submit_button[0].click().run()
    assert not app.exception
    assert app.error
    assert "analysis_result" not in app.session_state


def test_hindi_input_shows_scored_hindi_result_and_clean_copy():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()
    app.text_area[0].set_value("यह सामान बहुत खराब है।")
    app.form_submit_button[0].click().run()
    assert not app.exception
    assert app.session_state["analysis_result"]["hindi"]["label"] == "negative"
    assert app.session_state["analysis_result"]["hindi"]["score"] < -0.5
    assert app.metric[0].label == "Negative"
    copy = " ".join(e.value for e in app.markdown) + " ".join(e.value for e in app.info)
    assert "Agreement alone" not in copy
    assert "not trained" not in copy


def test_benchmark_filters_and_other_pages():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()
    app.switch_page("app_pages/benchmark.py").run()
    assert not app.exception
    app.selectbox(key="category").select("Hindi").run()
    assert not app.exception
    assert len(app.dataframe[0].value) == 6
    app.selectbox(key="view").select("Any tool incorrect").run()
    assert len(app.dataframe[0].value) == 4
    app.text_input(key="search").set_value("no such input").run()
    assert not app.exception
    assert len(app.dataframe) == 0
    for page in ("hindi", "guide"):
        app.switch_page(f"app_pages/{page}.py").run()
        assert not app.exception

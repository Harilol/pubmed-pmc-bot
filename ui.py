import time
from typing import Any, Dict, Optional

import streamlit as st
from dotenv import load_dotenv

from bot import fetch_full_papers, fetch_papers, shi


load_dotenv()

st.set_page_config(page_title="DD Research Bot", layout="wide")

DB_OPTIONS = {
    "Auto route": "auto",
    "PubMed abstracts": "pubmed",
    "PMC full text": "pmc",
}


if "previous_runs" not in st.session_state:
    st.session_state.previous_runs = []

if "run_cache" not in st.session_state:
    st.session_state.run_cache = {}

if "current_run_key" not in st.session_state:
    st.session_state.current_run_key = None


def run_research_agent(query: str, max_results: int, db_choice: str) -> Optional[Dict[str, Any]]:
    progress = st.progress(0)
    status = st.empty()
    started_at = time.perf_counter()

    try:
        status.info("Preparing research agents...")
        progress.progress(20)

        status.info("Routing query and fetching papers...")
        result = shi.invoke(
            {
                "query": query,
                "max_results": max_results,
                "db_choice": db_choice,
            }
        )
        progress.progress(85)

        elapsed = time.perf_counter() - started_at
        selected_db = result.get("db_choice", db_choice)
        progress.progress(100)
        status.success("Research run complete.")

        return {
            "query": query,
            "max_results": max_results,
            "db_choice": selected_db,
            "final": result.get("final", "No answer returned by the agent."),
            "raw_results": result.get("raw_results", ""),
            "elapsed": elapsed,
        }
    except Exception as exc:
        status.empty()
        progress.empty()
        st.error(f"Research agent failed: {exc}")
        return None


def save_run(result: Dict[str, Any]) -> str:
    cache_key = f"{result['query']}::{result['max_results']}::{result['db_choice']}::{time.time()}"
    st.session_state.run_cache[cache_key] = result
    st.session_state.previous_runs.append(
        {
            "key": cache_key,
            "query": result["query"],
            "db_choice": result["db_choice"],
            "max_results": result["max_results"],
        }
    )
    st.session_state.current_run_key = cache_key
    return cache_key


def build_history_sidebar() -> None:
    st.sidebar.header("Previous Runs")

    if st.sidebar.button("Clear history", use_container_width=True):
        st.session_state.previous_runs = []
        st.session_state.run_cache = {}
        st.session_state.current_run_key = None
        st.rerun()

    if not st.session_state.previous_runs:
        st.sidebar.info("No runs yet.")
        return

    for entry in reversed(st.session_state.previous_runs):
        label = f"{entry['query']} | {entry['db_choice']} | {entry['max_results']}"
        if st.sidebar.button(label, key=f"history_{entry['key']}", use_container_width=True):
            st.session_state.current_run_key = entry["key"]
            st.rerun()


def get_current_result() -> Optional[Dict[str, Any]]:
    current_key = st.session_state.get("current_run_key")
    if not current_key:
        return None
    return st.session_state.run_cache.get(current_key)


def render_agent_route(db_choice: str) -> None:
    db_label = "PMC full-text agent" if db_choice == "pmc" else "PubMed abstract agent"
    st.caption(f"Selected route: {db_label}")


def render_result(result: Dict[str, Any]) -> None:
    st.subheader("Agent Answer")
    render_agent_route(result["db_choice"])
    st.markdown(result["final"])

    metrics = st.columns(3)
    metrics[0].metric("Database", result["db_choice"].upper())
    metrics[1].metric("Max results", result["max_results"])
    metrics[2].metric("Processing time", f"{result['elapsed']:.1f}s")

    st.download_button(
        "Download answer",
        data=result["final"],
        file_name="dd_research_answer.md",
        mime="text/markdown",
    )

    with st.expander("Raw fetched research", expanded=False):
        if result.get("raw_results"):
            st.code(result["raw_results"])
        else:
            st.info("No raw research text was returned.")


def render_tool_preview(query: str, max_results: int, db_choice: str) -> None:
    if not query.strip():
        st.warning("Enter a query before previewing raw tool output.")
        return

    with st.spinner("Fetching raw tool output..."):
        try:
            if db_choice == "pmc":
                raw_text = fetch_full_papers.invoke({"query": query, "max_results": max_results})
            else:
                raw_text = fetch_papers.invoke({"query": query, "max_results": max_results})
            st.code(raw_text)
        except Exception as exc:
            st.error(f"Tool preview failed: {exc}")


def main() -> None:
    st.title("DD Research Bot")
    st.write("Search biomedical research with a supervisor agent that routes queries to PubMed abstracts or PMC full-text articles.")

    build_history_sidebar()

    with st.form(key="research_form"):
        query = st.text_area(
            "Research query",
            value="COVID-19 vaccine efficacy",
            height=90,
        )
        form_cols = st.columns([2, 1])
        with form_cols[0]:
            route_label = st.segmented_control(
                "Database route",
                options=list(DB_OPTIONS.keys()),
                default="Auto route",
            )
        with form_cols[1]:
            max_results = st.slider("Max papers", min_value=1, max_value=20, value=5)

        submitted = st.form_submit_button("Run research agent", use_container_width=True)

    db_choice = DB_OPTIONS[route_label]

    preview_col, clear_col = st.columns([1, 3])
    with preview_col:
        preview_raw = st.button("Preview raw tool", use_container_width=True)
    with clear_col:
        st.caption("Use preview to inspect PubMed or PMC output before running the summarizing agent.")

    if preview_raw:
        preview_db = "pubmed" if db_choice == "auto" else db_choice
        render_tool_preview(query, max_results, preview_db)

    if not submitted:
        current_result = get_current_result()
        if current_result:
            st.success(f"Loaded previous run: {current_result['query']}")
            render_result(current_result)
        else:
            st.info("Enter a query, choose a route, and run the research agent.")
        return

    if not query.strip():
        st.error("Please enter a research query.")
        return

    result = run_research_agent(query.strip(), max_results, db_choice)
    if result:
        save_run(result)
        st.rerun()


if __name__ == "__main__":
    main()

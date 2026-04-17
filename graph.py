from typing import TypedDict

import pandas as pd
from agents.drivers import analyse_drivers
from agents.summary import generate_summary
from agents.anomaly import detect_anomalies
from langgraph.graph import StateGraph, START, END



class FinState(TypedDict, total=False):
    long_df: pd.DataFrame        
    wide_df: pd.DataFrame        
    category_cols: list[str]
    detection: dict              
    findings: dict               
    summary: str              


def node_detect(state: FinState) -> FinState:
    detection = detect_anomalies(state["long_df"], value_col="value")
    return {"detection": detection}

def node_drivers(state: FinState) -> FinState:
    enriched = analyse_drivers(
        state["wide_df"],
        state["detection"]["anomalies"],
        state["category_cols"],
    )
    findings = {**state["detection"], "anomalies": enriched}
    return {"findings": findings}

def node_generate_summary(state: FinState) -> FinState:
    return {"summary": generate_summary(state["findings"])}

def build_graph():
    g = StateGraph(FinState)
    g.add_node("detect", node_detect)
    g.add_node("drivers", node_drivers)
    g.add_node("generate_summary", node_generate_summary)

    g.add_edge(START, "detect")
    g.add_edge("detect", "drivers")
    g.add_edge("drivers", "generate_summary")
    g.add_edge("generate_summary", END)
    return g.compile()

GRAPH = build_graph()


def run_pipeline(long_df: pd.DataFrame, wide_df: pd.DataFrame,
                 category_cols: list[str]) -> dict:
    result = GRAPH.invoke({
        "long_df": long_df,
        "wide_df": wide_df,
        "category_cols": category_cols,
    })
    return {
        "detection": result["detection"],
        "findings": result["findings"],
        "summary": result["summary"],
    }

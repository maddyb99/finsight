from typing import TypedDict

import pandas as pd
from langgraph.graph import StateGraph, START, END

from agents.anomaly import detect_anomalies


class FinState(TypedDict, total=False):
    long_df: pd.DataFrame        
    wide_df: pd.DataFrame        
    category_cols: list[str]
    detection: dict              
    findings: dict               
    commentary: str              


def node_detect(state: FinState) -> FinState:
    detection = detect_anomalies(state["long_df"], value_col="value")
    return {"detection": detection}



def build_graph():
    g = StateGraph(FinState)
    g.add_node("detect", node_detect)

    g.add_edge(START, "detect")
    g.add_edge("detect", END)
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
    }

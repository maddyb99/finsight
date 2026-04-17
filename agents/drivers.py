import pandas as pd

def analyse_drivers(wide_df: pd.DataFrame, anomalies: list[dict],
                    category_cols: list[str]) -> list[dict]:
    enriched = []
    for a in anomalies:
        idx = a["index"]
        if idx == 0:
            a = {**a, "drivers": [], "note": "First period; no prior to compare."}
            enriched.append(a)
            continue

        cur = wide_df.loc[idx, category_cols]
        prev = wide_df.loc[idx - 1, category_cols]
        delta = (cur - prev)
        total_delta = delta.sum()

        drivers = []
        for cat in category_cols:
            d = float(delta[cat])
            share = (d / total_delta * 100) if total_delta != 0 else 0.0
            drivers.append({
                "category": cat,
                "prev": round(float(prev[cat]), 2),
                "current": round(float(cur[cat]), 2),
                "delta": round(d, 2),
                "contribution_pct": round(share, 1),
            })

        drivers.sort(key=lambda d: abs(d["delta"]), reverse=True)
        enriched.append({**a, "drivers": drivers[:3],
                         "total_delta": round(float(total_delta), 2)})
    return enriched

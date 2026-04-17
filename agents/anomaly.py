import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def _robust_z(series: pd.Series) -> pd.Series:
    med = series.median()
    mad = (series - med).abs().median()
    if mad == 0:
        mad = series.std() or 1.0
    return 0.6745 * (series - med) / mad


def detect_anomalies(df: pd.DataFrame, value_col: str = "value",
                     contamination: float = 0.12) -> dict:
    work = df.copy().reset_index(drop=True)
    values = work[value_col].astype(float)

    pct_change = values.pct_change().fillna(0.0)
    rolling_mean = values.rolling(3, min_periods=1).mean()
    dev_from_trend = (values - rolling_mean) / rolling_mean.replace(0, np.nan)
    dev_from_trend = dev_from_trend.fillna(0.0)

    features = np.column_stack([
        values.values,
        pct_change.values,
        dev_from_trend.values,
    ])

    iso = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=200,
    )
    iso_pred = iso.fit_predict(features)
    iso_score = -iso.score_samples(features)

    z = _robust_z(pct_change)

    anomalies = []
    for i in range(len(work)):
        is_iso = iso_pred[i] == -1
        is_z = abs(z.iloc[i]) >= 3.0
        if is_iso or is_z:
            anomalies.append({
                "period": str(work.loc[i, "period"]),
                "value": round(float(values.iloc[i]), 2),
                "pct_change": round(float(pct_change.iloc[i]) * 100, 1),
                "iso_score": round(float(iso_score[i]), 3),
                "z_score": round(float(z.iloc[i]), 2),
                "flagged_by": [m for m, ok in
                               (("isolation_forest", is_iso), ("z_score", is_z))
                               if ok],
                "index": i,
            })

    anomalies.sort(key=lambda a: a["iso_score"], reverse=True)
    return {
        "n_periods": len(work),
        "n_anomalies": len(anomalies),
        "anomalies": anomalies,
        "method": "IsolationForest (primary) + robust z-score (secondary)",
    }

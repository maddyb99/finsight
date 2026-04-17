import pandas as pd

def to_frames(csv_df: pd.DataFrame):
    category_cols = sorted(csv_df["category"].unique().tolist())
    wide = (csv_df.pivot_table(index="period", columns="category",
                               values="value", aggfunc="sum")
            .reset_index())
    wide.columns.name = None
    wide = wide.sort_values("period").reset_index(drop=True)

    long_df = (csv_df.groupby("period", as_index=False)["value"].sum()
               .sort_values("period").reset_index(drop=True))
    return long_df, wide, category_cols


def load_csv(file_storage=None) -> pd.DataFrame:
    if file_storage is not None:
        tidy = pd.read_csv(file_storage)
        expected = {"period", "category", "value"}
        if not expected.issubset(tidy.columns):
            raise ValueError(f"CSV must have columns {expected}, got {set(tidy.columns)}")
        return tidy
    else:
        raise ValueError("No file provided")
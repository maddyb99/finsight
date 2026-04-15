import pandas as pd

def load_csv(file_storage=None) -> pd.DataFrame:
    if file_storage is not None:
        tidy = pd.read_csv(file_storage)
        expected = {"period", "category", "value"}
        if not expected.issubset(tidy.columns):
            raise ValueError(f"CSV must have columns {expected}, got {set(tidy.columns)}")
        print(tidy)
        return tidy
    else:
        raise ValueError("No file provided")
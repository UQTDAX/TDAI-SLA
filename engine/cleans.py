
import pandas as pd

from sklearn.preprocessing import StandardScaler

def build_feature_matrix(cleaned_file_path: str, normalized_file_path: str):
    try:
        # Read as text so label columns are saved back exactly as they were
        df = pd.read_csv(cleaned_file_path, dtype=str, keep_default_na=False)

        kpi_cols = [f"kpi_{i}_val" for i in range(1, 17)]

        # Handle nulls: impute with the column median, as dropping would lose the whole suburb
        df[kpi_cols] = df[kpi_cols].apply(pd.to_numeric)
        df[kpi_cols] = df[kpi_cols].fillna(df[kpi_cols].median())

        # Standardise so 0-1 and 0-100 KPIs contribute fairly
        scaler = StandardScaler()
        X = scaler.fit_transform(df[kpi_cols])

        df[kpi_cols] = X
        df.to_csv(normalized_file_path, index=False)

    except Exception as e:
        print(f"Failed to build feature matrix from {cleaned_file_path}: {e}")
        raise
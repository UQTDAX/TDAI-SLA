import os
import csv
import sys

from dotenv import load_dotenv

from db.bigquery_client import get_client
from engine.cleans import build_feature_matrix

load_dotenv()

def load_bigquery_data(query: str):
    try:
        client = get_client(os.environ["BIGQUERY_PROJECT"])
        results = client.query(query).result()
        return results
    except Exception as e:
        print(f"Failed to load data from BigQuery: {e}")
        raise

def save_bigquery_data_as_csv(results, file_path: str):
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([field.name for field in results.schema])  # header row
            for row in results:
                writer.writerow(row.values())
    except Exception as e:
        print(f"Failed to save BigQuery data to {file_path}: {e}")
        raise

def normalize_data_csv(cleaned_file_path: str, standardised_file_path: str):
    try:
        build_feature_matrix(cleaned_file_path, standardised_file_path)        
    except Exception as e:
        print(f"Failed to normalize data from {cleaned_file_path}: {e}")
        raise

def main():
    query = """
    SELECT  * 
    FROM `demografy.prod_tables.a_master_view`
    WHERE population != 0
    """
    try:        
        file_path = os.environ["BIGQUERY_DATA_FILE"]
        # cleaned_file_path = os.environ["CLEANED_DATA_FILE"]
        normalized_file_path = os.environ["NORMALIZED_DATA_FILE"]

        results = load_bigquery_data(query)
        save_bigquery_data_as_csv(results, file_path)
        normalize_data_csv(file_path, normalized_file_path)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
    
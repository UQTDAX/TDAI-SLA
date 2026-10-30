import os
import csv
import sys

from dotenv import load_dotenv
from db.bigquery_client import get_client

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

def main(): 
    query = """
    SELECT  * 
    FROM `demografy.prod_tables.a_master_view` 
    LIMIT 1000
    """
    try:
        results = load_bigquery_data(query)
        save_bigquery_data_as_csv(results, file_path=os.environ["BIGQUERY_DATA_FILE"])
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
    
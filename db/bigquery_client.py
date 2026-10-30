from google.cloud import bigquery

def get_client(project: str) -> bigquery.Client:
    return bigquery.Client(project)

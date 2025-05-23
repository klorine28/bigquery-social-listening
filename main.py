import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from typing import Optional


def get_bigquery_client(credentials_path: Optional[str] = None, project_id: Optional[str] = None):
    """
    Initialize BigQuery client with credentials.
    
    Args:
        credentials_path: Path to service account JSON file (optional)
        project_id: Google Cloud project ID
    
    Returns:
        BigQuery client instance
    
    Note:
        If no credentials_path is provided, uses Application Default Credentials.
        Set these up with: gcloud auth application-default login
    """
    if credentials_path and os.path.exists(credentials_path):
        # Use service account if provided
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = bigquery.Client(credentials=credentials, project=project_id)
        print(f"Using service account credentials from {credentials_path}")
    else:
        # Use Application Default Credentials (gcloud auth)
        try:
            from google.auth import default
            credentials, default_project = default()
            if not project_id and default_project:
                project_id = default_project
            client = bigquery.Client(project=project_id)
            print(f"Using Application Default Credentials for project: {project_id}")
        except Exception as e:
            print("Error: No credentials found. Please either:")
            print("1. Run: gcloud auth application-default login")
            print("2. Provide a service account JSON file")
            raise e
    
    return client


def query_to_dataframe(client: bigquery.Client, query: str) -> pd.DataFrame:
    """
    Execute BigQuery query and return results as pandas DataFrame.
    
    Args:
        client: BigQuery client instance
        query: SQL query string
    
    Returns:
        Query results as pandas DataFrame
    """
    query_job = client.query(query)
    return query_job.to_dataframe()


def export_to_csv(df: pd.DataFrame, filename: str, data_dir: str = "data"):
    """
    Export DataFrame to CSV file.
    
    Args:
        df: pandas DataFrame to export
        filename: Output filename
        data_dir: Directory to save the file (default: "data")
    
    Returns:
        Full path to exported file
    """
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"Data exported to {filepath}")
    return filepath


def query_to_csv(client: bigquery.Client, query: str, output_filename: str, chunk_size: Optional[int] = None):
    """
    Run BigQuery query and export directly to CSV.
    
    Args:
        client: BigQuery client instance
        query: SQL query string
        output_filename: Path for output CSV file
        chunk_size: If specified, write in chunks (useful for large datasets)
    
    Returns:
        Path to exported file
    """
    print("Running query...")
    query_job = client.query(query)
    
    if chunk_size:
        # For very large datasets, write in chunks
        print(f"Writing to {output_filename} in chunks of {chunk_size}...")
        for i, chunk in enumerate(query_job.to_dataframe_iterable(max_results=chunk_size)):
            mode = 'w' if i == 0 else 'a'
            header = i == 0
            chunk.to_csv(output_filename, mode=mode, header=header, index=False)
            print(f"Written chunk {i+1}")
    else:
        # For smaller datasets, load all at once
        df = query_job.to_dataframe()
        df.to_csv(output_filename, index=False)
        print(f"Query complete. {len(df)} rows saved to {output_filename}")
    
    return output_filename


def main():
    print("Google Cloud BigQuery Project")
    print("Use Jupyter Notebook (bigquery_tutorial.ipynb) to get started!")


if __name__ == "__main__":
    main()
# bigquery_client.py
import warnings
warnings.filterwarnings('ignore')

from google.cloud import bigquery

PROJETO = "dm-mottu-aluguel"

def get_client():
    return bigquery.Client(project=PROJETO)

def rodar_query(query: str):
    cliente = get_client()
    return cliente.query(query).to_dataframe()

def estimar_query(query: str):
    cliente = get_client()
    job_config = bigquery.QueryJobConfig(dry_run=True)
    job = cliente.query(query, job_config=job_config)
    gb = job.total_bytes_processed / 1e9
    print(f"⚠️ Estimativa: {gb:.2f} GB processados")


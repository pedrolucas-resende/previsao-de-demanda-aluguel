import pandas as pd
from google.cloud import bigquery

# ------------------------------------------------------------
# PASSO 4 — Inicializar o cliente BigQuery
# ------------------------------------------------------------
PROJETO = "dm-mottu-aluguel"

cliente = bigquery.Client(project=PROJETO)
print(f"✅ Conectado ao projeto: {PROJETO}") 

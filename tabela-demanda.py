import pandas as pd
from google.cloud import bigquery

PROJETO = "dm-mottu-aluguel"

cliente = bigquery.Client(project=PROJETO)
print(f"✅ Conectado ao projeto: {PROJETO}") 

query_demanda = """
SELECT
    DATE_TRUNC(dia, MONTH)          AS ano_mes,
    regiao,
    ROUND(AVG(motos_alugadas), 0)   AS media_motos_alugadas_dia
FROM `dm-mottu-aluguel.exp_frota.frota_alugada_historico`
WHERE
    pais = 'Brasil'
    AND DATE_TRUNC(dia, MONTH) < DATE_TRUNC(CURRENT_DATE(), MONTH)
    AND dia >= DATE_SUB(CURRENT_DATE(), INTERVAL 24 MONTH)
GROUP BY ano_mes, regiao
ORDER BY ano_mes DESC, regiao
"""


'''
query_debug = """
SELECT
    dia,
    regiao,
    SUM(motos_alugadas) AS motos_alugadas_dia
FROM `dm-mottu-aluguel.exp_frota.frota_alugada_historico`
WHERE pais = 'Brasil'
  AND dia BETWEEN '2025-01-01' AND '2025-01-31'
  AND regiao = 'Aracaju'
GROUP BY dia, regiao
ORDER BY dia
"""

df_debug = cliente.query(query_debug).to_dataframe()
print(df_debug)
'''


# 1. Roda a query e cria o dataframe
df = cliente.query(query_demanda).to_dataframe()
print(f"✅ {df.shape[0]} linhas x {df.shape[1]} colunas")

# 2. Cria a pasta se não existir
import os
os.makedirs("data/raw", exist_ok=True)

# 3. Salva o CSV
df.to_csv("data/raw/frota_alugada_historico.csv", index=False)
print("💾 Salvo em: data/raw/frota_alugada_historico.csv")

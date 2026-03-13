# sandbox.py — rascunho de queries, não sobe pro git
from bigquery_client import *

query_validacao = """
SELECT
    PARSE_DATE('%Y-%m', inicioMes) AS ano_mes,
    lugar,
    SUM(COALESCE(retirada, 0)) AS contratos_novos,
    CASE
        WHEN produto_categoria LIKE '%Conquiste%' THEN 'Conquiste'
        ELSE 'Aluguel / Minha Mottu'
    END                                         AS tipo_negocio,

    CASE
        WHEN produto LIKE '%0km%'       THEN 'Nova'
        WHEN produto LIKE '%Seminova%'  THEN 'Semi-nova'
        WHEN produto LIKE '%Usada%'     THEN 'Usada'
        ELSE 'Outros'
    END                                         AS tipo_moto
  FROM `grw_contrato.contrato`
  WHERE PARSE_DATE('%Y-%m', inicioMes) >= DATE '2025-01-01'
  GROUP BY 1, 2, produto, produto_categoria
"""

df = rodar_query(query_validacao)

import os
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/contratos_por_lugar_produto.csv", index=False)
print("💾 Salvo em: data/raw/contratos_por_lugar_produto.csv")

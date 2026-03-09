# sandbox.py — rascunho de queries, não sobe pro git
from bigquery_client import *

query_validacao = """
SELECT
    DATE_TRUNC(inicioData, MONTH)               AS ano_mes,
    lugar,
    CASE
        WHEN produto_categoria LIKE '%Conquiste%' THEN 'Venda'
        ELSE 'Aluguel'
    END                                         AS tipo_negocio,

    CASE
        WHEN produto LIKE '%0km%'       THEN 'Nova'
        WHEN produto LIKE '%Seminova%'  THEN 'Semi-nova'
        WHEN produto LIKE '%Usada%'     THEN 'Usada'
        ELSE 'Outros'
    END                                         AS tipo_moto,

    COUNT(DISTINCT locacaoCicloId)              AS todos_ciclos,
    COUNT(DISTINCT primeira_locacaoId)          AS contratos_novos,
    COUNT(DISTINCT usuarioId)                   AS clientes_unicos

FROM `dm-mottu-aluguel.grw_contrato.contrato_dia`
WHERE
    status_contrato = 'Ativo'
    AND pais = 'Brasil'
    AND dia = inicioData
    AND DATE_TRUNC(inicioData, MONTH) < DATE_TRUNC(CURRENT_DATE(), MONTH) 
    AND inicioData >= DATE_SUB(CURRENT_DATE(), INTERVAL 24 MONTH)
GROUP BY ano_mes, lugar, tipo_negocio, tipo_moto
ORDER BY ano_mes, lugar, tipo_negocio, tipo_moto
"""

df = rodar_query(query_validacao)

import os
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/contratos_por_lugar_produto.csv", index=False)
print("💾 Salvo em: data/raw/contratos_por_lugar_produto.csv")

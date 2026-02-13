WITH raw_data AS (
    SELECT *
    FROM {{ source('banco_origen', 'raw_transacciones') }}
)

SELECT DISTINCT
    id_tx,
    tarjeta,
    monto,
    comercio,
    rubro,
    ciudad,
    -- Convertimos el texto a fecha real
    CAST(timestamp AS TIMESTAMP) as fecha_hora
FROM raw_data
WHERE id_tx IS NOT NULL
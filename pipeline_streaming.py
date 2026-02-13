import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import os
import json

# --- CONFIGURACIÓN ---
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciales.json"

PROJECT_ID = "dataengineerp"
SUBSCRIPTION = "projects/dataengineerp/subscriptions/transacciones-bancarias-sub"
TABLE_ID = "dataengineerp.banco_transacciones.raw_transacciones"

def enmascarar_tarjeta(dato):
    try:
        # Recibe: '4500-1234-5678-9010'
        tarjeta_real = dato.get('tarjeta', '')
        if tarjeta_real:
            visible = tarjeta_real[-4:]
            dato['tarjeta'] = f"****-****-****-{visible}"
        return dato
    except Exception as e:
        return dato # Si falla, devuelve el dato tal cual para no romper el pipeline

def run():
    options = PipelineOptions(
        streaming=True,
        project=PROJECT_ID,
        runner='DirectRunner' # Correr localmente
    )
    
    print("🚀 Pipeline de Streaming escuchando... (Pulsa CTRL+C para detener)")
    
    with beam.Pipeline(options=options) as p:
        (
            p
            | "Leer PubSub" >> beam.io.ReadFromPubSub(subscription=SUBSCRIPTION)
            | "Bytes a JSON" >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
            | "Protegiendo Datos" >> beam.Map(enmascarar_tarjeta)
            | "Escribir en BQ" >> beam.io.WriteToBigQuery(
                TABLE_ID,
                schema="id_tx:STRING, tarjeta:STRING, monto:INTEGER, comercio:STRING, rubro:STRING, ciudad:STRING, timestamp:STRING",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

if __name__ == '__main__':
    run()
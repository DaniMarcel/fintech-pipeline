import os
import time
import json
import random
from datetime import datetime
from google.cloud import pubsub_v1
from faker import Faker

# Esto le dice a Google dónde está tu carnet de identidad
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciales.json"

# --- CONFIGURACIÓN ---
PROJECT_ID = "dataengineerp"  # Tu ID de proyecto
TOPIC_ID = "transacciones-bancarias"  # El tema que creaste

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
fake = Faker('es_CL') # Datos falsos chilenos

print(f"Iniciando simulador de transacciones bancarias...")
print(f"Enviando a: {topic_path}")
print("Presiona CTRL + C para detener.")

# Comercios y rubros para simular
COMERCIOS = [
    ('Lider', 'Supermercado'), ('Jumbo', 'Supermercado'),
    ('Copec', 'Combustible'), ('Shell', 'Combustible'),
    ('Uber', 'Transporte'), ('Cabify', 'Transporte'),
    ('Netflix', 'Suscripción'), ('Spotify', 'Suscripción'),
    ('Starbucks', 'Restaurante'), ('McDonalds', 'Restaurante'),
    ('Falabella', 'Retail'), ('Paris', 'Retail')
]

try:
    while True:
        # 1. Crear una transacción falsa
        comercio, rubro = random.choice(COMERCIOS)
        
        transaccion = {
            "id_tx": fake.uuid4(),
            "tarjeta": fake.credit_card_number(), # ¡DATO SENSIBLE! (PII)
            "monto": random.randint(1000, 1000000), # Montos entre 1 luca y 1 millón
            "comercio": comercio,
            "rubro": rubro,
            "ciudad": fake.city(),
            "timestamp": datetime.now().isoformat()
        }

        # 2. Convertir a JSON y Bytes (Pub/Sub solo come bytes)
        mensaje_json = json.dumps(transaccion)
        mensaje_bytes = mensaje_json.encode("utf-8")

        # 3. Publicar en la nube
        future = publisher.publish(topic_path, mensaje_bytes)
        
        # Log visual para nosotros
        print(f"Enviando: {transaccion['monto']} en {transaccion['comercio']} (ID: {future.result()})")
        
        # Esperar un poco entre ventas (0.5 a 2 segundos)
        time.sleep(random.uniform(0.5, 2.0))

except KeyboardInterrupt:
    print("\nSimulador detenido.")

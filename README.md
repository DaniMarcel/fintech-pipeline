# Real-Time Fintech Transaction Pipeline

**Ingeniería de Datos End-to-End: De Python a Looker Studio**

Este proyecto simula un ecosistema bancario completo. Genera transacciones financieras sintéticas en tiempo real, las ingesta mediante streaming, protege datos sensibles (PII), valida la calidad de los datos y visualiza KPIs financieros en un dashboard en vivo.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.11 (Generación de datos & Procesamiento).
* **Ingesta & Streaming:** Google Cloud Pub/Sub.
* **Procesamiento (ETL):** Apache Beam (Dataflow Runner compatible).
* **Data Warehouse:** Google BigQuery.
* **Transformación & Calidad (dbt):** dbt (Data Build Tool) para limpieza y testing automático.
* **Infraestructura como Código (IaC):** Terraform.
* **Visualización:** Looker Studio.

## Arquitectura del Pipeline

1.  **Generador (Producer):** Script en Python (`faker`) que simula compras en comercios reales (Uber, Lider, Copec) y envía mensajes JSON a Pub/Sub.
2.  **Streaming ETL (Consumer):** Pipeline de Apache Beam que:
    * Lee los mensajes en tiempo real.
    * **Enmascara** el número de tarjeta de crédito (PCI DSS Compliance) dejando solo los últimos 4 dígitos.
    * Escribe los datos crudos en BigQuery (`raw_transacciones`).
3.  **Analytics Engineering:** Modelos dbt que:
    * Materializan vistas limpias sin duplicados.
    * Ejecutan **Tests de Calidad** (Unique, Not Null) para asegurar integridad referencial.
4.  **Reporting:** Tablero en Looker Studio conectado a la capa "Curated" de dbt.

## Cómo ejecutarlo localmente

### Prerrequisitos
* Cuenta de Google Cloud Platform (GCP) con facturación habilitada.
* Python 3.11+ instalado.
* Terraform instalado.
* Service Account Key (`credenciales.json`) con permisos de Editor o BigQuery/PubSub Admin.

### Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/DaniMarcel/fintech-pipeline.git
    cd fintech-pipeline
    ```

2.  **Configurar entorno virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```

3.  **Desplegar Infraestructura (IaC):**
    ```bash
    terraform init
    terraform apply
    ```

4.  **Ejecutar Simulación:**
    * Terminal 1 (Generador): `python generador_transacciones.py`
    * Terminal 2 (Procesador): `python pipeline_streaming.py`

5.  **Transformación & Testing:**
    ```bash
    cd transformacion_bancaria
    dbt run
    dbt test
    ```

## Decisiones Técnicas Clave

* **¿Por qué Pub/Sub?** Para desacoplar el productor del consumidor, permitiendo escalar la ingesta sin perder mensajes si el procesador se detiene.
* **¿Por qué dbt?** Para traer las mejores prácticas de ingeniería de software (versionado, testing, CI/CD) al mundo de SQL.
* **¿Por qué Terraform?** Para evitar el "ClickOps" y asegurar que la infraestructura sea reproducible y auditable.
* **Enmascaramiento en Streaming:** La protección de datos sensibles (PII) se realiza *antes* de que el dato toque el disco (BigQuery) para cumplir con normativas de privacidad desde el diseño.

---
*Desarrollado por Daniel Marcel - Ingeniero de Datos*#



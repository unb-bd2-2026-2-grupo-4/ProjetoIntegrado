FROM python:3.12-slim

WORKDIR /app

COPY requirements-pipeline.txt .
RUN pip install --no-cache-dir -r requirements-pipeline.txt

COPY src/ src/

# Garante o schema (migrações idempotentes) e carrega os CSVs ainda não ingeridos.
CMD ["sh", "-c", "python src/db/migrar.py && python src/ingestao/carga_bronze.py"]

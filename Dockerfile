FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY web/ ./web/
COPY data/ ./data/

# Build uzex.duckdb at image build time if not already copied
RUN if [ ! -f data/uzex.duckdb ]; then python src/build_db.py; fi

ENV PORT=7860
EXPOSE 7860

CMD ["python", "src/server.py"]

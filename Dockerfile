# API image. The generated-code sandbox is a subprocess inside this container, so the container itself is the
# outer isolation layer: run it with a read-only filesystem and drop capabilities (see README).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY configs ./configs
COPY src ./src
COPY api ./api

# Run as an unprivileged user; results/logs must be writable for the router's usage file.
RUN useradd --uid 10001 --create-home app && mkdir -p results/logs && chown -R app /app/results
USER app

EXPOSE 8000
# GEMINI_API_KEY is passed at runtime (docker run -e), never baked into the image.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

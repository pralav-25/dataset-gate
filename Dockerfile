FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir '.[api]' && useradd --create-home --uid 10001 gate && mkdir /data && chown gate:gate /data
USER gate
EXPOSE 8765
VOLUME ["/data"]
CMD ["dataset-gate", "serve", "--host", "0.0.0.0", "--port", "8765", "--db", "/data/history.db"]

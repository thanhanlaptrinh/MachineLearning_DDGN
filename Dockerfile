FROM node:24-bookworm-slim AS webdeps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
FROM python:3.12-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 libstdc++6 && rm -rf /var/lib/apt/lists/*
COPY --from=webdeps /usr/local/bin/node /usr/local/bin/node
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=webdeps /app/node_modules ./node_modules
ENV PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PORT=3000
EXPOSE 3000
CMD ["python", "scripts/start_production.py"]

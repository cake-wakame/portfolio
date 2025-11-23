# ベースイメージ
FROM python:3.11-slim

LABEL maintainer="cake-wakame"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# シンプルなビルド依存を入れておく
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 依存解決（requirements.txt はリポジトリに存在する想定）
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt

# ソースをコピー
COPY . /app

# エントリポイントをコピーして実行権を付与
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

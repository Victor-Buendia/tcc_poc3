FROM postgres:13

RUN apt-get update && \
    apt-get install -y postgresql-contrib && \
    apt-get install -y postgresql-13-pgaudit && \
    rm -rf /var/lib/apt/lists/*

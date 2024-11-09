FROM --platform=linux/amd64 debian:bullseye-slim

RUN apt-get update && apt-get install curl unzip -y 
WORKDIR /duckdb

ARG DB_PATH_ARG
ENV DB_PATH ${DB_PATH_ARG}

RUN curl -L -O  https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip
RUN unzip duckdb_cli-linux-amd64.zip
RUN echo "alias duckdb='/duckdb/duckdb'" >> ~/.bashrc

WORKDIR /src
ENTRYPOINT [ "/duckdb/duckdb" ]
# ENTRYPOINT ["/duckdb/duckdb" "${DB_PATH}" "-init"]
FROM postgres:16.2

RUN apt-get update \
    && apt-get install -y \
       postgresql-server-dev-16 \
       build-essential \
       git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make \
    && make install \
    && cd / \
    && rm -rf /tmp/pgvector

RUN apt-get purge -y \
       postgresql-server-dev-16 \
       build-essential \
       git \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

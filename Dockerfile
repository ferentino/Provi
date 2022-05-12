FROM postgres
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB root
COPY world.sql /docker-entrypoint-initdb.d/
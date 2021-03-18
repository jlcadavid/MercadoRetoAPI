FROM postgres:latest
ENV POSTGRES_PASSWORD=07021997
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=data
COPY initializeDB.sql /docker-entrypoint-initdb.d/initializeDB.sql
EXPOSE 5432
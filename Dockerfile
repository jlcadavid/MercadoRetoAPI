FROM python:latest
ENV POSTGRES_PASSWORD=07021997
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=data
RUN apt-get -q update && apt-get -qy install postgresql-client
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
COPY utils.py /code
COPY dbManager.py /code
COPY publicAPIManager.py /code
COPY awsIPSearch.py /code
COPY main.py /code
COPY wait-for-postgres.sh /code
EXPOSE 5000
ENTRYPOINT [ "./wait-for-postgres.sh", "db", "python3", "-u", "main.py" ]
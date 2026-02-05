FROM apache/airflow:2.9.3

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

# Install python deps for jobs and GE
RUN pip install --no-cache-dir \
    great_expectations==0.18.21 \
    pandas \
    boto3 \
    requests \
    pyspark==3.5.1

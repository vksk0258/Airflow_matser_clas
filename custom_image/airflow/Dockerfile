FROM apache/airflow:2.9.2
USER root
RUN apt-get update && apt-get install -y --no-install-recommends gcc heimdal-dev g++ libsasl2-dev && apt-get autoremove -yqq --purge && apt-get clean && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install apache-airflow-providers-oracle
RUN pip uninstall -y argparse

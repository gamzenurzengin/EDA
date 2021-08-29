import os
import pandas as pd

credential_file = "/Users/nurzengin/Downloads/noted-episode-244108-274582e9a4f6.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_file

project_id = "noted-episode-244108"


def run_sql(query):
    return pd.read_gbq(query, project_id=project_id, dialect="standard", use_bqstorage_api=True)


#google bigquery i pycharm a bağlamak için aşağıdaki kodu kullanırız.
#aynı zamanda https://cloud.google.com/bigquery/docs/reference/libraries#cloud-console bu linkteki adımlar izlenerek
#aşağıdaki kod düzenlenir.

#from google.cloud import bigquery as bq














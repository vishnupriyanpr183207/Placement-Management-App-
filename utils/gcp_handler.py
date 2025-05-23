from google.cloud import storage
import pandas as pd
import io

def download_data_from_gcp(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_text()
    return pd.read_csv(io.StringIO(data))

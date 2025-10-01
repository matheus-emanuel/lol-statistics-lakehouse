import boto3
from botocore.client import Config
import os

# Configurações do MinIO/S3
endpoint_url = "http://minio:9000"  # ou s3:// se for AWS
access_key = "qOFclq6eGlFnjm18lIEc"
secret_key = "T3Wd9h3CjUe9pcRF0DakmrjTBDWYUmDGA9Wue5X0"
bucket_name = "lol-statistics-bronze-layer"

# Cria cliente S3/MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # URL do MinIO
    aws_access_key_id='qOFclq6eGlFnjm18lIEc',  # Acesso da access key
    aws_secret_access_key='T3Wd9h3CjUe9pcRF0DakmrjTBDWYUmDGA9Wue5X0',  # Acesso da access key
    region_name="us-east-1"  # Região fictícia para MinIO
    # config=Config(signature_version="s3v4"),  # Compatível com MinIO
)
# Lista os objetos do bucket
response = s3.list_objects_v2(Bucket=bucket_name)

if "Contents" in response:
    for obj in response["Contents"]:
        print(obj["Key"])
else:
    print("Nenhum arquivo encontrado no bucket.")

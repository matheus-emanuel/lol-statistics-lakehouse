import boto3
from botocore.client import Config
from dotenv import load_dotenv
import pandas as pd
import os

def create_bucket(s3, bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' criado com sucesso.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket '{bucket_name}' já existe e pertence a você.")
    except Exception as e:
        print("Erro ao criar o bucket:", e)
        
def load_files(s3, local_dir):
    for filename in os.listdir(local_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(local_dir, filename)
            object_name = filename  # Nome do arquivo no bucket
            try:
                s3.upload_file(file_path, bucket_name, object_name)
                print(f"Arquivo '{filename}' enviado com sucesso para o bucket '{bucket_name}'.")
                os.remove(file_path)
            except Exception as e:
                print(f"Erro ao enviar '{filename}':", e)
                
def convert_to_parquet():
    # Lê o CSV
    for filename in os.listdir(local_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(local_dir, filename)
            df = pd.read_csv(file_path, low_memory=False)
            
            parquet_filename = filename.rsplit('.', 1)[0] + ".parquet"
            parquet_path = os.path.join(local_dir, parquet_filename)
            
            df.to_parquet(parquet_path, engine="pyarrow", index=False)
            print(parquet_path)

# Loads enviroment configuration for connect in MinIO
load_dotenv('../configs/minio_connect.env')


# Create a low-level client with the service name
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # URL do MinIO
    aws_access_key_id=os.getenv("ACCESS_KEY"),  # Acesso da access key
    aws_secret_access_key=os.getenv("SECRET_KEY"),  # Acesso da access key
    region_name="us-east-1"  # Região fictícia para MinIO
    # config=Config(signature_version="s3v4"),  # Compatível com MinIO
)

# Start configurations
bucket_name = "lol-statistics-bronze-layer"
local_dir = "../data/raw"


# print("Iniciando processo de Envio dos arquivos")
# create_bucket(s3, bucket_name)
# load_files(s3, local_dir)
# print("Processo de Envio dos arquivos finalizado")
# converto_to_parquet()
from airflow import DAG
from airflow.operators.python import PythonOperator #type: ignore
from airflow.models import Variable #type: ignore
from datetime import datetime
import gdown
import boto3
from botocore.client import Config
from dotenv import load_dotenv
import pandas as pd
import os


with DAG(
    dag_id="lol_statistics_data_ingestion",
    start_date=datetime(2025, 5, 9),
    schedule="0 20 * * *",
    catchup=False,
) as dag:
    def download_data(temp_dir):
        url = "https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH?usp=drive_link"
        output = temp_dir
        try:
            gdown.download_folder(url=url, output=output)
            print("Dados baixados com sucesso")
        except Exception as e:
            print(f"Houve o seguinte erro ao baixar os arquivos: {e}")
            
    def create_bucket(s3, bucket_name):
        try:
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' criado com sucesso.")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            print(f"Bucket '{bucket_name}' já existe e pertence a você.")
        except Exception as e:
            print("Erro ao criar o bucket:", e)
            
    def load_files(s3, temp_dir):
        for filename in os.listdir(temp_dir):
            if filename.endswith(".parquet"):
                file_path = os.path.join(temp_dir, filename)
                object_name = filename  # Nome do arquivo no bucket
                try:
                    s3.upload_file(file_path, bucket_name, object_name)
                    print(f"Arquivo '{filename}' enviado com sucesso para o bucket '{bucket_name}'.")
                    os.remove(file_path)
                except Exception as e:
                    print(f"Erro ao enviar '{filename}':", e)
    
    def convert_to_csv_parquet(temp_dir):
        for filename in os.listdir(temp_dir):
            if filename.endswith(".csv"):
                file_path = os.path.join(temp_dir, filename)
                df = pd.read_csv(file_path, low_memory=False)
                
                parquet_filename = filename.rsplit('.', 1)[0] + ".parquet"
                parquet_path = os.path.join(temp_dir, parquet_filename)
                
                df.to_parquet(parquet_path, engine="pyarrow", index=False)
                print(parquet_path)
        
    # Create a low-level client with the service name
    s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",  # URL do MinIO
    aws_access_key_id=Variable.get("minio-connect-access-key"),  
    aws_secret_access_key=Variable.get("minio-connect-secret-key"),
    region_name="us-east-1"  # Região fictícia para MinIO
    )
    
    # Start configurations
    bucket_name = "lol-statistics-bronze-layer"
    temp_dir = "/tmp/downloaded_data"
    
    get_files = PythonOperator(
        task_id = 'get_files',
        python_callable=download_data,
        op_args=[temp_dir]
    )
    
    check_if_bucket_exists = PythonOperator(
        task_id = 'check_if_bucket_exists',
        python_callable = create_bucket,
        op_args=[s3, bucket_name]
    )
    
    convert_to_parquet = PythonOperator(
        task_id = 'convert_to_parquet',
        python_callable = convert_to_csv_parquet,
        op_args=[temp_dir]
    )
    
    upload_files = PythonOperator(
        task_id = 'upload_files',
        python_callable = load_files,
        op_args=[s3, temp_dir]
    )
    
    # Set task dependencies
    get_files >> check_if_bucket_exists >> convert_to_parquet >> upload_files
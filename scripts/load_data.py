import pandas as pd
import psycopg
import json
import os
from datetime import datetime
import io

def upload_data(df: pd.DataFrame, schema: str, table: str, dbname: str, password: str, host: str = 'localhost', user: str = 'postgresql', port: int = 5432):

    df = df.where(pd.notnull(df), None)

    # Cria buffer em memória
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False, sep='\t', na_rep='\\N')
    buffer.seek(0)

    columns = ', '.join(df.columns)
    copy_sql = f"COPY {schema}.{table} ({columns}) FROM STDIN WITH (FORMAT csv, DELIMITER E'\t', NULL '\\N')"

    try:
        with psycopg.connect(f"dbname={dbname} user={user} password={password} host={host} port={port}") as conn:
            with conn.cursor() as cur:
                with cur.copy(copy_sql) as copy:
                    for line in buffer:
                        copy.write(line)              
            conn.commit()
            print(f"Inseridos {len(df)} registros em {schema}.{table}")
    except Exception as e:
        print(f"Erro ao inserir dados em {schema}.{table}: {e}")

def get_columns(file_path: str) -> dict:
    """
    Descrição:
        Recupera as informações como colunas, partição, nome e descrição da tabela entre outras informações do arquivo de schema
    Args:
        file_path (str): Contém o caminho do arquivo em relação a este arquivo
    Returns:
        Retorna um dicionário simplificado contendo as seguintes informações:
    """

    # VALIDA DE UM ARQUIVO ESTÁ VAZIO
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"O arquivo '{file_path}' está vazio.")

    with open(file_path, 'r', encoding='utf-8') as arquivo:
        data = json.load(arquivo)
    
    metadata = data.get('metadata', {})
    fields = data.get('fields', [])
    return {
        "fields": fields,
        "table_name": metadata.get('table_name')
    }

def read_data(file_path: str, file_name: str, column_map: dict) -> pd.DataFrame:
    full_name = f'{file_path}{file_name}'
    data_frame = pd.read_csv(full_name)
    raw_names = [c for c in column_map.keys() if c in data_frame.columns]

    filtered_data_frame = data_frame[raw_names]
    filtered_data_frame = filtered_data_frame.rename(columns=column_map)

    filtered_data_frame['_file_name'] = file_name
    filtered_data_frame['_inserted_at'] = datetime.now()
    filtered_data_frame['_updated_at'] = datetime.now()

    return filtered_data_frame

def mount_query(column_name: list, dataframe_columns: list, schema: str, table: str, dataframe_values: object, file_name: str) -> str:
    columns = ', '.join(column_name)
    dataframe_values['_file_name'] = file_name
    dataframe_values['_inserted_at'] = datetime.now()
    dataframe_values['_updated_at'] = datetime.now()
    
    
    query = f"INSERT INTO {schema}.{table} ({columns}) VALUES ();"
    print(query)

    

if __name__ == '__main__':
    data_file_path = '../data/raw/'
    data_file_name = os.listdir(data_file_path)

    schema_file_path = '../schemas/'
    schema_file_name = os.listdir(schema_file_path)

    for data_file in data_file_name:
        for schema_file in schema_file_name:
            schema_full_name = f'{schema_file_path}{schema_file}'
            print(data_file)

            get_schema_info = get_columns(schema_full_name)
            fields = get_schema_info.get('fields')
            table_name = get_schema_info.get('table_name')
            column_map = {f['raw_name']: f['column_name'] for f in fields if f['raw_name']}

            data_df = read_data(data_file_path, data_file, column_map)
            upload_data(data_df, 'lol_statistics', table_name, dbname='lol_data_DW', password='postgresql')
    

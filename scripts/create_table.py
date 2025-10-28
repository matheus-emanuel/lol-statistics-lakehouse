import json
import psycopg
import os

def aux_type_map(list_type: list) -> list:
    field_type_pg = []
    TYPE_MAP = {
    "string": "TEXT",
    "integer": "INTEGER",
    "float": "NUMERIC",
    "double": "NUMERIC",
    "numeric": "NUMERIC",
    "boolean": "BOOLEAN",
    "bool": "BOOLEAN",
    "datetime": "TIMESTAMP",
    "timestamp": "TIMESTAMP",
    "date": "DATE",
    "time": "TIME",
    "array": "JSONB",
    "object": "JSONB",
    "struct": "JSONB",
    "bytes": "BYTEA"
    }

    field_type_pg = [TYPE_MAP.get(field.lower()) for field in list_type]
    return field_type_pg


def get_schema_file(file_path: str) -> dict:
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

    column_name = [f['column_name'] for f in fields]
    field_type = [f['type'] for f in fields]

    return {
        "table_name": metadata.get('table_name'),
        "description": metadata.get('description'),
        "partition_by": metadata.get('partition_by'),
        "group_by": metadata.get('group_by'),
        "column_name": column_name,
        "field_type": field_type
    }

def mount_query(dict_schema: dict, schema_name: str) -> str:
    """
    Descrição:
        Função responsável por montar a query de criação da tabela baseado em arquivo schema
    Args:
        disc_schema(dict): Dicionário contendo as informações necessárias do schema para a criação da query. As informações podem ser
        obtidas usando a função get_schema_file
        schema_name(str): Nome do schema no banco PostegreSQL
    Returns:
        Retorna a query de criação da tabela no formato de string
    """
    field_type_pg = aux_type_map(dict_schema.get('field_type'))
    columns = ",\n".join(
        f'{field} {field_type}' for field, field_type in zip(dict_schema.get('column_name'), field_type_pg)
    )
    
    sql_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.{dict_schema.get('table_name')} (
    {columns}
    );
    CREATE INDEX IF NOT EXISTS idx_{dict_schema.get('table_name')}_{dict_schema.get('partition_by')} ON {schema_name}.{dict_schema.get('table_name')} ({dict_schema.get('partition_by')});
    COMMENT ON TABLE {schema_name}.{dict_schema.get('table_name')} IS '{dict_schema.get('description')}';
        """
    return sql_query

def create_table(query: str, dbname: str, password: str, host: str = 'localhost', user: str = 'postgresql', port: int = 5432) -> None:
    """
    Descrição:
        Função responsável por criar a tabela dentro do banco
    Args:
        query(str): Variável do tipo string responsável por conter a query usada para criar a tabela
        dbname(str): Nome do banco
        user(str): Nome do usuário, por padrão é postgresql
        password(str): Senha do user
        host(str): host/IP do banco, por padrão é localhost
        port(int64): Porta de conexão com o banco, por padrão é 5432
    Return:
        Essa função não retorna nada
    """
    with psycopg.connect(f"dbname={dbname} user={user} password={password} host={host} port={5432}") as conn:
        with conn.cursor() as cur:
            cur.execute(query)

if __name__ == '__main__':
    file_path = '../schemas/'
    file_name = os.listdir(file_path)

    for file in file_name:
        full_name = f'{file_path}{file}'
        dict_schema = get_schema_file(full_name)
        sql_query = mount_query(dict_schema, 'lol_statistics')
        print(sql_query)
        create_table(sql_query, dbname='lol_data_DW', password='postgresql')
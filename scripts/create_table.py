import json

def aux_type_map(list_type: list) -> list:
    field_type_pg = []
    TYPE_MAP = {
    "string": "TEXT",
    "integer": "INTEGER",
    "float": "NUMERIC",
    "double": "NUMERIC",
    "numeric": "NUMERIC",
    "boolean": "BOOLEAN",
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

def mount_query(dict_schema: dict) -> str:
    """
    Descrição:
        Função responsável por montar a query de criação da tabela baseado em arquivo schema

    Args:
        disc_schema(dict): Dicionário contendo as informações necessárias do schema para a criação da query. As informações podem ser
        obtidas usando a função get_schema_file

    Return:
        Retorna a query de criação da tabela no formato de string
    """
    field_type_pg = aux_type_map(dict_schema.get('field_type'))
    columns = ",\n".join(
        f'{field} {field_type}' for field, field_type in zip(dict_schema.get('column_name'), field_type_pg)
    )
    
    sql_query = f"""
    CREATE TABLE schema.{dict_schema.get('table_name')} (
    {columns}
    );
    CREATE INDEX idx_{dict_schema.get('table_name')}_{dict_schema.get('partition_by')} ON {dict_schema.get('table_name')} ({dict_schema.get('partition_by')});
    COMMENT ON TABLE {dict_schema.get('table_name')} IS '{dict_schema.get('description')}';
        """
    print(sql_query)

def database_conn():
    pass

def create_table():
    pass

if __name__ == '__main__':
    file_path = '../schemas/table_schema_raw_leagues.json' 

    dict_schema = get_schema_file(file_path)
    mount_query(dict_schema)
    # print(dict_schema)
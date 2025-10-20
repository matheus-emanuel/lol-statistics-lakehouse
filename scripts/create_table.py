import json

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

def mount_query():
    pass

def database_conn():
    pass

def create_table():
    pass

if __name__ == '__main__':
    file_path = '../schemas/table_schema_raw_leagues.json' 

    dict_schema = get_schema_file(file_path)
    print(dict_schema)
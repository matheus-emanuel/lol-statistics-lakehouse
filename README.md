## Estrutura do Projeto
 ```
lol-data-lakehouse/
│── dags/                   # DAGs do Airflow
│   ├── download_lol_data.py   # DAG que baixa o CSV do Drive
│   ├── process_lol_data.py    # DAG que processa com Spark
│
│── scripts/                # Scripts auxiliares e testes
│   ├── download.py         # Baixa o arquivo manualmente (antes de virar DAG)
│   ├── upload_minio.py     # Faz upload para MinIO
│   ├── transform.py        # Testa lógica de transformação (antes de Spark)
│
│── data/                   # Dados locais (se precisar testar sem MinIO)
│   ├── raw/                # Dados brutos
│   ├── processed/          # Dados tratados
│
│── spark/                  # Código Spark
│   ├── jobs/               # Scripts Spark para processamento
│   │   ├── process_matches.py
│   │   ├── process_players.py
│   ├── config/             # Configuração do Spark
│   │   ├── spark-defaults.conf
│   │   ├── minio-credentials.conf
│
│── docker/                 # Configuração de containers
│   ├── docker-compose.yml  # MinIO, Spark, Airflow, etc.
│   ├── minio.env           # Configuração do MinIO
│   ├── airflow.env         # Configuração do Airflow
│
│── lakehouse/              # Estrutura do Data Lake (usando MinIO)
│   ├── bronze/             # Dados brutos do CSV
│   ├── silver/             # Dados limpos e organizados
│   │   ├── matches/        # Dados de partidas profissionais
│   │   ├── players/        # Estatísticas de jogadores
│   │   ├── teams/          # Informações de times
│   │   ├── champions/      # Dados agregados por campeão
│   ├── gold/               # Dados prontos para análise
│   │   ├── winrates/       # Taxa de vitória por campeão/time
│   │   ├── meta-analysis/  # Tendências de meta
│
│── notebooks/              # Notebooks Jupyter para análises
│   ├── data_exploration.ipynb
│   ├── winrate_analysis.ipynb
│
│── configs/                # Arquivos de configuração
│   ├── airflow.cfg
│   ├── spark-config.yaml
│
│── README.md               # Explicação do projeto
 ```

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Função para remover aspas se necessário (para por streamlit no ar)
def clean_env_var(var):
    return var.strip('"').strip("'") if var else var

# Configurações do banco de dados usando as variáveis de ambiente
host = clean_env_var(os.getenv("DB_HOST"))
port = clean_env_var(os.getenv("DB_PORT"))
user = clean_env_var(os.getenv("DB_USER"))
password = clean_env_var(os.getenv("DB_PASSWORD"))
database_name = clean_env_var(os.getenv("DB_NAME"))

DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)
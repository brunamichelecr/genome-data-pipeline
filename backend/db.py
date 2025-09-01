import os
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis de ambiente a partir do arquivo .env
# Isso garante que dados sensíveis (como senha do banco) não fiquem expostos no código
load_dotenv()

def get_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL
    utilizando a string armazenada em DATABASE_URL.

    Retorna:
        psycopg2.extensions.connection: objeto de conexão ativo
    """
    return psycopg2.connect(os.getenv("DATABASE_URL"))

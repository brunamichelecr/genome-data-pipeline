import os
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis de ambiente definidas no arquivo .env
load_dotenv()

# Recupera a string de conexão do PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    # Tenta estabelecer conexão com o banco
    conn = psycopg2.connect(DATABASE_URL)
    print("Conexão bem-sucedida!")
    
    # Fecha a conexão explicitamente após o teste
    conn.close()

except Exception as e:
    # Captura e exibe qualquer erro de conexão
    print("Erro na conexão:")
    print(e)

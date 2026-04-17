import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_conexao():
    try:
        conexao = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conexao
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
        return None
import psycopg2
def get_conexao():
    try:
        conexao = psycopg2.connect(
            database='SupplyChain',
            user='postgres',
            password='722406',
            host='localhost',
            port='5432'
        )
        return conexao
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
        return None
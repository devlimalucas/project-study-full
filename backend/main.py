from fastapi import FastAPI
import mysql.connector

app = FastAPI()


def get_connection():
    return mysql.connector.connect(
        host="db",  # nome do serviço no docker-compose
        user="root",
        password="root",
        database="loja"
    )


@app.get("/produtos")
def listar_produtos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Produto, Quantidade, Receita FROM vendas LIMIT 10")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

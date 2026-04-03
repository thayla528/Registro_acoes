import sqlite3

conn = sqlite3.connect("banco.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

#  BUSCA OS DADOS PRIMEIRO
cursor.execute("SELECT * FROM empresas")
dados = cursor.fetchall()

#  AGORA SIM percorre
for empresas in dados:
    print(dict(empresas))

conn.close()
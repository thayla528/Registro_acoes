import sqlite3

conn = sqlite3.connect("banco.db")
conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
cursor = conn.cursor()

# Listar todas as empresas
cursor.execute("SELECT * FROM empresas")
empresas = cursor.fetchall()

for empresa in empresas:
    print(dict(empresa))  # Mostra cada linha como dicionário

conn.close()

# para ver python ver_banco.py


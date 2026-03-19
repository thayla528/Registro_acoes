import sqlite3

conn = sqlite3.connect("banco.db")
conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
cursor = conn.cursor()

# Listar todos os usuários
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

for usuario in usuarios:
    print(dict(usuario))  # Mostra cada linha como dicionário

conn.close()

# para ver python ver_usuarios.py
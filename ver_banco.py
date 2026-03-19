import sqlite3

# Conecta ao banco
conn = sqlite3.connect("banco.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Pega todas as empresas
cursor.execute("SELECT * FROM empresas")
empresas = cursor.fetchall()

# Exibe todas
if empresas:
    for e in empresas:
        print(dict(e))  # Mostra como dicionário para facilitar leitura
else:
    print("Nenhuma empresa cadastrada.")

conn.close()

# para ver python ver_banco.py
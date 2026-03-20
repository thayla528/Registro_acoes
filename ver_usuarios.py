import sqlite3  # Importa o módulo sqlite3 para trabalhar com bancos SQLite

# Conecta ao banco de dados "banco.db"
conn = sqlite3.connect("banco.db")
# Permite acessar as colunas pelo nome, não apenas pelo índice
conn.row_factory = sqlite3.Row
# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Executa um comando SQL para selecionar todos os usuários
cursor.execute("SELECT * FROM usuarios")
# Recupera todas as linhas retornadas pelo SQL
usuarios = cursor.fetchall()

# Itera por cada usuário retornado
for usuario in usuarios:
    # Converte cada linha para dicionário e imprime, facilitando a leitura
    print(dict(usuario))

# Fecha a conexão com o banco de dados
conn.close()
import sqlite3  # Importa o módulo sqlite3 para trabalhar com banco de dados SQLite

# Conecta ao banco de dados "banco.db"
conn = sqlite3.connect("banco.db")
# Permite acessar os campos das tabelas pelo nome, não apenas pelo índice
conn.row_factory = sqlite3.Row
# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Executa um comando SQL para selecionar todas as linhas da tabela 'empresas'
cursor.execute("SELECT * FROM empresas")
# Recupera todas as linhas retornadas pelo comando SQL
empresas = cursor.fetchall()

# Verifica se existem empresas cadastradas
if empresas:
    # Itera por cada empresa retornada
    for e in empresas:
        # Converte a linha para dicionário e imprime, facilitando a leitura
        print(dict(e))
else:
    # Caso não haja empresas cadastradas
    print("Nenhuma empresa cadastrada.")

# Fecha a conexão com o banco de dados
conn.close()

# para ver python ver_banco.py
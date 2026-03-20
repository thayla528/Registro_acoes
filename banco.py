import sqlite3  # Importa o módulo sqlite3 para trabalhar com banco de dados SQLite

# Função para conectar ao banco de dados
def conectar():
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar ou atualizar as tabelas do banco
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    # ------------------ TABELA DE USUÁRIOS ------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nome TEXT NOT NULL,                    
            email TEXT UNIQUE NOT NULL,            
            senha TEXT NOT NULL                   
        )
    """)

    # ------------------ TABELA DE EMPRESAS ------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)

    # Lista de colunas que queremos garantir na tabela
    colunas = {
        "ticker": "TEXT NOT NULL",
        "empresa": "TEXT NOT NULL",
        "setor": "TEXT NOT NULL",
        "num_acoes": "INTEGER DEFAULT 0",
        "preco_acao": "REAL DEFAULT 0",
        "lucro_liquido": "REAL DEFAULT 0",
        "patrimonio": "REAL DEFAULT 0",
        "ativos": "REAL DEFAULT 0",
        "divida": "REAL DEFAULT 0",
        "lote": "INTEGER DEFAULT 100",
        "tipo_acao": "TEXT NOT NULL"
    }

    # Tabela de investimentos (renda fixa)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        tipo TEXT,              -- CDI, LCI, LCA, SELIC
        valor_investido REAL,
        taxa REAL,
        tempo INTEGER,          -- meses
        lucro REAL
    )
    """)

    # Tenta adicionar cada coluna (ignora erro se já existir)
    for coluna, tipo in colunas.items():
        try:
            cursor.execute(f"ALTER TABLE empresas ADD COLUMN {coluna} {tipo}")
        except sqlite3.OperationalError:
            # Coluna já existe, ignora
            pass



    conn.commit()
    conn.close()



# Executa a criação/atualização das tabelas quando o arquivo é rodado diretamente
if __name__ == "__main__":
    criar_tabela()
    print("Banco criado/atualizado com sucesso!")
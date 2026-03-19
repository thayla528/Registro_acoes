import sqlite3

def conectar():
    conn = sqlite3.connect("banco.db")
    # ESSA LINHA ABAIXO É O QUE RESOLVE O SEU ERRO:
    conn.row_factory = sqlite3.Row 
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    # Tabela de Empresas (Importante criar aqui também)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            num_acoes INTEGER NOT NULL,
            preco_acao REAL NOT NULL,
            lucro_liquido REAL NOT NULL,
            patrimonio REAL NOT NULL,
            ativos REAL NOT NULL,
            divida REAL NOT NULL,
            tipo_acao TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

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

    # Tabela de Empresas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            empresa TEXT NOT NULL,
            setor TEXT NOT NULL,
            num_acoes INTEGER NOT NULL,
            preco_acao REAL NOT NULL,
            lucro_liquido REAL NOT NULL,
            patrimonio REAL NOT NULL,
            ativos REAL NOT NULL,
            divida REAL NOT NULL,
            lote INTEGER NOT NULL,
            tipo_acao TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
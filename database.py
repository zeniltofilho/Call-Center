import sqlite3

DB_NAME = "callcenter.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = conectar()
    c = conn.cursor()

    # -------- operadores --------
    c.execute("""
    CREATE TABLE IF NOT EXISTS operadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ativo INTEGER DEFAULT 1
    )
    """)

    # -------- produção --------
    c.execute("""
    CREATE TABLE IF NOT EXISTS producao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operador_id INTEGER,
        data TEXT,
        quantidade INTEGER,
        valor REAL
    )
    """)

    # -------- metas --------
    c.execute("""
    CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT UNIQUE,
        meta_qtd INTEGER,
        meta_valor REAL
    )
    """)

    # -------- recibos --------
    c.execute("""
    CREATE TABLE IF NOT EXISTS recibos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contrib INTEGER,
        valor REAL,
        vencimento TEXT,
        nosso_num TEXT,
        operador TEXT
    )
    """)

    conn.commit()
    conn.close()

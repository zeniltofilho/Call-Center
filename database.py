import sqlite3

DB_NAME = "callcenter.db"

_conn = None


def conectar():
    return sqlite3.connect(DB_NAME)


def init_db():
    """
    Inicializa o banco UMA VEZ
    e mantém a conexão aberta para o sistema todo
    """
    global _conn

    if _conn is None:
        _conn = sqlite3.connect(DB_NAME)
        criar_tabelas(_conn)

    return _conn


def get_connection():
    """
    Retorna a mesma conexão já inicializada no main.py
    """
    return _conn


def criar_tabelas(conn):
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

    # -------- doações --------
    c.execute("""
    CREATE TABLE IF NOT EXISTS doacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contribuinte_id INTEGER,
        data_doacao TEXT,
        data_ligacao TEXT,
        valor REAL
    )
    """)

    conn.commit()

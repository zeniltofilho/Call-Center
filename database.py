import sqlite3

DB_NAME = "callcenter.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def init_db():
    """
    Inicializa o banco criando tabelas.
    """
    conn = conectar()
    criar_tabelas(conn)
    return conn


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

    # -------- contribuintes --------
    c.execute("""
    CREATE TABLE IF NOT EXISTS contribuintes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo INTEGER,
        nome TEXT,
        categoria TEXT,
        sexo TEXT,
        status TEXT,
        nascimento TEXT,
        inscricao TEXT,
        telefone1 TEXT,
        telefone2 TEXT,
        email TEXT,
        rua TEXT,
        bairro TEXT,
        cidade TEXT,
        cpf TEXT,
        rg TEXT,
        observacoes TEXT
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

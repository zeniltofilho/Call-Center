import sqlite3

DB_NAME = "callcenter.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def init_db():
    """
    Inicializa o banco criando tabelas e atualizando colunas faltantes.
    """
    conn = conectar()
    criar_tabelas(conn)
    return conn


def criar_tabelas(conn):
    c = conn.cursor()

    # =========================================================
    # 1) TABELA OPERADORES
    # =========================================================
    c.execute("""
    CREATE TABLE IF NOT EXISTS operadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ativo INTEGER DEFAULT 1
    )
    """)

    # =========================================================
    # 2) TABELA PRODUCAO
    # =========================================================
    c.execute("""
    CREATE TABLE IF NOT EXISTS producao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operador_id INTEGER,
        data TEXT,
        quantidade INTEGER,
        valor REAL
    )
    """)

    # =========================================================
    # 3) TABELA METAS
    # =========================================================
    c.execute("""
    CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT UNIQUE,
        meta_qtd INTEGER,
        meta_valor REAL
    )
    """)

    # =========================================================
    # 4) TABELA CONTRIBUINTES
    # =========================================================
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

    # -------- atualizar tabela contribuintes (se faltar colunas) --------
    c.execute("PRAGMA table_info(contribuintes)")
    cols = [x[1] for x in c.fetchall()]

    if "operador_atual" not in cols:
        c.execute("ALTER TABLE contribuintes ADD COLUMN operador_atual TEXT")

    if "operador_fixo" not in cols:
        c.execute("ALTER TABLE contribuintes ADD COLUMN operador_fixo TEXT")

    if "setor" not in cols:
        c.execute("ALTER TABLE contribuintes ADD COLUMN setor TEXT")

    if "numero" not in cols:
        c.execute("ALTER TABLE contribuintes ADD COLUMN numero TEXT")

    # =========================================================
    # 5) TABELA RECIBOS (cadastro simples)
    # =========================================================
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

    # -------- atualizar tabela recibos (se faltar colunas) --------
    c.execute("PRAGMA table_info(recibos)")
    cols = [x[1] for x in c.fetchall()]

    if "tipo" not in cols:
        c.execute("ALTER TABLE recibos ADD COLUMN tipo TEXT")

    if "pdf" not in cols:
        c.execute("ALTER TABLE recibos ADD COLUMN pdf TEXT")

    # =========================================================
    # 6) TABELA DOACOES
    # =========================================================
    c.execute("""
    CREATE TABLE IF NOT EXISTS doacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contribuinte_id INTEGER,
        data_doacao TEXT,
        data_ligacao TEXT,
        valor REAL
    )
    """)

    # =========================================================
    # 7) TABELA RECIBO_LAYOUT (layout por tipo)
    # =========================================================
    c.execute("""
    CREATE TABLE IF NOT EXISTS recibo_layout (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        nome TEXT NOT NULL,
        texto TEXT,
        x INTEGER,
        y INTEGER,
        fonte_nome TEXT,
        fonte_tamanho INTEGER,
        fonte_estilo TEXT
    )
    """)

    # =========================================================
    # 8) TABELA RECIBOS_EMITIDOS (histórico)
    # =========================================================
    c.execute("""
    CREATE TABLE IF NOT EXISTS recibos_emitidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        contribuinte_id INTEGER,
        nome TEXT,
        valor REAL,
        data TEXT,
        referente TEXT,
        operador TEXT,
        arquivo_pdf TEXT
    )
    """)

    conn.commit()

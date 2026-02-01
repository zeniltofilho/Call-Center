import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_NAME

# ================= BANCO =================

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mensageiros (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT,
            supervisor TEXT,
            status TEXT,
            visivel TEXT
        )
    """)
    con.commit()
    con.close()

# ================= LISTAGEM =================

def listar(tree, status_bar, filtro="", somente_ativos=False):
    tree.delete(*tree.get_children())

    con = conectar()
    cur = con.cursor()

    query = "SELECT * FROM mensageiros WHERE 1=1"
    params = []

    if filtro:
        query += " AND (codigo LIKE ? OR nome LIKE ?)"
        params.extend([f"%{filtro}%", f"%{filtro}%"])

    if somente_ativos:
        query += " AND status='ATIVO'"

    cur.execute(query, params)

    total = ativos = 0

    for row in cur.fetchall():
        total += 1
        tag = "ativo" if row[4] == "ATIVO" else "inativo"
        if tag == "ativo":
            ativos += 1
        tree.insert("", tk.END, values=row, tags=(tag,))

    con.close()

    status_bar.config(
        text=f"Total: {total}   |   Ativos: {ativos}   |   Inativos: {total-ativos}"
    )

# ================= CRUD =================

def salvar(tree, status_bar, dados):
    con = conectar()
    cur = con.cursor()

    if dados["codigo"]:
        cur.execute("""
            UPDATE mensageiros SET
            nome=?, turma=?, supervisor=?, status=?, visivel=?
            WHERE codigo=?
        """, (
            dados["nome"], dados["turma"], dados["supervisor"],
            dados["status"], dados["visivel"], dados["codigo"]
        ))
    else:
        cur.execute("""
            INSERT INTO mensageiros (nome, turma, supervisor, status, visivel)
            VALUES (?, ?, ?, ?, ?)
        """, (
            dados["nome"], dados["turma"], dados["supervisor"],
            dados["status"], dados["visivel"]
        ))

    con.commit()
    con.close()
    listar(tree, status_bar)

def excluir(tree, status_bar):
    item = tree.focus()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um registro para excluir.")
        return

    codigo = tree.item(item)["values"][0]

    if messagebox.askyesno("Confirmação", "Deseja excluir este registro?"):
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM mensageiros WHERE codigo=?", (codigo,))
        con.commit()
        con.close()
        listar(tree, status_bar)

# ================= CADASTRO =================

def tela_cadastro(root, tree, status_bar, dados=None):
    win = tk.Toplevel(root)
    win.title("Cadastro de Mensageiro")
    win.geometry("420x300")
    win.transient(root)
    win.grab_set()

    campos = ["Nome", "Turma", "Supervisor", "Status", "Visivel"]
    entradas = {}

    for i, campo in enumerate(campos):
        tk.Label(win, text=campo).grid(row=i, column=0, padx=10, pady=6, sticky="w")
        e = tk.Entry(win, width=30)
        e.grid(row=i, column=1, padx=10, pady=6)
        entradas[campo.lower()] = e

    codigo = None

    if dados:
        codigo = dados[0]
        for i, k in enumerate(entradas):
            entradas[k].insert(0, dados[i+1])

    def salvar_click():
        if not entradas["nome"].get().strip():
            messagebox.showwarning("Validação", "Informe o nome.")
            return

        salvar(tree, status_bar, {
            "codigo": codigo,
            "nome": entradas["nome"].get(),
            "turma": entradas["turma"].get(),
            "supervisor": entradas["supervisor"].get(),
            "status": entradas["status"].get().upper(),
            "visivel": entradas["visivel"].get()
        })
        win.destroy()

    tk.Button(win, text="Salvar", width=15, command=salvar_click)\
        .grid(row=len(campos)+1, column=0, columnspan=2, pady=15)

# ================= TELA PRINCIPAL =================

def tela_mensageiros(root):
    criar_tabela()

    win = tk.Toplevel(root)
    win.title("Mensageiros")
    win.geometry("950x550")
    win.transient(root)
    win.grab_set()

    # ---- GRID ----
    frame_grid = tk.Frame(win)
    frame_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    colunas = ("codigo", "nome", "turma", "supervisor", "status", "visivel")
    tree = ttk.Treeview(frame_grid, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=140, anchor="center")

    tree.tag_configure("ativo", background="#E8F5E9")
    tree.tag_configure("inativo", background="#FFEBEE")

    scrollbar = ttk.Scrollbar(frame_grid, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ---- STATUS BAR ----
    status_bar = tk.Label(win, bg="#D6D6E5", anchor="w",
                          font=("Segoe UI", 9, "bold"))
    status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # ---- BOTÕES ----
    frame_btn = tk.Frame(win)
    frame_btn.pack(fill=tk.X, padx=10)

    tk.Button(frame_btn, text="Inclusão",
              command=lambda: tela_cadastro(root, tree, status_bar)).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Alteração",
              command=lambda: tela_cadastro(root, tree, status_bar, tree.item(tree.focus())["values"])
              if tree.focus() else messagebox.showwarning("Aviso","Selecione um registro")
              ).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Exclusão",
              command=lambda: excluir(tree, status_bar)).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Saída", command=win.destroy).pack(side=tk.RIGHT, padx=10)

    # ---- PESQUISA ----
    frame_pesq = tk.Frame(win)
    frame_pesq.pack(fill=tk.X, padx=10, pady=6)

    pesquisa_var = tk.StringVar()
    somente_ativos = tk.BooleanVar()

    tk.Label(frame_pesq, text="Pesquisa:").pack(side=tk.LEFT)
    tk.Entry(frame_pesq, textvariable=pesquisa_var, width=30).pack(side=tk.LEFT, padx=5)

    tk.Checkbutton(frame_pesq, text="Só Ativos", variable=somente_ativos).pack(side=tk.LEFT)

    tk.Button(frame_pesq, text="Pesquisar",
              command=lambda: listar(tree, status_bar, pesquisa_var.get(), somente_ativos.get())
              ).pack(side=tk.LEFT)

    listar(tree, status_bar)

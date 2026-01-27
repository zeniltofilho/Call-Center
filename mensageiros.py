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

# ================= CRUD =================

def listar(tree, filtro=""):
    for item in tree.get_children():
        tree.delete(item)

    con = conectar()
    cur = con.cursor()

    if filtro:
        cur.execute("""
            SELECT * FROM mensageiros
            WHERE codigo LIKE ? OR nome LIKE ?
        """, (f"%{filtro}%", f"%{filtro}%"))
    else:
        cur.execute("SELECT * FROM mensageiros")

    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    con.close()

def salvar(tree, dados):
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
    listar(tree)

def excluir(tree):
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
        listar(tree)

# ================= TELA CADASTRO =================

def tela_cadastro(root, tree, dados=None):
    win = tk.Toplevel(root)
    win.title("Cadastro de Mensageiro")
    win.geometry("420x300")
    win.transient(root)
    win.grab_set()
    win.focus_force()

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
        entradas["nome"].insert(0, dados[1])
        entradas["turma"].insert(0, dados[2])
        entradas["supervisor"].insert(0, dados[3])
        entradas["status"].insert(0, dados[4])
        entradas["visivel"].insert(0, dados[5])

    def salvar_click():
        if not entradas["nome"].get().strip():
            messagebox.showwarning("Validação", "Informe o nome.")
            return

        salvar(tree, {
            "codigo": codigo,
            "nome": entradas["nome"].get(),
            "turma": entradas["turma"].get(),
            "supervisor": entradas["supervisor"].get(),
            "status": entradas["status"].get(),
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
    win.focus_force()

    # ---- GRID ----
    frame_grid = tk.Frame(win)
    frame_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    colunas = ("codigo", "nome", "turma", "supervisor", "status", "visivel")

    tree = ttk.Treeview(frame_grid, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=140, anchor="center")

    scrollbar = ttk.Scrollbar(frame_grid, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ---- BOTÕES ----
    frame_btn = tk.Frame(win)
    frame_btn.pack(fill=tk.X, padx=10)

    tk.Button(frame_btn, text="Inclusão",
              command=lambda: tela_cadastro(root, tree)).pack(side=tk.LEFT, padx=5)

    def alterar():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um registro para alterar.")
            return
        tela_cadastro(root, tree, tree.item(item)["values"])

    tk.Button(frame_btn, text="Alteração", command=alterar).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Exclusão",
              command=lambda: excluir(tree)).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Saída", command=win.destroy)\
        .pack(side=tk.RIGHT, padx=10)

    # ---- PESQUISA ----
    frame_pesq = tk.Frame(win)
    frame_pesq.pack(fill=tk.X, padx=10, pady=6)

    tk.Label(frame_pesq, text="Pesquisa:").pack(side=tk.LEFT)

    pesquisa_var = tk.StringVar()
    tk.Entry(frame_pesq, textvariable=pesquisa_var, width=30)\
        .pack(side=tk.LEFT, padx=5)

    tk.Button(frame_pesq, text="Pesquisar",
              command=lambda: listar(tree, pesquisa_var.get()))\
        .pack(side=tk.LEFT)

    listar(tree)

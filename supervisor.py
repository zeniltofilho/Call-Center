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
        CREATE TABLE IF NOT EXISTS supervisores (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turno TEXT,
            status TEXT
        )
    """)
    con.commit()
    con.close()

# ================= CRUD =================

def listar(tree, filtro=""):
    tree.delete(*tree.get_children())

    con = conectar()
    cur = con.cursor()

    if filtro:
        cur.execute("""
            SELECT * FROM supervisores
            WHERE codigo LIKE ? OR nome LIKE ?
        """, (f"%{filtro}%", f"%{filtro}%"))
    else:
        cur.execute("SELECT * FROM supervisores")

    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    con.close()

def salvar(tree, dados):
    con = conectar()
    cur = con.cursor()

    if dados["codigo"]:
        cur.execute("""
            UPDATE supervisores
            SET nome=?, turno=?, status=?
            WHERE codigo=?
        """, (dados["nome"], dados["turno"], dados["status"], dados["codigo"]))
    else:
        cur.execute("""
            INSERT INTO supervisores (nome, turno, status)
            VALUES (?, ?, ?)
        """, (dados["nome"], dados["turno"], dados["status"]))

    con.commit()
    con.close()
    listar(tree)

def excluir(tree):
    item = tree.focus()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um registro.")
        return

    codigo = tree.item(item)["values"][0]

    if messagebox.askyesno("Confirmação", "Deseja excluir este supervisor?"):
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM supervisores WHERE codigo=?", (codigo,))
        con.commit()
        con.close()
        listar(tree)

# ================= CADASTRO =================

def tela_cadastro(root, tree, dados=None):
    win = tk.Toplevel(root)
    win.title("Cadastro de Supervisor")
    win.geometry("350x220")
    win.transient(root)
    win.grab_set()

    tk.Label(win, text="Nome").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    e_nome = tk.Entry(win, width=30)
    e_nome.grid(row=0, column=1)

    tk.Label(win, text="Turno").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    e_turno = tk.Entry(win, width=30)
    e_turno.grid(row=1, column=1)

    tk.Label(win, text="Status").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    e_status = tk.Entry(win, width=30)
    e_status.grid(row=2, column=1)

    codigo = None

    if dados:
        codigo = dados[0]
        e_nome.insert(0, dados[1])
        e_turno.insert(0, dados[2])
        e_status.insert(0, dados[3])

    def salvar_click():
        if not e_nome.get().strip():
            messagebox.showwarning("Validação", "Informe o nome.")
            return

        salvar(tree, {
            "codigo": codigo,
            "nome": e_nome.get(),
            "turno": e_turno.get(),
            "status": e_status.get()
        })
        win.destroy()

    tk.Button(win, text="Salvar", width=15, command=salvar_click)\
        .grid(row=4, column=0, columnspan=2, pady=15)

# ================= TELA PRINCIPAL =================

def tela_supervisor(root):
    criar_tabela()

    win = tk.Toplevel(root)
    win.title("Supervisores")
    win.geometry("800x500")
    win.transient(root)
    win.grab_set()

    frame = tk.Frame(win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    colunas = ("codigo", "nome", "turno", "status")

    tree = ttk.Treeview(frame, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150, anchor="center")

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame_btn = tk.Frame(win)
    frame_btn.pack(fill=tk.X, padx=10)

    tk.Button(frame_btn, text="Inclusão",
              command=lambda: tela_cadastro(root, tree)).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Alteração",
              command=lambda: tela_cadastro(
                  root, tree, tree.item(tree.focus())["values"]
              ) if tree.focus() else messagebox.showwarning(
                  "Aviso", "Selecione um registro.")
              ).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Exclusão",
              command=lambda: excluir(tree)).pack(side=tk.LEFT, padx=5)

    tk.Button(frame_btn, text="Saída", command=win.destroy)\
        .pack(side=tk.RIGHT)

    listar(tree)

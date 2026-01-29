import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_NAME


def tela_operadores(root):
    win = tk.Toplevel(root)
    win.title("Operadores")
    win.geometry("900x400")

    # ---------- TABELA ----------
    colunas = (
        "codigo", "nome", "turno", "turma",
        "supervisor", "sts", "oper", "premio",
        "comissao", "rep", "mvf", "mvd"
    )

    tree = ttk.Treeview(win, columns=colunas, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    # Cabeçalhos
    tree.heading("codigo", text="Código")
    tree.heading("nome", text="Nome")
    tree.heading("turno", text="Turno")
    tree.heading("turma", text="Turma")
    tree.heading("supervisor", text="Supervisor")
    tree.heading("sts", text="Sts")
    tree.heading("oper", text="%Oper")
    tree.heading("premio", text="Prêmio/Desc")
    tree.heading("comissao", text="Valor Comis.")
    tree.heading("rep", text="Rep")
    tree.heading("mvf", text="M.V.F.")
    tree.heading("mvd", text="M.V.D.")

    # Largura das colunas
    for col in colunas:
        tree.column(col, width=80, anchor="center")

    tree.column("nome", width=150, anchor="w")

    # ---------- FUNÇÕES ----------
    def carregar_dados():
        tree.delete(*tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""
            SELECT id, nome, turno, turma, supervisor,
                   sts, oper, premio, comissao, rep, mvf, mvd
            FROM operadores
        """)

        for row in c.fetchall():
            tree.insert("", tk.END, values=row)

        conn.close()

    def incluir():
        tela_inclusao()

    # ---------- TELA DE INCLUSÃO ----------
    def tela_inclusao():
        top = tk.Toplevel(win)
        top.title("Incluir Operador")
        top.geometry("300x200")

        tk.Label(top, text="Nome").pack()
        entry_nome = tk.Entry(top)
        entry_nome.pack(fill=tk.X, padx=10)

        def salvar():
            if not entry_nome.get():
                return

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute(
                "INSERT INTO operadores (nome) VALUES (?)",
                (entry_nome.get(),)
            )
            conn.commit()
            conn.close()

            carregar_dados()
            top.destroy()
            messagebox.showinfo("Sucesso", "Operador cadastrado")

        tk.Button(top, text="Salvar", command=salvar).pack(pady=10)

    # ---------- BOTÕES ----------
    frame_botoes = tk.Frame(win)
    frame_botoes.pack(fill=tk.X)

    tk.Button(frame_botoes, text="Inclusão",
              command=incluir).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Excluir").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Alteração").pack(side=tk.LEFT, padx=5)

    carregar_dados()

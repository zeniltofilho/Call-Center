import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_NAME

def tela_operadores(root):
    win = tk.Toplevel(root)
    win.title("Operadores")
    win.geometry("950x450")
    win.configure(bg="#ECECF1")

    # ================= ESTILO TABELA =================
    style = ttk.Style()
    style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    # ================= TABELA =================
    colunas = (
        "codigo", "nome", "turno", "turma",
        "supervisor", "sts", "oper", "premio",
        "comissao", "rep", "mvf", "mvd"
    )

    frame_tabela = tk.Frame(win, bg="#ECECF1")
    frame_tabela.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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

    for col in colunas:
        tree.column(col, width=85, anchor="center")

    tree.column("nome", width=160, anchor="w")

    # ================= BANCO =================
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
        status.config(text=f"{len(tree.get_children())} operadores cadastrados")

    # ================= INCLUSÃO =================
    def incluir():
        top = tk.Toplevel(win)
        top.title("Incluir Operador")
        top.geometry("300x220")
        top.configure(bg="#ECECF1")

        tk.Label(top, text="Nome", bg="#ECECF1").pack(pady=4)
        entry_nome = tk.Entry(top)
        entry_nome.pack(fill=tk.X, padx=10)

        def salvar():
            if not entry_nome.get():
                messagebox.showwarning("Atenção", "Digite o nome")
                return

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO operadores (nome) VALUES (?)",
                      (entry_nome.get(),))
            conn.commit()
            conn.close()

            carregar_dados()
            top.destroy()
            messagebox.showinfo("Sucesso", "Operador cadastrado")

        tk.Button(
            top, text="Salvar", command=salvar,
            bg="#3949AB", fg="white", relief="flat"
        ).pack(pady=12)

    # ================= EXCLUIR =================
    def excluir():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um operador")
            return

        cod = tree.item(sel[0])['values'][0]

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM operadores WHERE id = ?", (cod,))
        conn.commit()
        conn.close()

        carregar_dados()
        messagebox.showinfo("OK", "Operador excluído")

    # ================= BOTÕES SUPERIORES =================
    frame_botoes = tk.Frame(win, bg="#E0E0E8")
    frame_botoes.pack(fill=tk.X)

    def botao(txt, cmd, cor="#2E3A59"):
        return tk.Button(
            frame_botoes, text=txt, width=14, command=cmd,
            bg=cor, fg="white", relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2", activebackground="#3F51B5"
        )

    botao("Inclusão", incluir).pack(side=tk.LEFT, padx=5, pady=6)
    botao("Excluir", excluir, "#B71C1C").pack(side=tk.LEFT, padx=5)
    botao("Alteração", lambda: messagebox.showinfo("Alterar", "Alterar operador")).pack(side=tk.LEFT, padx=5)

    # ================= STATUS BAR =================
    status = tk.Label(win, text="Carregando operadores...", anchor="w",
                      bg="#D6D6E5", font=("Segoe UI", 8))
    status.pack(fill=tk.X, side=tk.BOTTOM)

    carregar_dados()

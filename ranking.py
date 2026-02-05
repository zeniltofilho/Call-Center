import tkinter as tk
from tkinter import ttk
from database import conectar
import datetime


def tela_ranking(root):
    win = tk.Toplevel(root)
    win.title("Ranking - Metas Batidas")
    win.geometry("1050x560")
    win.configure(bg="#ECECF1")
    win.transient(root)
    win.grab_set()

    TelaRanking(win)


class TelaRanking:
    def __init__(self, root):
        self.root = root

        self.mes_atual = datetime.datetime.now().strftime("%Y-%m")

        self.criar_topo()
        self.criar_tabela()
        self.carregar_ranking()

    def criar_topo(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.X, padx=10, pady=(10, 6))

        tk.Label(
            frame,
            text="Ranking (Mês atual)",
            bg="#ECECF1",
            fg="#1A237E",
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT)

        self.lbl_mes = tk.Label(
            frame,
            text=f"Mês: {self.mes_atual}",
            bg="#ECECF1",
            fg="#333",
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_mes.pack(side=tk.RIGHT)

    def criar_tabela(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        colunas = ("pos", "operador", "qtd", "valor")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.heading("pos", text="#")
        self.tree.heading("operador", text="Operador")
        self.tree.heading("qtd", text="Qtd")
        self.tree.heading("valor", text="Valor (R$)")

        self.tree.column("pos", width=60, anchor="center")
        self.tree.column("operador", width=320, anchor="w")
        self.tree.column("qtd", width=120, anchor="center")
        self.tree.column("valor", width=150, anchor="center")

    def carregar_ranking(self):
        self.tree.delete(*self.tree.get_children())

        con = conectar()
        cur = con.cursor()

        # soma por operador no mês atual
        cur.execute("""
            SELECT o.nome,
                   SUM(p.quantidade) as total_qtd,
                   SUM(p.valor) as total_valor
            FROM producao p
            JOIN operadores o ON o.id = p.operador_id
            WHERE p.data LIKE ?
            GROUP BY o.nome
            ORDER BY total_valor DESC
        """, (self.mes_atual + "%",))

        dados = cur.fetchall()
        con.close()

        for i, row in enumerate(dados, start=1):
            nome, qtd, valor = row
            self.tree.insert("", tk.END, values=(i, nome, qtd or 0, f"{(valor or 0):.2f}"))

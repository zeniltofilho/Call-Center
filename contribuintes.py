import tkinter as tk
from tkinter import ttk, messagebox
import csv
from cadastroContribuinte import tela_cadastro_contribuintes
from boletos import tela_boletos
from doacoes import tela_doacoes
from recibo import tela_recibo


def tela_contribuintes(root):
    janela = tk.Toplevel(root)
    janela.title("Contribuintes")
    janela.geometry("1100x650")
    janela.configure(bg="#dcdcdc")
    janela.transient(root)
    janela.grab_set()

    App(janela)


class App:

    def __init__(self, root):
        self.root = root

        self.create_top_bar()
        self.create_table()
        self.create_actions_bar()
        self.create_bottom_tabs()

    # ---------------- TOPO ----------------
    def create_top_bar(self):
        frame = tk.Frame(self.root, bg="#cfcfcf", pady=5)
        frame.pack(fill="x")

        tk.Button(frame, text="Cadastrar Doações", command=self.btn_doacoes).pack(side="left", padx=5)
        tk.Button(frame, text="Exportar", command=self.btn_exportar).pack(side="left", padx=5)
        tk.Button(frame, text="Novo", command=self.btn_novo).pack(side="left", padx=5)

        tk.Label(frame, text="Pesq.:", bg="#cfcfcf").pack(side="left", padx=(20, 2))
        self.search_entry = tk.Entry(frame, width=30)
        self.search_entry.pack(side="left")

        self.combo_filter = ttk.Combobox(frame, values=["Código", "Nome", "Telefone"], width=12)
        self.combo_filter.current(0)
        self.combo_filter.pack(side="left", padx=5)

        self.combo_status = ttk.Combobox(frame, values=["Todos", "Ativo", "Inativo"], width=10)
        self.combo_status.current(0)
        self.combo_status.pack(side="left", padx=5)

        tk.Button(frame, text="Vendas").pack(side="right", padx=10)

    # ---------------- TABELA ----------------
    def create_table(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ["codigo", "dt_status", "nome", "tipo", "status", "telefone"]

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_cliente_select)

    # ---------------- AÇÕES ----------------
    def create_actions_bar(self):
        frame = tk.Frame(self.root, bg="#e5e5e5", pady=5)
        frame.pack(fill="x")

        tk.Button(frame, text="Inclusão", command=self.btn_inclusao).pack(side="left", padx=4)
        tk.Button(frame, text="Alteração", command=self.btn_alteracao).pack(side="left", padx=4)
        tk.Button(frame, text="Exclusão", command=self.btn_exclusao).pack(side="left", padx=4)

        tk.Button(frame, text="Recibo", command=self.btn_recibo).pack(side="left", padx=(50, 4))
        tk.Button(frame, text="Bol/Déb", command=self.btn_boleto).pack(side="left", padx=4)
        tk.Button(frame, text="Todos", command=self.btn_todos).pack(side="left", padx=4)
        tk.Button(frame, text="Cartão", command=self.btn_cartao).pack(side="left", padx=4)

    # ---------------- ABAS ----------------
    def create_bottom_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=False, padx=5, pady=5)

        tab_recibos = tk.Frame(notebook)
        notebook.add(tab_recibos, text="Recibos")

        self.tree_recibos = ttk.Treeview(
            tab_recibos,
            columns=("data", "valor"),
            show="headings"
        )
        self.tree_recibos.heading("data", text="Data")
        self.tree_recibos.heading("valor", text="Valor")
        self.tree_recibos.pack(fill="both", expand=True)

    # ---------------- UTIL ----------------
    def on_cliente_select(self, event):
        self.tree_recibos.delete(*self.tree_recibos.get_children())

    def cliente_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um cliente.")
            return None
        return self.tree.item(sel[0])["values"]

    # ---------------- BOTÕES ----------------
    def btn_inclusao(self):
        tela_cadastro_contribuintes(self.root)

    def btn_alteracao(self):
        cli = self.cliente_selecionado()
        if cli:
            tela_cadastro_contribuintes(self.root, cli)

    def btn_exclusao(self):
        sel = self.tree.selection()
        if not sel:
            return

        if messagebox.askyesno("Excluir", "Deseja excluir este contribuinte?"):
            self.tree.delete(sel[0])
            self.tree_recibos.delete(*self.tree_recibos.get_children())

    def btn_recibo(self):
        cli = self.cliente_selecionado()
        if not cli:
            return

        id_contrib = cli[0]
        nome = cli[2]

        tela_recibo(self.root, id_contrib, nome)

    def btn_boleto(self):
        cli = self.cliente_selecionado()
        if cli:
            tela_boletos(self.root, cli)

    def btn_todos(self):
        self.tree.selection_remove(self.tree.selection())
        self.tree_recibos.delete(*self.tree_recibos.get_children())

    def btn_cartao(self):
        cli = self.cliente_selecionado()
        if cli:
            messagebox.showinfo("Pagamento", f"Pagamento por cartão: {cli[2]}")

    def btn_doacoes(self):
        cli = self.cliente_selecionado()
        if cli:
            tela_doacoes(self.root, cli)

    def btn_exportar(self):
        if not self.tree.get_children():
            messagebox.showwarning("Exportar", "Nenhum dado para exportar.")
            return

        with open("contribuintes.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Código", "Data", "Nome", "Tipo", "Status", "Telefone"])
            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item)["values"])

        messagebox.showinfo("Exportar", "Arquivo contribuintes.csv gerado com sucesso!")

    def btn_novo(self):
        self.tree.selection_remove(self.tree.selection())
        tela_cadastro_contribuinte(self.root)

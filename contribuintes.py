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
    janela.configure(bg="#ECECF1")
    janela.transient(root)
    janela.grab_set()

    App(janela)


class App:

    def __init__(self, root):
        self.root = root

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.create_top_bar()
        self.create_table()
        self.create_actions_bar()
        self.create_bottom_tabs()

    # ---------------- TOPO ----------------
    def create_top_bar(self):
        frame = tk.Frame(self.root, bg="#DADAE3", pady=6)
        frame.pack(fill="x")

        def btn(txt, cmd):
            return tk.Button(frame, text=txt, command=cmd, bg="#144A88",
                             fg="white", relief="flat", font=("Segoe UI", 9, "bold"),
                             cursor="hand2", padx=10)

        btn("Cadastrar Doações", self.btn_doacoes).pack(side="left", padx=5)
        btn("Exportar", self.btn_exportar).pack(side="left", padx=5)
        btn("Novo", self.btn_novo).pack(side="left", padx=5)

        tk.Label(frame, text="Pesquisar:", bg="#DADAE3", font=("Segoe UI", 9)).pack(side="left", padx=(20, 5))
        self.search_entry = tk.Entry(frame, width=30)
        self.search_entry.pack(side="left")

        self.combo_filter = ttk.Combobox(frame, values=["Código", "Nome", "Telefone"], width=12)
        self.combo_filter.current(0)
        self.combo_filter.pack(side="left", padx=5)

        self.combo_status = ttk.Combobox(frame, values=["Todos", "Ativo", "Inativo"], width=10)
        self.combo_status.current(0)
        self.combo_status.pack(side="left", padx=5)

        btn("Vendas", lambda: None).pack(side="right", padx=10)

    # ---------------- TABELA ----------------
    def create_table(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=8, pady=6)

        columns = ["codigo", "dt_status", "nome", "tipo", "status", "telefone"]

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=130, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_cliente_select)

    # ---------------- AÇÕES ----------------
    def create_actions_bar(self):
        frame = tk.Frame(self.root, bg="#DADAE3", pady=6)
        frame.pack(fill="x")

        def btn(txt, cmd):
            return tk.Button(frame, text=txt, command=cmd, bg="#144A88",
                             fg="white", relief="flat", font=("Segoe UI", 9, "bold"),
                             cursor="hand2", padx=8)

        btn("Inclusão", self.btn_inclusao).pack(side="left", padx=4)
        btn("Alteração", self.btn_alteracao).pack(side="left", padx=4)
        btn("Exclusão", self.btn_exclusao).pack(side="left", padx=4)

        btn("Recibo", self.btn_recibo).pack(side="left", padx=(40, 4))
        btn("Bol/Déb", self.btn_boleto).pack(side="left", padx=4)
        btn("Todos", self.btn_todos).pack(side="left", padx=4)
        btn("Cartão", self.btn_cartao).pack(side="left", padx=4)

    # ---------------- ABAS ----------------
    def create_bottom_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", padx=6, pady=6)

        tab_recibos = tk.Frame(notebook)
        notebook.add(tab_recibos, text="Recibos")

        self.tree_recibos = ttk.Treeview(tab_recibos, columns=("data", "valor"), show="headings")
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
        if sel and messagebox.askyesno("Excluir", "Deseja excluir este contribuinte?"):
            self.tree.delete(sel[0])
            self.tree_recibos.delete(*self.tree_recibos.get_children())

    def btn_recibo(self):
        cli = self.cliente_selecionado()
        if cli:
            tela_recibo(self.root, cli[0], cli[2])

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
        tela_cadastro_contribuintes(self.root)

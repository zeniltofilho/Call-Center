import tkinter as tk
from tkinter import ttk, messagebox
from cadastroContribuinte import tela_cadastro_contribuinte
from boletos import tela_boletos
from doacoes import tela_doacoes

def tela_contribuintes(root):

    class App(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)

            self.title("Contribuintes")
            self.geometry("1100x650")
            self.configure(bg="#dcdcdc")

            self.recibos_por_cliente = self.gerar_recibos_fake()

            self.create_top_bar()
            self.create_table()
            self.create_actions_bar()
            self.create_bottom_tabs()

        # ---------------- DADOS FAKE ----------------
        def gerar_recibos_fake(self):
            dados = {}
            for cliente_id in range(1, 21):
                recibos = []
                for i in range(1, 6):
                    recibos.append((
                        "07/01/2026", "06/01/2026", f"R$ {i*10},00", "Impresso",
                        f"{cliente_id}{i}2475218", "Ent. Prévia", 38,
                        "16/12/2025", "07/01/2026", ""
                    ))
                dados[cliente_id] = recibos
            return dados

        # ---------------- TOPO ----------------
        def create_top_bar(self):
            frame = tk.Frame(self, bg="#cfcfcf", pady=5)
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
            frame = tk.Frame(self)
            frame.pack(fill="both", expand=True, padx=5, pady=5)

            columns = ["codigo", "dt_status", "nome", "tipo", "status", "telefone"]

            self.tree = ttk.Treeview(frame, columns=columns, show="headings")

            for col in columns:
                self.tree.heading(col, text=col.upper())
                self.tree.column(col, width=120, anchor="center")

            self.tree.pack(fill="both", expand=True)

            self.tree.bind("<<TreeviewSelect>>", self.on_cliente_select)

            for i in range(20):
                self.tree.insert("", "end", values=(i+1, "06/01/2026", f"CLIENTE {i+1}", "E", "Ativo", "(11)99999-0000"))

        # ---------------- BARRA AÇÕES ----------------
        def create_actions_bar(self):
            frame = tk.Frame(self, bg="#e5e5e5", pady=5)
            frame.pack(fill="x")

            tk.Button(frame, text="Inclusão", command=self.btn_inclusao).pack(side="left", padx=4)
            tk.Button(frame, text="Alteração", command=self.btn_alteracao).pack(side="left", padx=4)
            tk.Button(frame, text="Exclusão", command=self.btn_exclusao).pack(side="left", padx=4)
            tk.Button(frame, text="Recibo", command=self.btn_recibo).pack(side="left", padx=(50,4))
            tk.Button(frame, text="Bol/Déb", command=self.btn_boleto).pack(side="left", padx=4)
            tk.Button(frame, text="Todos", command=self.btn_todos).pack(side="left", padx=4)
            tk.Button(frame, text="Cartão", command=self.btn_cartao).pack(side="left", padx=4)

        # ---------------- ABAS ----------------
        def create_bottom_tabs(self):
            notebook = ttk.Notebook(self)
            notebook.pack(fill="both", expand=False, padx=5, pady=5)

            tab_recibos = tk.Frame(notebook)
            notebook.add(tab_recibos, text="Recibos")

            self.tree_recibos = ttk.Treeview(tab_recibos, columns=("data", "valor"), show="headings")
            self.tree_recibos.heading("data", text="Data")
            self.tree_recibos.heading("valor", text="Valor")
            self.tree_recibos.pack(fill="both", expand=True)

        # ---------------- EVENTOS ----------------
        def on_cliente_select(self, event):
            sel = self.tree.selection()
            if not sel:
                return

            cliente_id = self.tree.item(sel)["values"][0]
            self.carregar_recibos(cliente_id)

        def carregar_recibos(self, cliente_id):
            self.tree_recibos.delete(*self.tree_recibos.get_children())

            for rec in self.recibos_por_cliente.get(cliente_id, []):
                self.tree_recibos.insert("", "end", values=(rec[0], rec[2]))

        # ---------------- BOTÕES ----------------
        def cliente_selecionado(self):
            sel = self.tree.selection()
            if not sel:
                messagebox.showwarning("Atenção", "Selecione um cliente.")
                return None
            return self.tree.item(sel)["values"]

        def btn_inclusao(self):
            tela_cadastro_contribuinte(self)

        def btn_alteracao(self):
            cli = self.cliente_selecionado()
            if cli:
                messagebox.showinfo("Alteração", cli[2])

        def btn_exclusao(self):
            messagebox.showinfo("Exclusão", "Excluído.")

        def btn_recibo(self):
            messagebox.showinfo("Recibo", "Recibo.")

        def btn_boleto (self):
            tela_boletos(self)

        def btn_todos(self):
            messagebox.showinfo("Todos", "Todos.")

        def btn_cartao(self):
            messagebox.showinfo("Cartão", "Cartão.")        

        def btn_doacoes(self):
            tela_doacoes(self)

        def btn_exportar(self):
            messagebox.showinfo("Exportar", "Exportado.")

        def btn_novo(self):
            messagebox.showinfo("Novo", "Novo registro.")

    App(root)

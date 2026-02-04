import tkinter as tk
from tkinter import ttk, messagebox
import csv
import sqlite3
from datetime import datetime
from database import DB_NAME
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

        self.atualizar_tabela()

    # ---------------- BANCO ----------------
    def conectar(self):
        return sqlite3.connect(DB_NAME)

    def garantir_tabela_contribuintes(self):
        with self.conectar() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contribuintes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo INTEGER UNIQUE,
                    data TEXT,
                    tipo TEXT,
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
                    observacoes TEXT,
                    operador_atual TEXT,
                    operador_fixo TEXT,
                    setor TEXT,
                    data_vl TEXT
                )
            """)
            # Garante compatibilidade com bancos antigos
            try: cur.execute("ALTER TABLE contribuintes ADD COLUMN data TEXT")
            except: pass
            try: cur.execute("ALTER TABLE contribuintes ADD COLUMN tipo TEXT")
            except: pass

    def garantir_tabela_recibos(self):
        with self.conectar() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS recibos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contrib INTEGER,
                    vencimento TEXT,
                    valor TEXT
                )
            """)

    # ---------------- UTIL ----------------
    def cliente_selecionado(self, silencioso=False):
        sel = self.tree.selection()
        if not sel:
            if not silencioso:
                messagebox.showwarning("Seleção", "Selecione um contribuinte na lista.")
            return None
        return self.tree.item(sel[0])["values"]

    # ---------------- TOPO ----------------
    def create_top_bar(self):
        frame = tk.Frame(self.root, bg="#DADAE3", pady=6)
        frame.pack(fill="x")

        def btn(txt, cmd):
            return tk.Button(
                frame, text=txt, command=cmd, bg="#144A88",
                fg="white", relief="flat", font=("Segoe UI", 9, "bold"),
                cursor="hand2", padx=10
            )

        btn("Cadastrar Doações", self.btn_doacoes).pack(side="left", padx=5)
        btn("Exportar", self.btn_exportar).pack(side="left", padx=5)
        btn("Novo", self.btn_novo).pack(side="left", padx=5)

        tk.Label(frame, text="Pesquisar:", bg="#DADAE3", font=("Segoe UI", 9)).pack(side="left", padx=(20, 5))

        self.search_entry = tk.Entry(frame, width=30)
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        self.combo_filter = ttk.Combobox(frame, values=["Código", "Nome", "Telefone"], width=12, state="readonly")
        self.combo_filter.current(1)
        self.combo_filter.pack(side="left", padx=5)
        self.combo_filter.bind("<<ComboboxSelected>>", lambda e: self.atualizar_tabela())

        self.combo_status = ttk.Combobox(frame, values=["Todos", "Ativo", "Inativo"], width=10, state="readonly")
        self.combo_status.current(0)
        self.combo_status.pack(side="left", padx=5)
        self.combo_status.bind("<<ComboboxSelected>>", lambda e: self.atualizar_tabela())

        btn("Vendas", lambda: None).pack(side="right", padx=10)

    # ---------------- TABELA ----------------
    def create_table(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=8, pady=6)

        columns = ["Codigo", "Data", "Nome", "Tipo", "Status", "Telefone", 
                   "Operador Atual", "Operador Fixo", "Setor", "Valor", "Rua", "Numero", "Email"]

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        headers = {
            "Codigo": "Código",
            "Data": "Data",
            "Nome": "Nome",
            "Tipo": "Tipo",
            "Status": "Status",
            "Telefone": "Telefone",
            "Operador Atual": "Operador Atual",
            "Operador Fixo": "Operador Fixo",
            "Setor": "Setor",
            "Valor": "Último VL",
            "Rua": "Rua",
            "Numero": "Número",
            "Email": "E-mail"
        }

        widths = {col: 80 for col in columns}
        widths["Nome"] = 150
        widths["Rua"] = 120
        widths["Email"] = 150
        widths["Valor"] = 100

        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], anchor="center")

        self.tree.column("Nome", anchor="w")
        self.tree.column("Rua", anchor="w")
        self.tree.column("Email", anchor="w")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_cliente_select)

    # ---------------- AÇÕES ----------------
    def create_actions_bar(self):
        frame = tk.Frame(self.root, bg="#DADAE3", pady=6)
        frame.pack(fill="x")

        def btn(txt, cmd):
            return tk.Button(
                frame, text=txt, command=cmd, bg="#144A88",
                fg="white", relief="flat", font=("Segoe UI", 9, "bold"),
                cursor="hand2", padx=8
            )

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

        tab_recibos = tk.Frame(notebook, bg="#ECECF1")
        notebook.add(tab_recibos, text="Recibos")

        frame_lista = tk.Frame(tab_recibos, bg="#ECECF1")
        frame_lista.pack(fill="x", padx=10, pady=10)

        self.tree_recibos = ttk.Treeview(
            frame_lista,
            columns=("data", "valor"),
            show="headings",
            height=6
        )

        self.tree_recibos.heading("data", text="Data")
        self.tree_recibos.heading("valor", text="Valor")

        self.tree_recibos.column("data", width=140, anchor="center")
        self.tree_recibos.column("valor", width=200, anchor="center")

        self.tree_recibos.pack(side="left", fill="x", expand=False)

        scroll = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_recibos.yview)
        self.tree_recibos.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

    # ---------------- CARREGAR DO BANCO ----------------
    def buscar_contribuintes(self):
        self.garantir_tabela_contribuintes()
        self.garantir_tabela_recibos()

        with self.conectar() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT 
                    c.codigo, c.data, c.nome, c.tipo, c.status, c.telefone1,
                    c.operador_atual, c.operador_fixo, c.setor,
                    (SELECT valor FROM recibos r WHERE r.contrib = c.codigo ORDER BY r.vencimento DESC LIMIT 1) AS ultimo_vl,
                    c.rua, c.numero, c.email
                FROM contribuintes c
                ORDER BY CAST(c.codigo AS INTEGER) ASC
            """)
            dados = cur.fetchall()

        # Formata data e valor
        dados_formatados = []
        for row in dados:
            codigo, data, nome, tipo, st, tel, op_atual, op_fixo, setor, vl, rua, numero, email = row

            # Formata data de YYYY-MM-DD para DD/MM/YYYY
            if data:
                try:
                    data = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    pass

            # Formata valor em R$
            if vl:
                try:
                    vl_float = float(str(vl).replace(",", "."))
                    vl = f"R$ {vl_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except:
                    vl = "R$ 0,00"
            else:
                vl = "R$ 0,00"

            dados_formatados.append((codigo, data, nome, tipo, st, tel, op_atual, op_fixo, setor, vl, rua, numero, email))

        return dados_formatados

    # ---------------- RECIBOS ----------------
    def carregar_recibos_contribuinte(self, codigo_contribuinte):
        self.tree_recibos.delete(*self.tree_recibos.get_children())

        try:
            with self.conectar() as con:
                cur = con.cursor()
                cur.execute("""
                    SELECT vencimento, valor
                    FROM recibos
                    WHERE contrib = ?
                    ORDER BY vencimento DESC
                """, (codigo_contribuinte,))
                dados = cur.fetchall()

            for vencimento, valor in dados:
                try:
                    valor_float = float(str(valor).replace(",", "."))
                except:
                    valor_float = 0

                valor_formatado = f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                self.tree_recibos.insert("", "end", values=(vencimento, valor_formatado))

        except Exception as e:
            print("Erro ao carregar recibos:", e)

    # ---------------- FILTRO/PESQUISA ----------------
    def atualizar_tabela(self):
        texto = self.search_entry.get().strip().lower()
        filtro = self.combo_filter.get()
        status = self.combo_status.get()

        self.tree.delete(*self.tree.get_children())
        self.tree_recibos.delete(*self.tree_recibos.get_children())

        dados = self.buscar_contribuintes()

        for row in dados:
            codigo, data, nome, tipo, st, tel, op_atual, op_fixo, setor, vl, rua, numero, email = row

            if status != "Todos" and st != status:
                continue

            if texto:
                if filtro == "Código":
                    alvo = str(codigo).lower()
                elif filtro == "Nome":
                    alvo = (nome or "").lower()
                else:
                    alvo = (tel or "").lower()

                if texto not in alvo:
                    continue

            self.tree.insert("", "end", values=(
                codigo, data, nome, tipo, st, tel, op_atual, op_fixo, setor, vl, rua, numero, email
            ))

    # ---------------- EVENTO ----------------
    def on_cliente_select(self, event):
        cli = self.cliente_selecionado(silencioso=True)
        if not cli:
            return

        codigo = cli[0]
        self.carregar_recibos_contribuinte(codigo)

    # ---------------- BOTÕES ----------------
    def btn_inclusao(self):
        tela_cadastro_contribuintes(self.root, None, self.atualizar_tabela)

    def btn_alteracao(self):
        cli = self.cliente_selecionado()
        if cli:
            dados_para_editar = [cli[0], cli[1], cli[3], cli[2], cli[4], cli[5]]  # Código, Data, Tipo, Nome, Status, Telefone
            tela_cadastro_contribuintes(self.root, dados_para_editar, self.atualizar_tabela)

    def btn_exclusao(self):
        cli = self.cliente_selecionado()
        if not cli:
            return

        codigo = cli[0]
        nome = cli[2]

        if messagebox.askyesno("Excluir", f"Deseja excluir o contribuinte {nome} (Código {codigo})?"):
            try:
                with self.conectar() as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM contribuintes WHERE codigo = ?", (codigo,))
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Contribuinte excluído com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    def btn_recibo(self):
        cli = self.cliente_selecionado()
        if cli:
            tela_recibo(self.root, cli[0], cli[2])

    def btn_boleto(self):
        cli = self.cliente_selecionado()
        if cli:
            tela_boletos(self.root, cli)

    def btn_todos(self):
        self.search_entry.delete(0, "end")
        self.combo_status.current(0)
        self.tree.selection_remove(self.tree.selection())
        self.atualizar_tabela()

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
            writer.writerow(["Código", "Data", "Nome", "Tipo", "Status", "Telefone", "Operador Atual",
                             "Operador Fixo", "Setor", "Último VL", "Rua", "Número", "Email"])

            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item)["values"])

        messagebox.showinfo("Exportar", "Arquivo contribuintes.csv gerado com sucesso!")

    def btn_novo(self):
        self.tree.selection_remove(self.tree.selection())
        tela_cadastro_contribuintes(self.root, None, self.atualizar_tabela)

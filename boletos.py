import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar


# ===============================
# CONSTANTES VISUAIS
# ===============================
COR_FUNDO = "#ECECF1"
COR_BARRA = "#E0E0E8"
COR_STATUS = "#D6D6E5"
COR_TEXTO = "#1A237E"

FONTE_PADRAO = ("Segoe UI", 9)
FONTE_TITULO = ("Segoe UI", 11, "bold")


# ===============================
# FUNÇÃO DE ABERTURA
# ===============================
def tela_boletos(root, cli=None):
    """
    cli = (codigo, nome, categoria, status, telefone)
    """
    janela = tk.Toplevel(root)

    if cli:
        codigo, nome = cli[0], cli[1]
    else:
        codigo, nome = None, "TODOS"

    TelaBoletos(janela, codigo, nome)


# ===============================
# CLASSE PRINCIPAL
# ===============================
class TelaBoletos:

    def __init__(self, root, codigo_contribuinte=None, nome_contribuinte="TODOS"):
        self.root = root
        self.codigo_contribuinte = codigo_contribuinte
        self.nome_contribuinte = nome_contribuinte

        self.configurar_janela()
        self.criar_label_cliente()
        self.criar_tabela()
        self.criar_botoes()
        self.criar_barra_status()
        self.carregar_dados_banco()

    # ===============================
    # CONFIGURAÇÕES DA JANELA
    # ===============================
    def configurar_janela(self):
        self.root.title(f"Boletos / Débitos - {self.nome_contribuinte}")
        self.root.geometry("1250x600")
        self.root.configure(bg=COR_FUNDO)

    def criar_label_cliente(self):
        self.lbl_cliente = tk.Label(
            self.root,
            text=f"Contribuinte: {self.nome_contribuinte}",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=FONTE_TITULO,
            anchor="w"
        )
        self.lbl_cliente.pack(fill=tk.X, padx=10, pady=(8, 0))

    # ===============================
    # TABELA
    # ===============================
    def criar_tabela(self):
        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=FONTE_PADRAO)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        self.colunas = [
            "Contrib", "Flag", "Sts", "StsContr",
            "Valor", "ValDoado", "Carteira",
            "Registro", "Vencimento", "DtPagto",
            "NossoNum", "DtLiga", "Setor", "Oper",
            "TipoEnvio", "CodBol", "ParBol",
            "Super", "Recibo"
        ]

        self.tree = ttk.Treeview(frame, columns=self.colunas, show="headings")

        for col in self.colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ===============================
    # BOTÕES
    # ===============================
    def criar_botoes(self):
        frame = tk.Frame(self.root, bg=COR_BARRA)
        frame.pack(fill=tk.X)

        def botao(texto, comando, cor="#2E3A59"):
            return tk.Button(
                frame,
                text=texto,
                width=14,
                command=comando,
                bg=cor,
                fg="white",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                activebackground="#3F51B5",
                cursor="hand2"
            )

        botao("Incluir", self.incluir).pack(side=tk.LEFT, padx=5, pady=6)
        botao("Alterar", self.alterar).pack(side=tk.LEFT, padx=5)
        botao("Excluir", self.excluir, "#B71C1C").pack(side=tk.LEFT, padx=5)
        botao("Imprimir Recibo", self.imprimir).pack(side=tk.LEFT, padx=5)
        botao("Email", self.email).pack(side=tk.LEFT, padx=5)
        botao("WhatsApp", self.whatsapp, "#1B5E20").pack(side=tk.LEFT, padx=5)
        botao("Confirmar", self.confirmar, "#1565C0").pack(side=tk.LEFT, padx=5)

    # ===============================
    # BARRA DE STATUS / PESQUISA
    # ===============================
    def criar_barra_status(self):
        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(fill=tk.X, padx=8)

        tk.Label(frame, text="Pesquisar:", bg=COR_FUNDO, font=FONTE_PADRAO).pack(side=tk.LEFT)

        self.pesquisa = tk.Entry(frame, width=35)
        self.pesquisa.pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame,
            text="Buscar",
            command=self.pesquisar,
            bg="#3949AB",
            fg="white",
            relief="flat"
        ).pack(side=tk.LEFT)

        self.status = tk.Label(
            self.root,
            text="Sistema de Boletos / Débitos",
            anchor="w",
            bg=COR_STATUS,
            font=("Segoe UI", 8)
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ===============================
    # BANCO DE DADOS
    # ===============================
    def carregar_dados_banco(self):
        con = conectar()
        cur = con.cursor()

        sql = """
            SELECT
                contrib, 1, 1, 1,
                valor, valor, '', '',
                vencimento, '', nosso_num,
                '', '', operador, '',
                id, '', '', id
            FROM recibos
        """

        params = ()
        if self.codigo_contribuinte:
            sql += " WHERE contrib = ?"
            params = (self.codigo_contribuinte,)

        sql += " ORDER BY id DESC"

        cur.execute(sql, params)
        registros = cur.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())

        for r in registros:
            self.tree.insert("", tk.END, values=r)

        self.status.config(text=f"{len(registros)} registros carregados")

    # ===============================
    # UTILITÁRIOS
    # ===============================
    def registro_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um registro")
            return None
        return self.tree.item(sel[0])["values"]

    # ===============================
    # AÇÕES
    # ===============================
    def incluir(self):
        if not self.codigo_contribuinte:
            messagebox.showwarning(
                "Atenção",
                "Abra os boletos a partir de um contribuinte."
            )
            return

        valor = 52.00
        vencimento = "06/01/2026"
        nosso_num = "275540"
        operador = "SISTEMA"

        con = conectar()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO recibos (contrib, valor, vencimento, nosso_num, operador)
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.codigo_contribuinte, valor, vencimento, nosso_num, operador)
        )
        con.commit()
        con.close()

        self.carregar_dados_banco()
        messagebox.showinfo("Sucesso", "Boleto incluído!")

    def alterar(self):
        messagebox.showinfo("Alterar", "Alterar boleto")

    def excluir(self):
        valores = self.registro_selecionado()
        if not valores:
            return

        id_boleto = valores[15]

        if not messagebox.askyesno("Confirmar", "Deseja excluir este registro?"):
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM recibos WHERE id = ?", (id_boleto,))
        con.commit()
        con.close()

        self.carregar_dados_banco()
        messagebox.showinfo("OK", "Registro excluído")

    def imprimir(self):
        messagebox.showinfo("Imprimir", "Imprimir boleto/recibo")

    def confirmar(self):
        messagebox.showinfo("Confirmar", "Confirmado")

    def email(self):
        messagebox.showinfo("Email", "Enviar Email")

    def whatsapp(self):
        messagebox.showinfo("WhatsApp", "Enviar WhatsApp")

    def pesquisar(self):
        termo = self.pesquisa.get().lower().strip()
        self.carregar_dados_banco()

        if not termo:
            return

        for item in self.tree.get_children():
            valores = " ".join(map(str, self.tree.item(item)["values"])).lower()
            if termo not in valores:
                self.tree.delete(item)

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar


def tela_boletos(root):
    janela = tk.Toplevel(root)
    TelaBoletos(janela)

class TelaBoletos:

    def __init__(self, root):
        self.root = root
        self.root.title("Boletos / Débitos")
        self.root.geometry("1250x600")
        self.root.configure(bg="#ECECF1")

        self.criar_tabela()
        self.criar_botoes()
        self.criar_barra_status()
        self.carregar_dados_banco()

    # ================= TABELA =================
    def criar_tabela(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        self.colunas = [
            "Contrib", "Flag", "Sts", "StsContr",
            "Valor", "ValDoado", "Carteira",
            "Registro", "Vencimento", "DtPagto",
            "NossoNum", "DtLiga", "Setor", "Oper",
            "TipoEnvio", "CodBol", "ParBol", "Super", "Recibo"
        ]

        self.tree = ttk.Treeview(frame, columns=self.colunas, show="headings")

        for col in self.colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ================= BOTÕES =================
    def criar_botoes(self):
        frame = tk.Frame(self.root, bg="#E0E0E8")
        frame.pack(fill=tk.X)

        def botao(txt, cmd, cor="#2E3A59"):
            return tk.Button(
                frame, text=txt, width=14, command=cmd,
                bg=cor, fg="white", relief="flat",
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

    # ================= STATUS / PESQUISA =================
    def criar_barra_status(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.X, padx=8)

        tk.Label(frame, text="Pesquisar:", bg="#ECECF1", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.pesquisa = tk.Entry(frame, width=35)
        self.pesquisa.pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame, text="Buscar", command=self.pesquisar,
            bg="#3949AB", fg="white", relief="flat"
        ).pack(side=tk.LEFT)

        self.status = tk.Label(
            self.root,
            text="Sistema de Boletos / Débitos",
            anchor="w",
            bg="#D6D6E5",
            font=("Segoe UI", 8)
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ================= BANCO =================
    def carregar_dados_banco(self):
        con = conectar()
        cur = con.cursor()

        cur.execute("""
            SELECT
                contrib, 1, 1, 1,
                valor, valor, '', '',
                vencimento, '', nosso_num,
                '', '', operador, '',
                id, '', '', id
            FROM recibos
        """)

        registros = cur.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())

        for r in registros:
            self.tree.insert("", tk.END, values=r)

        self.status.config(text=f"{len(registros)} registros carregados")

    # ================= AÇÕES =================
    def incluir(self):
        con = conectar()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO recibos (contrib, valor, vencimento, nosso_num, operador)
            VALUES (?, ?, ?, ?, ?)
        """, (999, 52.00, "06/01/2026", "275540", "SISTEMA"))

        con.commit()
        con.close()

        self.carregar_dados_banco()
        messagebox.showinfo("Sucesso", "Boleto incluído!")

    def alterar(self):
        messagebox.showinfo("Alterar", "Alterar boleto")

    def excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um registro")
            return

        cod = self.tree.item(sel[0])['values'][15]

        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM recibos WHERE id = ?", (cod,))
        con.commit()
        con.close()

        self.carregar_dados_banco()
        messagebox.showinfo("OK", "Registro excluído")

    def imprimir(self): messagebox.showinfo("Imprimir", "Imprimir boleto/recibo")
    def confirmar(self): messagebox.showinfo("Confirmar", "Confirmado")
    def email(self): messagebox.showinfo("Email", "Enviar Email")
    def whatsapp(self): messagebox.showinfo("WhatsApp", "Enviar WhatsApp")

    def pesquisar(self):
        termo = self.pesquisa.get().lower()
        for item in self.tree.get_children():
            valores = " ".join(map(str, self.tree.item(item)["values"])).lower()
            self.tree.item(item, open=(termo in valores))

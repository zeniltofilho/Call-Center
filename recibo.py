import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
import webbrowser
import urllib.parse


# ================= TELA =================
def tela_recibo(root, id_contribuinte=None, nome_contribuinte="TODOS"):
    janela = tk.Toplevel(root)
    janela.title(f"Recibos - {nome_contribuinte}")
    janela.geometry("1250x600")
    janela.transient(root)
    janela.grab_set()

    TelaRecibos(janela, id_contribuinte, nome_contribuinte)


class TelaRecibos:

    def __init__(self, root, id_contribuinte, nome_contribuinte):
        self.root = root
        self.id_contribuinte = id_contribuinte
        self.nome_contribuinte = nome_contribuinte

        self.criar_tabela()
        self.criar_botoes()
        self.criar_barra_status()
        self.carregar_dados_banco()

    # ================= TABELA =================
    def criar_tabela(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.colunas = [
            "ID", "Contribuinte", "Valor",
            "Vencimento", "Nosso Número", "Operador"
        ]

        self.tree = ttk.Treeview(
            frame, columns=self.colunas, show="headings"
        )

        for col in self.colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ================= BOTÕES =================
    def criar_botoes(self):
        frame = tk.Frame(self.root, bg="#e6e6e6")
        frame.pack(fill=tk.X)

        botoes = [
            ("Incluir", self.incluir),
            ("Alterar", self.alterar),
            ("Excluir", self.excluir),
            ("Imprimir", self.imprimir),
            ("Abrir PDF", self.abrir_pdf),
            ("Email", self.email),
            ("WhatsApp", self.whatsapp)
        ]

        for texto, comando in botoes:
            tk.Button(
                frame, text=texto, width=14, command=comando
            ).pack(side=tk.LEFT, padx=4, pady=6)

    # ================= STATUS =================
    def criar_barra_status(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Pesquisa:").pack(side=tk.LEFT, padx=5)
        self.pesquisa = tk.Entry(frame, width=40)
        self.pesquisa.pack(side=tk.LEFT)

        tk.Button(
            frame, text="Pesquisar", command=self.pesquisar
        ).pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(
            self.root,
            text="Impressora: Microsoft Print to PDF",
            anchor="w"
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ================= BANCO =================
    def carregar_dados_banco(self):
        con = conectar()
        cur = con.cursor()

        if self.id_contribuinte:
            cur.execute("""
                SELECT id, contrib, valor, vencimento, nosso_num, operador
                FROM recibos
                WHERE contrib = ?
            """, (self.id_contribuinte,))
        else:
            cur.execute("""
                SELECT id, contrib, valor, vencimento, nosso_num, operador
                FROM recibos
            """)

        registros = cur.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())

        for r in registros:
            self.tree.insert("", "end", iid=r[0], values=r)

    # ================= UTIL =================
    def recibo_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um recibo")
            return None
        return sel[0]

    def buscar_telefone_contribuinte(self):
        if not self.id_contribuinte:
            return None

        con = conectar()
        cur = con.cursor()
        cur.execute(
            "SELECT telefone FROM contribuintes WHERE id = ?",
            (self.id_contribuinte,)
        )
        dado = cur.fetchone()
        con.close()

        return dado[0] if dado and dado[0] else None

    # ================= AÇÕES =================
    def incluir(self):
        if not self.id_contribuinte:
            messagebox.showwarning(
                "Atenção",
                "Selecione um contribuinte para incluir recibo"
            )
            return

        messagebox.showinfo(
            "Incluir",
            "Aqui você abrirá a tela de cadastro de recibo"
        )

    def alterar(self):
        id_recibo = self.recibo_selecionado()
        if not id_recibo:
            return
        messagebox.showinfo("Alterar", f"Alterar recibo {id_recibo}")

    def excluir(self):
        id_recibo = self.recibo_selecionado()
        if not id_recibo:
            return

        if not messagebox.askyesno("Confirmar", "Deseja excluir este recibo?"):
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM recibos WHERE id = ?", (id_recibo,))
        con.commit()
        con.close()

        self.carregar_dados_banco()
        messagebox.showinfo("OK", "Recibo excluído")

    def imprimir(self):
        messagebox.showinfo("Imprimir", "Enviar para impressora")

    def abrir_pdf(self):
        messagebox.showinfo("PDF", "Abrir PDF do recibo")

    def email(self):
        messagebox.showinfo("Email", "Enviar recibo por email")

    def whatsapp(self):
        telefone = self.buscar_telefone_contribuinte()

        if not telefone:
            messagebox.showwarning(
                "Atenção",
                "Contribuinte sem telefone cadastrado"
            )
            return

        id_recibo = self.recibo_selecionado()
        if not id_recibo:
            return

        mensagem = (
            f"Olá {self.nome_contribuinte},\n\n"
            f"Segue o seu recibo:\n"
            f"Recibo Nº: {id_recibo}\n\n"
            f"Qualquer dúvida estamos à disposição.\n\n"
            f"Atenciosamente."
        )

        texto = urllib.parse.quote(mensagem)
        url = f"https://wa.me/{telefone}?text={texto}"

        webbrowser.open(url)

    def pesquisar(self):
        self.carregar_dados_banco()

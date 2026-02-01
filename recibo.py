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
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        self.colunas = ["ID", "Contribuinte", "Valor", "Vencimento", "Nosso Número", "Operador"]

        self.tree = ttk.Treeview(frame, columns=self.colunas, show="headings")

        larguras = [60, 200, 90, 110, 130, 120]

        for col, w in zip(self.colunas, larguras):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=tk.CENTER)

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
                frame, text=txt, width=13, command=cmd,
                bg=cor, fg="white", relief="flat",
                font=("Segoe UI", 9, "bold"),
                activebackground="#3F51B5",
                cursor="hand2"
            )

        botao("Incluir", self.incluir).pack(side=tk.LEFT, padx=5, pady=6)
        botao("Alterar", self.alterar).pack(side=tk.LEFT, padx=5)
        botao("Excluir", self.excluir, "#B71C1C").pack(side=tk.LEFT, padx=5)
        botao("Imprimir", self.imprimir).pack(side=tk.LEFT, padx=5)
        botao("Abrir PDF", self.abrir_pdf).pack(side=tk.LEFT, padx=5)
        botao("Email", self.email).pack(side=tk.LEFT, padx=5)
        botao("WhatsApp", self.whatsapp, "#1B5E20").pack(side=tk.LEFT, padx=5)

    # ================= STATUS / PESQUISA =================
    def criar_barra_status(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.X, padx=8)

        tk.Label(frame, text="Pesquisar:", bg="#ECECF1", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.pesquisa = tk.Entry(frame, width=35)
        self.pesquisa.pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="Buscar", command=self.pesquisar,
                  bg="#3949AB", fg="white", relief="flat").pack(side=tk.LEFT)

        self.status = tk.Label(
            self.root,
            text="Impressora: Microsoft Print to PDF",
            anchor="w",
            bg="#D6D6E5",
            font=("Segoe UI", 8)
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ================= BANCO =================
    def carregar_dados_banco(self):
        con = conectar()
        cur = con.cursor()

        if self.id_contribuinte:
            cur.execute("""SELECT id, contrib, valor, vencimento, nosso_num, operador
                           FROM recibos WHERE contrib = ?""", (self.id_contribuinte,))
        else:
            cur.execute("""SELECT id, contrib, valor, vencimento, nosso_num, operador FROM recibos""")

        registros = cur.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())

        for r in registros:
            self.tree.insert("", "end", iid=r[0], values=r)

        self.status.config(text=f"{len(registros)} recibos encontrados")

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
        cur.execute("SELECT telefone1 FROM contribuintes WHERE id = ?", (self.id_contribuinte,))
        dado = cur.fetchone()
        con.close()
        return dado[0] if dado and dado[0] else None

    # ================= AÇÕES =================
    def incluir(self):
        messagebox.showinfo("Incluir", "Abrir tela de cadastro de recibo")

    def alterar(self):
        id_recibo = self.recibo_selecionado()
        if id_recibo:
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

    def imprimir(self): messagebox.showinfo("Imprimir", "Enviar para impressora")
    def abrir_pdf(self): messagebox.showinfo("PDF", "Abrir PDF do recibo")
    def email(self): messagebox.showinfo("Email", "Enviar recibo por email")

    def whatsapp(self):
        telefone = self.buscar_telefone_contribuinte()
        if not telefone:
            messagebox.showwarning("Atenção", "Contribuinte sem telefone cadastrado")
            return

        id_recibo = self.recibo_selecionado()
        if not id_recibo:
            return

        mensagem = f"Olá {self.nome_contribuinte}, seu recibo Nº {id_recibo} está disponível."
        texto = urllib.parse.quote(mensagem)
        url = f"https://wa.me/{telefone}?text={texto}"
        webbrowser.open(url)

    def pesquisar(self):
        termo = self.pesquisa.get().lower()
        for item in self.tree.get_children():
            valores = " ".join(map(str, self.tree.item(item)["values"])).lower()
            self.tree.item(item, open=(termo in valores))

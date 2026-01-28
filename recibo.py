import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar 

def tela_recibo(root):
    janela = tk.Toplevel(root)
    TelaRecibos(janela)


class TelaRecibos:

    def __init__(self, root):
        self.root = root
        self.root.title("Recibos")
        self.root.geometry("1250x600")

        self.criar_tabela()
        self.criar_botoes()
        self.criar_barra_status()

        # carregar dados reais do banco
        self.carregar_dados_banco()

    # ================= TABELA =================
    def criar_tabela(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.colunas = [
            "Contrib", "Flag", "Sts", "Valor", "Vencimento", "NossoNum",
            "Dt_Liga", "Setor", "Oper", "Mens", "Super", "CodRec",
            "ParRec", "Tela", "Via", "Rifa", "Assina"
        ]

        self.tree = ttk.Treeview(frame, columns=self.colunas, show="headings")

        for col in self.colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
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
            ("Cancelar", self.cancelar),
            ("Imprimir", self.imprimir),
            ("Confirmar", self.confirmar),
            ("Abrir PDF", self.abrir_pdf),
            ("Enviar Email", self.email),
            ("WhatsApp", self.whatsapp)
        ]

        for texto, comando in botoes:
            tk.Button(frame, text=texto, width=12, command=comando).pack(
                side=tk.LEFT, padx=3, pady=5
            )

    # ================= STATUS =================
    def criar_barra_status(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Pesquisa:").pack(side=tk.LEFT, padx=5)
        self.pesquisa = tk.Entry(frame, width=40)
        self.pesquisa.pack(side=tk.LEFT)

        tk.Button(frame, text="Pesquisar", command=self.pesquisar).pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self.root, text="Impressora: Microsoft Print to PDF", anchor="w")
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ================= BANCO DE DADOS =================
    def carregar_dados_banco(self):
        con = conectar()
        cur = con.cursor()

        cur.execute("""
            SELECT contrib, 1, 1, valor, vencimento, nosso_num,
                   '', '', operador, '', '', id, '', '', '', '', operador
            FROM recibos
        """)

        registros = cur.fetchall()
        con.close()

        # limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in registros:
            self.tree.insert("", tk.END, values=r)

    # ================= AÇÕES =================
    def incluir(self):
        con = conectar()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO recibos (contrib, valor, vencimento, nosso_num, operador)
            VALUES (?, ?, ?, ?, ?)
        """, (123, 50.0, "10/02/2026", "999999", "EVELYN"))

        con.commit()
        con.close()

        self.carregar_dados_banco()
        messagebox.showinfo("Sucesso", "Recibo cadastrado no banco!")

    def alterar(self):
        messagebox.showinfo("Alterar", "Alterar recibo")

    def excluir(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um recibo")
            return

        codrec = self.tree.item(selecionado)['values'][11]

        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM recibos WHERE id = ?", (codrec,))
        con.commit()
        con.close()

        self.carregar_dados_banco()
        messagebox.showinfo("OK", "Recibo excluído")

    def cancelar(self):
        messagebox.showinfo("Cancelar", "Cancelar operação")

    def imprimir(self):
        messagebox.showinfo("Imprimir", "Imprimindo...")

    def confirmar(self):
        messagebox.showinfo("Confirmar", "Confirmado")

    def abrir_pdf(self):
        messagebox.showinfo("PDF", "Abrir PDF")

    def email(self):
        messagebox.showinfo("Email", "Enviar Email")

    def whatsapp(self):
        messagebox.showinfo("WhatsApp", "Enviar WhatsApp")

    def pesquisar(self):
        termo = self.pesquisa.get()
        messagebox.showinfo("Pesquisa", f"Pesquisar: {termo}")


# Teste isolado
if __name__ == "__main__":
    root = tk.Tk()
    TelaRecibos(root)
    root.mainloop()

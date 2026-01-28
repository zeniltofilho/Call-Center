import tkinter as tk
from tkinter import ttk, messagebox


def tela_recibo(root):
    janela = tk.Toplevel(root)
    app = TelaRecibos(janela)


class TelaRecibos:

    def __init__(self, root):
        self.root = root
        self.root.title("Recibos")
        self.root.geometry("1250x600")

        self.criar_tabela()
        self.criar_botoes()
        self.criar_barra_status()

        # Exemplo de dados
        self.carregar_dados_teste()

    def criar_tabela(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        colunas = [
            "Contrib", "Flag", "Sts", "Valor", "Vencimento", "NossoNum",
            "Dt_Liga", "Setor", "Oper", "Mens", "Super", "CodRec",
            "ParRec", "Tela", "Via", "Rifa", "Assina"
        ]

        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor=tk.CENTER)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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

    def criar_barra_status(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Pesquisa:").pack(side=tk.LEFT, padx=5)
        self.pesquisa = tk.Entry(frame, width=40)
        self.pesquisa.pack(side=tk.LEFT)

        tk.Button(frame, text="Pesquisar", command=self.pesquisar).pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self.root, text="Impressora: Microsoft Print to PDF", anchor="w")
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def carregar_dados_teste(self):
        dados = [
            (401,1,1,15,"06/01/2026","12475124","11/02/2025",3,20,70,1,36,1,0,1,0,"EVELYN"),
            (6015,1,9,20,"06/01/2026","12475142","06/01/2026",19,14,70,4,95,1,0,1,0,"EVELYN"),
            (3512,1,9,50,"06/01/2026","12475177","06/01/2026",1,14,16,4,86,1,0,1,0,"EVELYN"),
        ]

        for d in dados:
            self.tree.insert("", tk.END, values=d)

    # Funções dos botões
    def incluir(self):
        messagebox.showinfo("Incluir", "Novo recibo")

    def alterar(self):
        messagebox.showinfo("Alterar", "Alterar recibo")

    def excluir(self):
        messagebox.showinfo("Excluir", "Excluir recibo")

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
    app = TelaRecibos(root)
    root.mainloop()

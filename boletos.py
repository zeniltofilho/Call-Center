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

        self.criar_tabela()
        self.criar_botoes()
        self.criar_barra_status()

        self.carregar_dados_banco()

    # ================= TABELA =================
    def criar_tabela(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

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
            self.tree.column(col, width=85, anchor=tk.CENTER)

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
            ("Imprimir Recibo", self.imprimir),
            ("Email", self.email),
            ("WhatsApp", self.whatsapp),
            ("Confirmar", self.confirmar),
        ]

        for texto, comando in botoes:
            tk.Button(frame, text=texto, width=15, command=comando).pack(
                side=tk.LEFT, padx=3, pady=5
            )

    # ================= STATUS =================
    def criar_barra_status(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Pesquisa:").pack(side=tk.LEFT, padx=5)
        self.pesquisa = tk.Entry(frame, width=40)
        self.pesquisa.pack(side=tk.LEFT)

        tk.Button(frame, text="Pesquisar", command=self.pesquisar).pack(
            side=tk.LEFT, padx=5
        )

        self.status = tk.Label(
            self.root,
            text="Sistema de Boletos / Débitos",
            anchor="w"
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ================= BANCO =================
    def carregar_dados_banco(self):
        con = conectar()
        cur = con.cursor()

        # MESMA TABELA recibos
        cur.execute("""
            SELECT
                contrib,
                1,
                1,
                1,
                valor,
                valor,
                '',
                '',
                vencimento,
                '',
                nosso_num,
                '',
                '',
                operador,
                '',
                id,
                '',
                '',
                id
            FROM recibos
        """)

        registros = cur.fetchall()
        con.close()

        self.tree.delete(*self.tree.get_children())

        for r in registros:
            self.tree.insert("", tk.END, values=r)

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
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um registro")
            return

        cod = self.tree.item(selecionado)['values'][15]

        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM recibos WHERE id = ?", (cod,))
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
        termo = self.pesquisa.get()
        messagebox.showinfo("Pesquisa", f"Pesquisar: {termo}")


# Teste isolado
if __name__ == "__main__":
    root = tk.Tk()
    TelaBoletos(root)
    root.mainloop()

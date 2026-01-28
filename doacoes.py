import tkinter as tk
from tkinter import ttk
from database import get_connection   # 👈 mesmo banco do main.py


def tela_doacoes(root):
    janela = tk.Toplevel(root)
    TelaDoacoes(janela)


class TelaDoacoes:

    def __init__(self, root):
        self.root = root
        self.conn = get_connection()   # 👈 conexão compartilhada
        self.cursor = self.conn.cursor()

        self.root.title("Doações")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        self.criar_campos_superiores()
        self.criar_observacoes()
        self.criar_tabela()
        self.criar_campos_inferiores()
        self.criar_botoes()

        self.carregar_doacoes()

    # ================= CAMPOS SUPERIORES =================
    def criar_campos_superiores(self):
        tk.Label(self.root, text="Nome Contribuinte").place(x=10, y=10)
        self.ent_nome = tk.Entry(self.root, width=60)
        self.ent_nome.place(x=10, y=30)

        tk.Label(self.root, text="Tipo").place(x=500, y=10)
        self.ent_tipo = tk.Entry(self.root, width=5)
        self.ent_tipo.place(x=500, y=30)

        tk.Label(self.root, text="Contato").place(x=550, y=10)
        self.ent_contato = tk.Entry(self.root, width=30)
        self.ent_contato.place(x=550, y=30)

        tk.Label(self.root, text="Endereço").place(x=10, y=60)
        self.ent_endereco = tk.Entry(self.root, width=100)
        self.ent_endereco.place(x=10, y=80)

    # ================= OBSERVAÇÕES =================
    def criar_observacoes(self):
        tk.Label(self.root, text="Observações").place(x=10, y=115)
        self.ent_obs = tk.Entry(self.root, width=120)
        self.ent_obs.place(x=10, y=135)

        tk.Label(self.root, text="Informações ao Cobrador").place(x=10, y=165)
        self.ent_info1 = tk.Entry(self.root, width=120)
        self.ent_info1.place(x=10, y=185)

        self.ent_info2 = tk.Entry(self.root, width=120)
        self.ent_info2.place(x=10, y=215)

    # ================= TABELA =================
    def criar_tabela(self):
        frame = tk.Frame(self.root)
        frame.place(x=10, y=250, width=880, height=180)

        colunas = ("Data", "Ligação", "Valor")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings", height=7)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ================= BANCO / DADOS =================
    def carregar_doacoes(self):
        self.tree.delete(*self.tree.get_children())

        try:
            self.cursor.execute("""
                SELECT data_doacao, data_ligacao, valor
                FROM doacoes
                ORDER BY data_doacao DESC
            """)
            for row in self.cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            print("Erro ao carregar doações:", e)

    # ================= CAMPOS INFERIORES =================
    def criar_campos_inferiores(self):
        frame = tk.Frame(self.root)
        frame.place(x=10, y=440, width=880, height=130)

        tk.Label(frame, text="Parcelas").place(x=10, y=10)
        self.ent_parcelas = tk.Entry(frame, width=5)
        self.ent_parcelas.place(x=80, y=10)

        tk.Checkbutton(frame, text="Extra F2").place(x=140, y=10)
        tk.Checkbutton(frame, text="Pagamento com Cl").place(x=230, y=10)
        tk.Checkbutton(frame, text="Múltiplas Parcelas").place(x=380, y=10)

    # ================= BOTÕES =================
    def criar_botoes(self):
        frame = tk.Frame(self.root, bg="#dcdcdc")
        frame.place(x=0, y=580, width=900, height=40)

        tk.Button(frame, text="Alteração", width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="OK", width=12).pack(side=tk.RIGHT, padx=10)
        tk.Button(
            frame,
            text="Cancelar Transação",
            width=18,
            fg="red",
            command=self.root.destroy
        ).pack(side=tk.RIGHT, padx=10)

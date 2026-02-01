import tkinter as tk
from tkinter import ttk
from database import get_connection


def tela_doacoes(root):
    janela = tk.Toplevel(root)
    TelaDoacoes(janela)


class TelaDoacoes:

    def __init__(self, root):
        self.root = root
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.root.title("Doações")
        self.root.geometry("920x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#f2f2f2")

        self.criar_estilo()
        self.criar_campos_superiores()
        self.criar_observacoes()
        self.criar_tabela()
        self.criar_campos_inferiores()
        self.criar_botoes()
        self.criar_status_bar()

        self.carregar_doacoes()

    # ================= ESTILO =================
    def criar_estilo(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="white",
                        fieldbackground="white",
                        rowheight=26,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 9, "bold"))

    # ================= CAMPOS SUPERIORES =================
    def criar_campos_superiores(self):
        frame = tk.LabelFrame(self.root, text="Dados do Contribuinte", bg="#f2f2f2")
        frame.place(x=10, y=10, width=900, height=95)

        tk.Label(frame, text="Nome Contribuinte", bg="#f2f2f2").place(x=10, y=10)
        self.ent_nome = tk.Entry(frame, width=60)
        self.ent_nome.place(x=10, y=35)

        tk.Label(frame, text="Tipo", bg="#f2f2f2").place(x=500, y=10)
        self.ent_tipo = tk.Entry(frame, width=5)
        self.ent_tipo.place(x=500, y=35)

        tk.Label(frame, text="Contato", bg="#f2f2f2").place(x=550, y=10)
        self.ent_contato = tk.Entry(frame, width=30)
        self.ent_contato.place(x=550, y=35)

        tk.Label(frame, text="Endereço", bg="#f2f2f2").place(x=10, y=60)
        self.ent_endereco = tk.Entry(frame, width=100)
        self.ent_endereco.place(x=80, y=60)

    # ================= OBSERVAÇÕES =================
    def criar_observacoes(self):
        frame = tk.LabelFrame(self.root, text="Observações", bg="#f2f2f2")
        frame.place(x=10, y=110, width=900, height=110)

        self.ent_obs = tk.Entry(frame, width=120)
        self.ent_obs.place(x=10, y=10)

        tk.Label(frame, text="Informações ao Cobrador", bg="#f2f2f2").place(x=10, y=40)
        self.ent_info1 = tk.Entry(frame, width=120)
        self.ent_info1.place(x=10, y=60)
        self.ent_info2 = tk.Entry(frame, width=120)
        self.ent_info2.place(x=10, y=85)

    # ================= TABELA =================
    def criar_tabela(self):
        frame = tk.LabelFrame(self.root, text="Histórico de Doações", bg="#f2f2f2")
        frame.place(x=10, y=230, width=900, height=230)

        colunas = ("Data", "Ligação", "Valor")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tags de cor
        self.tree.tag_configure("alto", background="#E8F5E9")
        self.tree.tag_configure("normal", background="white")

    # ================= CARREGAR DADOS =================
    def carregar_doacoes(self):
        self.tree.delete(*self.tree.get_children())
        total = 0

        try:
            self.cursor.execute("""
                SELECT data_doacao, data_ligacao, valor
                FROM doacoes
                ORDER BY data_doacao DESC
            """)

            for data_doacao, data_ligacao, valor in self.cursor.fetchall():
                total += float(valor)

                tag = "alto" if float(valor) >= 100 else "normal"

                self.tree.insert("", tk.END,
                                 values=(data_doacao, data_ligacao, f"R$ {valor:.2f}"),
                                 tags=(tag,))

            self.lbl_total.config(text=f"Total Doações: R$ {total:.2f}")

        except Exception as e:
            print("Erro ao carregar doações:", e)

    # ================= CAMPOS INFERIORES =================
    def criar_campos_inferiores(self):
        frame = tk.LabelFrame(self.root, text="Configuração", bg="#f2f2f2")
        frame.place(x=10, y=470, width=900, height=100)

        tk.Label(frame, text="Parcelas", bg="#f2f2f2").place(x=10, y=10)
        self.ent_parcelas = tk.Entry(frame, width=5)
        self.ent_parcelas.place(x=80, y=10)

        tk.Checkbutton(frame, text="Extra F2", bg="#f2f2f2").place(x=150, y=10)
        tk.Checkbutton(frame, text="Pagamento com Cl", bg="#f2f2f2").place(x=240, y=10)
        tk.Checkbutton(frame, text="Múltiplas Parcelas", bg="#f2f2f2").place(x=400, y=10)

    # ================= BOTÕES =================
    def criar_botoes(self):
        frame = tk.Frame(self.root, bg="#dcdcdc")
        frame.place(x=0, y=580, width=920, height=45)

        tk.Button(frame, text="Alteração", width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="OK", width=12).pack(side=tk.RIGHT, padx=10)
        tk.Button(frame, text="Cancelar Transação",
                  width=18, fg="red",
                  command=self.root.destroy).pack(side=tk.RIGHT, padx=10)

    # ================= STATUS BAR =================
    def criar_status_bar(self):
        self.lbl_total = tk.Label(self.root,
                                  text="Total Doações: R$ 0.00",
                                  anchor="w",
                                  bg="#d6d6e5",
                                  font=("Segoe UI", 9, "bold"))
        self.lbl_total.pack(fill=tk.X, side=tk.BOTTOM)

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar


def tela_doacoes(root, cli):
    janela = tk.Toplevel(root)
    TelaDoacoes(janela, cli)


class TelaDoacoes:
    """Tela inspirada no layout da imagem (Doações).

    - Topo com Nome/Tipo/Contato
    - Endereço
    - Observações (3 linhas)
    - Informações ao cobrador (2 linhas)
    - Histórico (Data / Ligação / Valor)
    - Rodapé com Recibo + checkboxes + datas + operador + valor
    - Botões: Alteração / OK / Cancelar Transação

    Observação: mantém sua estrutura e banco. Ajustei apenas layout e alguns bugs.
    """

    def __init__(self, root, cli):
        self.root = root
        self.cli = cli

        self.conn = conectar()
        self.cursor = self.conn.cursor()

        self.root.title("Doações")
        self.root.geometry("920x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#e9e9e9")

        self.criar_estilo()

        # ====== CONTAINER PRINCIPAL ======
        self.frm_topo = tk.Frame(self.root, bg="#e9e9e9")
        self.frm_topo.place(x=10, y=10, width=900, height=210)

        self.frm_grid = tk.Frame(self.root, bg="#e9e9e9")
        self.frm_grid.place(x=10, y=225, width=900, height=255)

        self.frm_rodape = tk.Frame(self.root, bg="#e9e9e9")
        self.frm_rodape.place(x=10, y=485, width=900, height=130)

        self.frm_botoes = tk.Frame(self.root, bg="#dcdcdc")
        self.frm_botoes.place(x=0, y=620, width=920, height=45)

        # ====== MONTAGEM ======
        self.criar_campos_superiores()
        self.criar_observacoes()
        self.criar_tabela()
        self.criar_campos_inferiores()
        self.criar_botoes()
        self.criar_status_bar()

        self.preencher_dados_contribuinte()
        self.carregar_doacoes()

        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

    # ================= FECHAR =================
    def fechar(self):
        try:
            self.conn.close()
        except:
            pass
        self.root.destroy()

    # ================= ESTILO =================
    def criar_estilo(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="white",
                        fieldbackground="white",
                        rowheight=24,
                        font=("Segoe UI", 9))

        style.configure("Treeview.Heading",
                        font=("Segoe UI", 9, "bold"),
                        background="#2f2f2f",
                        foreground="white")

        style.map("Treeview",
                  background=[("selected", "#cfe3ff")],
                  foreground=[("selected", "black")])

    # ================= PREENCHER CONTRIBUINTE =================
    def preencher_dados_contribuinte(self):
        if isinstance(self.cli, dict):
            nome = self.cli.get("nome", "")
            tipo = self.cli.get("tipo", "")
            contato = self.cli.get("contato", "")
            endereco = self.cli.get("endereco", "")
            contribuinte_id = self.cli.get("id", None)
        else:
            contribuinte_id = self.cli[0] if len(self.cli) > 0 else None
            nome = self.cli[1] if len(self.cli) > 1 else ""
            tipo = self.cli[2] if len(self.cli) > 2 else ""
            contato = self.cli[3] if len(self.cli) > 3 else ""
            endereco = self.cli[4] if len(self.cli) > 4 else ""

        self.contribuinte_id = contribuinte_id

        self.ent_nome.config(state="normal")
        self.ent_tipo.config(state="normal")
        self.ent_contato.config(state="normal")
        self.ent_endereco.config(state="normal")

        self.ent_nome.delete(0, tk.END)
        self.ent_nome.insert(0, nome)

        self.ent_tipo.delete(0, tk.END)
        self.ent_tipo.insert(0, tipo)

        self.ent_contato.delete(0, tk.END)
        self.ent_contato.insert(0, contato)

        self.ent_endereco.delete(0, tk.END)
        self.ent_endereco.insert(0, endereco)

        # travar edição
        self.ent_nome.config(state="disabled")
        self.ent_tipo.config(state="disabled")
        self.ent_contato.config(state="disabled")
        self.ent_endereco.config(state="disabled")

    # ================= CAMPOS SUPERIORES =================
    def criar_campos_superiores(self):
        # linha 1
        tk.Label(self.frm_topo, text="Nome Contribuinte", bg="#e9e9e9").place(x=0, y=0)
        self.ent_nome = tk.Entry(self.frm_topo, width=62)
        self.ent_nome.place(x=0, y=20, height=22)

        tk.Label(self.frm_topo, text="Tipo", bg="#e9e9e9").place(x=470, y=0)
        self.ent_tipo = tk.Entry(self.frm_topo, width=5, justify="center")
        self.ent_tipo.place(x=470, y=20, height=22)

        tk.Label(self.frm_topo, text="Contato", bg="#e9e9e9").place(x=520, y=0)
        self.ent_contato = tk.Entry(self.frm_topo, width=44)
        self.ent_contato.place(x=520, y=20, height=22)

        # linha 2
        tk.Label(self.frm_topo, text="Endereço", bg="#e9e9e9").place(x=0, y=45)
        self.ent_endereco = tk.Entry(self.frm_topo, width=110)
        self.ent_endereco.place(x=0, y=65, height=22)

    # ================= OBSERVAÇÕES =================
    def criar_observacoes(self):
        # --- Observações (3 linhas) ---
        tk.Label(self.frm_topo, text="Observações", bg="#e9e9e9").place(x=0, y=95)

        self.ent_obs1 = tk.Entry(self.frm_topo, width=110)
        self.ent_obs1.place(x=0, y=115, height=22)

        self.ent_obs2 = tk.Entry(self.frm_topo, width=110)
        self.ent_obs2.place(x=0, y=140, height=22)

        self.ent_obs3 = tk.Entry(self.frm_topo, width=110)
        self.ent_obs3.place(x=0, y=165, height=22)

        # --- Informações ao Cobrador (2 linhas) ---
        tk.Label(self.frm_topo, text="Informações ao Cobrador", bg="#e9e9e9").place(x=0, y=190)

        # (na imagem fica logo abaixo; aqui usamos o espaço do topo até 210)
        # Para caber certinho, colocamos no frame da tabela (acima dela)

    # ================= TABELA =================
    def criar_tabela(self):
        # frame superior da grade: info cobrador
        frm_info = tk.Frame(self.frm_grid, bg="#e9e9e9")
        frm_info.place(x=0, y=0, width=900, height=50)

        self.ent_info1 = tk.Entry(frm_info, width=110)
        self.ent_info1.place(x=0, y=0, height=22)

        self.ent_info2 = tk.Entry(frm_info, width=110)
        self.ent_info2.place(x=0, y=25, height=22)

        # frame da tabela
        frm_table = tk.Frame(self.frm_grid, bg="#e9e9e9")
        frm_table.place(x=0, y=55, width=900, height=200)

        colunas = ("Data", "Ligação", "Valor")
        self.tree = ttk.Treeview(frm_table, columns=colunas, show="headings")

        self.tree.heading("Data", text="Data")
        self.tree.heading("Ligação", text="Ligação")
        self.tree.heading("Valor", text="Valor")

        self.tree.column("Data", width=180, anchor="center")
        self.tree.column("Ligação", width=180, anchor="center")
        self.tree.column("Valor", width=180, anchor="e")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frm_table, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # tags
        self.tree.tag_configure("alto", background="#E8F5E9")
        self.tree.tag_configure("normal", background="white")

    # ================= CARREGAR DADOS =================
    def carregar_doacoes(self):
        self.tree.delete(*self.tree.get_children())
        total = 0.0

        if not self.contribuinte_id:
            self.lbl_total.config(text="Total Doações: R$ 0,00")
            return

        try:
            self.cursor.execute("""
                SELECT data_doacao, data_ligacao, valor
                FROM doacoes
                WHERE contribuinte_id = ?
                ORDER BY data_doacao DESC
            """, (self.contribuinte_id,))

            for data_doacao, data_ligacao, valor in self.cursor.fetchall():
                try:
                    v = float(valor)
                except:
                    v = 0.0

                total += v
                tag = "alto" if v >= 100 else "normal"

                self.tree.insert("", tk.END,
                                 values=(data_doacao, data_ligacao, f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
                                 tags=(tag,))

            self.lbl_total.config(text=f"Total Doações: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        except Exception as e:
            print("Erro ao carregar doações:", e)

    # ================= CAMPOS INFERIORES =================
    def criar_campos_inferiores(self):
        # Linha 1 (Recibo + checks)
        tk.Label(self.frm_rodape, text="0  - Recibo", bg="#e9e9e9").place(x=380, y=0)

        self.var_extra_f2 = tk.IntVar(value=0)
        self.var_pagamento_cli = tk.IntVar(value=0)
        self.var_mult_parcelas = tk.IntVar(value=1)
        self.var_dois_em_dois = tk.IntVar(value=0)

        tk.Label(self.frm_rodape, text="Parcelas:", bg="#e9e9e9").place(x=0, y=30)
        self.ent_parcelas = tk.Entry(self.frm_rodape, width=6, justify="center")
        self.ent_parcelas.place(x=65, y=28, height=22)
        self.ent_parcelas.insert(0, "12")

        tk.Checkbutton(self.frm_rodape, text="Extra F2", bg="#e9e9e9", variable=self.var_extra_f2).place(x=140, y=28)
        tk.Checkbutton(self.frm_rodape, text="Pagamento com Cl", bg="#e9e9e9", variable=self.var_pagamento_cli).place(x=230, y=28)
        tk.Checkbutton(self.frm_rodape, text="Múltiplas Parcelas", bg="#e9e9e9", variable=self.var_mult_parcelas).place(x=380, y=28)

        tk.Checkbutton(self.frm_rodape, text="De dois em dois meses", bg="#e9e9e9", variable=self.var_dois_em_dois).place(x=640, y=28)

        # Linha 2 (Datas)
        tk.Label(self.frm_rodape, text="Data de Ligação:", bg="#e9e9e9").place(x=0, y=60)
        self.ent_data_ligacao = tk.Entry(self.frm_rodape, width=12, justify="center")
        self.ent_data_ligacao.place(x=110, y=58, height=22)

        tk.Label(self.frm_rodape, text="Data da Doação:", bg="#e9e9e9").place(x=0, y=85)
        self.ent_data_doacao = tk.Entry(self.frm_rodape, width=12, justify="center")
        self.ent_data_doacao.place(x=110, y=83, height=22)

        tk.Label(self.frm_rodape, text="Data de Entrada:", bg="#e9e9e9").place(x=0, y=110)
        self.ent_data_entrada = tk.Entry(self.frm_rodape, width=12, justify="center")
        self.ent_data_entrada.place(x=110, y=108, height=22)

        tk.Label(self.frm_rodape, text="Data de VL:", bg="#e9e9e9").place(x=0, y=135)
        # (não cabe no 130px, então fica como na imagem: mais compacto)

        # Coluna do meio (QtdeRifa)
        tk.Label(self.frm_rodape, text="QtdeRifa:", bg="#e9e9e9").place(x=270, y=60)
        self.ent_qtde_rifa = tk.Entry(self.frm_rodape, width=6, justify="center")
        self.ent_qtde_rifa.place(x=335, y=58, height=22)
        self.ent_qtde_rifa.insert(0, "0")

        # Coluna direita (Operador / Valor / cadastrar)
        tk.Label(self.frm_rodape, text="Operador:", bg="#e9e9e9").place(x=520, y=60)
        self.ent_operador = tk.Entry(self.frm_rodape, width=6, justify="center")
        self.ent_operador.place(x=585, y=58, height=22)

        tk.Label(self.frm_rodape, text="Valor:", bg="#e9e9e9").place(x=520, y=85)
        self.ent_valor = tk.Entry(self.frm_rodape, width=10, justify="center")
        self.ent_valor.place(x=585, y=83, height=22)
        self.ent_valor.insert(0, "10")

        self.var_cadastrar_credito = tk.IntVar(value=0)
        tk.Checkbutton(self.frm_rodape, text="Cadastrar Credi", bg="#e9e9e9", variable=self.var_cadastrar_credito).place(x=700, y=83)

        # Texto azul (como na imagem)
        tk.Label(self.frm_rodape,
                 text="quarta  1ª Parcela - Q",
                 fg="#1b3cff",
                 bg="#e9e9e9",
                 font=("Segoe UI", 10, "bold")).place(x=620, y=108)

        # Preencher datas (simples)
        from datetime import datetime
        hoje = datetime.now().strftime("%d/%m/%Y")
        self.ent_data_ligacao.insert(0, hoje)
        self.ent_data_doacao.insert(0, hoje)
        self.ent_data_entrada.insert(0, hoje)

    # ================= BOTÕES =================
    def criar_botoes(self):
        btn_alt = tk.Button(self.frm_botoes, text="Alteração", width=12)
        btn_alt.pack(side=tk.LEFT, padx=10, pady=6)

        btn_cancelar = tk.Button(self.frm_botoes,
                                 text="Cancelar Transação",
                                 width=18,
                                 fg="red",
                                 command=self.fechar)
        btn_cancelar.pack(side=tk.RIGHT, padx=10, pady=6)

        btn_ok = tk.Button(self.frm_botoes, text="OK", width=12)
        btn_ok.pack(side=tk.RIGHT, padx=10, pady=6)

    # ================= STATUS BAR =================
    def criar_status_bar(self):
        self.lbl_total = tk.Label(self.root,
                                  text="Total Doações: R$ 0,00",
                                  anchor="w",
                                  bg="#cfcfcf",
                                  font=("Segoe UI", 9, "bold"))
        self.lbl_total.pack(fill=tk.X, side=tk.BOTTOM)

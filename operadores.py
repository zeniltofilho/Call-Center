import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_NAME


def tela_operadores(root):
    win = tk.Toplevel(root)
    win.title("Operadores")
    win.geometry("1200x520")
    win.configure(bg="#ECECF1")
    win.transient(root)
    win.grab_set()

    AppOperadores(win)


class AppOperadores:
    def __init__(self, win):
        self.win = win

        # ================= ESTILO =================
        style = ttk.Style()
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        # ================= TOPO =================
        topo = tk.Frame(self.win, bg="#ECECF1")
        topo.pack(fill=tk.X, padx=10, pady=(10, 4))

        tk.Label(
            topo, text="Operadores",
            bg="#ECECF1", fg="#1A237E",
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT)

        # ================= PESQUISA =================
        pesquisa_frame = tk.Frame(self.win, bg="#ECECF1")
        pesquisa_frame.pack(fill=tk.X, padx=10, pady=(0, 6))

        tk.Label(pesquisa_frame, text="Pesquisar:", bg="#ECECF1").pack(side=tk.LEFT)
        self.entry_busca = tk.Entry(pesquisa_frame, width=35)
        self.entry_busca.pack(side=tk.LEFT, padx=6)

        tk.Button(
            pesquisa_frame,
            text="Buscar",
            command=self.buscar,
            bg="#3949AB",
            fg="white",
            relief="flat",
            cursor="hand2"
        ).pack(side=tk.LEFT)

        tk.Button(
            pesquisa_frame,
            text="Limpar",
            command=self.limpar_busca,
            bg="#2E3A59",
            fg="white",
            relief="flat",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=6)

        # ================= TABELA =================
        self.colunas = (
            "id", "nome", "turno", "turma", "supervisor",
            "sts", "oper", "premio", "comissao", "rep", "mvf", "mvd"
        )

        frame_tabela = tk.Frame(self.win, bg="#ECECF1")
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cabeçalhos
        self.tree.heading("id", text="Código")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("turno", text="Turno")
        self.tree.heading("turma", text="Turma")
        self.tree.heading("supervisor", text="Supervisor")
        self.tree.heading("sts", text="Sts")
        self.tree.heading("oper", text="%Oper")
        self.tree.heading("premio", text="Prêmio/Desc")
        self.tree.heading("comissao", text="Valor Comis.")
        self.tree.heading("rep", text="Rep")
        self.tree.heading("mvf", text="M.V.F.")
        self.tree.heading("mvd", text="M.V.D.")

        # Colunas
        self.tree.column("id", width=70, anchor="center")
        self.tree.column("nome", width=190, anchor="w")

        for col in self.colunas:
            if col not in ("id", "nome"):
                self.tree.column(col, width=95, anchor="center")

        # Duplo clique = editar
        self.tree.bind("<Double-1>", lambda e: self.alterar())

        # ================= BOTÕES =================
        frame_botoes = tk.Frame(self.win, bg="#E0E0E8")
        frame_botoes.pack(fill=tk.X)

        def botao(txt, cmd, cor="#2E3A59"):
            return tk.Button(
                frame_botoes, text=txt, width=14, command=cmd,
                bg=cor, fg="white", relief="flat",
                font=("Segoe UI", 9, "bold"),
                cursor="hand2", activebackground="#3F51B5"
            )

        botao("Incluir", self.incluir).pack(side=tk.LEFT, padx=6, pady=7)
        botao("Alterar", self.alterar).pack(side=tk.LEFT, padx=6)
        botao("Excluir", self.excluir, "#B71C1C").pack(side=tk.LEFT, padx=6)

        # ================= STATUS =================
        self.status = tk.Label(
            self.win,
            text="Carregando operadores...",
            anchor="w",
            bg="#D6D6E5",
            font=("Segoe UI", 8)
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

        self.carregar_dados()

    # ================= BANCO =================
    def conectar(self):
        return sqlite3.connect(DB_NAME)

    def carregar_dados(self, termo=""):
        termo = (termo or "").strip().lower()

        self.tree.delete(*self.tree.get_children())
        conn = self.conectar()
        c = conn.cursor()

        c.execute("""
            SELECT id, nome, turno, turma, supervisor,
                   sts, oper, premio, comissao, rep, mvf, mvd
            FROM operadores
            ORDER BY id DESC
        """)

        dados = c.fetchall()
        conn.close()

        if termo:
            dados = [d for d in dados if termo in (d[1] or "").lower()]

        for row in dados:
            self.tree.insert("", tk.END, iid=row[0], values=row)

        self.status.config(text=f"{len(dados)} operadores cadastrados")

    def buscar(self):
        termo = self.entry_busca.get().strip()
        self.carregar_dados(termo)

    def limpar_busca(self):
        self.entry_busca.delete(0, tk.END)
        self.carregar_dados()

    # ================= UTIL =================
    def operador_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um operador")
            return None
        return int(sel[0])

    def buscar_operador(self, operador_id):
        conn = self.conectar()
        c = conn.cursor()
        c.execute("""
            SELECT id, nome, turno, turma, supervisor,
                   sts, oper, premio, comissao, rep, mvf, mvd
            FROM operadores
            WHERE id = ?
        """, (operador_id,))
        dado = c.fetchone()
        conn.close()
        return dado

    # ================= FORMULÁRIO =================
    def abrir_form(self, titulo, dados=None):
        top = tk.Toplevel(self.win)
        top.title(titulo)
        top.geometry("520x520")
        top.configure(bg="#ECECF1")
        top.transient(self.win)
        top.grab_set()

        campos = [
            ("Nome", "nome"),
            ("Turno", "turno"),
            ("Turma", "turma"),
            ("Supervisor", "supervisor"),
            ("Sts", "sts"),
            ("%Oper", "oper"),
            ("Prêmio/Desc", "premio"),
            ("Valor Comissão", "comissao"),
            ("Rep", "rep"),
            ("M.V.F.", "mvf"),
            ("M.V.D.", "mvd"),
        ]

        entradas = {}

        tk.Label(
            top, text=titulo,
            bg="#ECECF1", fg="#1A237E",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(10, 6))

        form = tk.Frame(top, bg="#ECECF1")
        form.pack(fill=tk.BOTH, expand=True, padx=14)

        for i, (label, key) in enumerate(campos):
            tk.Label(form, text=label, bg="#ECECF1", anchor="w").grid(
                row=i, column=0, sticky="w", pady=5
            )
            ent = tk.Entry(form)
            ent.grid(row=i, column=1, sticky="ew", pady=5, padx=(8, 0))
            entradas[key] = ent

        form.grid_columnconfigure(1, weight=1)

        # preencher se for alteração
        if dados:
            # dados = (id, nome, turno, turma, supervisor, sts, oper, premio, comissao, rep, mvf, mvd)
            entradas["nome"].insert(0, dados[1] or "")
            entradas["turno"].insert(0, dados[2] or "")
            entradas["turma"].insert(0, dados[3] or "")
            entradas["supervisor"].insert(0, dados[4] or "")
            entradas["sts"].insert(0, dados[5] or "")
            entradas["oper"].insert(0, "" if dados[6] is None else str(dados[6]))
            entradas["premio"].insert(0, "" if dados[7] is None else str(dados[7]))
            entradas["comissao"].insert(0, "" if dados[8] is None else str(dados[8]))
            entradas["rep"].insert(0, dados[9] or "")
            entradas["mvf"].insert(0, dados[10] or "")
            entradas["mvd"].insert(0, dados[11] or "")

        # ================= SALVAR =================
        def salvar():
            nome = entradas["nome"].get().strip()
            if not nome:
                messagebox.showwarning("Atenção", "Digite o nome do operador")
                return

            turno = entradas["turno"].get().strip()
            turma = entradas["turma"].get().strip()
            supervisor = entradas["supervisor"].get().strip()
            sts = entradas["sts"].get().strip()
            rep = entradas["rep"].get().strip()
            mvf = entradas["mvf"].get().strip()
            mvd = entradas["mvd"].get().strip()

            # campos numéricos
            def num(valor):
                valor = (valor or "").strip().replace(",", ".")
                if valor == "":
                    return None
                try:
                    return float(valor)
                except:
                    return None

            oper = num(entradas["oper"].get())
            premio = num(entradas["premio"].get())
            comissao = num(entradas["comissao"].get())

            conn = self.conectar()
            c = conn.cursor()

            if dados:  # alterar
                operador_id = dados[0]
                c.execute("""
                    UPDATE operadores SET
                        nome = ?,
                        turno = ?,
                        turma = ?,
                        supervisor = ?,
                        sts = ?,
                        oper = ?,
                        premio = ?,
                        comissao = ?,
                        rep = ?,
                        mvf = ?,
                        mvd = ?
                    WHERE id = ?
                """, (
                    nome, turno, turma, supervisor, sts,
                    oper, premio, comissao, rep, mvf, mvd,
                    operador_id
                ))
            else:  # incluir
                c.execute("""
                    INSERT INTO operadores (
                        nome, turno, turma, supervisor,
                        sts, oper, premio, comissao,
                        rep, mvf, mvd
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    nome, turno, turma, supervisor,
                    sts, oper, premio, comissao,
                    rep, mvf, mvd
                ))

            conn.commit()
            conn.close()

            self.carregar_dados()
            top.destroy()
            messagebox.showinfo("OK", "Salvo com sucesso!")

        # ================= BOTÕES =================
        botoes = tk.Frame(top, bg="#ECECF1")
        botoes.pack(fill=tk.X, padx=14, pady=12)

        tk.Button(
            botoes,
            text="Salvar",
            command=salvar,
            bg="#3949AB",
            fg="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT)

        tk.Button(
            botoes,
            text="Cancelar",
            command=top.destroy,
            bg="#B0B0B0",
            fg="black",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=8)

    # ================= AÇÕES =================
    def incluir(self):
        self.abrir_form("Incluir Operador")

    def alterar(self):
        operador_id = self.operador_selecionado()
        if not operador_id:
            return
        dados = self.buscar_operador(operador_id)
        if not dados:
            messagebox.showwarning("Erro", "Operador não encontrado")
            return
        self.abrir_form("Alterar Operador", dados=dados)

    def excluir(self):
        operador_id = self.operador_selecionado()
        if not operador_id:
            return

        if not messagebox.askyesno("Confirmar", "Deseja excluir este operador?"):
            return

        conn = self.conectar()
        c = conn.cursor()
        c.execute("DELETE FROM operadores WHERE id = ?", (operador_id,))
        conn.commit()
        conn.close()

        self.carregar_dados()
        messagebox.showinfo("OK", "Operador excluído!")

import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar


def tela_producao(root):
    win = tk.Toplevel(root)
    win.title("Produção")
    win.geometry("1150x600")
    win.configure(bg="#ECECF1")
    win.transient(root)
    win.grab_set()

    TelaProducao(win)


class TelaProducao:
    def __init__(self, root):
        self.root = root

        self.operadores = []  # (id, nome)

        self.criar_topo()
        self.criar_formulario()
        self.criar_tabela()
        self.criar_botoes()
        self.criar_status()

        self.carregar_operadores()
        self.carregar_producao()

    # ================= UI =================
    def criar_topo(self):
        topo = tk.Frame(self.root, bg="#ECECF1")
        topo.pack(fill=tk.X, padx=10, pady=(10, 4))

        tk.Label(
            topo,
            text="Produção",
            bg="#ECECF1",
            fg="#1A237E",
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT)

    def criar_formulario(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame, text="Operador:", bg="#ECECF1").grid(row=0, column=0, sticky="w")
        self.cb_operador = ttk.Combobox(frame, state="readonly", width=35)
        self.cb_operador.grid(row=0, column=1, padx=6, pady=3)

        tk.Label(frame, text="Data (AAAA-MM-DD):", bg="#ECECF1").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.entry_data = tk.Entry(frame, width=15)
        self.entry_data.grid(row=0, column=3, padx=6, pady=3)

        tk.Label(frame, text="Qtd:", bg="#ECECF1").grid(row=0, column=4, sticky="w", padx=(20, 0))
        self.entry_qtd = tk.Entry(frame, width=8)
        self.entry_qtd.grid(row=0, column=5, padx=6, pady=3)

        tk.Label(frame, text="Valor (R$):", bg="#ECECF1").grid(row=0, column=6, sticky="w", padx=(20, 0))
        self.entry_valor = tk.Entry(frame, width=10)
        self.entry_valor.grid(row=0, column=7, padx=6, pady=3)

    def criar_tabela(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        style = ttk.Style()
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        colunas = ("id", "operador", "data", "quantidade", "valor")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.heading("id", text="ID")
        self.tree.heading("operador", text="Operador")
        self.tree.heading("data", text="Data")
        self.tree.heading("quantidade", text="Qtd")
        self.tree.heading("valor", text="Valor")

        self.tree.column("id", width=70, anchor="center")
        self.tree.column("operador", width=260, anchor="w")
        self.tree.column("data", width=120, anchor="center")
        self.tree.column("quantidade", width=90, anchor="center")
        self.tree.column("valor", width=120, anchor="center")

        self.tree.bind("<Double-1>", lambda e: self.preencher_formulario())

    def criar_botoes(self):
        frame = tk.Frame(self.root, bg="#E0E0E8")
        frame.pack(fill=tk.X)

        def botao(txt, cmd, cor="#2E3A59"):
            return tk.Button(
                frame,
                text=txt,
                width=14,
                command=cmd,
                bg=cor,
                fg="white",
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
                activebackground="#3F51B5"
            )

        botao("Salvar", self.salvar).pack(side=tk.LEFT, padx=6, pady=7)
        botao("Alterar", self.alterar).pack(side=tk.LEFT, padx=6)
        botao("Excluir", self.excluir, "#B71C1C").pack(side=tk.LEFT, padx=6)
        botao("Limpar", self.limpar_form, "#455A64").pack(side=tk.LEFT, padx=6)

    def criar_status(self):
        self.status = tk.Label(
            self.root,
            text="",
            anchor="w",
            bg="#D6D6E5",
            font=("Segoe UI", 8)
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ================= DADOS =================
    def carregar_operadores(self):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id, nome FROM operadores WHERE ativo = 1 ORDER BY nome ASC")
        self.operadores = cur.fetchall()
        con.close()

        nomes = [f"{op[0]} - {op[1]}" for op in self.operadores]
        self.cb_operador["values"] = nomes
        if nomes:
            self.cb_operador.current(0)

    def carregar_producao(self):
        self.tree.delete(*self.tree.get_children())

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT p.id, o.nome, p.data, p.quantidade, p.valor
            FROM producao p
            LEFT JOIN operadores o ON o.id = p.operador_id
            ORDER BY p.id DESC
        """)
        dados = cur.fetchall()
        con.close()

        for row in dados:
            self.tree.insert("", tk.END, iid=row[0], values=row)

        self.status.config(text=f"{len(dados)} registros encontrados")

    # ================= UTIL =================
    def get_operador_id(self):
        valor = self.cb_operador.get().strip()
        if not valor:
            return None
        try:
            return int(valor.split("-")[0].strip())
        except:
            return None

    def limpar_form(self):
        self.entry_data.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)

    def preencher_formulario(self):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]

        # item = (id, operador_nome, data, qtd, valor)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, item[2] or "")

        self.entry_qtd.delete(0, tk.END)
        self.entry_qtd.insert(0, item[3] if item[3] is not None else "")

        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, item[4] if item[4] is not None else "")

    def registro_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um registro na tabela")
            return None
        return int(sel[0])

    # ================= CRUD =================
    def salvar(self):
        operador_id = self.get_operador_id()
        data = self.entry_data.get().strip()
        qtd = self.entry_qtd.get().strip()
        valor = self.entry_valor.get().strip().replace(",", ".")

        if not operador_id:
            messagebox.showwarning("Atenção", "Selecione um operador")
            return
        if not data:
            messagebox.showwarning("Atenção", "Digite a data")
            return

        try:
            qtd = int(qtd) if qtd else 0
        except:
            messagebox.showwarning("Erro", "Quantidade inválida")
            return

        try:
            valor = float(valor) if valor else 0.0
        except:
            messagebox.showwarning("Erro", "Valor inválido")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO producao (operador_id, data, quantidade, valor)
            VALUES (?, ?, ?, ?)
        """, (operador_id, data, qtd, valor))
        con.commit()
        con.close()

        self.carregar_producao()
        self.limpar_form()
        messagebox.showinfo("OK", "Produção salva!")

    def alterar(self):
        reg_id = self.registro_selecionado()
        if not reg_id:
            return

        operador_id = self.get_operador_id()
        data = self.entry_data.get().strip()
        qtd = self.entry_qtd.get().strip()
        valor = self.entry_valor.get().strip().replace(",", ".")

        if not operador_id or not data:
            messagebox.showwarning("Atenção", "Preencha operador e data")
            return

        try:
            qtd = int(qtd) if qtd else 0
        except:
            messagebox.showwarning("Erro", "Quantidade inválida")
            return

        try:
            valor = float(valor) if valor else 0.0
        except:
            messagebox.showwarning("Erro", "Valor inválido")
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE producao SET operador_id=?, data=?, quantidade=?, valor=?
            WHERE id=?
        """, (operador_id, data, qtd, valor, reg_id))
        con.commit()
        con.close()

        self.carregar_producao()
        messagebox.showinfo("OK", "Registro alterado!")

    def excluir(self):
        reg_id = self.registro_selecionado()
        if not reg_id:
            return

        if not messagebox.askyesno("Confirmar", "Deseja excluir este registro?"):
            return

        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM producao WHERE id = ?", (reg_id,))
        con.commit()
        con.close()

        self.carregar_producao()
        messagebox.showinfo("OK", "Registro excluído!")

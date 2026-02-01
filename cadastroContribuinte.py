import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_NAME

def tela_cadastro_contribuintes(root, callback_atualizar=None):

    class CadastroContribuinte(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)

            self.title("Cadastro de Contribuintes")
            self.resizable(False, False)
            self.configure(bg="#ECECF1")

            self.fonte = ("Segoe UI", 9)
            self.centralizar(980, 620)
            self.criar_tabela()
            self.create_widgets()
            self.definir_codigo_automatico()

        def centralizar(self, largura, altura):
            self.update_idletasks()
            x = (self.winfo_screenwidth() // 2) - (largura // 2)
            y = (self.winfo_screenheight() // 2) - (altura // 2)
            self.geometry(f"{largura}x{altura}+{x}+{y}")

        def conectar(self):
            return sqlite3.connect(DB_NAME)

        def criar_tabela(self):
            with self.conectar() as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS contribuintes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        codigo INTEGER, nome TEXT, categoria TEXT, sexo TEXT,
                        status TEXT, nascimento TEXT, inscricao TEXT,
                        telefone1 TEXT, telefone2 TEXT, email TEXT,
                        rua TEXT, bairro TEXT, cidade TEXT,
                        cpf TEXT, rg TEXT, observacoes TEXT)""")

        def gerar_proximo_codigo(self):
            with self.conectar() as con:
                cur = con.cursor()
                cur.execute("SELECT MAX(CAST(codigo AS INTEGER)) FROM contribuintes")
                resultado = cur.fetchone()[0]
                return 1001 if resultado is None else int(resultado) + 1

        def definir_codigo_automatico(self):
            self.ent_codigo.config(state='normal')
            self.ent_codigo.delete(0, tk.END)
            self.ent_codigo.insert(0, str(self.gerar_proximo_codigo()))
            self.ent_codigo.config(state='readonly')

        def create_widgets(self):

            # 🔹 ESTILO
            style = ttk.Style()
            style.configure("TLabelframe", background="#ECECF1", font=("Segoe UI", 9, "bold"))
            style.configure("TLabel", background="#ECECF1", font=self.fonte)

            # ================= TOPO =================
            topo = ttk.LabelFrame(self, text="Dados Principais")
            topo.place(x=10, y=10, width=960, height=130)

            ttk.Label(topo, text="Código").place(x=10, y=10)
            self.ent_codigo = tk.Entry(topo, width=10, font=("Segoe UI", 9, "bold"),
                                       fg="#0B5394", justify="center", state="readonly")
            self.ent_codigo.place(x=70, y=10)

            ttk.Label(topo, text="Nome").place(x=150, y=10)
            self.ent_nome = tk.Entry(topo, width=45)
            self.ent_nome.place(x=200, y=10)

            ttk.Label(topo, text="Categoria").place(x=580, y=10)
            self.cb_categoria = ttk.Combobox(topo, values=["A", "B", "C"], width=5)
            self.cb_categoria.place(x=650, y=10)

            ttk.Label(topo, text="Sexo").place(x=720, y=10)
            self.cb_sexo = ttk.Combobox(topo, values=["M", "F"], width=5)
            self.cb_sexo.place(x=760, y=10)

            ttk.Label(topo, text="Status").place(x=10, y=50)
            self.ent_status = tk.Entry(topo, width=15)
            self.ent_status.insert(0, "FICHA NOVA")
            self.ent_status.place(x=70, y=50)

            ttk.Label(topo, text="Nascimento").place(x=230, y=50)
            self.ent_nasc = tk.Entry(topo, width=12)
            self.ent_nasc.place(x=310, y=50)

            ttk.Label(topo, text="Inscrição").place(x=450, y=50)
            self.ent_insc = tk.Entry(topo, width=12)
            self.ent_insc.place(x=520, y=50)

            # ================= CONTATOS =================
            contatos = ttk.LabelFrame(self, text="Contatos")
            contatos.place(x=10, y=150, width=960, height=80)

            ttk.Label(contatos, text="Telefone 1").place(x=10, y=10)
            self.ent_tel1 = tk.Entry(contatos, width=18); self.ent_tel1.place(x=80, y=10)
            ttk.Label(contatos, text="Telefone 2").place(x=240, y=10)
            self.ent_tel2 = tk.Entry(contatos, width=18); self.ent_tel2.place(x=310, y=10)
            ttk.Label(contatos, text="E-mail").place(x=470, y=10)
            self.ent_email = tk.Entry(contatos, width=40); self.ent_email.place(x=520, y=10)

            # ================= ENDEREÇO =================
            endereco = ttk.LabelFrame(self, text="Endereço")
            endereco.place(x=10, y=240, width=960, height=100)

            ttk.Label(endereco, text="Rua").place(x=10, y=10)
            self.ent_rua = tk.Entry(endereco, width=60); self.ent_rua.place(x=50, y=10)
            ttk.Label(endereco, text="Bairro").place(x=10, y=45)
            self.ent_bairro = tk.Entry(endereco, width=25); self.ent_bairro.place(x=60, y=45)
            ttk.Label(endereco, text="Cidade").place(x=300, y=45)
            self.ent_cidade = tk.Entry(endereco, width=25); self.ent_cidade.place(x=360, y=45)

            # ================= DOCUMENTOS =================
            docs = ttk.LabelFrame(self, text="Documentos")
            docs.place(x=10, y=350, width=960, height=80)

            ttk.Label(docs, text="CPF").place(x=10, y=10)
            self.ent_cpf = tk.Entry(docs, width=20); self.ent_cpf.place(x=50, y=10)
            ttk.Label(docs, text="RG").place(x=250, y=10)
            self.ent_rg = tk.Entry(docs, width=20); self.ent_rg.place(x=290, y=10)

            # ================= OBS =================
            obs = ttk.LabelFrame(self, text="Observações")
            obs.place(x=10, y=440, width=960, height=90)
            self.txt_obs = tk.Text(obs, height=4, font=self.fonte)
            self.txt_obs.pack(fill="both", padx=5, pady=5)

            # ================= BOTÕES =================
            frame_btn = tk.Frame(self, bg="#ECECF1")
            frame_btn.place(x=0, y=540, width=980, height=60)

            def btn(txt, cmd, cor):
                return tk.Button(frame_btn, text=txt, width=14, command=cmd,
                                 bg=cor, fg="white", relief="flat",
                                 font=("Segoe UI", 9, "bold"), cursor="hand2")

            btn("💾 Gravar", self.salvar, "#2E7D32").pack(side="right", padx=10)
            btn("Cancelar", self.destroy, "#B71C1C").pack(side="right")

        def salvar(self):
            if not self.ent_nome.get():
                messagebox.showwarning("Atenção", "Informe o nome.")
                return

            try:
                with self.conectar() as con:
                    cur = con.cursor()
                    cur.execute("""INSERT INTO contribuintes 
                        (codigo, nome, categoria, sexo, status, nascimento, inscricao,
                         telefone1, telefone2, email, rua, bairro, cidade, cpf, rg, observacoes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (self.ent_codigo.get(), self.ent_nome.get(), self.cb_categoria.get(),
                         self.cb_sexo.get(), self.ent_status.get(), self.ent_nasc.get(),
                         self.ent_insc.get(), self.ent_tel1.get(), self.ent_tel2.get(),
                         self.ent_email.get(), self.ent_rua.get(), self.ent_bairro.get(),
                         self.ent_cidade.get(), self.ent_cpf.get(), self.ent_rg.get(),
                         self.txt_obs.get("1.0", tk.END).strip()))

                messagebox.showinfo("Sucesso", "Contribuinte salvo com sucesso!")

                if callback_atualizar:
                    callback_atualizar()

                self.destroy()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    CadastroContribuinte(root)

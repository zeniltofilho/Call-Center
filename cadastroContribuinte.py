import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_NAME

def tela_cadastro_contribuintes(root, callback_atualizar=None):

    class CadastroContribuinte(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)

            self.title("Contribuintes")
            self.resizable(False, False)
            self.configure(bg="#d9d9d9")

            self.centralizar(980, 620)
            self.criar_tabela()
            self.create_widgets()
            
            # Gera o código assim que a tela abre
            self.definir_codigo_automatico()

        def centralizar(self, largura, altura):
            x = (self.winfo_screenwidth() // 2) - (largura // 2)
            y = (self.winfo_screenheight() // 2) - (altura // 2)
            self.geometry(f"{largura}x{altura}+{x}+{y}")

        def conectar(self):
            return sqlite3.connect(DB_NAME)

        def criar_tabela(self):
            with self.conectar() as con:
                cur = con.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS contribuintes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        codigo INTEGER,
                        nome TEXT,
                        categoria TEXT,
                        sexo TEXT,
                        status TEXT,
                        nascimento TEXT,
                        inscricao TEXT,
                        telefone1 TEXT,
                        telefone2 TEXT,
                        email TEXT,
                        rua TEXT,
                        bairro TEXT,
                        cidade TEXT,
                        cpf TEXT,
                        rg TEXT,
                        observacoes TEXT
                    )
                """)

        # --- NOVIDADE: Lógica para gerar código automático ---
        def gerar_proximo_codigo(self):
            try:
                with self.conectar() as con:
                    cur = con.cursor()
                    # Seleciona o maior valor da coluna codigo
                    cur.execute("SELECT MAX(CAST(codigo AS INTEGER)) FROM contribuintes")
                    resultado = cur.fetchone()[0]
                    if resultado is None:
                        return 1001  # Começa em 1001 se for o primeiro registro
                    return int(resultado) + 1
            except Exception as e:
                print(f"Erro ao gerar código: {e}")
                return 1

        def definir_codigo_automatico(self):
            novo_cod = self.gerar_proximo_codigo()
            self.ent_codigo.config(state='normal') # Habilita para inserir
            self.ent_codigo.delete(0, tk.END)
            self.ent_codigo.insert(0, str(novo_cod))
            self.ent_codigo.config(state='readonly') # Trava novamente

        def create_widgets(self):
            fonte = ("Segoe UI", 9)

            # ================= TOPO =================
            topo = tk.LabelFrame(self, text="Dados principais", bg="#d9d9d9", font=fonte)
            topo.place(x=10, y=10, width=960, height=130)

            tk.Label(topo, text="Código").place(x=10, y=10)
            # Campo Código agora é Readonly (apenas leitura)
            self.ent_codigo = tk.Entry(topo, width=10, font=(fonte[0], fonte[1], "bold"), fg="blue")
            self.ent_codigo.place(x=60, y=10)

            tk.Label(topo, text="Nome").place(x=150, y=10)
            self.ent_nome = tk.Entry(topo, width=45)
            self.ent_nome.place(x=200, y=10)

            tk.Label(topo, text="Categoria").place(x=580, y=10)
            self.cb_categoria = ttk.Combobox(topo, values=["A", "B", "C"], width=5)
            self.cb_categoria.place(x=650, y=10)

            tk.Label(topo, text="Sexo").place(x=720, y=10)
            self.cb_sexo = ttk.Combobox(topo, values=["M", "F"], width=5)
            self.cb_sexo.place(x=760, y=10)

            tk.Label(topo, text="Status").place(x=10, y=45)
            self.ent_status = tk.Entry(topo, width=15)
            self.ent_status.insert(0, "FICHA NOVA")
            self.ent_status.place(x=60, y=45)

            tk.Label(topo, text="Nascimento").place(x=230, y=45)
            self.ent_nasc = tk.Entry(topo, width=12)
            self.ent_nasc.place(x=310, y=45)

            tk.Label(topo, text="Inscrição").place(x=450, y=45)
            self.ent_insc = tk.Entry(topo, width=12)
            self.ent_insc.place(x=520, y=45)

            # ... (Restante dos widgets: Contatos, Endereço, Documentos permanecem iguais) ...
            
            # ================= CONTATOS =================
            contatos = tk.LabelFrame(self, text="Contatos", bg="#d9d9d9")
            contatos.place(x=10, y=150, width=960, height=80)
            tk.Label(contatos, text="Telefone 1").place(x=10, y=10)
            self.ent_tel1 = tk.Entry(contatos, width=18); self.ent_tel1.place(x=80, y=10)
            tk.Label(contatos, text="Telefone 2").place(x=240, y=10)
            self.ent_tel2 = tk.Entry(contatos, width=18); self.ent_tel2.place(x=310, y=10)
            tk.Label(contatos, text="E-mail").place(x=470, y=10)
            self.ent_email = tk.Entry(contatos, width=40); self.ent_email.place(x=520, y=10)

            # ================= ENDEREÇO =================
            endereco = tk.LabelFrame(self, text="Endereço", bg="#d9d9d9")
            endereco.place(x=10, y=240, width=960, height=100)
            tk.Label(endereco, text="Rua").place(x=10, y=10)
            self.ent_rua = tk.Entry(endereco, width=60); self.ent_rua.place(x=50, y=10)
            tk.Label(endereco, text="Bairro").place(x=10, y=45)
            self.ent_bairro = tk.Entry(endereco, width=25); self.ent_bairro.place(x=60, y=45)
            tk.Label(endereco, text="Cidade").place(x=300, y=45)
            self.ent_cidade = tk.Entry(endereco, width=25); self.ent_cidade.place(x=360, y=45)

            # ================= DOCUMENTOS =================
            docs = tk.LabelFrame(self, text="Documentos", bg="#d9d9d9")
            docs.place(x=10, y=350, width=960, height=80)
            tk.Label(docs, text="CPF").place(x=10, y=10)
            self.ent_cpf = tk.Entry(docs, width=20); self.ent_cpf.place(x=50, y=10)
            tk.Label(docs, text="RG").place(x=250, y=10)
            self.ent_rg = tk.Entry(docs, width=20); self.ent_rg.place(x=290, y=10)

            # ================= OBSERVAÇÕES =================
            obs = tk.LabelFrame(self, text="Observações", bg="#d9d9d9")
            obs.place(x=10, y=440, width=960, height=90)
            self.txt_obs = tk.Text(obs, height=4)
            self.txt_obs.pack(fill="both", padx=5, pady=5)

            # ================= BOTÕES =================
            frame_btn = tk.Frame(self, bg="#d9d9d9")
            frame_btn.place(x=0, y=540, width=980, height=60)
            tk.Button(frame_btn, text="💾 Gravar", width=14, command=self.salvar).pack(side="right", padx=10)
            tk.Button(frame_btn, text="❌ Cancelar", width=14, command=self.destroy).pack(side="right")

        def salvar(self):
            if not self.ent_nome.get():
                messagebox.showwarning("Atenção", "Informe o nome.")
                return

            try:
                con = self.conectar()
                cur = con.cursor()

                dados = (
                    self.ent_codigo.get(),
                    self.ent_nome.get(),
                    self.cb_categoria.get(),
                    self.cb_sexo.get(),
                    self.ent_status.get(),
                    self.ent_nasc.get(),
                    self.ent_insc.get(),
                    self.ent_tel1.get(),
                    self.ent_tel2.get(),
                    self.ent_email.get(),
                    self.ent_rua.get(),
                    self.ent_bairro.get(),
                    self.ent_cidade.get(),
                    self.ent_cpf.get(),
                    self.ent_rg.get(),
                    self.txt_obs.get("1.0", tk.END).strip()
                )

                cur.execute("""
                    INSERT INTO contribuintes 
                    (codigo, nome, categoria, sexo, status, nascimento, inscricao, 
                     telefone1, telefone2, email, rua, bairro, cidade, cpf, rg, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, dados)

                con.commit()
                con.close()

                messagebox.showinfo("Sucesso", "Contribuinte salvo com sucesso!")
                
                if callback_atualizar:
                    callback_atualizar()
                
                self.destroy() # Fecha a janela após salvar
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    CadastroContribuinte(root)
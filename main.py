import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

from database import init_db
from dashboard import Dashboard
from operadores import tela_operadores
from mensageiros import tela_mensageiros
from contribuintes import tela_contribuintes
from recibo import tela_recibo
from boletos import tela_boletos
from supervisor import tela_supervisor
from relatorios import relatorio_excel
from backup import fazer_backup, importar_backup

# ---------------- CORES ----------------
BG_TOOLBAR = "#B7B7C4"
BTN_NORMAL = "#355CAA"
BTN_HOVER = "#9CA0EC"


class CallCenterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Telemarketing")
        self.root.geometry("1200x720")
        self.root.state("zoomed")

        self.icons = {}
        self.carregar_icones()

        self.create_menu()
        self.create_toolbar()

        self.dashboard = Dashboard(self.root)

    def atualizar_dashboard(self):
        self.dashboard.atualizar()

    # ================= ÍCONES =================
    def carregar_icones(self):
        base = Path(__file__).parent / "icons"
        tamanho = (24, 24)

        def load(nome):
            img = Image.open(base / nome).resize(tamanho, Image.LANCZOS)
            return ImageTk.PhotoImage(img)

        try:
            self.icons["Contribuintes"] = load("contribuintes.png")
            self.icons["Recibos"] = load("recibos.png")
            self.icons["Boletos"] = load("boletos.png")
            self.icons["Operadores"] = load("operadores.png")
            self.icons["Mensageiros"] = load("mensageiros.png")
            self.icons["Supervisores"] = load("supervisor.png")
            self.icons["Sair"] = load("sair.png")
        except Exception as e:
            print("Erro ao carregar ícones:", e)

    # ================= MENU =================
    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # -------- Cadastros --------
        menu_cadastros = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Cadastros", menu=menu_cadastros)

        menu_cadastros.add_command(
            label="Contribuintes", command=lambda: tela_contribuintes(self.root))
        menu_cadastros.add_separator()
        menu_cadastros.add_command(
            label="Recibos", command=lambda: tela_recibo(self.root))
        menu_cadastros.add_command(
            label="Boletos", command=lambda: tela_boletos(self.root))
        menu_cadastros.add_command(label="Cobrança")
        menu_cadastros.add_separator()
        menu_cadastros.add_command(
            label="Operadores", command=lambda: tela_operadores(self.root))
        menu_cadastros.add_command(
            label="Mensageiros", command=lambda: tela_mensageiros(self.root))
        menu_cadastros.add_command(label="Supervisores", command=lambda: tela_supervisor(self.root))
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Ruas")
        menu_cadastros.add_command(label="Setores")
        menu_cadastros.add_command(label="E-mail")

        # -------- Consultas --------
        menu_consultas = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Consultas", menu=menu_consultas)
        menu_consultas.add_command(label="Recibos")
        menu_consultas.add_command(label="Boletos/Débitos/Cartão")
        menu_consultas.add_separator()
        menu_consultas.add_command(label="Operadores")
        menu_consultas.add_command(label="Mensageiros")
        menu_consultas.add_separator()
        menu_consultas.add_command(label="Eventos do Recibo")
        menu_consultas.add_command(label="Gerencial p/Valor")

        # -------- Impressão --------
        menu_impressao = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Impressão", menu=menu_impressao)
        menu_impressao.add_command(label="Recibos")
        menu_impressao.add_command(label="Relatórios")
        menu_impressao.add_command(label="GeradorSqlDinamico")

        # -------- Opções --------
        menu_opcoes = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Opções", menu=menu_opcoes)
        menu_opcoes.add_command(label="Cobrança de Recibos")
        menu_opcoes.add_command(label="Cobrança de Boletos")
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Gera Repique")
        menu_opcoes.add_command(label="Troca Distribuição")
        menu_opcoes.add_command(label="Troca Status Contribuinte")
        menu_opcoes.add_command(label="Controle Escelsa")
        menu_opcoes.add_command(label="Excel", command=relatorio_excel)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Campanha Extra")
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Bancos")
        menu_opcoes.add_command(label="Cartão de Crédito")
        menu_opcoes.add_command(label="Rota")
        menu_opcoes.add_command(label="Gera Boletos para Inadimplentes")

        # -------- Tabelas --------
        menu_tabelas = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tabelas", menu=menu_tabelas)
        menu_tabelas.add_command(label="Status")
        menu_tabelas.add_command(label="Parâmetros")
        menu_tabelas.add_separator()
        menu_tabelas.add_command(label="Grupo de Usuários")
        menu_tabelas.add_command(label="Níveis de Acesso")
        menu_tabelas.add_separator()
        menu_tabelas.add_command(label="Itens")
        menu_tabelas.add_command(label="Fluxo de Caixa")
        menu_tabelas.add_command(label="Produtos")
        menu_tabelas.add_command(label="Tipo de Pagamentos")
        menu_tabelas.add_separator()
        menu_tabelas.add_command(label="Feriados")

        # -------- Utilitários --------
        menu_utilitarios = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Utilitários", menu=menu_utilitarios)
        menu_utilitarios.add_command(label="Parâmetros do Sistema")
        menu_utilitarios.add_command(label="Site Web")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Auditoria")
        menu_utilitarios.add_command(label="Importa Arquivo Ruas dos Correios")
        menu_utilitarios.add_command(label="Atualiza Intervalo")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Mudança de Usuário")
        menu_utilitarios.add_command(label="Troca Senha")
        menu_utilitarios.add_command(label="Caixa Postal")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Backup", command=fazer_backup)
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Importar Backup", command=importar_backup)
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Atualização do Software")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Solicitar Manutenção AnyDesk")
        menu_utilitarios.add_command(label="Solicitar Manutenção TeamViewer")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Ticket")
        menu_utilitarios.add_command(label="Gerar Dados Estatísticos")
        menu_utilitarios.add_command(label="Sobre")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Fechar", command=self.root.destroy)

        self.root.config(menu=menu_bar)

    # ================= TOOLBAR =================
    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg=BG_TOOLBAR, height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        botoes = [
            ("Contribuintes", self.icons.get("Contribuintes"), lambda: tela_contribuintes(self.root)),
            ("Recibos", self.icons.get("Recibos"), lambda: tela_recibo(self.root)),
            ("Boletos", self.icons.get("Boletos"), lambda: tela_boletos(self.root)),
            ("Operadores", self.icons.get("Operadores"), lambda: tela_operadores(self.root)),
            ("Mensageiros", self.icons.get("Mensageiros"), lambda: tela_mensageiros(self.root)),
            ("Supervisores", self.icons.get("Supervisores"), lambda: tela_supervisor(self.root)),
            ("Sair", self.icons.get("Sair"), self.root.quit)
        ]

        for txt, icon, cmd in botoes:
            btn = tk.Button(
                toolbar,
                text=txt,
                image=icon,
                compound="top",
                command=cmd,
                bg=BTN_NORMAL,
                fg="white",
                activebackground=BTN_HOVER,
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=6, pady=4)

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_NORMAL))


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = CallCenterApp(root)
    root.mainloop()

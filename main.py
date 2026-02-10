import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# Pillow (seguro)
try:
    from PIL import Image, ImageTk
except:
    Image = None
    ImageTk = None

# Telas
from produ import tela_producao
from ranking import tela_ranking
from operadores import tela_operadores
from mensageiros import tela_mensageiros
from contribuintes import tela_contribuintes
from recibo import tela_recibo
from boletos import tela_boletos
from supervisor import tela_supervisor

from database import init_db
init_db()

# ================= FUNÇÕES AUXILIARES =================
def relatorio_excel():
    messagebox.showinfo("Excel", "Relatório Excel em desenvolvimento")

def visualizar_recibo(root):
    messagebox.showinfo("Recibo", "Visualização de recibo em desenvolvimento")

def fazer_backup():
    messagebox.showinfo("Backup", "Backup realizado (simulação)")

def importar_backup():
    messagebox.showinfo("Backup", "Importação de backup em desenvolvimento")

# ================= CORES =================
BG_APP = "#F4F6F8"
HEADER = "#2B055C"
TOOLBAR_BG = "#503692"
TOOLBAR_HOVER = "#603AC0"
SUBMENU = "#E9E9EE"
CARD_BG = "#FFFFFF"
TEXT = "#2E2E2E"
AZUL = "#2F80ED"
VERDE = "#27AE60"
VERMELHO = "#EB5757"


class CallCenterApp:

    # ================= HEADER =================
    def create_header(self):
        header = tk.Frame(self.root, bg=HEADER, height=50)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="",
            bg=HEADER,
            fg="white",
            font=("Segoe UI", 1, "bold")
        ).pack(side=tk.LEFT, padx=20)


    def __init__(self, root):
        self.root = root
        self.root.title("Call Center Dashboard")
        self.root.state("zoomed")
        self.root.configure(bg=BG_APP)

        self.icons = {}
        self.carregar_icones()

        self.create_header()
        self.create_menu()      # corrigido
        self.create_toolbar()
        self.create_submenu()   # agora existe
        self.create_dashboard()

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
        menu_cadastros.add_command(
            label="Supervisores", command=lambda: tela_supervisor(self.root))
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
        menu_tabelas.add_command(
            label="Ajuste Recibo", command=lambda: visualizar_recibo(self.root))
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
        menu_utilitarios.add_command(
            label="Importar Backup", command=importar_backup)
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

    # ================= SUBMENU =================
    def create_submenu(self):
        frame = tk.Frame(self.root, bg=SUBMENU, height=30)
        frame.pack(fill=tk.X)

        tk.Label(
            frame,
            text="Sistema de Gestão - Call Center",
            bg=SUBMENU,
            fg=TEXT,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=15)

    # ================= TOOLBAR =================
    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg=TOOLBAR_BG, height=70)
        toolbar.pack(fill=tk.X)

        botoes = [
            ("Contribuintes", "contribuintes.png", lambda: tela_contribuintes(self.root)),
            ("Recibos", "recibos.png", lambda: tela_recibo(self.root)),
            ("Boletos", "boletos.png", lambda: tela_boletos(self.root)),
            ("Operadores", "operadores.png", lambda: tela_operadores(self.root)),
            ("Mensageiros", "mensageiros.png", lambda: tela_mensageiros(self.root)),
            ("Supervisores", "supervisor.png", lambda: tela_supervisor(self.root)),
            ("Produção", "producao.png", lambda: tela_producao(self.root)),  # sem acento
            ("Ranking", "ranking.png", lambda: tela_ranking(self.root)),
            ("Sair", "sair.png", self.root.quit)
        ]

        for txt, icon_name, cmd in botoes:
            icon = self.icons.get(icon_name)

            btn = tk.Button(
                toolbar,
                text=txt,
                image=icon,
                compound="top",
                command=cmd,
                bg=TOOLBAR_BG,
                fg="white",
                activebackground=TOOLBAR_HOVER,
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=8, pady=6)

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=TOOLBAR_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=TOOLBAR_BG))

    # ================= DASHBOARD =================
    def create_dashboard(self):
        container = tk.Frame(self.root, bg=BG_APP)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        for i in range(4):
            container.columnconfigure(i, weight=1)

        self.criar_card(container, "Service level", "71%", "< 80%", 0, 0, VERMELHO)
        self.criar_card(container, "Longest wait time", "09:47", "< 08:00", 0, 1, TEXT)
        self.criar_card(container, "Agent contacts", "375", "", 0, 2, AZUL)
        self.criar_card(container, "Average wait", "02:51", "< 05:00", 0, 3, VERDE)

    # ================= CARD =================
    def criar_card(self, parent, titulo, valor, meta, row, col, cor):
        card = tk.Frame(parent, bg=CARD_BG, bd=1, relief="solid")
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        tk.Label(card, text=titulo, bg=CARD_BG, fg="#666", font=("Segoe UI", 10)).pack(anchor="w", padx=15, pady=10)
        tk.Label(card, text=valor, bg=CARD_BG, fg=cor, font=("Segoe UI", 28, "bold")).pack()

        if meta:
            tk.Label(card, text=meta, bg=CARD_BG, fg="#888", font=("Segoe UI", 9)).pack()

    # ================= ÍCONES =================
    def carregar_icones(self):
        base = Path(__file__).parent / "icons"
        tamanho = (32, 32)

        def load(nome):
            if Image is None:
                return None
            try:
                caminho = base / nome
                if caminho.exists():
                    img = Image.open(caminho).resize(tamanho, Image.LANCZOS)
                    return ImageTk.PhotoImage(img)
            except:
                pass
            return None

        nomes = [
            "contribuintes.png",
            "recibos.png",
            "boletos.png",
            "operadores.png",
            "mensageiros.png",
            "supervisor.png",
            "producao.png",  # sem acento
            "ranking.png",
            "sair.png"
        ]

        for n in nomes:
            self.icons[n] = load(n)


# ================= EXECUÇÃO =================
if __name__ == "__main__":
    root = tk.Tk()
    app = CallCenterApp(root)
    root.mainloop()

import tkinter as tk
from database import init_db
from dashboard import Dashboard
from operadores import tela_operadores
from mensageiros import tela_mensageiros
from producao import tela_producao
from metas import tela_metas
from relatorios import relatorio_pdf, relatorio_excel
from contribuintes import tela_contribuintes
from recibo import tela_recibo

# --------------------------------------------------


class CallCenterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Telemarketing")
        self.root.geometry("1200x720")
        self.root.state("zoomed")

        self.create_menu()
        self.create_toolbar()

        self.dashboard = Dashboard(self.root)

    def atualizar_dashboard(self):
        self.dashboard.atualizar()

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
            label="Boletos" , command=lambda: tela_boleto(self.root))
        menu_cadastros.add_command(label="Cobrança")
        menu_cadastros.add_separator()
        menu_cadastros.add_command(
            label="Operadores", command=lambda: tela_operadores(self.root))
        menu_cadastros.add_command(
            label="Mensageiros", command=lambda: tela_mensageiros(self.root))
        menu_cadastros.add_command(label="Supervisores")
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
        menu_opcoes.add_command(label="Campanha Extra")
        menu_opcoes.add_command(label="Bancos")
        menu_opcoes.add_command(label="Cartão de Crédito")
        menu_opcoes.add_command(label="Rota")
        menu_opcoes.add_command(label="Gera Boletos para Inadimplentes")
        menu_opcoes.add_command(label="Registra Boletos na Iugu")

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
        menu_tabelas.add_command(label="Feriados")

        # -------- Utilitários --------
        menu_utilitarios = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Utilitários", menu=menu_utilitarios)
        menu_utilitarios.add_command(label="Parâmetros do Sistema")
        menu_utilitarios.add_command(label="Site Web")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Auditoria")
        menu_utilitarios.add_command(label="Importa Arquivo Ruas dos Correios")
        menu_utilitarios.add_command(label="Listagem Voltar Backup - 3")
        menu_utilitarios.add_command(label="Atualiza Intervalo")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Mudança de Usuário")
        menu_utilitarios.add_command(label="Troca Senha")
        menu_utilitarios.add_command(label="Caixa Postal")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Backup")
        menu_utilitarios.add_command(label="Atualização do Software")
        menu_utilitarios.add_command(label="Solicitar Manutenção AnyDesk")
        menu_utilitarios.add_command(label="Solicitar Manutenção TeamViewer")
        menu_utilitarios.add_command(label="Reconectar ao Banco de Dados")
        menu_utilitarios.add_command(label="Ticket")
        menu_utilitarios.add_command(label="Gerar Dados Estatísticos")
        menu_utilitarios.add_command(label="Sobre")
        menu_utilitarios.add_separator()
        menu_utilitarios.add_command(label="Fechar", command=self.root.destroy)

        self.root.config(menu=menu_bar)

    # ================= TOOLBAR =================
    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        botoes = [
            ("Contribuintes", lambda: tela_contribuintes(self.root)),
            ("Recibos", lambda: tela_recibo(self.root)),
            ("Bol/Deb/Car", lambda: tela_metas(self.root, self.atualizar_dashboard)),
            ("Operadores", lambda: tela_operadores(self.root)),
            ("Mensageiros", lambda: tela_mensageiros(self.root)),
            ("Supervisores", lambda: tela_operadores(self.root)),
            ("Ruas", lambda: tela_operadores(self.root)),
            ("Setores", lambda: tela_operadores(self.root)),
            ("Usuários", lambda: tela_operadores(self.root)),

            # ("PDF", relatorio_pdf),
            # ("Excel", relatorio_excel),

            ("Sair", self.root.quit)
        ]

        for txt, cmd in botoes:
            tk.Button(toolbar, text=txt, width=12, command=cmd).pack(
                side=tk.LEFT, padx=2, pady=2
            )


# ================= MAIN =================
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = CallCenterApp(root)
    root.mainloop()

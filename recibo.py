import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import conectar
import webbrowser
import urllib.parse
import os
import pyautogui
import time
from cadastro_recibo import tela_cadastro_recibo

# NOVO: layout + impressão PDF
from visualizarRecibo import visualizar_recibo, imprimir_recibo_pdf


# ================= TELA =================
def tela_recibo(root, codigo_contribuinte=None, nome_contribuinte="TODOS"):
    janela = tk.Toplevel(root)
    janela.title(f"Recibos - {nome_contribuinte}")
    janela.geometry("1250x600")
    janela.configure(bg="#ECECF1")
    janela.transient(root)
    janela.grab_set()

    TelaRecibos(janela, codigo_contribuinte, nome_contribuinte)


class TelaRecibos:
    def __init__(self, root, codigo_contribuinte, nome_contribuinte):
        self.root = root
        self.codigo_contribuinte = codigo_contribuinte
        self.nome_contribuinte = nome_contribuinte

        self.lbl_cliente = tk.Label(
            self.root,
            text=f"Contribuinte: {self.nome_contribuinte}",
            bg="#ECECF1",
            fg="#1A237E",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        )
        self.lbl_cliente.pack(fill=tk.X, padx=10, pady=(8, 0))

        self.criar_tabela()
        self.criar_botoes()
        self.criar_barra_status()
        self.carregar_dados_banco()

    # ================= TABELA =================
    def criar_tabela(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        style = ttk.Style()
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        # ADICIONADO: Tipo + PDF
        self.colunas = ["ID", "Contribuinte", "Tipo", "Valor", "Vencimento", "Nosso Número", "Operador", "PDF"]
        self.tree = ttk.Treeview(frame, columns=self.colunas, show="headings")

        larguras = [70, 260, 130, 100, 120, 140, 140, 230]
        for col, w in zip(self.colunas, larguras):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=tk.CENTER)

        self.tree.column("Contribuinte", anchor="w")
        self.tree.column("PDF", anchor="w")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ================= BOTÕES =================
    def criar_botoes(self):
        frame = tk.Frame(self.root, bg="#E0E0E8")
        frame.pack(fill=tk.X)

        def botao(txt, cmd, cor="#2E3A59", w=13):
            return tk.Button(
                frame, text=txt, width=w, command=cmd,
                bg=cor, fg="white", relief="flat",
                font=("Segoe UI", 9, "bold"),
                activebackground="#3F51B5",
                cursor="hand2"
            )

        botao("Incluir", self.incluir).pack(side=tk.LEFT, padx=5, pady=6)
        botao("Alterar", self.alterar).pack(side=tk.LEFT, padx=5)
        botao("Excluir", self.excluir, "#B71C1C").pack(side=tk.LEFT, padx=5)

        # NOVOS BOTÕES
        botao("🖨️ Emitir PDF", self.emitir_pdf, "#4A148C", w=14).pack(side=tk.LEFT, padx=5)
        botao("⚙️ Ajuste Layout", self.ajuste_layout, "#0D47A1", w=15).pack(side=tk.LEFT, padx=5)

        botao("WhatsApp PDF", self.whatsapp_pdf, "#1B5E20", w=15).pack(side=tk.LEFT, padx=5)

    # ================= STATUS / PESQUISA =================
    def criar_barra_status(self):
        frame = tk.Frame(self.root, bg="#ECECF1")
        frame.pack(fill=tk.X, padx=8)

        tk.Label(frame, text="Pesquisar:", bg="#ECECF1", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.pesquisa = tk.Entry(frame, width=35)
        self.pesquisa.pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame, text="Buscar", command=self.pesquisar,
            bg="#3949AB", fg="white", relief="flat"
        ).pack(side=tk.LEFT)

        self.status = tk.Label(
            self.root,
            text="",
            anchor="w",
            bg="#D6D6E5",
            font=("Segoe UI", 8)
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    # ================= BANCO =================
    def carregar_dados_banco(self, termo=""):
        con = conectar()
        cur = con.cursor()
        termo = (termo or "").strip()

        if self.codigo_contribuinte:
            sql = """
                SELECT r.id,
                       c.nome,
                       COALESCE(r.tipo, '') as tipo,
                       r.valor,
                       r.vencimento,
                       r.nosso_num,
                       r.operador,
                       COALESCE(r.pdf, '') as pdf
                FROM recibos r
                JOIN contribuintes c ON c.codigo = r.contrib
                WHERE r.contrib = ?
                ORDER BY r.id DESC
            """
            params = (self.codigo_contribuinte,)
        else:
            sql = """
                SELECT r.id,
                       c.nome,
                       COALESCE(r.tipo, '') as tipo,
                       r.valor,
                       r.vencimento,
                       r.nosso_num,
                       r.operador,
                       COALESCE(r.pdf, '') as pdf
                FROM recibos r
                JOIN contribuintes c ON c.codigo = r.contrib
                ORDER BY r.id DESC
            """
            params = ()

        cur.execute(sql, params)
        registros = cur.fetchall()
        con.close()

        if termo:
            registros = [r for r in registros if termo.lower() in (r[1] or "").lower()]

        self.tree.delete(*self.tree.get_children())
        for r in registros:
            self.tree.insert("", "end", iid=r[0], values=r)

        self.status.config(text=f"{len(registros)} recibos encontrados")

    # ================= UTIL =================
    def recibo_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um recibo")
            return None
        return sel[0]

    def dados_recibo_selecionado(self):
        rid = self.recibo_selecionado()
        if not rid:
            return None
        vals = self.tree.item(rid, "values")
        return {
            "id": int(vals[0]),
            "nome": vals[1],
            "tipo": vals[2] or "",
            "valor": vals[3],
            "vencimento": vals[4],
            "nosso_num": vals[5],
            "operador": vals[6],
            "pdf": vals[7] or ""
        }

    def buscar_telefone_contribuinte(self):
        if not self.codigo_contribuinte:
            return None
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT telefone1 FROM contribuintes WHERE codigo = ?", (self.codigo_contribuinte,))
        dado = cur.fetchone()
        con.close()
        return dado[0] if dado and dado[0] else None

    # ================= AÇÕES =================
    def incluir(self):
        if not self.codigo_contribuinte:
            messagebox.showwarning("Atenção", "Abra os recibos a partir de um contribuinte.")
            return

        tela_cadastro_recibo(
            self.root,
            self.codigo_contribuinte,
            self.nome_contribuinte,
            self.carregar_dados_banco
        )

    def alterar(self):
        id_recibo = self.recibo_selecionado()
        if id_recibo:
            messagebox.showinfo("Alterar", f"Alterar recibo {id_recibo}")

    def excluir(self):
        id_recibo = self.recibo_selecionado()
        if not id_recibo:
            return
        if not messagebox.askyesno("Confirmar", "Deseja excluir este recibo?"):
            return
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM recibos WHERE id = ?", (id_recibo,))
        con.commit()
        con.close()
        self.carregar_dados_banco()
        messagebox.showinfo("OK", "Recibo excluído")

    # ================= NOVO: AJUSTE LAYOUT =================
    def ajuste_layout(self):
        visualizar_recibo(self.root)

    # ================= NOVO: EMITIR PDF =================
    def emitir_pdf(self):
        if not self.codigo_contribuinte:
            messagebox.showwarning("Atenção", "Abra os recibos a partir de um contribuinte.")
            return

        dados = self.dados_recibo_selecionado()
        if not dados:
            return

        # se tipo não existir, pede
        tipo = (dados["tipo"] or "").strip().upper()
        if not tipo:
            tipo = simpledialog.askstring(
                "Tipo de Recibo",
                "Digite o tipo (DOACAO / CONTRIBUICAO / MENSALIDADE / OUTRO):"
            )
            if not tipo:
                return
            tipo = tipo.strip().upper()

            # salva tipo no recibo
            con = conectar()
            cur = con.cursor()
            cur.execute("UPDATE recibos SET tipo = ? WHERE id = ?", (tipo, dados["id"]))
            con.commit()
            con.close()

        # dados para substituir no layout
        # Você deve escrever no layout:
        # "Recebemos de: {NOME}"
        # "Valor: R$ {VALOR}"
        # "Data: {DATA}"
        # "Referente: {REFERENTE}"
        dados_pdf = {
            "NOME": dados["nome"],
            "VALOR": str(dados["valor"]),
            "DATA": dados["vencimento"] or "",
            "REFERENTE": tipo
        }

        imprimir_recibo_pdf(
            tipo=tipo,
            dados=dados_pdf,
            operador=dados["operador"] or "SISTEMA",
            salvar_historico=True,
            contribuinte_id=self.codigo_contribuinte
        )

        # salva caminho do pdf no recibo (mesmo nome que o imprimir_recibo_pdf gera)
        nome_cliente = str(dados_pdf["NOME"]).strip().replace(" ", "_").lower()
        nome_pdf = f"recibo_{tipo.lower()}_{nome_cliente}.pdf"

        con = conectar()
        cur = con.cursor()
        cur.execute("UPDATE recibos SET pdf = ? WHERE id = ?", (nome_pdf, dados["id"]))
        con.commit()
        con.close()

        self.carregar_dados_banco()

    # ================= WHATSAPP PDF =================
    def whatsapp_pdf(self):
        telefone = self.buscar_telefone_contribuinte()
        if not telefone:
            messagebox.showwarning("Atenção", "Contribuinte sem telefone cadastrado")
            return

        dados = self.dados_recibo_selecionado()
        if not dados:
            return

        caminho_pdf = dados["pdf"]

        if not caminho_pdf:
            messagebox.showwarning("PDF", "Este recibo ainda não tem PDF. Clique em 'Emitir PDF'.")
            return

        # se você quiser salvar tudo em uma pasta fixa:
        # caminho_pdf = os.path.join("C:/recibos", caminho_pdf)

        if not os.path.exists(caminho_pdf):
            messagebox.showwarning("PDF", f"Arquivo PDF não encontrado:\n{caminho_pdf}")
            return

        tel = "".join([c for c in telefone if c.isdigit()])
        if not tel.startswith("55"):
            tel = "55" + tel

        url = f"https://web.whatsapp.com/send?phone={tel}"
        webbrowser.open(url)

        messagebox.showinfo("WhatsApp", "WhatsApp Web será aberto. Aguarde 10 segundos para carregar...")

        time.sleep(10)

        pyautogui.hotkey('ctrl', 'o')
        time.sleep(2)

        pyautogui.write(caminho_pdf)
        time.sleep(1)

        pyautogui.press('enter')
        time.sleep(2)

        pyautogui.press('enter')
        messagebox.showinfo("WhatsApp", "Recibo enviado via WhatsApp!")

    def pesquisar(self):
        termo = self.pesquisa.get().strip()
        self.carregar_dados_banco(termo=termo)

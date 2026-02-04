import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
import webbrowser
import urllib.parse
import os
import pyautogui
import time
from cadastro_recibo import tela_cadastro_recibo

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

        self.colunas = ["ID", "Contribuinte", "Valor", "Vencimento", "Nosso Número", "Operador"]
        self.tree = ttk.Treeview(frame, columns=self.colunas, show="headings")

        larguras = [70, 280, 100, 120, 140, 140]
        for col, w in zip(self.colunas, larguras):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=tk.CENTER)
        self.tree.column("Contribuinte", anchor="w")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ================= BOTÕES =================
    def criar_botoes(self):
        frame = tk.Frame(self.root, bg="#E0E0E8")
        frame.pack(fill=tk.X)

        def botao(txt, cmd, cor="#2E3A59"):
            return tk.Button(
                frame, text=txt, width=13, command=cmd,
                bg=cor, fg="white", relief="flat",
                font=("Segoe UI", 9, "bold"),
                activebackground="#3F51B5",
                cursor="hand2"
            )

        botao("Incluir", self.incluir).pack(side=tk.LEFT, padx=5, pady=6)
        botao("Alterar", self.alterar).pack(side=tk.LEFT, padx=5)
        botao("Excluir", self.excluir, "#B71C1C").pack(side=tk.LEFT, padx=5)
        botao("WhatsApp PDF", self.whatsapp_pdf, "#1B5E20").pack(side=tk.LEFT, padx=5)

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
                       r.valor,
                       r.vencimento,
                       r.nosso_num,
                       r.operador
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
                       r.valor,
                       r.vencimento,
                       r.nosso_num,
                       r.operador
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

    # ================= WHATSAPP PDF =================
    def whatsapp_pdf(self):
        telefone = self.buscar_telefone_contribuinte()
        if not telefone:
            messagebox.showwarning("Atenção", "Contribuinte sem telefone cadastrado")
            return

        id_recibo = self.recibo_selecionado()
        if not id_recibo:
            return

        # Caminho do PDF (exemplo, ajuste conforme seu diretório)
        caminho_pdf = f"C:/recibos/recibo_{id_recibo}.pdf"
        if not os.path.exists(caminho_pdf):
            messagebox.showwarning("PDF", "Arquivo PDF do recibo não encontrado.")
            return

        # Abre WhatsApp Web
        tel = "".join([c for c in telefone if c.isdigit()])
        if not tel.startswith("55"):
            tel = "55" + tel
        url = f"https://web.whatsapp.com/send?phone={tel}"
        webbrowser.open(url)

        messagebox.showinfo("WhatsApp", "WhatsApp Web será aberto. Aguarde 10 segundos para carregar...")

        # Aguarda o WhatsApp Web carregar
        time.sleep(10)

        # Simula CTRL+V para anexar PDF via pyautogui
        pyautogui.hotkey('ctrl', 'o')  # abrir anexar arquivo
        time.sleep(2)
        pyautogui.write(caminho_pdf)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')  # envia o arquivo
        messagebox.showinfo("WhatsApp", "Recibo enviado via WhatsApp!")

    def pesquisar(self):
        termo = self.pesquisa.get().strip()
        self.carregar_dados_banco(termo=termo)

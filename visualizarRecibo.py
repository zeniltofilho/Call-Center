import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import os
from datetime import datetime

from database import conectar

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# ==================================================
# AJUSTE: A4 MAIS NO TOPO
# ==================================================
MARGEM_ESQUERDA = 50
MARGEM_TOPO = 35


# ==================================================
# ITEM EDITÁVEL DO RECIBO
# ==================================================
class ItemRecibo(tk.Label):

    def __init__(self, master, nome, texto, x, y, fonte):
        super().__init__(
            master,
            text=texto,
            bg="white",
            font=fonte,
            cursor="fleur"
        )

        self.nome = nome
        self.place(x=x, y=y)

        self.bind("<Button-1>", self.iniciar_arraste)
        self.bind("<B1-Motion>", self.arrastar)
        self.bind("<Double-Button-1>", self.editar)
        self.bind("<Button-3>", self.menu_contexto)

    def iniciar_arraste(self, event):
        self._x = event.x
        self._y = event.y
        self.config(relief="solid", bd=1)

    def arrastar(self, event):
        x = self.winfo_x() + event.x - self._x
        y = self.winfo_y() + event.y - self._y
        self.place(x=x, y=y)

    def editar(self, event=None):
        novo = simpledialog.askstring(
            "Editar campo",
            f"Editar texto de '{self.nome}':",
            initialvalue=self.cget("text")
        )
        if novo is not None:
            self.config(text=novo)

    def menu_contexto(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Editar texto", command=self.editar)
        menu.add_command(label="Excluir campo", command=self.excluir)
        menu.tk_popup(event.x_root, event.y_root)

    def excluir(self):
        if messagebox.askyesno("Excluir", f"Excluir '{self.nome}'?"):
            try:
                self.master.editor.itens.pop(self.nome, None)
            except:
                pass
            self.destroy()


# ==================================================
# EDITOR DO RECIBO (SALVA POR TIPO)
# ==================================================
class EditorRecibo:

    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Recibo - Layout por Tipo")
        self.root.geometry("1100x740")
        self.root.configure(bg="#DDD")

        self.itens = {}

        self.tipo_atual = "DOACAO"

        self.criar_barra_ferramentas()
        self.criar_papel()

        self.combo_tipo.set(self.tipo_atual)
        self.carregar_layout_tipo()

    # -------------------------
    def criar_barra_ferramentas(self):
        barra = tk.Frame(self.root, bg="#2E3A59")
        barra.pack(fill=tk.X)

        frame_btn = tk.Frame(barra, bg="#2E3A59")
        frame_btn.pack(side=tk.LEFT, padx=6)

        def btn(txt, cmd):
            tk.Button(
                frame_btn, text=txt, command=cmd,
                bg="#3949AB", fg="white",
                relief="flat", padx=10
            ).pack(side=tk.LEFT, padx=4, pady=6)

        btn("➕ Incluir Campo", self.incluir_campo)
        btn("💾 Salvar Layout", self.salvar_layout_banco)
        btn("📂 Carregar Layout", self.carregar_layout_tipo)
        btn("🖨️ Testar PDF", self.gerar_pdf_teste)
        btn("🗑️ Resetar Tipo", self.resetar_layout_tipo)

        frame_tipo = tk.Frame(barra, bg="#2E3A59")
        frame_tipo.pack(side=tk.RIGHT, padx=10)

        tk.Label(
            frame_tipo,
            text="Tipo de Recibo:",
            bg="#2E3A59",
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.combo_tipo = ttk.Combobox(
            frame_tipo,
            values=["DOACAO", "CONTRIBUICAO", "MENSALIDADE", "OUTRO"],
            state="readonly",
            width=18
        )
        self.combo_tipo.pack(side=tk.LEFT)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.trocar_tipo)

    # -------------------------
    def criar_papel(self):
        self.paper = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="solid"
        )
        self.paper.place(relx=0.5, rely=0.56, anchor="center", width=850, height=580)
        self.paper.editor = self

    # -------------------------
    def trocar_tipo(self, event=None):
        self.tipo_atual = self.combo_tipo.get().strip().upper()
        self.carregar_layout_tipo()

    # -------------------------
    def adicionar_item(self, nome, texto, x, y, fonte):
        item = ItemRecibo(self.paper, nome, texto, x, y, fonte)
        self.itens[nome] = item

    # -------------------------
    def limpar_papel(self):
        for item in list(self.itens.values()):
            try:
                item.destroy()
            except:
                pass
        self.itens.clear()

    # -------------------------
    def carregar_modelo_inicial(self):
        self.limpar_papel()

        self.adicionar_item(
            "titulo",
            f"RECIBO ({self.tipo_atual}) - VALOR R$:",
            40, 80, ("Segoe UI", 11, "bold")
        )

        self.adicionar_item(
            "recebemos",
            "Recebemos de:",
            40, 120, ("Segoe UI", 9, "normal")
        )

        self.adicionar_item(
            "quantia",
            "A Quantia de:",
            40, 150, ("Segoe UI", 9, "normal")
        )

        self.adicionar_item(
            "referente",
            "Referente a:",
            40, 180, ("Segoe UI", 9, "normal")
        )

        self.adicionar_item(
            "data",
            "Data:",
            40, 210, ("Segoe UI", 9, "normal")
        )

        self.adicionar_item(
            "assinatura",
            "Responsável pelo Recebimento",
            420, 260, ("Segoe UI", 9, "normal")
        )

        self.adicionar_item(
            "linha",
            "______________________________________________________________",
            40, 240, ("Segoe UI", 9, "normal")
        )

    # -------------------------
    def incluir_campo(self):
        nome = simpledialog.askstring("Novo campo", "Nome interno do campo:")
        texto = simpledialog.askstring("Novo campo", "Texto inicial:")

        if not nome or not texto:
            return

        nome = nome.strip()

        if nome in self.itens:
            messagebox.showerror("Erro", "Já existe um campo com esse nome!")
            return

        self.adicionar_item(nome, texto, 50, 50, ("Segoe UI", 9, "normal"))

    # ==================================================
    # BANCO
    # ==================================================
    def salvar_layout_banco(self):
        con = conectar()
        cur = con.cursor()

        cur.execute("DELETE FROM recibo_layout WHERE tipo = ?", (self.tipo_atual,))

        for nome, item in self.itens.items():
            x = item.winfo_x()
            y = item.winfo_y()
            texto = item.cget("text")

            fonte = item.cget("font")
            if isinstance(fonte, str):
                fonte_nome = "Segoe UI"
                fonte_tamanho = 9
                fonte_estilo = "normal"
            else:
                fonte_nome = fonte[0] if len(fonte) > 0 else "Segoe UI"
                fonte_tamanho = fonte[1] if len(fonte) > 1 else 9
                fonte_estilo = fonte[2] if len(fonte) > 2 else "normal"

            cur.execute("""
                INSERT INTO recibo_layout (tipo, nome, texto, x, y, fonte_nome, fonte_tamanho, fonte_estilo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.tipo_atual,
                nome,
                texto,
                x,
                y,
                fonte_nome,
                fonte_tamanho,
                fonte_estilo
            ))

        con.commit()
        con.close()

        messagebox.showinfo("Salvo", f"Layout do tipo '{self.tipo_atual}' salvo com sucesso!")

    def carregar_layout_tipo(self):
        con = conectar()
        cur = con.cursor()

        cur.execute("""
            SELECT nome, texto, x, y, fonte_nome, fonte_tamanho, fonte_estilo
            FROM recibo_layout
            WHERE tipo = ?
            ORDER BY id ASC
        """, (self.tipo_atual,))

        dados = cur.fetchall()
        con.close()

        if not dados:
            self.carregar_modelo_inicial()
            return

        self.limpar_papel()

        for nome, texto, x, y, fonte_nome, fonte_tamanho, fonte_estilo in dados:
            fonte = (fonte_nome, fonte_tamanho, fonte_estilo)
            self.adicionar_item(nome, texto, x, y, fonte)

    def resetar_layout_tipo(self):
        if not messagebox.askyesno(
            "Resetar Tipo",
            f"Deseja apagar o layout salvo do tipo '{self.tipo_atual}'?"
        ):
            return

        con = conectar()
        cur = con.cursor()

        cur.execute("DELETE FROM recibo_layout WHERE tipo = ?", (self.tipo_atual,))

        con.commit()
        con.close()

        self.carregar_modelo_inicial()
        messagebox.showinfo("Resetado", f"Layout do tipo '{self.tipo_atual}' apagado com sucesso!")

    # ==================================================
    # PDF DE TESTE
    # ==================================================
    def gerar_pdf_teste(self):
        dados = {
            "NOME": "CLIENTE TESTE",
            "VALOR": "150,00",
            "DATA": datetime.now().strftime("%d/%m/%Y"),
            "REFERENTE": f"{self.tipo_atual} (TESTE)"
        }

        imprimir_recibo_pdf(
            tipo=self.tipo_atual,
            dados=dados,
            operador="TESTE",
            salvar_historico=False
        )


# ==================================================
# IMPRESSÃO REAL (PDF) - USANDO LAYOUT DO BANCO
# ==================================================
def imprimir_recibo_pdf(tipo, dados, operador="SISTEMA", salvar_historico=True, contribuinte_id=None):
    """
    dados exemplo:
    {
        "NOME": "JOAO",
        "VALOR": "120,00",
        "DATA": "05/02/2026",
        "REFERENTE": "DOAÇÃO"
    }
    """

    tipo = tipo.strip().upper()

    # --- carrega layout ---
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT nome, texto, x, y, fonte_nome, fonte_tamanho, fonte_estilo
        FROM recibo_layout
        WHERE tipo = ?
        ORDER BY id ASC
    """, (tipo,))

    layout = cur.fetchall()

    # se não existir layout, não imprime
    if not layout:
        con.close()
        messagebox.showerror("Erro", f"Não existe layout salvo para o tipo: {tipo}")
        return

    # nome arquivo
    nome_cliente = str(dados.get("NOME", "cliente")).strip().replace(" ", "_").lower()
    nome_arquivo = f"recibo_{tipo.lower()}_{nome_cliente}.pdf"

    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    for nome, texto, x, y, fonte_nome, fonte_tamanho, fonte_estilo in layout:
        # texto do layout (padrão)
        final_text = texto or ""

        # substituições automáticas
        # você pode colocar no texto do campo:
        # "Recebemos de: {NOME}"
        # "Valor: R$ {VALOR}"
        for chave, valor in dados.items():
            final_text = final_text.replace("{" + chave + "}", str(valor))

        # fontes
        fonte_pdf = "Helvetica-Bold" if "bold" in str(fonte_estilo).lower() else "Helvetica"
        c.setFont(fonte_pdf, int(fonte_tamanho or 9))

        pdf_x = MARGEM_ESQUERDA + int(x or 0)
        pdf_y = altura - (MARGEM_TOPO + int(y or 0))

        c.drawString(pdf_x, pdf_y, final_text)

    c.showPage()
    c.save()

    # --- salva histórico ---
    if salvar_historico:
        cur.execute("""
            INSERT INTO recibos_emitidos (tipo, contribuinte_id, nome, valor, data, referente, operador, arquivo_pdf)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tipo,
            contribuinte_id,
            str(dados.get("NOME", "")),
            float(str(dados.get("VALOR", "0")).replace(".", "").replace(",", ".")) if dados.get("VALOR") else 0,
            str(dados.get("DATA", "")),
            str(dados.get("REFERENTE", "")),
            operador,
            nome_arquivo
        ))
        con.commit()

    con.close()

    try:
        os.startfile(nome_arquivo)
    except:
        pass

    messagebox.showinfo("PDF Gerado", f"PDF criado com sucesso:\n{nome_arquivo}")


# ==================================================
# FUNÇÃO PADRÃO (MAIN)
# ==================================================
def visualizar_recibo(root):
    win = tk.Toplevel(root)
    EditorRecibo(win)


# ==================================================
# TESTE
# ==================================================
if __name__ == "__main__":
    root = tk.Tk()
    visualizar_recibo(root)
    root.mainloop()

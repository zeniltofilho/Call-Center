import tkinter as tk
from tkinter import simpledialog, messagebox


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

    # -------- mover --------
    def iniciar_arraste(self, event):
        self._x = event.x
        self._y = event.y
        self.config(relief="solid", bd=1)

    def arrastar(self, event):
        x = self.winfo_x() + event.x - self._x
        y = self.winfo_y() + event.y - self._y
        self.place(x=x, y=y)

    # -------- editar --------
    def editar(self, event=None):
        novo = simpledialog.askstring(
            "Editar campo",
            f"Editar texto de '{self.nome}':",
            initialvalue=self.cget("text")
        )
        if novo is not None:
            self.config(text=novo)

    # -------- menu botão direito --------
    def menu_contexto(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Editar texto", command=self.editar)
        menu.add_command(label="Excluir campo", command=self.excluir)
        menu.tk_popup(event.x_root, event.y_root)

    def excluir(self):
        if messagebox.askyesno("Excluir", f"Excluir '{self.nome}'?"):
            self.destroy()


# ==================================================
# EDITOR DO RECIBO
# ==================================================
class EditorRecibo:

    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Recibo - LFA")
        self.root.geometry("1000x700")
        self.root.configure(bg="#DDD")

        self.itens = {}

        self.criar_barra_ferramentas()
        self.criar_papel()
        self.carregar_modelo_inicial()

    # -------------------------
    def criar_barra_ferramentas(self):
        barra = tk.Frame(self.root, bg="#2E3A59")
        barra.pack(fill=tk.X)

        def btn(txt, cmd):
            tk.Button(
                barra, text=txt, command=cmd,
                bg="#3949AB", fg="white",
                relief="flat", padx=10
            ).pack(side=tk.LEFT, padx=4, pady=4)

        btn("➕ Incluir Campo", self.incluir_campo)
        btn("🔄 Atualizar", self.atualizar)
        btn("💾 Mostrar Layout", self.mostrar_layout)

    # -------------------------
    def criar_papel(self):
        self.paper = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="solid"
        )
        self.paper.place(relx=0.5, rely=0.55, anchor="center", width=850, height=580)

    # -------------------------
    def adicionar_item(self, nome, texto, x, y, fonte):
        item = ItemRecibo(self.paper, nome, texto, x, y, fonte)
        self.itens[nome] = item

    # -------------------------
    def carregar_modelo_inicial(self):
        self.adicionar_item(
            "titulo",
            "RECIBO DE DOAÇÃO - SÉRIE \"A\" - VALOR R$:",
            40, 80, ("Segoe UI", 11, "bold")
        )

        self.adicionar_item(
            "recebemos",
            "Recebemos de:",
            40, 120, ("Segoe UI", 9)
        )

        self.adicionar_item(
            "quantia",
            "A Quantia de:",
            40, 150, ("Segoe UI", 9)
        )

        self.adicionar_item(
            "assinatura",
            "Responsável pelo Receb. Telemarketing",
            420, 260, ("Segoe UI", 9)
        )

    # -------------------------
    def incluir_campo(self):
        nome = simpledialog.askstring("Novo campo", "Nome interno do campo:")
        texto = simpledialog.askstring("Novo campo", "Texto inicial:")

        if not nome or not texto:
            return

        self.adicionar_item(nome, texto, 50, 50, ("Segoe UI", 9))

    # -------------------------
    def atualizar(self):
        self.paper.update()
        messagebox.showinfo("Atualizado", "Layout atualizado com sucesso.")

    # -------------------------
    def mostrar_layout(self):
        print("\nLAYOUT ATUAL:")
        for nome, item in self.itens.items():
            print(
                f'"{nome}": {{'
                f'"x": {item.winfo_x()}, '
                f'"y": {item.winfo_y()}, '
                f'"texto": "{item.cget("text")}"'
                f'}}'
            )


# ==================================================
# FUNÇÃO DE ABERTURA PADRÃO
# ==================================================
def visualizar_recibo(root):
    win = tk.Toplevel(root)
    EditorRecibo(win)


# ==================================================
# TESTE ISOLADO
# ==================================================
if __name__ == "__main__":
    root = tk.Tk()
    visualizar_recibo(root)
    root.mainloop()

import tkinter as tk
import sqlite3
from datetime import date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import DB_NAME

class Dashboard:

    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.frame_grafico = tk.LabelFrame(self.frame, text="Produção do Dia x Meta")
        self.frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.atualizar()

    def atualizar(self):
        for w in self.frame_grafico.winfo_children():
            w.destroy()

        hoje = date.today().isoformat()

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("SELECT IFNULL(SUM(quantidade),0), IFNULL(SUM(valor),0) FROM producao WHERE data=?", (hoje,))
        prod_qtd, prod_valor = c.fetchone()

        c.execute("SELECT meta_qtd, meta_valor FROM metas WHERE data=?", (hoje,))
        meta = c.fetchone()

        meta_qtd = meta[0] if meta else 0
        meta_valor = meta[1] if meta else 0
        conn.close()

        fig = Figure(figsize=(6,4), dpi=100)
        ax = fig.add_subplot(111)

        labels = ['Quantidade', 'Valor']
        metas = [meta_qtd, meta_valor]
        prod = [prod_qtd, prod_valor]

        x = range(2)
        ax.bar(x, metas, width=0.4, label='Meta')
        ax.bar([i+0.4 for i in x], prod, width=0.4, label='Produção')

        ax.set_xticks([i+0.2 for i in x])
        ax.set_xticklabels(labels)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

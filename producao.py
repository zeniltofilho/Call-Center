import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
from database import DB_NAME

def tela_producao(root, atualizar_dashboard):

    win = tk.Toplevel(root)
    win.title("Produção por Operador")
    win.geometry("500x400")

    tk.Label(win, text="Operador").pack()
    operador_cb = ttk.Combobox(win)
    operador_cb.pack(fill=tk.X, padx=10)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, nome FROM operadores")
    operadores = c.fetchall()
    conn.close()

    operador_cb['values'] = [f"{o[0]} - {o[1]}" for o in operadores]

    tk.Label(win, text="Quantidade:").pack()
    qtd = tk.Entry(win)
    qtd.pack(fill=tk.X, padx=10)

    tk.Label(win, text="Valor:").pack()
    valor = tk.Entry(win)
    valor.pack(fill=tk.X, padx=10)

    def salvar():
        if not operador_cb.get():
            return

        op_id = int(operador_cb.get().split(' - ')[0])

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO producao VALUES (NULL,?,?,?,?)",
                  (op_id, date.today().isoformat(), int(qtd.get()), float(valor.get())))
        conn.commit()
        conn.close()

        messagebox.showinfo("OK", "Produção registrada")
        win.destroy()
        atualizar_dashboard()

    tk.Button(win, text="Registrar", command=salvar).pack(pady=10)

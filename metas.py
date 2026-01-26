import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date
from database import DB_NAME

def tela_metas(root, atualizar_dashboard):

    win = tk.Toplevel(root)
    win.title("Metas do Dia")
    win.geometry("400x300")

    tk.Label(win, text="Meta Quantidade:").pack()
    meta_qtd = tk.Entry(win)
    meta_qtd.pack(fill=tk.X, padx=10)

    tk.Label(win, text="Meta Valor:").pack()
    meta_valor = tk.Entry(win)
    meta_valor.pack(fill=tk.X, padx=10)

    def salvar():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
        INSERT OR REPLACE INTO metas(data, meta_qtd, meta_valor)
        VALUES (?,?,?)
        """, (date.today().isoformat(), int(meta_qtd.get()), float(meta_valor.get())))

        conn.commit()
        conn.close()

        messagebox.showinfo("OK", "Meta salva")
        win.destroy()
        atualizar_dashboard()

    tk.Button(win, text="Salvar Meta", command=salvar).pack(pady=10)

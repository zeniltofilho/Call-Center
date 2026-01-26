import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import DB_NAME

def tela_operadores(root):

    win = tk.Toplevel(root)
    win.title("Operadores")
    win.geometry("400x400")

    tk.Label(win, text="Nome:").pack()
    nome = tk.Entry(win)
    nome.pack(fill=tk.X, padx=10)

    def salvar():
        if nome.get():
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO operadores(nome) VALUES (?)", (nome.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("OK", "Operador cadastrado")
            win.destroy()

    tk.Button(win, text="Salvar", command=salvar).pack(pady=10)

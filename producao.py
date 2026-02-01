import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
from database import DB_NAME


def tela_producao(root, atualizar_dashboard):

    win = tk.Toplevel(root)
    win.title("Produção por Operador")
    win.geometry("520x420")
    win.resizable(False, False)
    win.configure(bg="#f2f2f2")

    # ================= FRAME =================
    frame = tk.LabelFrame(win, text="Registro de Produção", bg="#f2f2f2")
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    tk.Label(frame, text="Operador", bg="#f2f2f2").pack(anchor="w")
    operador_cb = ttk.Combobox(frame)
    operador_cb.pack(fill=tk.X, pady=3)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, nome FROM operadores WHERE sts='ATIVO'")
    operadores = c.fetchall()
    conn.close()

    operador_cb['values'] = [f"{o[0]} - {o[1]}" for o in operadores]

    tk.Label(frame, text="Quantidade", bg="#f2f2f2").pack(anchor="w", pady=(10, 0))
    qtd = tk.Entry(frame)
    qtd.pack(fill=tk.X, pady=3)

    tk.Label(frame, text="Valor Total (R$)", bg="#f2f2f2").pack(anchor="w", pady=(10, 0))
    valor = tk.Entry(frame)
    valor.pack(fill=tk.X, pady=3)

    # ================= TOTAL DO DIA =================
    lbl_total = tk.Label(frame, text="", bg="#f2f2f2",
                         font=("Segoe UI", 9, "bold"), fg="blue")
    lbl_total.pack(pady=10)

    def atualizar_total_dia():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT SUM(valor) FROM producao WHERE data = ?", (date.today().isoformat(),))
        total = c.fetchone()[0]
        conn.close()
        lbl_total.config(text=f"Total produzido hoje: R$ {total:.2f}" if total else "Sem produção hoje")

    atualizar_total_dia()

    # ================= SALVAR =================
    def salvar():
        if not operador_cb.get():
            messagebox.showwarning("Atenção", "Selecione o operador.")
            return

        if not qtd.get().isdigit():
            messagebox.showwarning("Atenção", "Quantidade inválida.")
            return

        try:
            valor_float = float(valor.get().replace(",", "."))
        except:
            messagebox.showwarning("Atenção", "Valor inválido.")
            return

        op_id = int(operador_cb.get().split(' - ')[0])

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            INSERT INTO producao (operador_id, data, quantidade, valor)
            VALUES (?, ?, ?, ?)
        """, (op_id, date.today().isoformat(), int(qtd.get()), valor_float))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Produção registrada!")
        atualizar_total_dia()
        atualizar_dashboard()

        qtd.delete(0, tk.END)
        valor.delete(0, tk.END)

    # ================= BOTÃO =================
    tk.Button(win,
              text="Registrar Produção",
              bg="#4CAF50",
              fg="white",
              font=("Segoe UI", 10, "bold"),
              command=salvar).pack(pady=10)

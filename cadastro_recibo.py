import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar


def tela_cadastro_recibo(root, id_contribuinte, nome_contribuinte, callback_atualizar=None):
    janela = tk.Toplevel(root)
    janela.title("Cadastro de Recibo")
    janela.geometry("520x320")
    janela.resizable(False, False)
    janela.configure(bg="#ECECF1")

    # Centralizar
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (520 // 2)
    y = (janela.winfo_screenheight() // 2) - (320 // 2)
    janela.geometry(f"520x320+{x}+{y}")

    fonte = ("Segoe UI", 10)

    # ---------------- TITULO ----------------
    tk.Label(
        janela,
        text=f"Contribuinte: {nome_contribuinte}",
        bg="#ECECF1",
        fg="#1A237E",
        font=("Segoe UI", 11, "bold"),
        anchor="w"
    ).pack(fill=tk.X, padx=10, pady=(10, 5))

    # ---------------- FORM ----------------
    frame = ttk.LabelFrame(janela, text="Dados do Recibo")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame, text="Valor (R$):").place(x=20, y=20)
    ent_valor = tk.Entry(frame, width=20, font=fonte)
    ent_valor.place(x=120, y=20)

    ttk.Label(frame, text="Vencimento:").place(x=20, y=60)
    ent_venc = tk.Entry(frame, width=20, font=fonte)
    ent_venc.place(x=120, y=60)

    ttk.Label(frame, text="Nosso Número:").place(x=20, y=100)
    ent_nosso = tk.Entry(frame, width=25, font=fonte)
    ent_nosso.place(x=120, y=100)

    ttk.Label(frame, text="Operador:").place(x=20, y=140)
    ent_operador = tk.Entry(frame, width=25, font=fonte)
    ent_operador.place(x=120, y=140)

    # ---------------- BOTÕES ----------------
    frame_btn = tk.Frame(janela, bg="#ECECF1")
    frame_btn.pack(fill=tk.X, padx=10, pady=5)

    def salvar():
        valor = ent_valor.get().strip().replace(",", ".")
        venc = ent_venc.get().strip()
        nosso = ent_nosso.get().strip()
        operador = ent_operador.get().strip()

        if not valor:
            messagebox.showwarning("Atenção", "Informe o valor.")
            return

        try:
            valor_float = float(valor)
        except:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        try:
            con = conectar()
            cur = con.cursor()

            cur.execute("""
                INSERT INTO recibos (contrib, valor, vencimento, nosso_num, operador)
                VALUES (?, ?, ?, ?, ?)
            """, (id_contribuinte, valor_float, venc, nosso, operador))

            con.commit()
            con.close()

            messagebox.showinfo("Sucesso", "Recibo cadastrado com sucesso!")

            if callback_atualizar:
                callback_atualizar()

            janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar recibo:\n{e}")

    tk.Button(
        frame_btn,
        text="💾 Salvar",
        command=salvar,
        bg="#2E7D32",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        width=14,
        cursor="hand2"
    ).pack(side="right", padx=5)

    tk.Button(
        frame_btn,
        text="Cancelar",
        command=janela.destroy,
        bg="#B71C1C",
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        width=14,
        cursor="hand2"
    ).pack(side="right", padx=5)

import os
import zipfile
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox


PASTA_SISTEMA = os.getcwd()
EXTENSAO_BANCO = ".db"


# ==================================================
# BACKUP (ZIP)
# ==================================================
def fazer_backup():
    arquivos_db = [
        f for f in os.listdir(PASTA_SISTEMA)
        if f.endswith(EXTENSAO_BANCO)
    ]

    if not arquivos_db:
        messagebox.showwarning("Backup", "Nenhum banco encontrado.")
        return

    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"backup_callcenter_{data}.zip"

    destino = filedialog.asksaveasfilename(
        defaultextension=".zip",
        initialfile=nome_backup,
        filetypes=[("Arquivo ZIP", "*.zip")]
    )

    if not destino:
        return

    try:
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zipf:
            for arquivo in arquivos_db:
                zipf.write(
                    os.path.join(PASTA_SISTEMA, arquivo),
                    arcname=arquivo
                )

        messagebox.showinfo("Backup", "Backup realizado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar backup:\n{e}")


# ==================================================
# IMPORTAR BACKUP (QUALQUER ARQUIVO)
# ==================================================
def importar_backup():
    arquivo = filedialog.askopenfilename(
        title="Selecionar arquivo de backup",
        filetypes=[("Todos os arquivos", "*.*")]
    )

    if not arquivo:
        return

    if not messagebox.askyesno(
        "Importar Backup",
        "⚠ ATENÇÃO!\n\n"
        "Os dados atuais serão SUBSTITUÍDOS.\n"
        "Um backup automático será criado.\n\n"
        "Deseja continuar?"
    ):
        return

    try:
        # 🔒 BACKUP AUTOMÁTICO DE SEGURANÇA
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        pasta_seg = os.path.join(PASTA_SISTEMA, f"backup_auto_{data}")
        os.makedirs(pasta_seg, exist_ok=True)

        for f in os.listdir(PASTA_SISTEMA):
            if f.endswith(EXTENSAO_BANCO):
                shutil.copy(
                    os.path.join(PASTA_SISTEMA, f),
                    os.path.join(pasta_seg, f)
                )

        # ===============================
        # SE FOR ZIP → EXTRAI
        # ===============================
        if zipfile.is_zipfile(arquivo):
            with zipfile.ZipFile(arquivo, "r") as zipf:
                zipf.extractall(PASTA_SISTEMA)

            messagebox.showinfo(
                "Backup",
                "Backup ZIP restaurado com sucesso!\n\n"
                "Reinicie o sistema."
            )
            return

        # ===============================
        # SE FOR QUALQUER OUTRO ARQUIVO
        # ===============================
        nome = os.path.basename(arquivo)

        if not nome.endswith(".db"):
            resp = messagebox.askyesno(
                "Arquivo não identificado",
                "O arquivo selecionado não é .db nem .zip.\n\n"
                "Deseja copiá-lo mesmo assim para o sistema?"
            )
            if not resp:
                return

        destino = os.path.join(PASTA_SISTEMA, nome)
        shutil.copy(arquivo, destino)

        messagebox.showinfo(
            "Backup",
            "Arquivo importado com sucesso!\n\n"
            "Se for um banco de dados, reinicie o sistema."
        )

    except Exception as e:
        messagebox.showerror(
            "Erro",
            f"Erro ao importar backup:\n{e}"
        )

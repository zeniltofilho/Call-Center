import sqlite3
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook
from database import DB_NAME

def relatorio_pdf():

    path = filedialog.asksaveasfilename(defaultextension=".pdf")
    if not path:
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT o.nome, p.data, p.quantidade, p.valor
    FROM producao p
    JOIN operadores o ON o.id = p.operador_id
    ORDER BY p.data
    """)

    dados = c.fetchall()
    conn.close()

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=A4)
    elements = [Paragraph("Relatório de Produção", styles['Title']), Spacer(1,12)]

    tabela = [['Operador','Data','Qtd','Valor']]
    for d in dados:
        tabela.append(list(d))

    elements.append(Table(tabela))
    doc.build(elements)

    messagebox.showinfo("OK", "PDF gerado com sucesso")


def relatorio_excel():

    path = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if not path:
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Produção"

    ws.append(["Operador","Data","Quantidade","Valor"])

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT o.nome, p.data, p.quantidade, p.valor
    FROM producao p
    JOIN operadores o ON o.id = p.operador_id
    ORDER BY p.data
    """)

    for row in c.fetchall():
        ws.append(row)

    conn.close()
    wb.save(path)

    messagebox.showinfo("OK", "Excel gerado com sucesso")

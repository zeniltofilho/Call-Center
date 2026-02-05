from database import conectar

con = conectar()
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS recibo_layout")
con.commit()

con.close()
print("Tabela recibo_layout apagada com sucesso!")

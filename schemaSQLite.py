import sqlite3 as lite

con = lite.connect('data.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE categorias(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

#Criando tabela de receitas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)")

#Criando tabela de gastos
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")
import sqlite3 as lite
import pandas as pd

con = lite.connect('data.db')

#Insertting category
def insert_category(i):
    with con:
        cur = con.cursor()
        sql = "INSERT INTO categorias (nome) VALUES (?)"
        cur.execute(sql, i)

#Insertting revenue
def insert_revenue(i):
    with con:
        cur = con.cursor()
        sql = "INSERT INTO receitas(categoria, adicionado_em, valor) VALUES (?, ?, ?)"
        cur.execute(sql, i)

#Insertting speding
def insert_spending(i):
    with con:
        cur = con.cursor()
        sql = "INSERT INTO gastos(categoria, retirado_em, valor) VALUES (?, ?, ?)"
        cur.execute(sql, i)


#Functions to delete
def delete_revenue(i):
    with con:
        cur = con.cursor()
        sql = "DELETE FROM receitas WHERE id =?"
        cur.execute(sql, i)

        table()


def delete_category(i):
    with con:
        cur = con.cursor()
        sql = "DELETE FROM categorias WHERE id=?"
        cur.execute(sql, i)


def delete_spending(i):
    with con:
        cur = con.cursor()
        sql = "DELETE FROM gastos WHERE id =?"
        cur.execute(sql, i)

        table()


#Functions to view datas

#View categories
def view_category():
    lista = []

    with con:
        cur = con.cursor()
        sql = "SELECT * FROM categorias"
        cur.execute(sql)
        linhas = cur.fetchall()

        for linha in linhas:
            lista.append(linha)

    return lista

def view_revenue():
    lista = []

    with con:
        cur = con.cursor()
        sql = "SELECT * FROM receitas"
        cur.execute(sql)
        linhas = cur.fetchall()

        for linha in linhas:
            lista.append(linha)

    return lista

def view_spending():
    lista = []

    with con:
        cur = con.cursor()
        sql = "SELECT * FROM gastos"
        cur.execute(sql)
        linhas = cur.fetchall()
        print(linhas)

        for linha in linhas:
            lista.append(linha)

    return lista

def table():
    spends = view_spending()
    revenues = view_revenue()

    table_list = []

    for i in spends:
        table_list.append(i)
    for i in revenues:
        table_list.append(i)
    return table_list

def bar_values():

    revenues = view_revenue()
    revenues_list = []
    for i in revenues:
        revenues_list.append(i[3])

#Function Grafic Bar
def bar_values():
    #Total revenue
    revenues = view_revenue()
    revenue_list = []

    for i in revenues:
        revenue_list.append(i[3])

    revenue_total = sum(revenue_list)

    # Total spend
    spends = view_spending()
    spends_list = []

    for i in spends:
        spends_list.append(i[3])

    spends_total = sum(spends_list)

    balance_total = revenue_total - spends_total

    return [revenue_total, spends_total, balance_total]

#Function grafic pie
def pie_values():
    spend = view_spending()
    table_list = []

    for i in spend:
        table_list.append(i)

    dataframe = pd.DataFrame(table_list, columns=['id', 'categoria', 'retirado_em','valor'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()


    list_amounts = dataframe.values.tolist()
    list_categories = []
    list_category = []


    for i in dataframe.index:
        list_categories.append(i)
    for j in list_categories:
        list_category.append(j)

    return([list_category, list_amounts])


#Function Grafic Bar
def function_percentagem():
    #Total revenue
    revenues = view_revenue()
    revenue_list = []

    for i in revenues:
        revenue_list.append(i[3])

    revenue_total = sum(revenue_list)

    # Total spend
    spends = view_spending()
    spends_list = []

    for i in spends:
        spends_list.append(i[3])

    spends_total = sum(spends_list)

    total = ((revenue_total - spends_total)/revenue_total)*100

    return total
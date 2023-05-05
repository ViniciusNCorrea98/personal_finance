from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox

from PIL import Image, ImageTk

from tkinter.ttk import Progressbar

from tkcalendar import Calendar, DateEntry
from datetime import date

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from handleSQLite import pie_values, function_percentagem,insert_category, insert_spending, insert_revenue, view_category, view_revenue, view_spending, table, delete_spending, delete_revenue, bar_values

co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#3fbfb9"   # verde
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # + verde

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

janela = Tk()
janela.title('')
janela.geometry('900x650')
janela.configure(background="#454C61")

janela.resizable(width=FALSE, height=FALSE)

style= ttk.Style(janela)
style.theme_use("clam")

#Creatting frames
frame_header = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frame_header.grid(row=0, column=0)

frame_top = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
frame_top.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frame_bottom = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frame_bottom.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

#Configure frame header

app_img = Image.open('images/logo_finance_personal.png')
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frame_header, image=app_img, text=' Personal Finance', width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0, y=0)

global tree

#Function to insert category
def insert_category_db():
    nome = entry_revenue_value.get()
    list_insert = [nome]

    for i in list_insert:
       if i =='':
           messagebox.showerror('Erro', 'Fill all the blanks')
           return

    insert_category(list_insert)

    messagebox.showinfo('Success', "The dates were insert")

    entry_revenue_value

    categories_function = view_category()
    category = []

    for i in categories_function:
        category.append(i[1])

    combo_category_spend['values'] = (category)

#Function insert revenues
def insert_revenue_db():
    name = 'Revenue'
    date = entry_date_revenue.get()
    amount = entry_revenue.get()
    print(amount, date)

    list_insert = [name, date, amount]

    for i in list_insert:
        if i=='':
            messagebox.showerror('Erro', 'Fill all the blanks!')
            return

    insert_revenue(list_insert)

    messagebox.showinfo('Success', "The dates were insert")

    entry_date_revenue.delete(0, 'end')
    entry_revenue_value.delete(0, 'end')

    show_income()
    percentagem()
    grafic_bar()
    grafic_pie()
    resume()

#Function insert spends
def insert_spends_db():
    name = combo_category_spend.get()
    date = entry_cal_spends.get()
    amount = entry_value_spends.get()


    list_insert = [name, date, amount]

    for i in list_insert:
        if i=='':
            messagebox.showerror('Erro', 'Fill all the blanks!')
            return

    insert_spending(list_insert)

    messagebox.showinfo('Success', "The dates were insert")

    entry_cal_spends.delete(0, 'end')
    entry_value_spends.delete(0, 'end')
    combo_category_spend.delete(0, 'end')

    show_income()
    percentagem()
    grafic_bar()
    grafic_pie()
    resume()

#Function delete spends
def delete_spends_db():
    try:
        treev_dados = tree.focus()
        treev_dic = tree.item(treev_dados)
        treev_list = treev_dic['values']
        valor = treev_list[0]
        nome = treev_list[1]
        print(valor)
        if nome =='Revenue':
            delete_revenue([valor])
            messagebox.showinfo('Success', 'Your dates were delete successfuly')
            percentagem()
            grafic_bar()
            grafic_bar()
            show_income()
            resume()
        else:
            delete_spending([valor])
            messagebox.showinfo('Success', 'Your dates were delete successfuly')
            percentagem()
            grafic_bar()
            grafic_bar()
            show_income()
            resume()
    except IndexError:
        messagebox.showerror('Erro', 'Select a date in the table')




#Percentagem

def percentagem():
    label_nome = Label(frame_top, text='Percentage of Revenue spent', height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    label_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('back.Horizontal.TProgressbar', background='#daed6b')
    style.configure('TProgressbar', thickness=25)

    bar = Progressbar(frame_top, length=180, style='back.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = function_percentagem()
    valor = function_percentagem()
    label_percentagem = Label(frame_top, text="{:,.2f}%".format(valor), anchor=NW, font=("Verdana 12"), bg=co1, fg=co4)
    label_percentagem.place(x=200, y=35)

def grafic_bar():
        list_categories = ['Income', 'Speding', 'Balance']
        list_values = bar_values()


        figure = plt.Figure(figsize=(4, 3.45), dpi=60)
        ax = figure.add_subplot(111)

        ax.bar(list_categories, list_values, color=colors, width=0.9)

        c = 0

        for i in ax.patches:
            ax.text(i.get_x()-.001, i.get_height() +5,
                    str("{:,.0f}".format(list_values[c])), fontsize=17, fontstyle='italic', verticalalignment='bottom', color='dimgrey')
            c+=1

        ax.set_xticklabels(list_categories, fontsize=16)

        ax.patch.set_facecolor('#ffffff')
        ax.spines['bottom'].set_color('#CCCCCC')
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['right'].set_linewidth(0)
        ax.spines['top'].set_linewidth(0)
        ax.spines['left'].set_color('#CCCCCC')
        ax.spines['left'].set_linewidth(1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color='#EEEEEE')
        ax.xaxis.grid(False)

        canva = FigureCanvasTkAgg(figure, frame_top)
        canva.get_tk_widget().place(x=10, y=70)

#Function resume total
def resume():
    valor = bar_values()
    label_linha_TIM = Label(frame_top, text="", width=215, height=1, anchor=NW, font=("Arial 1"), bg='#545454')
    label_linha_TIM.place(x=309, y=52)
    label_sumario = Label(frame_top, text="Total income mounthly    ".upper(), width=90, height=1, anchor=NW, font=("Verdana 12"), bg=co1, fg="#83a9e6")
    label_sumario.place(x=309, y=35)
    label_sumario_value1 = Label(frame_top, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=("Arial 17"), bg=co1, fg="#545454")
    label_sumario_value1.place(x=309, y=70)

    label_linha_TSM = Label(frame_top, text="", width=90, height=1, anchor=NW, font=("Arial 1"), bg='#545454')
    label_linha_TSM.place(x=309, y=132)
    label_sumario_TSM = Label(frame_top, text="Total spends mounthly    ".upper(),  height=1, anchor=NW, font=("Verdana 12"), bg=co1, fg="#83a9e6")
    label_sumario_TSM.place(x=309, y=115)
    label_sumario_value2 = Label(frame_top, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=("Arial 17"), bg=co1,fg="#545454")
    label_sumario_value2.place(x=309, y=150)

    label_linha_TBM = Label(frame_top, text="", width=215, height=1, anchor=NW, font=("Arial 1"), bg='#545454')
    label_linha_TBM.place(x=309, y=207)
    label_sumario_TBM = Label(frame_top, text="Total Balance mounthly    ".upper(),  height=1, anchor=NW,font=("Verdana 12"), bg=co1,fg="#83a9e6")
    label_sumario_TBM.place(x=309, y=190)
    label_sumario_value2 = Label(frame_top, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=("Arial 17"), bg=co1,fg="#545454")
    label_sumario_value2.place(x=309, y=220)

frame_grafic_pie = Frame(frame_top, width=580, height=250, bg=co2)
frame_grafic_pie.place(x=415, y=5)

def grafic_pie():

    figure = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figure.add_subplot(111)

    list_values = pie_values()[1]
    list_categories = pie_values()[0]


    explode = []
    for i in list_categories:
        explode.append(0.05)

    if len(explode) != len(list_values):
        messagebox.showerror('Erro', 'Length of explode must match length of list_values')

    ax.pie(list_values, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(list_categories, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figure, frame_grafic_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)

percentagem()
grafic_bar()
grafic_pie()
resume()

#Creatting frames into the frame bottom
frame_income = Frame(frame_bottom, width=300, height=350, bg=co1)
frame_income.grid(row=0, column=0)

frame_operations = Frame(frame_bottom, width=220, height=250, bg=co1)
frame_operations.grid(row=0, column=1, padx=5)

frame_settings = Frame(frame_bottom, width=220, height=250, bg=co1)
frame_settings.grid(row=0, column=2, padx=5)

#Table income mounthly
app_income = Label(frame_top, text='Incomes and spedings table', anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
app_income.place(x=5, y=309)

def show_income():
    table_head = ['#Id', 'Category', 'Date', 'Amount']

    list_itens = table()

    global tree
    tree = ttk.Treeview(frame_income, selectmode="extended", columns=table_head, show="headings")
    vsb = ttk.Scrollbar(frame_income, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')

    hd = ["center", "center", "center", "center"]
    h = [30, 100, 100, 100]
    n = 0

    for col in table_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])

        n += 1

    for item in list_itens:
        tree.insert('', 'end', values=item)

#Configuration Spedings
label_information = Label(frame_operations, text='Insert news spends', height=1, anchor=NW, font=("Verdana 10 bold"), bg=co1, fg=co4)
label_information.place(x=10, y=10)

label_category = Label(frame_operations, text='Category', height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
label_category.place(x=10, y=40)

#Getting categories

category_function = view_category()
category = []

for i in category_function:
    category.append(i[1])


combo_category_spend = ttk.Combobox(frame_operations, width=10, font=("Ivy 10"))
combo_category_spend['values'] = (category)
combo_category_spend.place(x=110, y=41)



label_cal_spends = Label(frame_operations, text='Date', height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
label_cal_spends.place(x=10, y=70)
entry_cal_spends = DateEntry(frame_operations, width=12, background='darkblue', foreground='white', borderwidth=2, year=2022)
entry_cal_spends.place(x=110, y=71)

label_value_spends = Label(frame_operations, text='Total amount', height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
label_value_spends.place(x=10, y=100)
entry_value_spends = Entry(frame_operations, width=14, justify='left', relief='solid')
entry_value_spends.place(x=110, y=101)

#Insert Button
add_spend_img = Image.open('images/botao_adicionar.png')
add_spend_img = add_spend_img.resize((17, 17))
add_spend_img = ImageTk.PhotoImage(add_spend_img)

button_insert_spend = Button(frame_operations, command=insert_spends_db,image=add_spend_img, text='Insert'.upper(), width=80, compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8 bold"),bg=co1, fg=co0)
button_insert_spend.place(x=110, y=131)

#Delete Button
label_delete = Label(frame_operations,text='Delete', height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
label_delete.place(x=10, y=174)

add_delete_img = Image.open('images/botao_deletar.png')
add_delete_img = add_delete_img.resize((17, 17))
add_delete_img = ImageTk.PhotoImage(add_delete_img)

button_delete = Button(frame_operations, command=delete_spends_db,image=add_delete_img, text='Delete'.upper(), width=80, compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8 bold"),bg=co1, fg=co0)
button_delete.place(x=110, y=177)




#Configuration Revenues
label_information_revenue = Label(frame_settings, text='Insert news revenues', height=1, anchor=NW, font=("Verdana 10 bold"), bg=co1, fg=co4)
label_information_revenue.place(x=10, y=10)

label_date_revenue = Label(frame_settings, text='Date', height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
label_date_revenue.place(x=10, y=40)
entry_date_revenue = DateEntry(frame_settings, width=12, background='darkblue', foreground='white', borderwidth=2, year=2022)
entry_date_revenue.place(x=97, y=40)

label_revenue_value = Label(frame_settings, text='Total amount', height=1, anchor=NW, font=("Ivy 8 bold"), bg=co1, fg=co4)
label_revenue_value.place(x=10, y=68)
entry_revenue = Entry(frame_settings, width=14, justify='left', relief='solid')
entry_revenue.place(x=97, y=68)

add_revenue_img = Image.open('images/botao_adicionar.png')
add_revenue_img = add_revenue_img.resize((17, 17))
add_revenue_img = ImageTk.PhotoImage(add_revenue_img)

button_insert_revenue = Button(frame_settings, command=insert_revenue_db,image=add_revenue_img, text='Insert'.upper(), width=80, compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8 bold"),bg=co1, fg=co0)
button_insert_revenue.place(x=97, y=97)


label_revenue_category = Label(frame_settings, text='Category', height=1, anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4)
label_revenue_category.place(x=10, y=145)

entry_revenue_value = Entry(frame_settings, width=14, justify='left', relief='solid')
entry_revenue_value.place(x=97, y=145)

button_ctg_revenue = Button(frame_settings, command=insert_category_db,image=add_revenue_img, text='Insert'.upper(), width=80, compound=LEFT, anchor=NW, overrelief=RIDGE, font=("Ivy 8 bold"),bg=co1, fg=co0)
button_ctg_revenue.place(x=97, y=176)


percentagem()
grafic_bar()
show_income()
resume()
grafic_pie()
janela.mainloop()
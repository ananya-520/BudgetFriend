#Importing Libraries and Connectivities

import MySQLdb as sq
import tkinter as tk
from dotenv import load_dotenv
import os
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import csv
import pickle
import sys
from tabulate import tabulate
from tkinter import ttk
from PIL import ImageTk, Image

load_dotenv()

#Define SQL Parameters
sql_host = os.getenv("SQL_HOST")
sql_user = os.getenv("SQL_USER")
sql_pass = os.getenv("SQL_PASSWORD")


#Creating a Window TKinter

window=tk.Tk()
window.title("Budget Friend!")
window.geometry("1220x686")
window.resizable(0,0)
bg=tk.PhotoImage(file=os.getenv("MAINPAGE"))
label1=tk.Label(window, image=bg)
label1.place(x=0, y=0)



#Global Variables

date=""
desc=""
amtp=""
mod=""
month=""
savingsvar=0
spendingsvar=0



#Creating a Binary File to Save Certain Values: 

def create_binfile():
    with open("./Assets/Values_BudgetFriend.dat","wb") as f:
        V={}
        V["S.No."]=0
        V["Total Amount"]=0
        V["Bank Amount"]=0
        V["Hand Amount"]=0
        V["Savings"]=0
        V["Spendings"]=0
        pickle.dump(V,f)
create_binfile()

with open("./Assets/Values_BudgetFriend.dat","rb") as f:
    V=pickle.load(f)
    sno=V["S.No."]
    savingsvar=V["Savings"]
    spendingsvar=V["Spendings"]



#Defining More Variables

totamt=tk.IntVar()
curamt=tk.IntVar()
handamt=tk.IntVar()
savingsamt=tk.IntVar()


#Creating a Binary File to Store & Change Values of Variables

with open("./Assets/Values_BudgetFriend.dat","rb") as f:
    V=pickle.load(f)
    print(V)
    totamt.set(V["Total Amount"])
    curamt.set(V["Bank Amount"])
    handamt.set(V["Hand Amount"])
    savingsamt.set(V["Savings"])


'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''



#Main Function

def budgetfriend(): #Create the MySQL Database and Table
    create_sqltable()   #Creates MySQL table
    heading()               #Creates separate frame for the main buttons
    menu()                 #Creates top menu widgets
    data_entry()          #Enters all data saves to MySQL, Binary & CSV file



        
#Heading Frame

def heading():#Creating the heading frame
        hed_frame=tk.LabelFrame(window, font=(50), bd=0, bg="#E8F1F2")
        hed_frame.place(x=20, y=20)
        current_amt_monthly=tk.Label(hed_frame, text="MONTHLY AMOUNT\nIN BANK", bg="#ededed", font=(20)).grid(row=1,column=1)
        currentamt=tk.Button(hed_frame,textvariable=curamt,font=("Open Sans", 16, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11).place(x=170, y=20)
        current_amt_inhand=tk.Label(hed_frame, text="CURRENT AMOUNT\nIN HAND             ", bg="#F1F2EB", font=(20)).grid(row=1,column=4)
        currentamtinhand=tk.Button(hed_frame, textvariable=handamt, font=("Open Sans", 16, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11).place(x=490, y=20)
        andom3=tk.Label(hed_frame, text="  ").grid(row=0, column=20)
        todo=tk.Label(hed_frame, text="START BUDGETING!", font=(20), bg="#F1F2EB").grid(row=2, column=1)
        currspend=tk.Button(hed_frame, text="SPENDINGS", font=("Open Sans", 16, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11, command=spendings_tab).grid(row=2, column=4)
        random=tk.Label(hed_frame, text="   ").grid(row=2, column=3)
        random1=tk.Label(hed_frame, text="   ").grid(row=2, column=5)
        currsav=tk.Button(hed_frame, text="SAVINGS", font=("Open Sans", 16, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11, command=sav_vs_spend_graph_tab).grid(row=2, column=5)
        random3=tk.Label(hed_frame, text="  ").grid(row=2, column=6)
        graphs=tk.Button(hed_frame, text="GRAPHS", command=graphs_tab, font=("Open Sans", 16, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11).grid(row=2, column=2)
        random3=tk.Label(hed_frame, text=" ").grid(row=3, column=0)
        random3=tk.Label(hed_frame, text=" ").grid(row=3, column=1)
        random3=tk.Label(hed_frame, text=" ").grid(row=3, column=2)
        

#Menu
        
def menu():
    main_menu=tk.Menu(window)
    window.config(menu=main_menu)
    main_menu.add_cascade(label="Home")
    main_menu.add_cascade(label="Settings",command=setting_tab)
    main_menu.add_cascade(label="About",command=about_button)

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''


#Spendings Button
    
def spendings_tab():
    spendings_tab=tk.Toplevel()
    spendings_tab.title("Budget Friend! -- Spendings")
    spendings_tab.geometry("1220x686")
    spendings_tab.resizable(0,0)
    spendings_tab_frame=tk.Frame(spendings_tab, bg="#EBFEFE", bd=0)
    spendings_tab_frame.pack(fill="both", expand=1)
    canvas=tk.Canvas(spendings_tab_frame, bg="#EBFEFE")
    canvas.pack(side="left", fill="both", expand=1)
    scroll=ttk.Scrollbar(spendings_tab_frame, orient="vertical", command=canvas.yview)
    scroll.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scroll.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_spendings_tab=tk.Frame(canvas, bg="#EBFEFE")
    canvas.create_window((0,0), window=second_spendings_tab, anchor="nw")

    for i in months:
        if i=="January":
            jan=tk.Label(second_spendings_tab, text="January Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            jan.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-01-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-01-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="February":
            feb=tk.Label(second_spendings_tab, text="February Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            feb.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-02-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-02-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="March":
            mar=tk.Label(second_spendings_tab, text="March Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            mar.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-03-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-03-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="April":
            apr=tk.Label(second_spendings_tab, text="April Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            apr.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-04-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-04-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"

        elif i=="May":
            may=tk.Label(second_spendings_tab, text="May Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            may.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-05-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-05-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="June":
            jun=tk.Label(second_spendings_tab, text="June Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            jun.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-06-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-06-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="July":
            jul=tk.Label(second_spendings_tab, text="July Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            jul.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-07-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-07-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="August":
            aug=tk.Label(second_spendings_tab, text="August Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            aug.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.insert("", tk.END, values=x)
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-08-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-08-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="September":
            sep=tk.Label(second_spendings_tab, text="September Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            sep.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-09-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-09-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="October":
            octo=tk.Label(second_spendings_tab, text="October Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            octo.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-10-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-10-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
            
        elif i=="November":
            nov=tk.Label(second_spendings_tab, text="November Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            nov.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=6)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-11-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-11-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
                
        elif i=="December":
            dec=tk.Label(second_spendings_tab, text="December Spendings:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE")
            dec.grid(sticky="W")
            spend=tk.Entry(second_spendings_tab, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
            spend.grid(sticky="W")
            tree = ttk.Treeview(second_spendings_tab, column=("c1", "c2", "c3","c4","c5"), show='headings', height=5)
            tree.column("#1", anchor=tk.CENTER)
            tree.heading("#1", text="S_No")
            tree.column("#2", anchor=tk.CENTER)
            tree.heading("#2", text="Date")
            tree.column("#3", anchor=tk.CENTER)
            tree.heading("#3", text="Description")
            tree.column("#4", anchor=tk.CENTER)
            tree.heading("#4", text="Amount Paid")
            tree.column("#5", anchor=tk.CENTER)
            tree.heading("#5", text="Mode of Payment")
            tree.grid()
            sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-12-%%'"
            cur.execute(sql8)
            result=cur.fetchall()
            for index, x in enumerate(result):
                num=0
                tree.insert("", tk.END, values=x)
            sql9="SELECT SUM(Amount_paid) FROM LogExpenditure WHERE DATE LIKE '%%-12-%%'"
            cur.execute(sql9)
            result=cur.fetchone()
            for number in result:
                if number==None:
                    spend.insert(0, "Null")
                    spend["state"]="disabled"
                else:
                    spend.insert(0, str(number))
                    spend["state"]="disabled"
        else:
            pass

'''-------------------------------------------------------------------------------------------------------------------------------'''

        
#Settings Tab

def setting_tab():
    setting_window=tk.Toplevel()
    setting_window.title("Budget Friend!-- Settings")
    setting_window.geometry("600x500")
    setting_window["background"]="#EBFEFE"
    setting_window_frame=tk.Label(setting_window, bd=0, bg="#EBFEFE")
    setting_window_frame.grid(row=0, column=0)
    setting_window.resizable(0,0)
    login_label=tk.Label(setting_window_frame, text="LOGIN DETAILS\n.....................................",
                         font=("Lora", 16, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=1, column=1, sticky="W")
    name_label=tk.Label(setting_window_frame, text="Name:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=2, column=1, sticky="W")
    name_entry=tk.Entry(setting_window_frame, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
    name_entry.grid(row=2, column=2)
    line2=tk.Frame(setting_window_frame, width=150, height=2, bg="#73A5D3" )
    line2.place(x=270, y=80)
    email_label=tk.Label(setting_window_frame, text="Email:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=3, column=1, sticky="W")
    email_entry=tk.Entry(setting_window_frame, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
    email_entry.grid(row=3, column=2)
    line2=tk.Frame(setting_window_frame, width=150, height=2, bg="#73A5D3" )
    line2.place(x=270, y=110)    
    username_entry=tk.Label(setting_window_frame, text="Username:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=4, column=1, sticky="W")
    username_entry=tk.Entry(setting_window_frame, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
    username_entry.grid(row=4, column=2)
    line2=tk.Frame(setting_window_frame, width=150, height=2, bg="#73A5D3" )
    line2.place(x=270, y=135) 
    pass_entry=tk.Label(setting_window_frame, text="Password:", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=5, column=1, sticky="W")
    passw_entry=tk.Entry(setting_window_frame, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#EBFEFE")
    passw_entry.grid(row=5, column=2)
    line2=tk.Frame(setting_window_frame, width=150, height=2, bg="#73A5D3" )
    line2.place(x=270, y=160)   
    space=tk.Label(setting_window_frame, text="              ", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=6, column=1, sticky="W")
    trans_label=tk.Label(setting_window_frame, text="TRANSACTIONS\n.....................................",
                         font=("Lora", 16, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=7, column=1, sticky="W")
    tot_amt=tk.Label(setting_window_frame, text="Total Amount for the Month:\n ", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=8, column=1, sticky="W")
    tot_button=tk.Button(setting_window_frame, text="SAVE", font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                         activebackground="#73A5D3", bd=0, width=9).grid(row=8, column=3)
    curramt_change_label=tk.Label(setting_window_frame, text="Current Amount in Bank:\n ", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=9, column=1,sticky="W")
    handamt_change_label=tk.Label(setting_window_frame, text="Current Amount in Hand:\n ", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=10, column=1, sticky="W")
    savings_percent=tk.Label(setting_window_frame, text="Percentage in Savings:\n ", font=("Lora", 14, "bold"), fg="#001E3D", bg="#EBFEFE").grid(row=11, column=1, sticky="W")
    totamtentry=tk.Entry(setting_window_frame, width=25, borderwidth=5)
    totamtentry.grid(row=8, column=2)
    curamtentry=tk.Entry(setting_window_frame, width=25, borderwidth=5)
    curamtentry.grid(row=9, column=2)
    oldcuramt=curamt.get()
    handamtentry=tk.Entry(setting_window_frame, width=25, borderwidth=5)
    handamtentry.grid(row=10, column=2)
    oldhandamt=handamt.get()
    savingsentry=tk.Entry(setting_window_frame, width=25, borderwidth=5)
    savingsentry.grid(row=11, column=2)

    def savings_change():
        global savingsvar
        savingsvariable=savingsentry.get()
        getcuramtvar=curamtentry.get()
        curamt.set(getcuramtvar)
        savingsvar=int(savingsvariable)*curamt.get()/100
        newcuramt=curamt.get()-savingsvar
        curamt.set(newcuramt)
        with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
            V=pickle.load(f)
            V["Bank Amount"]=newcuramt
            V["Savings"]=savingsvar
            f.seek(0)
            pickle.dump(V,f)    
            print(V)

    def savecuramt():
        getcuramtvar=curamtentry.get()
        curamt.set(getcuramtvar)
        newcuramt=curamt.get()
        curamt.set(newcuramt)
        with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
            V=pickle.load(f)
            V["Bank Amount"]=newcuramt
            f.seek(0)
            pickle.dump(V,f)    
            print(V)
        if (curamt.get()<=100)==True:
            messagebox.showwarning("Beware!", "Your Amount in Bank is at 100 Rs.")
        elif (curamt.get()<=10)==True:
            messagebox.showwarning("Beware!", "Your Amount in Bank is at 10 Rs.")
        elif (curamt.get()<=0)==True:
            messagebox.showerror("Error", "No More Money")
        savcuramt["state"]="disabled"

    def savehandamt():
        gethandamtvar=handamtentry.get()
        handamt.set(gethandamtvar)
        newhandamt=handamt.get()
        handamt.set(newhandamt)
        with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
            V=pickle.load(f)
            V["Hand Amount"]=newhandamt
            f.seek(0)
            pickle.dump(V,f)    
            print(V)
        savhandamt["state"]="disabled"
        if (handamt.get()<=100)==True:
            messagebox.showwarning("Beware!", "Your Amount in Hand is at 100 Rs.")
        elif (handamt.get()<=10)==True:
            messagebox.showwarning("Beware!", "Your Amount in Hand is at 10 Rs.")
        elif (handamt.get()<=0)==True:
            messagebox.showerror("Error", "No More Money")

    savcuramt=tk.Button(setting_window_frame, text="SAVE", font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", width=9, bd=0, command=savecuramt)
    savcuramt.grid(row=9, column=3)
    savhandamt=tk.Button(setting_window_frame, text="SAVE", font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", width=9, bd=0, command=savehandamt)
    savhandamt.grid(row=10, column=3)
    savings_button=tk.Button(setting_window_frame, command=savings_change, text="SAVE", font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=9).grid(row=11, column=3)

    def reset_onsave():
        #saves all the current data cash in bank, cash in hand, graph details, tables in csv/txt files and resets everything
        return

'''---------------------------------------------------------------------------------------------------------------------------------'''

#About Button

def about_button():
    about_window=tk.Toplevel()
    about_window.title("Budget Friend! -- About")
    about_window.geometry("975x500")
    about_window["background"]="#EBFEFE"
    about_window_frame=tk.Label(about_window, bg="#EBFEFE")
    about_window_frame.grid(row=0, column=4)
    about1=tk.Label(about_window, text="About the App", font=("Lora", 16, "bold"), fg="#001E3D", bg="#EBFEFE")
    about1.grid(row=0, column=4)
    about1_info="""\nTracking your spending is the first step in
getting your finances in order. \
By understanding what you spend money on and how much you spend, you
can see exactly where your cash is going and areas where you can cut
back. \n\n\
The app, BudgetFriend, is a simple budget tracking application which
helps you users to have a rough overview on \
how much you spend you money and gives tips on different ways to
reduce spending their money. \
It will help you users to keep track of their savings and construct a
suitable budget plan according to their choice and convenience.\n\n
"""
    about1_var=tk.Label(about_window, text=about1_info, font=("Lora", 12), fg="#001E3D", bg="#EBFEFE")
    about1_var.grid(row=1, column=4)
    about2=tk.Label(about_window, text="About the Developers", font=("Lora", 16, "bold"), fg="#001E3D", bg="#EBFEFE")
    about2.grid(row=6, column=4)
    about2_info="""The developers of this application are just \n\
two ordinary friends with a passion for Computer Science and Coding. \n\
To create this application is a great opportunity for both of us to
explore more in the world of coding and computer programming. \n
We are immensely grateful for all the support we had in creating this app. \
Hopefully, we will be able to make many more such applications and
websites with optimum usage and productivity to help users, both
students and workers alike.\n\n"""
    about2_var=tk.Label(about_window, text=about2_info, font=("Lora", 12), fg="#001E3D", bg="#EBFEFE")
    about2_var.grid(row=7, column=4)


'''-----------------------------------------------------------------------------------------------------------------------------------'''


#Data Entry

def data_entry():
    #Creating data entry frame
    sav_frame=tk.LabelFrame(window, bd=0, bg="#E8F1F2")
    sav_frame.place(x=20, y=170)
    
    def save_onclick(): #Function for the save button
        
        def saving_data():
            global sno
            global date
            global desc
            global amtp
            global mod
            sno+=1
            date=entry1.get()
            desc=entry2.get()
            amtp=entry3.get()
            mod=entry4.get()
            if ((mod=="Cash" or mod=="CASH") and (handamt.get()>=int(amtp))==True) or ((mod=="Card" or mod=="CARD") and (curamt.get()>=int(amtp))==True):
                print("S_No:", sno)
                print("Date of Entry:", date)
                print("Description:", desc)
                print("Amount paid:", amtp)
                print("Mode of payment:", mod)
                print("------------------")
                entry1.delete(0,tk.END)
                entry2.set("Select")
                entry3.delete(0,tk.END)
                entry4.delete(0,tk.END)
                enter_datatomysql()
                print_sqltable()
                with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                        V=pickle.load(f)
                        V["S.No."]=sno
                        f.seek(0)
                        pickle.dump(V,f)    
                        print(V)
                return sno, date, desc, amtp, mod
            else:
                pass

        def update_amt():
            global amtp
            global spendingsvar
            
            if mod=="Cash" or mod=="CASH":
                if (int(amtp)<=handamt.get())==True:
                    spendingsvar+=int(amtp)
                    with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                        V=pickle.load(f)
                        V["Spendings"]=spendingsvar
                        f.seek(0)
                        pickle.dump(V,f)    
                        print(V)
                    int_handamt=handamt.get()
                    presentamt=int_handamt-int(amtp)
                    handamt.set(presentamt)
                    with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                        V=pickle.load(f)
                        V["Hand Amount"]=presentamt
                        f.seek(0)
                        pickle.dump(V,f)    
                        print(V)
                else:
                    messagebox.showerror("Error", "No More Money")
                    
            elif mod=="Card" or mod=="CARD":
                if (int(amtp)<=curamt.get())==True:
                    spendingsvar+=int(amtp)
                    with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                        V=pickle.load(f)
                        V["Spendings"]=spendingsvar
                        f.seek(0)
                        pickle.dump(V,f)    
                        print(V)
                    int_curamt=curamt.get()
                    presentamt=int_curamt-int(amtp)
                    curamt.set(presentamt)
                    with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                        V=pickle.load(f)
                        V["Bank Amount"]=presentamt
                        f.seek(0)
                        pickle.dump(V,f)    
                        print(V)
                else:
                    messagebox.showerror("Error", "No More Money")
        saving_data()
        update_amt()
        savedata_csv()

    def clearfields(): #Function for the clear button
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')
        entry4.delete(0, 'end')

    def del_onclick(): #Function for the delete button which does not work yet
        delrecordmysql()
        print_sqltable()

    #Widgets related to saving data
    random3=tk.Label(sav_frame, text=" ").grid(row=0, column=0)
    ldat=tk.Label(sav_frame, text="  DATE OF ENTRY(YYYY-MM-DD): ", bd=0, font=("Lora", 10, "bold"), fg="#001E3D").grid(row=4, column=0, sticky="W")
    ldes=tk.Label(sav_frame, text="  DESCRIPTION:", bd=0, font=("Lora", 10, "bold"), fg="#001E3D").grid(row=5, column=0, sticky="W")
    lamtp=tk.Label(sav_frame, text="  AMOUNT PAID:", bd=0, font=("Lora", 10, "bold"), fg="#001E3D").grid(row=6, column=0, sticky="W")
    lmod=tk.Label(sav_frame, text="  MODE OF PAYMENT:", bd=0, font=("Lora", 10, "bold"), fg="#001E3D").grid(row=7, column=0, sticky="W")
    entry1=tk.Entry(sav_frame, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#E8F1F2")
    entry1.grid(row=4, column=1)
    line2=tk.Frame(window, width=145, height=2, bg="#73A5D3" )
    line2.place(x=230, y=210)
    entry2=tk.StringVar()
    entry2.set("SELECT")
    lst=['Grocery',
         'Stationery',
         'Toys',
         'Books',
         'Fees',
         'Hospital',
         'Education',
         'Repayment of Loan',
         'Food','Entertainment',
         'Gift',
         'House Rent',
         'Car Rent',
         'Donation',
         'Travel',
         'Commute',
         'Subscription',
         'Work',
         'Event',
         'Household',
         'Other']
    opts=tk.OptionMenu(sav_frame,entry2,*lst)
    opts.config(bd=0, fg="#001E3D", bg="#E8F1F2", activebackground="#E8F1F2", font=("Lora", 9, "bold"))
    opts.grid(row=5, column=1)
    entry3=tk.Entry(sav_frame, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#E8F1F2")
    entry3.grid(row=6, column=1)
    line2=tk.Frame(window, width=145, height=2, bg="#73A5D3" )
    line2.place(x=230, y=260)
    entry4=tk.Entry(sav_frame, font=("Lora", 11, "bold"), bd=0, fg="#001E3D", bg="#E8F1F2")
    entry4.grid(row=7, column=1)
    line2=tk.Frame(window, width=145, height=2, bg="#73A5D3" )
    line2.place(x=230, y=285)
    random3=tk.Label(sav_frame, text=" ").grid(row=8, column=2)
    saveb=tk.Button(sav_frame, text="SAVE", command=save_onclick, font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11).grid(row=9, column=0)
    delb=tk.Button(sav_frame, text="DELETE", command=delrecordmysql, font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11).grid(row=9, column=1)
    random3=tk.Label(sav_frame, text=" ").grid(row=10, column=2)
    clear=tk.Button(sav_frame, text="CLEAR", command=clearfields, font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11).grid(row=11, column=0)
    printtablerecs=tk.Button(sav_frame, text="DISPLAY ALL", command=ViewTableTk, font=("Lora", 14, "bold"), fg="white", bg="#73A5D3", activeforeground="white",
                   activebackground="#73A5D3", bd=0, width=11).grid(row=11, column=1)
    random3=tk.Label(sav_frame, text=" ").grid(row=12, column=2)

c=tk.IntVar() #increement variable for serial no.
s=0 #random variable for csv
def savedata_csv():
    global db
    global cur
    global sno
    global date
    global desc
    global amtp
    global mod
    global month
    global s
    with open("./Assets/reduceamt.csv", "a+", newline="") as f:
        r=csv.reader(f)
        w=csv.writer(f)
        stdate=str(date)
        lstdate=stdate.split("-")
        if lstdate[1]=="01":
            month="January"
        elif lstdate[1]=="02":
            month="February"
        elif lstdate[1]=="03":
            month="March"
        elif lstdate[1]=="04":
            month="April"
        elif lstdate[1]=="05":
            month="May"
        elif lstdate[1]=="06":
            month="June"
        elif lstdate[1]=="07":
            month="July"
        elif lstdate[1]=="08":
            month="August"
        elif lstdate[1]=="09":
            month="September"
        elif lstdate[1]=="10":
            month="October"
        elif lstdate[1]=="11":
            month="November"
        elif lstdate[1]=="12":
            month="December"
        else:
            print("Invalid")
        hed=["S. No.", "Month", "Date", "Description", "Mode of Payment", "Current Cash in Bank", "Current Cash in Hand", "Amount Paid"]
        if s==0:
            c.set(s)
            w.writerow(hed)
            s+=1
            c.set(s)
        else:
            s+=1
            c.set(s)
            pass

        if mod=="Cash" or mod=="CASH" or mod=="cash":
            presenthandamt=handamt.get()
            presentcuramt=curamt.get()
        elif mod=="Card" or mod=="CARD" or mod=="card":
            presentcuramt=curamt.get()
            presenthandamt=handamt.get()
        else:
            print("Invalid")

        rec=[c.get(), month, date, desc, mod, presentcuramt, presenthandamt, amtp]
        w.writerow(rec)
        print("Data recorded to CSV file.")


'''----------------------------------------------------------------------------------------------------------------------------------'''

#Creating Database & Table

db=sq.connect(sql_host,sql_user,sql_pass)
cur=db.cursor()
def create_sqltable():
    global db
    global cur
    s1="CREATE DATABASE if not exists BudgetFriend"
    cur.execute(s1)
    s2="USE BudgetFriend"
    cur.execute(s2)
    s3="CREATE TABLE if not exists LogExpenditure(S_No INT(4), Date DATE, Description VARCHAR(50), Amount_Paid DECIMAL(20,3), Mode_of_Payment VARCHAR(10))"
    cur.execute(s3)
    db.commit()

#Enter data to mysql table

def enter_datatomysql():
    global db
    global cur
    global sno
    global date
    global desc
    global amtp
    global mod
    if date!="":
        if ((mod=="Cash" or mod=="CASH") and (handamt.get()>=int(amtp))==True) or ((mod=="Card" or mod=="CARD") and (curamt.get()>=int(amtp))==True):
            s4="INSERT ignore INTO LogExpenditure VALUES({},'{}','{}','{}','{}')".format(sno,date,desc,amtp,mod)
            cur.execute(s4)
            db.commit()
            print("Saved Successfully")
        else:
            pass
    else:
        pass

#Delete entries
def delrecordmysql():
    curitem=tree.focus()
    drec=dict(tree.item(curitem))
    drecval=list(drec['values'])
    y=int(drecval[0])
    def del_value_add():
        global spendingsvar
        print(drecval[3])
        del_amt=float(drecval[3])
        if mod=="Cash" or mod=="CASH":
            spendingsvar=spendingsvar-int(del_amt)
            with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                            V=pickle.load(f)
                            V["Spendings"]=spendingsvar
                            f.seek(0)
                            pickle.dump(V,f)    
                            print(V)
            int_handamt=handamt.get()
            presentamt=int_handamt+int(del_amt)
            handamt.set(presentamt)
            with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                V=pickle.load(f)
                V["Hand Amount"]=presentamt
                f.seek(0)
                pickle.dump(V,f)    
                print(V)
            
        elif mod=="Card" or mod=="CARD":
            spendingsvar-=int(del_amt)
            with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                            V=pickle.load(f)
                            V["Spendings"]=spendingsvar
                            f.seek(0)
                            pickle.dump(V,f)    
                            print(V)
            int_curamt=curamt.get()
            presentamt=int_curamt+int(del_amt)
            curamt.set(presentamt)
            with open("./Assets/Values_BudgetFriend.dat","rb+") as f:
                V=pickle.load(f)
                V["Bank Amount"]=presentamt
                f.seek(0)
                pickle.dump(V,f)    
                print(V)

    sq6="DELETE FROM LogExpenditure WHERE S_No={}".format(y)
    cur.execute(sq6)
    db.commit()
    del_value_add()
    tree.delete(curitem)

#Print The Entries on IDLE

def print_sqltable():
    global db
    global cur
    s5="SELECT * FROM LogExpenditure"
    cur.execute(s5)
    output=cur.fetchall()
    print(tabulate(output,headers=['S_No','Date','Description','Amount_Paid','Mode_of_Payment'],tablefmt='psql',showindex=False))

'''----------------------------------------------------------------------------------------------------------------------------------'''


#Creating Tables in TKinter


clicked=tk.StringVar()
def MonthlyTables():
    tree.delete(*tree.get_children())
    create_sqltable()
    if clicked.get()=="January":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-01-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="February":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-02-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="March":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-03-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="April":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-04-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="May":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-05-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="June":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-06-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="July":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-07-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="August":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-08-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="September":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-09-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="October":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-10-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="November":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-11-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    elif clicked.get()=="December":
        sql8="SELECT * FROM LogExpenditure WHERE DATE LIKE '%%-12-%%'"
        cur.execute(sql8)
        result=cur.fetchall()
        for index, x in enumerate(result):
            num=0
            tree.insert("", tk.END, values=x)
    else:
        pass

def ViewTableTk():
    tree.delete(*tree.get_children())
    create_sqltable()
    s7="SELECT * FROM LogExpenditure"
    cur.execute(s7)
    output=cur.fetchall()
    for index, x in enumerate(output):
        num=0
        tree.insert("", tk.END, values=x)
        num+=1
months=["January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"]
clicked.set("SELECT MONTH")

tab_frame=tk.LabelFrame(window, bd=0, bg="#E8F1F2")
tab_frame.place(x=20, y=430)
drop=tk.OptionMenu(tab_frame, clicked, *months)
drop.config(bd=0, fg="#001E3D", bg="#E8F1F2", activebackground="#E8F1F2",   font=("Lora", 9, "bold"))
drop.grid(row=0, column=0, sticky="W")
tab_button=tk.Button(tab_frame, text="  SHOW TABLE", command=MonthlyTables, bd=0, fg="#001E3D", bg="#E8F1F2", font=("Lora", 9, "bold"))
tab_button.grid(sticky="W")
tree = ttk.Treeview(tab_frame, column=("c1", "c2", "c3","c4","c5"), show='headings', height=7)
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="S_No")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Date")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Description")
tree.column("#4", anchor=tk.CENTER)
tree.heading("#4", text="Amount Paid")
tree.column("#5", anchor=tk.CENTER)
tree.heading("#5", text="Mode of Payment")
tree.grid()

'''----------------------------------------------------------------------------------------------------------------------------------'''

#Graphs Tab

def graphs_tab():
    grcy=stnry=toys=bks=fee=hosp=ed=rol=food=entrmn=gift=hr=cr=don=travel=comm=subs=work=event=hh=other=0
    d={"Grocery":grcy,
       "Stationery":stnry,
       'Toys':toys,
        'Books':bks,
        'Fees':fee,
        'Hospital':hosp,
        'Education':ed,
        'Repayment of Loan':rol,
        'Food':food,
       'Entertainment':entrmn,
        'Gift':gift,
         'House Rent':hr,
         'Car Rent':cr,
         'Donation':don,
         'Travel':travel,
         'Commute':comm,
         'Subscription':subs,
         'Work':work,
         'Event':event,
         'Household':hh,
         'Other':other}
    s8="SELECT * FROM LogExpenditure"
    cur.execute(s8)
    output=cur.fetchall()
    arlst=[]
    labels_arlst=[]
    labels_from_our_table=[]
    MAIN_arlst=[]
    
    for anonymous_var in output:
        if anonymous_var[2] not in labels_from_our_table:
            labels_from_our_table.append(anonymous_var[2])
    for i in labels_from_our_table:
        s10="SELECT SUM(Amount_Paid) FROM LOGEXPENDITURE WHERE DESCRIPTION='{}'".format(i)
        cur.execute(s10)
        output=cur.fetchall()
        d[i]=output
        var=str(output)
        k=''
        for m in var:
            if m in '0123456789.':
                k+=str(m)
            else:
                continue
        k=float(k)
        MAIN_arlst.append(k)
    y=np.array(MAIN_arlst)
    plt.pie(y, labels = labels_from_our_table)
    plt.show()


#Graph between Spendings and Savings
    
def sav_vs_spend_graph_tab():
    global savingsvar
    column_names = ['Spendings','Savings']
    column_values = [spendingsvar,savingsvar]
    colors = ['#7393B3','#A7C7E7']
    plt.bar(column_names, column_values, color=colors)
    plt.title('Spendings Vs Savings', fontsize=14)
    plt.xlabel('Spendings', fontsize=14)
    plt.ylabel('Savings', fontsize=14)
    plt.grid(True)
    plt.show()

#Logo
    
picture_frame=tk.Frame(window,width=400, height=400)
picture_frame.place(x=800, y=20)
image=Image.open(os.getenv("LOGO"))
resized_img=image.resize((400,120))
logo_img=ImageTk.PhotoImage(resized_img)
pic_label=tk.Label(picture_frame,image=logo_img)
pic_label.pack()


budgetfriend()
##printing()
tk.mainloop()

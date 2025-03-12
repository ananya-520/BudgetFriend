#Sign Up Page

from tkinter import *
from PIL import ImageTk
import MySQLdb as sq
from MySQLdb import connect
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()

#Define SQL Parameters
sql_host = os.getenv("SQL_HOST")
sql_user = os.getenv("SQL_USER")
sql_pass = os.getenv("SQL_PASSWORD")

window=Tk()
window.geometry("1000x562")
window.resizable(0,0)
window.title("Sign Up Page")
bg=ImageTk.PhotoImage(file=os.getenv("SIGNUPPAGE"))
bglabel=Label(window, image=bg)
bglabel.place(x=0, y=0)
heading=Label(window, text="SIGNUP", font=("Microsoft Yahei UI Light", 23, "bold"), fg="white", bg="#C7AF9A")
heading.place(x=440, y=60)

def on_enteremail(event):
    if email.get()=="Enter Email":
        email.delete(0, END)

def on_enteruser(event):
    if username.get()=="Username":
        username.delete(0, END)

def on_enterpass(event):
    if password.get()=="Password":
        password.delete(0, END)

def on_enterconpass(event):
    if confirmpass.get()=="Confirm Password":
        confirmpass.delete(0, END)

def clear_signup():
    email.delete(0, END)
    username.delete(0, END)
    password.delete(0, END)
    confirmpass.delete(0, END)
   
def logindb():
    global sq
    if email.get()=="Enter Email" or username.get()=="Username" or password.get()=="Password" or confirmpass.get()=="Confirm Password":
        messagebox.showerror("Error", "Enter valid information")
    elif password.get()!=confirmpass.get():
        messagebox.showerror("Error", "!Password Mismatch!")
    elif email.get()=="" or username.get()=="" or password.get()=="" or confirmpass.get()=="":
        messagebox.showerror("Error", "Enter valid information")
    else:
        try:
            db=sq.connect(sql_host,sql_user,sql_pass)
            cur=db.cursor()
        except:
            messagebox.showerror("Error", "Database connectivity issue")
            return
       
        s1="CREATE DATABASE if not exists BudgetFriend"
        cur.execute(s1)
        s2="USE BudgetFriend"
        cur.execute(s2)
        s3="CREATE TABLE if not exists Security(id INT auto_increment PRIMARY KEY NOT NULL, EMAIL VARCHAR(50), USERNAME VARCHAR(50), PASSWORD VARCHAR(50))"
        cur.execute(s3)
        s5="SELECT * FROM SECURITY WHERE USERNAME='{}'".format(username.get())
        cur.execute(s5)
        rec=cur.fetchone()
        if rec!=None:
            messagebox.showerror("Error", "!Username already exists!")
        else:
            s4="INSERT ignore INTO Security(email, username, password) VALUES (%s, %s, %s)"
            cur.execute(s4, (email.get(), username.get(), password.get()))
            db.commit()
            print("Account Created")
            messagebox.showinfo("Success", "Account Created!")
            clear_signup()
            redirect_login()
       
def redirect_login():
    window.destroy()
    import Login_Page

def user():
    user=username.get()
    emaill=email.get()
    passw=password.get()
   
email=Entry(window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="#C7AF9A", bg="white")
email.place(x=350, y=200)
email.insert(0, "Enter Email")

email.bind("<FocusIn>", on_enteremail)

line1=Frame(window, width=250, height=2, bg="#C7AF9A" )
line1.place(x=350, y=222)

username=Entry(window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="#C7AF9A", bg="white")
username.place(x=350, y=250)
username.insert(0, "Username")

username.bind("<FocusIn>", on_enteruser)

line2=Frame(window, width=250, height=2, bg="#C7AF9A" )
line2.place(x=350, y=272)

password=Entry(window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="#C7AF9A", bg="white")
password.place(x=350, y=300)
password.insert(0, "Password")

password.bind("<FocusIn>", on_enterpass)

line3=Frame(window, width=250, height=2, bg="#C7AF9A" )
line3.place(x=350, y=322)

confirmpass=Entry(window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="#C7AF9A", bg="white")
confirmpass.place(x=350, y=350)
confirmpass.insert(0, "Confirm Password")

confirmpass.bind("<FocusIn>", on_enterconpass)

line4=Frame(window, width=250, height=2, bg="#C7AF9A" )
line4.place(x=350, y=372)

signupbutton=Button(window, text="Sign Up", command=logindb, font=("Open Sans", 16, "bold"), fg="white", bg="#C7AF9A", activeforeground="white", activebackground="#C7AF9A", bd=0, width=19)
signupbutton.place(x=350, y=400)
nosignup=Button(window, text="Already have an account? Click Here", command=redirect_login, font=("Open Sans", 9, "bold"), fg="#C7AF9A", bg="white", activeforeground="white", activebackground="#C7AF9A", bd=0, width=30)
nosignup.place(x=350, y=450)

mainloop()

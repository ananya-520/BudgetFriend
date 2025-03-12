#Login Page

from tkinter import *
from PIL import ImageTk
import MySQLdb as sq
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
window.title("Login Page")
bg=ImageTk.PhotoImage(file=os.getenv("SIGNUPPAGE"))
bglabel=Label(window, image=bg)
bglabel.place(x=0, y=0)
heading=Label(window, text="LOGIN", font=("Microsoft Yahei UI Light", 23, "bold"), fg="white", bg="#C7AF9A")
heading.place(x=440, y=60)
def on_enteruser(event):
    if username.get()=="Username":
        username.delete(0, END)

def on_enterpass(event):
    if password.get()=="Password":
        password.delete(0, END)

def eye_on_click():
    openeye.config(file=os.getenv("CLOSEEYE"))
    password.config(show="*")
    openeye1.config(command=second_click)
   
def second_click():
    openeye.config(file=os.getenv("OPENEYE"))
    password.config(show="")
    openeye1.config(command=eye_on_click)

def redirect_bf():
    if username.get()=="" or password.get()=="":
            messagebox.showerror("Error", "Enter valid information")
    else:
        global sq
        db=sq.connect(sql_host,sql_user,sql_pass)
        cur=db.cursor()
        s1="CREATE DATABASE if not exists BudgetFriend"
        cur.execute(s1)
        s2="USE BudgetFriend"
        cur.execute(s2)
        s3="SELECT * FROM SECURITY WHERE USERNAME=%s AND PASSWORD=%s"
        cur.execute(s3, (username.get(), password.get()))
        res=cur.fetchone()
        if res==None:
            messagebox.showerror("Error", "!Incorrect Username or Password")
        else:
            messagebox.showinfo("Success", "Access Granted")
            window.destroy()
            import BudgetFriendMain


def redirect_signup():
    window.destroy()
    import Sign_Up_Page

username=Entry(window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="#C7AF9A", bg="white")
username.place(x=350, y=200)
username.insert(0, "Username")

username.bind("<FocusIn>", on_enteruser)

line1=Frame(window, width=250, height=2, bg="#C7AF9A" )
line1.place(x=350, y=222)

password=Entry(window, width=25, font=("Microsoft Yahei UI Light", 11, "bold"), bd=0, fg="#C7AF9A", bg="white")
password.place(x=350, y=250)
password.insert(0, "Password")

password.bind("<FocusIn>", on_enterpass)

line2=Frame(window, width=250, height=2, bg="#C7AF9A" )
line2.place(x=350, y=272)

openeye=PhotoImage(file=os.getenv("OPENEYE"))
openeye1=Button(window, image=openeye, bd=0, bg="white", command=eye_on_click)
openeye1.place(x=570, y=245)

loginbutton=Button(window, text="Login", command=redirect_bf, font=("Open Sans", 16, "bold"), fg="white", bg="#C7AF9A", activeforeground="white",
                   activebackground="#C7AF9A", bd=0, width=19)
loginbutton.place(x=350, y=300)

nosignup=Button(window, text="Don't have an account? Click Here", command=redirect_signup, font=("Open Sans", 9, "bold"), fg="#C7AF9A", bg="white",
                activeforeground="white", activebackground="#C7AF9A", bd=0, width=30)
nosignup.place(x=350, y=350)

mainloop()

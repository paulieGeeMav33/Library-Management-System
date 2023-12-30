
from tkinter import *

import sqlite3

root = Tk()

root.title("Library")

root.geometry("400x400")


#Connect to library db

library_connect = sqlite3.connect("library2.sqlite")

library_cursor = library_connect.cursor()

def insert_borrower():
    submit_conn = sqlite3.connect("library2.sqlite")

    submit_cur = submit_conn.cursor()

    submit_cur.execute("INSERT INTO BORROWER(Name,Address,Phone) VALUES(:name,:address,:phone)",
                       {
                           'name':name.get(),
                           'address':address.get(),
                           'phone':phone.get()
                       })
    
    submit_conn.commit()
    submit_conn.close()

def input_query():
    iq_conn = sqlite3.connect("library2.sqlite")
    
    iq_cur = iq_conn.cursor()
    
    iq_cur.execute()
    
def display_insert_borrower():
    #Text fields
    name = Entry(root, width=30)
    name.grid(row = 0, column=1)

    address = Entry(root, width=30)
    address.grid(row = 1, column=1)

    phone = Entry(root, width=30)
    phone.grid(row = 2, column=1)


    #Text labels
    name_label = Label(root,text="Name:")
    name_label.grid(row=0,column=0)

    address_label = Label(root,text="Address:")
    address_label.grid(row=1,column=0)

    phone_label = Label(root,text="Phone:")
    phone_label.grid(row=2,column=0)

    #Buttons
    submit_button = Button(root,text="Insert Borrower",command=insert_borrower)
    submit_button.grid(row=3,column=0)

root.mainloop()
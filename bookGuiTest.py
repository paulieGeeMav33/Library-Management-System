import tkinter as tk
import sqlite3
import datetime

from tkinter import ttk

def insert_borrower():
    conn = sqlite3.connect("library2.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO Borrower(Name, Address, Phone) VALUES (?, ?, ?)", 
                (name_entry.get(), address_entry.get(), phone_entry.get()))
    conn.commit()
    conn.close()

def checkout_book():
    conn = sqlite3.connect("library2.sqlite")
    cur = conn.cursor()
    today = datetime.date.today()
    Date_out = today.strftime("%y-%m-%d")
    Due_Date = today + datetime.timedelta(days= 14)
    cur.execute("INSERT INTO Book_Loans(Card_No, book_id,Branch_Id,Date_Out,Due_Date) VALUES (?, ?, ?,?,?)", 
                (borrower_id_entry.get(), book_id_entry.get(), branch_id_entry.get(), Date_out, Due_Date))
    conn.commit()
    conn.close()

def add_new_book():
    conn = sqlite3.connect("library2.sqlite")
    cur = conn.cursor()

    cur.execute("INSERT INTO Book(Title,Publisher_name) VALUES(?,?)",
                (new_book_title_entry.get(),publisher_entry.get()))
    curr_id = cur.lastrowid
    for branch_id in range(1, 6):
        cur.execute("INSERT INTO Book_Copies(book_id, branch_id, no_of_copies) VALUES (?, ?, ?)", 
                    (book_id_entry.get(), branch_id, 5))
    
    cur.execute("INSERT INTO Book_authors(book_id,author_name) VALUES(?,?)",
                (curr_id,author_entry.get()))
    conn.commit()
    conn.close()

def list_loaned_copies():
    conn = sqlite3.connect("library2.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT branch_id, COUNT(*) FROM Book_Loans JOIN Book ON Book_Loans.book_id = Book.book_id WHERE Book.title = ? GROUP BY branch_id", 
                (book_title_entry.get(),))
    #if(book_title_entry.get() == ""):
    #    cur.execute("SELECT branch_id, COUNT(*) FROM Book_Loans JOIN Book ON Book_Loans.book_id = Book.book_id GROUP BY branch_id", 
    #            )
    loans = cur.fetchall()
    conn.close()
    loan_text.set('\n'.join([f"Branch ID: {branch}, Copies: {count}" for branch, count in loans]))

def list_late_loans():
    conn = sqlite3.connect("library2.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Book_Loans WHERE due_date BETWEEN ? AND ? AND returned_date > due_date", 
                (start_date_entry.get(), end_date_entry.get()))
    late_loans = cur.fetchall()
    conn.close()
    late_loan_text.set('\n'.join(str(loan) for loan in late_loans))

def list_lateFee_Balance():
    conn = sqlite3.connect("library2.sqlite")
    cur = conn.cursor()
    cur.execute("""
                SELECT
    BL.Card_No AS Borrower_ID,
    B.Name AS Borrower_Name,
    COALESCE(SUM(BL.LateFeeBalance), 0) AS LateFee_Balance
FROM
    vBookLoanInfo BL
JOIN BORROWER B ON BL.Card_No = B.Card_No
WHERE
    (B.Card_No = ? OR ? IS NULL)
    AND (B.Name LIKE ? OR ? IS NULL)
GROUP BY
    BL.Card_No, B.Name
ORDER BY
    LateFee_Balance;
                """,(vCard_entry.get(),vCard_entry.get() if vCard_entry.get() != "" else None,"%"+vname_entry.get()+"%",vname_entry.get()if vname_entry.get()!= "" else None))
    

    
    late_fee = cur.fetchall()
    conn.close()
    late_fee_balance_text.set('\n'.join(str(fee) for fee in late_fee))


def list_bookInfo_view():
    conn = sqlite3.connect("library2.sqlite")
    cur = conn.cursor()
    cur.execute("""
                SELECT
    BL.Card_No,
    Bo.Book_Id,
    Bo.Title AS Book_Title,
    BL.LateFeeBalance,
    CASE
        WHEN BL.LateFeeBalance IS NULL THEN 'Non-Applicable'
        ELSE '$' || ROUND(BL.LateFeeBalance, 2)
    END AS FormattedLateFee
FROM
    vBookLoanInfo BL
JOIN BOOK Bo ON BL.Title = Bo.Title
WHERE
    (BL.Card_No = ? OR ? IS NULL)
    AND (Bo.Book_Id = ? OR Bo.Title LIKE ? OR ? IS NULL)
ORDER BY
    BL.LateFeeBalance DESC NULLS LAST;
                """,(vBook_Card_Entry.get(), vBook_Card_Entry.get() if vBook_Card_Entry.get() != "" else None,
                     vBook_ID_Entry.get(),
                     "%"+vBook_Title_Entry.get()+"%", vBook_Title_Entry.get() if vBook_Title_Entry.get() != "" else None))
    
    
    
    vBookInfo = cur.fetchall()
    conn.close()
    vBookInfo_text.set('\n'.join(str(book) for book in vBookInfo))

# Create the main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")

# Create a notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Tab 1: Add Borrower
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Add Borrower')

name_entry = tk.Entry(tab1)
name_entry.grid(row=0, column=1)
tk.Label(tab1, text="Name").grid(row=0, column=0)

address_entry = tk.Entry(tab1)
address_entry.grid(row=1, column=1)
tk.Label(tab1, text="Address").grid(row=1, column=0)

phone_entry = tk.Entry(tab1)
phone_entry.grid(row=2, column=1)
tk.Label(tab1, text="Phone").grid(row=2, column=0)

tk.Button(tab1, text="Add Borrower", command=insert_borrower).grid(row=3, column=0, columnspan=2)

# Tab 2: Checkout Book
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Checkout Book')

borrower_id_entry = tk.Entry(tab2)
borrower_id_entry.grid(row=4, column=1)
tk.Label(tab2, text="Borrower ID").grid(row=4, column=0)

book_id_entry = tk.Entry(tab2)
book_id_entry.grid(row=5, column=1)
tk.Label(tab2, text="Book ID").grid(row=5, column=0)

branch_id_entry = tk.Entry(tab2)
branch_id_entry.grid(row=6, column=1)
tk.Label(tab2, text="Branch ID").grid(row=6, column=0)

tk.Button(tab2, text="Checkout Book", command=checkout_book).grid(row=7, column=0, columnspan=2)
# ... (similar structure for Checkout Book)

# Tab 3: Add New Book
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Add New Book')

new_book_title_entry = tk.Entry(tab3)
new_book_title_entry.grid(row=8,column=1)
tk.Label(tab3,text="New book title").grid(row=8,column=0)

publisher_entry = tk.Entry(tab3)
publisher_entry.grid(row=9,column=1)
tk.Label(tab3,text="Publisher").grid(row=9,column=0)

author_entry = tk.Entry(tab3)
author_entry.grid(row=10,column=1)
tk.Label(tab3,text="Author Name").grid(row=10,column=0)

tk.Button(tab3, text="Add New Book", command=add_new_book).grid(row=11, column=0, columnspan=2)
# ... (similar structure for Add New Book)

# Tab 4: List Loaned Copies
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text='List Loaned Copies')

book_title_entry = tk.Entry(tab4)
book_title_entry.grid(row=12, column=1)
tk.Label(tab4, text="Book Title").grid(row=12, column=0)

loan_text = tk.StringVar()
tk.Label(tab4, textvariable=loan_text).grid(row=13, column=0, columnspan=2)
tk.Button(tab4, text="List Loaned Copies", command=list_loaned_copies).grid(row=14, column=0, columnspan=2)

# ... (similar structure for List Loaned Copies)

# Tab 5: List Late Loans
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text='List Late Loans')

start_date_entry = tk.Entry(tab5)
start_date_entry.grid(row=15, column=1)
tk.Label(tab5, text="Start Date").grid(row=15, column=0)

end_date_entry = tk.Entry(tab5)
end_date_entry.grid(row=16, column=1)
tk.Label(tab5, text="End Date").grid(row=16, column=0)

late_loan_text = tk.StringVar()
tk.Label(tab5, textvariable=late_loan_text).grid(row=17, column=0, columnspan=2)
tk.Button(tab5, text="List Late Loans", command=list_late_loans).grid(row=18, column=0, columnspan=2)

# ... (similar structure for List Late Loans)

# Tab 6: List Late Fee Balance
tab6 = ttk.Frame(notebook)
notebook.add(tab6, text='List Late Fee Balance')

vname_entry = tk.Entry(tab6)
vname_entry.grid(row= 19, column=1)
tk.Label(tab6, text="Borrower Name").grid(row=19, column=0)

vCard_entry = tk.Entry(tab6)
vCard_entry.grid(row= 20, column=1)
tk.Label(tab6, text="Card Number").grid(row=20, column=0)

tk.Button(tab6, text="List Late fees", command= list_lateFee_Balance).grid(row=21, column=0, columnspan=2)


late_fee_balance_text = tk.StringVar()
tk.Label(tab6, textvariable=late_fee_balance_text).grid(row=22, column=0, columnspan=2)

# ... (similar structure for List Late Fee Balance)

# Tab 7: List Book Info View
tab7 = ttk.Frame(notebook)
notebook.add(tab7, text='List Book Info View')

vBook_Card_Entry = tk.Entry(tab7)
vBook_Card_Entry.grid(row=0, column=1)
tk.Label(tab7, text= "Card No").grid(row=0,column=0)

vBook_ID_Entry = tk.Entry(tab7)
vBook_ID_Entry.grid(row=1, column=1)
tk.Label(tab7, text= "Book ID").grid(row=1,column=0)

vBook_Title_Entry = tk.Entry(tab7)
vBook_Title_Entry.grid(row=2, column=1)
tk.Label(tab7, text= "Book Title").grid(row=2,column=0)

tk.Button(tab7, text="List Book Info", command= list_bookInfo_view).grid(row=3, column=0, columnspan=2)

vBookInfo_text = tk.StringVar()
tk.Label(tab7, textvariable=vBookInfo_text).grid(row=4, column=0, columnspan=2)

# ... (similar structure for List Book Info View)

# Start the Tkinter event loop
root.mainloop()
-- sqlite

-- Create the table for PUBLISHER
DROP TABLE IF EXISTS PUBLISHER;
CREATE TABLE PUBLISHER (
    Publisher_Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    PRIMARY KEY (Publisher_Name)
);


-- Create the table for LIBRARY_BRANCH
DROP TABLE IF EXISTS LIBRARY_BRANCH;
CREATE TABLE LIBRARY_BRANCH (
    Branch_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Branch_Name VARCHAR(100) NOT NULL,
    Branch_Address VARCHAR(100) NOT NULL,
    Late_Fee INTEGER
);


-- Create the table for BORROWER
DROP TABLE IF EXISTS BORROWER;
CREATE TABLE BORROWER (
    Card_No INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    Phone VARCHAR(20) NOT NULL
);


-- Create the table for BOOK
DROP TABLE IF EXISTS BOOK;
CREATE TABLE BOOK (
    Book_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(100) NOT NULL,
    Publisher_Name VARCHAR(100) NOT NULL,
    FOREIGN KEY (Publisher_Name) REFERENCES PUBLISHER
);


-- Create the table for BOOK_LOANS
DROP TABLE IF EXISTS BOOK_LOANS;
CREATE TABLE BOOK_LOANS (
    Book_Id INT NOT NULL,
    Branch_Id INT NOT NULL,
    Card_No INT NOT NULL,
    Date_Out DATE NOT NULL,
    Due_Date DATE NOT NULL,
    Returned_date DATE,
    Late BOOLEAN,
    FOREIGN KEY (Book_Id) REFERENCES BOOK,
    FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH,
    FOREIGN KEY (Card_No) REFERENCES BORROWER
);



-- Create the table for BOOK_COPIES
DROP TABLE IF EXISTS BOOK_COPIES;
CREATE TABLE BOOK_COPIES (
    Book_Id INT NOT NULL,
    Branch_Id INT NOT NULL,
    No_Of_Copies INT NOT NULL,
    FOREIGN KEY (Book_Id) REFERENCES BOOK,
    FOREIGN KEY (Branch_Id) REFERENCES LIBRARY_BRANCH
);


-- Create the table for BOOK_AUTHORS
DROP TABLE IF EXISTS BOOK_AUTHORS;
CREATE TABLE BOOK_AUTHORS (
    Book_Id INT NOT NULL,
    Author_Name VARCHAR(100) NOT NULL,
    PRIMARY KEY (Book_Id, Author_Name),
    FOREIGN KEY (Book_Id) REFERENCES BOOK
);

DROP TRIGGER IF EXISTS Borrowing_Book;
CREATE TRIGGER Borrowing_Book
BEFORE INSERT ON BOOK_LOANS
FOR EACH ROW

BEGIN
UPDATE BOOK_COPIES
SET No_Of_Copies = No_Of_Copies - 1
WHERE NEW.Book_Id = BOOK_COPIES.Book_Id;

END;
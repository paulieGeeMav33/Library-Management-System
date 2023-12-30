-- SQLite
--DROP VIEW IF EXISTS vBookLoanInfo;
/*CREATE VIEW vBookLoanInfo AS
SELECT Br.Card_No, Br.Name, BL.Date_Out,BL.Due_Date,BL.Returned_date, 
julianday(Returned_date) - julianday(Date_Out) AS TotalDays,
Bk.Title,LB.Branch_Id,
IFNULL(julianday(Returned_date) - julianday(Due_Date) , 0) AS DaysReturnedLate,
IIF(BL.Returned_Date <= BL.Due_Date, 0, (LB.Late_Fee * (julianday(Returned_date)- julianday(Due_Date) ))) AS LateFeeBalance
FROM BORROWER Br JOIN BOOK_LOANS BL ON BL.Card_No = Br.Card_No
Join BOOK Bk ON Bk.Book_Id = BL.Book_Id*/

CREATE VIEW vBookLoanInfo AS 
SELECT 
  Br.Card_No, 
  Br.Name, 
  BL.Date_Out,
  BL.Due_Date,
  BL.Returned_date,  
  julianday(BL.Returned_date) - julianday(BL.Date_Out) AS TotalDays, 
  Bk.Title,
  BL.Branch_Id, 
  MAX(julianday(BL.Returned_date) - julianday(BL.Due_Date), 0) AS DaysReturnedLate,  
  CASE 
    WHEN BL.Returned_Date <= BL.Due_Date THEN 0 
    ELSE LB.Late_Fee * (julianday(BL.Returned_date) - julianday(BL.Due_Date))
  END AS LateFeeBalance 
FROM BORROWER Br 
JOIN BOOK_LOANS BL ON Br.Card_No = BL.Card_No 
JOIN BOOK Bk ON Bk.Book_Id = BL.Book_Id 
JOIN LIBRARY_BRANCH LB ON LB.Branch_Id = BL.Branch_Id;

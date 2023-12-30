-- SQLite



UPDATE BOOK_LOANS
SET Late = TRUE
WHERE julianday(Due_Date) - julianday(Returned_date) < 0;
UPDATE BOOK_LOANS
SET Late = FALSE
WHERE julianday(Due_Date) - julianday(Returned_date) >= 0 OR Returned_date = "NULL";

UPDATE LIBRARY_BRANCH
SET Late_Fee = 20;


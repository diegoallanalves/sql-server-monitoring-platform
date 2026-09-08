/*====================================================================
  STEP 3 - GENERATE A REALISTIC TEST DATASET
====================================================================

The data was generated from Python and inserted into SQL Server.
Observed lab totals:

Customers  : 5,000
Products   : 500
Orders     : 50,000
OrderItems : 124,634

Why generate this volume?
-------------------------
Performance problems become easier to demonstrate when tables contain
many rows. A query that appears instant on 10 rows may behave very
differently on 50,000+ rows.

Verify the generated dataset with the SQL below.
====================================================================*/

USE DBA_Performance_Lab;
GO

SELECT COUNT(*) AS Customers FROM Customers;
SELECT COUNT(*) AS Products FROM Products;
SELECT COUNT(*) AS Orders FROM Orders;
SELECT COUNT(*) AS OrderItems FROM OrderItems;

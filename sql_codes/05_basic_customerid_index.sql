/*====================================================================
  STEP 5 - BASIC NONCLUSTERED INDEX

  Goal: make CustomerID searchable without scanning the entire Orders
  table.
====================================================================*/

USE DBA_Performance_Lab;
GO

CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders(CustomerID);
GO

SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Status
FROM Orders
WHERE CustomerID = 2500;

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;

/*
Expected learning point:
The optimizer can use an Index Seek on CustomerID, but because the query
also asks for OrderDate and Status, SQL Server may perform a Key Lookup
against the clustered index to fetch those missing columns.

Our lab showed:
    Index Seek -> Key Lookup
*/

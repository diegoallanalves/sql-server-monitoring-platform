/*====================================================================
  STEP 6 - COVERING INDEX OPTIMIZATION

  Goal: remove the Key Lookup by storing the additional query columns
  inside the nonclustered index.
====================================================================*/

USE DBA_Performance_Lab;
GO

DROP INDEX IX_Orders_CustomerID ON Orders;
GO

CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders(CustomerID)
INCLUDE (
    OrderDate,
    Status
);
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
Observed result in the lab:
    Index Seek (NonClustered)

The previous Key Lookup disappeared.

Why is OrderID still available?
The clustered key is automatically carried in a nonclustered index in
this SQL Server design, so the query can be covered by the index.
*/

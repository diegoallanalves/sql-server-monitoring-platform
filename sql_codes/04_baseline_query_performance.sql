/*====================================================================
  STEP 4 - BASELINE QUERY PERFORMANCE

  Goal: measure the query BEFORE adding the useful CustomerID index.
  In SSMS, press Ctrl+M before execution to include the Actual
  Execution Plan.
====================================================================*/

USE DBA_Performance_Lab;
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
What to inspect:
- Messages -> logical reads and execution time.
- Execution plan -> initially SQL Server may scan the Orders structure
  because CustomerID has no dedicated search index.

In our lab the pre-optimization plan showed a Clustered Index Scan.
*/

/*====================================================================
  STEP 7 - MULTI-TABLE JOIN PERFORMANCE ANALYSIS

  Goal: analyze a more realistic business query joining all four tables.
  Press Ctrl+M before execution to capture the Actual Execution Plan.
====================================================================*/

USE DBA_Performance_Lab;
GO

SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT TOP 100
    c.CustomerID,
    c.CustomerName,
    o.OrderID,
    o.OrderDate,
    o.Status,
    p.ProductName,
    p.Category,
    oi.Quantity,
    oi.UnitPrice,
    (oi.Quantity * oi.UnitPrice) AS LineTotal
FROM Customers AS c
INNER JOIN Orders AS o
    ON c.CustomerID = o.CustomerID
INNER JOIN OrderItems AS oi
    ON o.OrderID = oi.OrderID
INNER JOIN Products AS p
    ON oi.ProductID = p.ProductID
ORDER BY o.OrderDate DESC;

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;

/*
Observed in our execution plan:
- OrderItems contained 124,634 rows.
- SQL Server showed a Clustered Index Scan on OrderItems.
- The plan displayed a Missing Index recommendation with an estimated
  impact of about 25.93% for an index on OrderItems(OrderID), including
  ProductID, Quantity and UnitPrice.

Important DBA lesson:
Do not blindly create every missing-index suggestion. Understand the
query and workload first. Here it makes sense because OrderID is the
JOIN key and the included columns are required by the query.
*/

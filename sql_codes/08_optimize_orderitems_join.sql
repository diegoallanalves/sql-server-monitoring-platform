/*====================================================================
  STEP 8 - OPTIMIZE THE ORDERITEMS JOIN

  Goal: give SQL Server an efficient index for locating the OrderItems
  belonging to an OrderID while also carrying the columns required by
  the reporting query.
====================================================================*/

USE DBA_Performance_Lab;
GO

CREATE NONCLUSTERED INDEX IX_OrderItems_OrderID
ON OrderItems(OrderID)
INCLUDE (
    ProductID,
    Quantity,
    UnitPrice
);
GO

/* Re-run the JOIN to let SQL Server choose the new access path. */
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
Compare the new Actual Execution Plan and STATISTICS IO/TIME against
Step 7. The optimizer is free to choose the cheapest plan; an index does
not guarantee a Seek for every workload.
*/

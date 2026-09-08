USE DBA_Performance_Lab;
GO

/* STEP 2A - Inspect the data. */
SELECT TOP 20 * FROM Customers;
SELECT TOP 20 * FROM Products;
SELECT TOP 20 * FROM Orders;
SELECT TOP 20 * FROM OrderItems;

SELECT COUNT(*) AS TotalCustomers FROM Customers;
SELECT COUNT(*) AS TotalProducts FROM Products;
SELECT COUNT(*) AS TotalOrders FROM Orders;
SELECT COUNT(*) AS TotalOrderItems FROM OrderItems;

/*
STEP 2B - OPTIONAL CLEANUP
WARNING: The statements below DELETE ALL LAB DATA.
Only run them when you intentionally want to regenerate the dataset.
Child tables must be deleted first because of Foreign Keys.
*/

/*
DELETE FROM OrderItems;
DELETE FROM Orders;
DELETE FROM Products;
DELETE FROM Customers;

DBCC CHECKIDENT ('OrderItems', RESEED, 0);
DBCC CHECKIDENT ('Orders', RESEED, 0);
DBCC CHECKIDENT ('Products', RESEED, 0);
DBCC CHECKIDENT ('Customers', RESEED, 0);

PRINT 'Database cleaned successfully.';
*/

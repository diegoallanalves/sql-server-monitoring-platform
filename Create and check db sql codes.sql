/*====================================================================
    PROJECT: DBA Performance Lab
    DATABASE: Microsoft SQL Server

    PURPOSE:
        Practical SQL Server laboratory covering:

        - Relational database design
        - Primary Keys and Foreign Keys
        - Data integrity
        - Database population
        - SQL performance analysis
        - Execution plans
        - Query tuning
        - Nonclustered indexes
        - Covering indexes
        - Data modelling
        - VLDB (Very Large Database) concepts

    RELATIONSHIPS:

        Customers
            |
            | 1 : MANY
            v
        Orders
            |
            | 1 : MANY
            v
        OrderItems
            ^
            | MANY : 1
            |
        Products

====================================================================*/


/*====================================================================
    STEP 1 - CREATE DATABASE
====================================================================*/

CREATE DATABASE DBA_Performance_Lab;
GO

USE DBA_Performance_Lab;
GO


/*====================================================================
    STEP 2 - CREATE CUSTOMERS TABLE
====================================================================*/

CREATE TABLE Customers (

    -- BIGINT supports very large integer values.
    --
    -- IDENTITY(1,1) automatically generates IDs:
    -- 1, 2, 3, 4...
    --
    -- PRIMARY KEY uniquely identifies each customer.

    CustomerID BIGINT IDENTITY(1,1) PRIMARY KEY,

    -- Customer name is mandatory.
    CustomerName VARCHAR(150) NOT NULL,

    -- Email is mandatory and cannot be duplicated.
    Email VARCHAR(255) NOT NULL UNIQUE,

    -- Optional country.
    Country VARCHAR(50),

    -- Automatically records creation date/time.
    CreatedAt DATETIME2 DEFAULT GETDATE()
);
GO


/*====================================================================
    STEP 3 - CREATE PRODUCTS TABLE
====================================================================*/

CREATE TABLE Products (

    ProductID BIGINT IDENTITY(1,1) PRIMARY KEY,

    ProductName VARCHAR(200) NOT NULL,

    Category VARCHAR(100),

    -- DECIMAL(12,2):
    -- Up to 12 digits total, with 2 decimal places.

    Price DECIMAL(12,2) NOT NULL
);
GO


/*====================================================================
    STEP 4 - CREATE ORDERS TABLE
====================================================================*/

CREATE TABLE Orders (

    OrderID BIGINT IDENTITY(1,1) PRIMARY KEY,

    -- Identifies the customer who placed the order.
    CustomerID BIGINT NOT NULL,

    -- Uses current date/time when no value is provided.
    OrderDate DATETIME2 DEFAULT GETDATE(),

    -- Example:
    -- Completed
    -- Pending
    -- Cancelled

    Status VARCHAR(30),

    /*--------------------------------------------------------------
        FOREIGN KEY
        Orders -> Customers
    --------------------------------------------------------------*/

    CONSTRAINT FK_Orders_Customers
        FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID)
);
GO


/*
    RELATIONSHIP:

        Customers
            |
            | 1
            |
            | MANY
            v
        Orders

    One customer can have many orders.

    Every CustomerID stored in Orders must reference an existing
    customer.

    This helps enforce REFERENTIAL INTEGRITY.
*/


/*====================================================================
    STEP 5 - CREATE ORDER ITEMS TABLE
====================================================================*/

CREATE TABLE OrderItems (

    OrderItemID BIGINT IDENTITY(1,1) PRIMARY KEY,

    OrderID BIGINT NOT NULL,

    ProductID BIGINT NOT NULL,

    Quantity INT NOT NULL,

    -- Stores the product price at the time of purchase.
    UnitPrice DECIMAL(12,2) NOT NULL,

    /*--------------------------------------------------------------
        FOREIGN KEY
        OrderItems -> Orders
    --------------------------------------------------------------*/

    CONSTRAINT FK_OrderItems_Orders
        FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID),

    /*--------------------------------------------------------------
        FOREIGN KEY
        OrderItems -> Products
    --------------------------------------------------------------*/

    CONSTRAINT FK_OrderItems_Products
        FOREIGN KEY (ProductID)
        REFERENCES Products(ProductID)
);
GO


/*
    COMPLETE DATA MODEL:

    CUSTOMERS
    ----------------
    CustomerID (PK)
         |
         | 1 : MANY
         v
    ORDERS
    ----------------
    OrderID (PK)
    CustomerID (FK)
         |
         | 1 : MANY
         v
    ORDER ITEMS
    ----------------
    OrderItemID (PK)
    OrderID (FK)
    ProductID (FK)
         |
         | MANY : 1
         v
    PRODUCTS
    ----------------
    ProductID (PK)


    PK = Primary Key
    FK = Foreign Key
*/


/*====================================================================
    STEP 6 - VIEW TABLE DATA
====================================================================*/

SELECT *
FROM Customers;

SELECT *
FROM Products;

SELECT *
FROM Orders;

SELECT *
FROM OrderItems;


/*====================================================================
    STEP 7 - VIEW A SAMPLE OF ORDERS
====================================================================*/

-- TOP prevents SQL Server from returning the entire table.
-- This becomes increasingly important as the database grows.

SELECT TOP 20 *
FROM Orders;


/*====================================================================
    STEP 8 - CHECK NUMBER OF RECORDS
====================================================================*/

SELECT COUNT(*) AS TotalCustomers
FROM Customers;

SELECT COUNT(*) AS TotalProducts
FROM Products;

SELECT COUNT(*) AS TotalOrders
FROM Orders;

SELECT COUNT(*) AS TotalOrderItems
FROM OrderItems;


/*====================================================================
    STEP 9 - OPTIONAL DATABASE CLEANUP

    WARNING:
    Run this section ONLY when you intentionally want to remove
    the generated test data.
====================================================================*/

USE DBA_Performance_Lab;
GO

-- Child tables must be cleared before parent tables because
-- Foreign Key relationships exist.

DELETE FROM OrderItems;
DELETE FROM Orders;
DELETE FROM Products;
DELETE FROM Customers;


-- Reset IDENTITY values back to zero.
-- The next generated ID will therefore start at 1.

DBCC CHECKIDENT ('OrderItems', RESEED, 0);
DBCC CHECKIDENT ('Orders', RESEED, 0);
DBCC CHECKIDENT ('Products', RESEED, 0);
DBCC CHECKIDENT ('Customers', RESEED, 0);

PRINT 'Database cleaned successfully.';
GO


/*====================================================================
    STEP 10 - VERIFY DATABASE COUNTS
====================================================================*/

SELECT COUNT(*) AS Customers
FROM Customers;

SELECT COUNT(*) AS Products
FROM Products;

SELECT COUNT(*) AS Orders
FROM Orders;

SELECT COUNT(*) AS OrderItems
FROM OrderItems;


/*====================================================================
    STEP 11 - PERFORMANCE TEST BEFORE INDEXING

    PURPOSE:
        Measure how SQL Server retrieves orders for one customer
        before creating a useful index.

    TEST DATABASE:
        5,000 Customers
        500 Products
        50,000 Orders
        124,634 OrderItems

    TEST:
        Find orders belonging to CustomerID 2500.

    OBSERVED BEFORE OPTIMIZATION:
        Rows returned: 7
        Logical reads: 283
        Execution plan: Clustered Index Scan

    INTERPRETATION:
        SQL Server does not currently have an index designed to
        search Orders efficiently by CustomerID.

        It therefore scans the clustered structure looking for
        matching records.
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


/*====================================================================
    STEP 12 - FIRST QUERY OPTIMIZATION

    CREATE A NONCLUSTERED INDEX ON CustomerID

    PURPOSE:
        CustomerID is used in the WHERE condition:

            WHERE CustomerID = 2500

        Creating an index allows SQL Server to locate matching
        CustomerID values directly rather than scanning the
        clustered index.
====================================================================*/

CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders(CustomerID);
GO


/*====================================================================
    STEP 13 - TEST PERFORMANCE AFTER BASIC INDEX
====================================================================*/

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
    OBSERVED EXECUTION PLAN:

        Index Seek (NonClustered)
                 |
                 v
            Key Lookup
                 |
                 v
           Nested Loops


    IMPROVEMENT:

        BEFORE:
            Clustered Index Scan

        AFTER:
            Nonclustered Index Seek


    SQL Server can now efficiently locate CustomerID = 2500.


    HOWEVER:

        The execution plan also contains a Key Lookup.

        The index currently contains CustomerID, but the query
        also needs:

            OrderDate
            Status

        SQL Server therefore uses the nonclustered index to find
        the matching records and then accesses the clustered
        index to retrieve the additional columns.

        In our execution plan, the Key Lookup represented a large
        proportion of the estimated query cost.

        We can improve this further with a COVERING INDEX.
*/


/*====================================================================
    STEP 14 - CREATE A COVERING INDEX

    IMPORTANT:
        This is the NEXT section to execute.

    PURPOSE:
        Eliminate the Key Lookup by storing the additional columns
        required by the query inside the nonclustered index.
====================================================================*/


-- First remove the basic index created during the previous experiment.

DROP INDEX IX_Orders_CustomerID
ON Orders;
GO


-- Recreate the index as a covering index.
--
-- CustomerID:
-- Used to search/filter the data.
--
-- INCLUDE:
-- Stores additional columns at the leaf level of the index so
-- SQL Server can return them without performing a Key Lookup.

CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders(CustomerID)
INCLUDE (
    OrderDate,
    Status
);
GO


/*
    Why isn't OrderID explicitly included?

    OrderID is the clustered Primary Key of Orders.

    SQL Server includes the clustered key as the row locator in
    nonclustered indexes, so it can already be available to satisfy
    this query.
*/


/*====================================================================
    STEP 15 - TEST THE COVERING INDEX
====================================================================*/

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
    EXPECTED EXECUTION PLAN:

            Index Seek (NonClustered)
                     |
                     v
                   SELECT


    The Key Lookup should disappear because the index now contains
    the columns needed by this query.


    ================================================================
                    QUERY TUNING COMPARISON
    ================================================================

    STAGE 1 - NO CUSTOMER INDEX

        Clustered Index Scan

        Observed:
        283 logical reads
        7 rows returned


    STAGE 2 - BASIC NONCLUSTERED INDEX

        Index Seek
             +
        Key Lookup

        Improvement:
        SQL Server can efficiently locate CustomerID.

        Remaining problem:
        Additional columns must be retrieved from the clustered
        index.


    STAGE 3 - COVERING NONCLUSTERED INDEX

        Index Seek

        Expected improvement:
        Key Lookup eliminated.
        Fewer data-page accesses.
        More efficient query execution.


    This demonstrates an important DBA/query-tuning workflow:

        1. Identify a query
        2. Measure performance
        3. Examine the execution plan
        4. Identify scans/lookups
        5. Create an appropriate index
        6. Measure again
        7. Refine the index
        8. Compare before vs after

====================================================================*/
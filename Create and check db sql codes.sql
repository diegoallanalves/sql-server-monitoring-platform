/*====================================================================
    PROJECT: DBA Performance Lab
    DATABASE: Microsoft SQL Server
    PURPOSE:
        Learn SQL Server database administration, relational modelling,
        query tuning, indexing, performance and VLDB concepts.

    TABLE RELATIONSHIPS:

        Customers
            |
            | 1 : Many
            v
        Orders
            |
            | 1 : Many
            v
        OrderItems
            ^
            | Many : 1
            |
        Products

====================================================================*/


/*====================================================================
    STEP 1 - CREATE THE DATABASE
====================================================================*/

-- Creates a new SQL Server database called DBA_Performance_Lab.
CREATE DATABASE DBA_Performance_Lab;
GO


-- Changes the current database context.
-- All commands after this point will run against DBA_Performance_Lab.
USE DBA_Performance_Lab;
GO



/*====================================================================
    STEP 2 - CREATE CUSTOMERS TABLE
====================================================================*/

CREATE TABLE Customers (

    -- Unique identifier for each customer.
    --
    -- BIGINT:
    -- Allows very large integer values.
    --
    -- IDENTITY(1,1):
    -- SQL Server automatically generates the number.
    -- Starts at 1 and increases by 1.
    --
    -- PRIMARY KEY:
    -- Uniquely identifies every customer.

    CustomerID BIGINT IDENTITY(1,1) PRIMARY KEY,


    -- Customer name is required.
    -- VARCHAR(150) allows up to 150 characters.
    --
    -- NOT NULL means the value cannot be empty.

    CustomerName VARCHAR(150) NOT NULL,


    -- Email is mandatory.
    --
    -- UNIQUE prevents two customers from having
    -- the same email address.

    Email VARCHAR(255) NOT NULL UNIQUE,


    -- Country is optional because we haven't specified NOT NULL.

    Country VARCHAR(50),


    -- Automatically records when the customer was created.
    --
    -- DATETIME2 stores date + time.
    -- GETDATE() returns the current date/time.

    CreatedAt DATETIME2 DEFAULT GETDATE()
);



/*====================================================================
    STEP 3 - CREATE PRODUCTS TABLE
====================================================================*/

CREATE TABLE Products (

    -- Automatically generated Product ID.

    ProductID BIGINT IDENTITY(1,1) PRIMARY KEY,


    -- Product name is mandatory.

    ProductName VARCHAR(200) NOT NULL,


    -- Product category is optional.

    Category VARCHAR(100),


    -- DECIMAL(12,2) means:
    --
    -- Maximum 12 digits in total
    -- 2 digits after the decimal point.
    --
    -- Example:
    -- 4500.99

    Price DECIMAL(12,2) NOT NULL
);



/*====================================================================
    STEP 4 - CREATE ORDERS TABLE
====================================================================*/

CREATE TABLE Orders (

    -- Unique ID for every order.

    OrderID BIGINT IDENTITY(1,1) PRIMARY KEY,


    -- Identifies which customer made the order.
    --
    -- This will become a FOREIGN KEY.

    CustomerID BIGINT NOT NULL,


    -- Automatically records the order date/time
    -- if one isn't provided.

    OrderDate DATETIME2 DEFAULT GETDATE(),


    -- Example values:
    -- Completed
    -- Pending
    -- Cancelled

    Status VARCHAR(30),


    /*--------------------------------------------------------------
        FOREIGN KEY CONSTRAINT
    --------------------------------------------------------------*/

    -- We give the relationship a meaningful name:
    -- FK_Orders_Customers

    CONSTRAINT FK_Orders_Customers

        FOREIGN KEY (CustomerID)

        REFERENCES Customers(CustomerID)
);


/*
    This relationship means:

        Customers
            |
            | CustomerID
            |
            | 1
            |
            | MANY
            v
        Orders


    One customer can have MANY orders.

    But every order must reference an existing customer.

    This is called REFERENTIAL INTEGRITY.
*/



/*====================================================================
    STEP 5 - CREATE ORDER ITEMS TABLE
====================================================================*/

CREATE TABLE OrderItems (

    -- Unique identifier for each order line.

    OrderItemID BIGINT IDENTITY(1,1) PRIMARY KEY,


    -- Identifies the order.

    OrderID BIGINT NOT NULL,


    -- Identifies the product.

    ProductID BIGINT NOT NULL,


    -- Number of units purchased.

    Quantity INT NOT NULL,


    -- We store the price at the moment the order was made.
    --
    -- This is important because the current product price
    -- could change in the future.

    UnitPrice DECIMAL(12,2) NOT NULL,


    /*--------------------------------------------------------------
        RELATIONSHIP 1
        OrderItems -> Orders
    --------------------------------------------------------------*/

    CONSTRAINT FK_OrderItems_Orders

        FOREIGN KEY (OrderID)

        REFERENCES Orders(OrderID),


    /*--------------------------------------------------------------
        RELATIONSHIP 2
        OrderItems -> Products
    --------------------------------------------------------------*/

    CONSTRAINT FK_OrderItems_Products

        FOREIGN KEY (ProductID)

        REFERENCES Products(ProductID)
);



/*
    Our complete relational model is now:


    CUSTOMERS
    ----------
    CustomerID (PK)
         |
         |
         | 1 : MANY
         |
         v
    ORDERS
    ----------
    OrderID (PK)
    CustomerID (FK)
         |
         |
         | 1 : MANY
         |
         v
    ORDER ITEMS
    ----------
    OrderItemID (PK)
    OrderID (FK)
    ProductID (FK)
         |
         |
         | MANY : 1
         |
         v
    PRODUCTS
    ----------
    ProductID (PK)


    PK = Primary Key
    FK = Foreign Key
*/



/*====================================================================
    STEP 6 - VIEW THE DATA
====================================================================*/

-- Show all customers.
SELECT *
FROM Customers;


-- Show all products.
SELECT *
FROM Products;


-- Show all orders.
SELECT *
FROM Orders;


-- Show all order items.
SELECT *
FROM OrderItems;



/*====================================================================
    STEP 7 - VIEW ONLY A SAMPLE OF ORDERS
====================================================================*/

-- TOP 20 prevents SQL Server from returning every row.
--
-- This becomes particularly important later when our Orders table
-- contains hundreds of thousands or millions of records.

SELECT TOP 20 *
FROM Orders;



/*====================================================================
    STEP 8 - COUNT THE RECORDS
====================================================================*/

-- Count customers.

SELECT COUNT(*) AS TotalCustomers
FROM Customers;


-- Count products.

SELECT COUNT(*) AS TotalProducts
FROM Products;


-- Count orders.

SELECT COUNT(*) AS TotalOrders
FROM Orders;


-- Count order items.

SELECT COUNT(*) AS TotalOrderItems
FROM OrderItems;
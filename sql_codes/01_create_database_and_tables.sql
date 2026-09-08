/*====================================================================
  STEP 1 - CREATE DATABASE AND RELATIONAL MODEL
====================================================================*/

CREATE DATABASE DBA_Performance_Lab;
GO

USE DBA_Performance_Lab;
GO

/* Customers: one customer can have many orders. */
CREATE TABLE Customers (
    CustomerID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CustomerName VARCHAR(150) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Country VARCHAR(50),
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

/* Products: master list of products. */
CREATE TABLE Products (
    ProductID BIGINT IDENTITY(1,1) PRIMARY KEY,
    ProductName VARCHAR(200) NOT NULL,
    Category VARCHAR(100),
    Price DECIMAL(12,2) NOT NULL
);

/* Orders: each order must belong to an existing customer. */
CREATE TABLE Orders (
    OrderID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CustomerID BIGINT NOT NULL,
    OrderDate DATETIME2 DEFAULT GETDATE(),
    Status VARCHAR(30),
    CONSTRAINT FK_Orders_Customers
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

/* OrderItems: line-level products belonging to an order. */
CREATE TABLE OrderItems (
    OrderItemID BIGINT IDENTITY(1,1) PRIMARY KEY,
    OrderID BIGINT NOT NULL,
    ProductID BIGINT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(12,2) NOT NULL,
    CONSTRAINT FK_OrderItems_Orders
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    CONSTRAINT FK_OrderItems_Products
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

/*
Relationship model:

Customers 1 ---- many Orders 1 ---- many OrderItems many ---- 1 Products

Primary Keys uniquely identify rows.
Foreign Keys enforce referential integrity between related tables.
*/

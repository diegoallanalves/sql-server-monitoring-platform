DBA PERFORMANCE LAB - SQL SERVER
================================

Purpose
-------
This learning project demonstrates practical SQL Server DBA and query-performance skills using Microsoft SQL Server Management Studio (SSMS) and Python-generated test data.

Learning sequence
-----------------
01_create_database_and_tables.sql
    Creates the database and relational model: Customers -> Orders -> OrderItems <- Products.

02_check_and_clean_data.sql
    Shows how to inspect row counts and, when needed, clean/reset the lab tables. WARNING: the cleanup section deletes data.

03_generate_test_data_notes.sql
    Documents the test dataset generated with Python: 5,000 customers, 500 products, 50,000 orders and about 124,634 order items.

04_baseline_query_performance.sql
    Measures a customer-order lookup with STATISTICS IO/TIME before optimization.

05_basic_customerid_index.sql
    Adds a nonclustered index on Orders(CustomerID). This demonstrates moving from a table/index scan toward an Index Seek, but may still require a Key Lookup.

06_covering_index_optimization.sql
    Replaces the basic index with a covering index using INCLUDE(OrderDate, Status), eliminating the Key Lookup for the target query.

07_join_performance_analysis.sql
    Runs a realistic four-table JOIN and inspects its execution plan.

08_optimize_orderitems_join.sql
    Adds a covering index on OrderItems(OrderID) including ProductID, Quantity and UnitPrice to support the JOIN.

09_final_dba_health_checks.sql
    Runs DBCC CHECKDB, table row-count checks, index inventory and database-size checks.

Important concepts
------------------
PK = Primary Key
FK = Foreign Key
SGBD/DBMS = Database Management System
DBA = Database Administrator
Query tuning = improving how efficiently SQL Server executes queries
Index Seek = SQL Server navigates an index to locate required rows
Index Scan = SQL Server reads a larger portion/all of an index
Key Lookup = SQL Server finds rows in a nonclustered index, then returns to the clustered index for missing columns
Covering index = an index containing everything a particular query needs
STATISTICS IO = reports page reads performed by a query
STATISTICS TIME = reports CPU and elapsed execution time
Execution Plan = visual representation of how SQL Server executes a query

Recommended way to revisit the lab
-----------------------------------
Run the scripts in numeric order on a fresh lab database. Do not repeatedly run CREATE DATABASE, CREATE TABLE, or CREATE INDEX statements against an already-created lab unless the script explicitly handles the existing object.

The Python data generator used during the exercise connected to SQL Server and generated the synthetic rows. The SQL scripts in this package focus on the SQL Server/DBA learning sequence.

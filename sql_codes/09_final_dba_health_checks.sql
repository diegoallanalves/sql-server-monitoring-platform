/*====================================================================
  STEP 9 - FINAL DBA HEALTH CHECKS
====================================================================*/

USE DBA_Performance_Lab;
GO

/* 1. Integrity check: looks for allocation and consistency errors. */
DBCC CHECKDB ('DBA_Performance_Lab');
GO

/* Desired message:
   CHECKDB found 0 allocation errors and 0 consistency errors.
*/

/* 2. Table sizes / row counts. */
SELECT
    t.name AS TableName,
    SUM(p.rows) AS TotalRows
FROM sys.tables AS t
INNER JOIN sys.partitions AS p
    ON t.object_id = p.object_id
WHERE p.index_id IN (0,1)
GROUP BY t.name
ORDER BY TotalRows DESC;
GO

/* 3. Inventory the indexes currently defined in the database. */
SELECT
    t.name AS TableName,
    i.name AS IndexName,
    i.type_desc AS IndexType
FROM sys.tables AS t
INNER JOIN sys.indexes AS i
    ON t.object_id = i.object_id
WHERE i.name IS NOT NULL
ORDER BY t.name, i.name;
GO

/* 4. Inspect database data/log file sizes in MB. */
SELECT
    DB_NAME(database_id) AS DatabaseName,
    type_desc AS FileType,
    CAST(SUM(size) * 8.0 / 1024 AS DECIMAL(10,2)) AS SizeMB
FROM sys.master_files
WHERE database_id = DB_ID('DBA_Performance_Lab')
GROUP BY database_id, type_desc;
GO

/*
Project complete.
Skills demonstrated:
- SQL Server relational modelling
- Primary/Foreign Keys and referential integrity
- SQL performance measurement
- Actual Execution Plans
- Query tuning
- Nonclustered indexes
- Covering indexes / INCLUDE columns
- JOIN performance analysis
- Database integrity and metadata checks
*/

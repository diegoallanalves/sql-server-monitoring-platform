import pyodbc

SERVER = r"LAPTOP-HSERDTUR\SQLEXPRESS"
DATABASE = "DBA_Performance_Lab"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(connection_string)

    print("✅ Connected successfully!")
    print(f"Server: {SERVER}")
    print(f"Database: {DATABASE}")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            @@SERVERNAME AS ServerName,
            DB_NAME() AS DatabaseName,
            @@VERSION AS SQLServerVersion
    """)

    row = cursor.fetchone()

    print("\nSQL Server information:")
    print("Server:", row.ServerName)
    print("Database:", row.DatabaseName)
    print("Version:", row.SQLServerVersion)

    conn.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)
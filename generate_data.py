# ============================================================
# DBA PERFORMANCE LAB
# STEP 3 - GENERATE SAMPLE DATA
# ============================================================

import pyodbc
import random
from datetime import datetime, timedelta


# ============================================================
# 1. DATABASE CONNECTION SETTINGS
# ============================================================

SERVER = r"LAPTOP-HSERDTUR\SQLEXPRESS"
DATABASE = "DBA_Performance_Lab"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)


# ============================================================
# 2. CONNECT TO SQL SERVER
# ============================================================

conn = pyodbc.connect(connection_string)

cursor = conn.cursor()

# Makes bulk inserts faster.
cursor.fast_executemany = True

print("Connected to SQL Server.")


# ============================================================
# 3. CONFIGURATION
# ============================================================

NUM_CUSTOMERS = 5_000
NUM_PRODUCTS = 500
NUM_ORDERS = 50_000


countries = [
    "Brazil",
    "United Kingdom",
    "United States",
    "Germany",
    "France",
    "Spain",
    "Portugal",
    "Hungary",
    "Canada",
    "Australia"
]


categories = [
    "Electronics",
    "Furniture",
    "Clothing",
    "Sports",
    "Books",
    "Home",
    "Beauty",
    "Automotive"
]


statuses = [
    "Completed",
    "Pending",
    "Cancelled"
]


# ============================================================
# 4. GENERATE CUSTOMERS
# ============================================================

print("Generating customers...")

customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    name = f"Customer {i}"

    email = f"customer{i}@example.com"

    country = random.choice(countries)

    customers.append(
        (
            name,
            email,
            country
        )
    )


# Insert customers into SQL Server.
cursor.executemany(
    """
    INSERT INTO Customers
        (CustomerName, Email, Country)
    VALUES (?, ?, ?)
    """,
    customers
)

conn.commit()

print(f"{NUM_CUSTOMERS:,} customers inserted.")


# ============================================================
# 5. GENERATE PRODUCTS
# ============================================================

print("Generating products...")

products = []

for i in range(1, NUM_PRODUCTS + 1):

    product_name = f"Product {i}"

    category = random.choice(categories)

    price = round(
        random.uniform(10, 5000),
        2
    )

    products.append(
        (
            product_name,
            category,
            price
        )
    )


cursor.executemany(
    """
    INSERT INTO Products
        (ProductName, Category, Price)
    VALUES (?, ?, ?)
    """,
    products
)

conn.commit()

print(f"{NUM_PRODUCTS:,} products inserted.")


# ============================================================
# 6. GENERATE ORDERS
# ============================================================

print("Generating orders...")

orders = []

for i in range(NUM_ORDERS):

    customer_id = random.randint(
        1,
        NUM_CUSTOMERS
    )

    order_date = datetime.now() - timedelta(
        days=random.randint(0, 730)
    )

    status = random.choice(statuses)

    orders.append(
        (
            customer_id,
            order_date,
            status
        )
    )


cursor.executemany(
    """
    INSERT INTO Orders
        (CustomerID, OrderDate, Status)
    VALUES (?, ?, ?)
    """,
    orders
)

conn.commit()

print(f"{NUM_ORDERS:,} orders inserted.")


# ============================================================
# 7. READ THE ORDER IDS
# ============================================================

cursor.execute(
    """
    SELECT OrderID
    FROM Orders
    """
)

order_ids = [
    row.OrderID
    for row in cursor.fetchall()
]


# ============================================================
# 8. GENERATE ORDER ITEMS
# ============================================================

print("Generating order items...")

order_items = []


for order_id in order_ids:

    # Each order will contain between 1 and 4 products.
    number_of_items = random.randint(
        1,
        4
    )

    for _ in range(number_of_items):

        product_id = random.randint(
            1,
            NUM_PRODUCTS
        )

        quantity = random.randint(
            1,
            5
        )

        unit_price = round(
            random.uniform(10, 5000),
            2
        )

        order_items.append(
            (
                order_id,
                product_id,
                quantity,
                unit_price
            )
        )


cursor.executemany(
    """
    INSERT INTO OrderItems
        (
            OrderID,
            ProductID,
            Quantity,
            UnitPrice
        )
    VALUES (?, ?, ?, ?)
    """,
    order_items
)

conn.commit()


print(
    f"{len(order_items):,} order items inserted."
)


# ============================================================
# 9. CHECK THE FINAL RECORD COUNTS
# ============================================================

print("\nFinal database counts:")


tables = [
    "Customers",
    "Products",
    "Orders",
    "OrderItems"
]


for table in tables:

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM {table}
        """
    )

    count = cursor.fetchone()[0]

    print(
        f"{table}: {count:,}"
    )


# ============================================================
# 10. CLOSE THE CONNECTION
# ============================================================

cursor.close()
conn.close()

print("\nConnection closed.")
print("Data generation complete.")
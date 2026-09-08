# ============================================================
# DBA PERFORMANCE LAB
# SQL SERVER DATABASE HEALTH & PERFORMANCE COMMAND CENTER
#
# Stack:
# SQL Server + Python + pyodbc + Pandas + Streamlit + Plotly
# ============================================================

import pyodbc
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DBA Command Center",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   MAIN APPLICATION
   ========================================================== */

.stApp {
    background:
        radial-gradient(circle at top right, #13213b 0%, #090d16 38%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1800px;
}


/* ==========================================================
   HEADER
   ========================================================== */

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    margin-bottom: 0;
    letter-spacing: -0.04em;
}

.hero-subtitle {
    color: #8b9bb4;
    font-size: 0.95rem;
    margin-top: 3px;
}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 1.7rem;
    margin-bottom: .8rem;
}


/* ==========================================================
   HEALTH BANNER
   ========================================================== */

.health-banner {
    border: 1px solid rgba(49, 211, 137, .35);
    background: rgba(20, 112, 74, .18);
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 18px;
    margin-bottom: 18px;
}


/* ==========================================================
   INFORMATION CARDS
   ========================================================== */

.info-card {
    background: rgba(18, 25, 39, .82);
    border: 1px solid rgba(148, 163, 184, .16);
    border-radius: 14px;
    padding: 18px;
    min-height: 110px;
}

.info-label {
    color: #8492a6;
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .06em;
}

.info-value {
    font-size: 1.6rem;
    font-weight: 750;
    margin-top: 8px;
}

.info-small {
    color: #7f8da3;
    font-size: .78rem;
    margin-top: 4px;
}


/* ==========================================================
   ARCHITECTURE
   ========================================================== */

.architecture {
    background: rgba(14, 20, 32, .9);
    border: 1px solid rgba(148, 163, 184, .16);
    border-radius: 14px;
    padding: 20px;
    overflow-x: auto;
}


/* ==========================================================
   STREAMLIT METRICS
   ========================================================== */

[data-testid="stMetric"] {
    background: rgba(18, 25, 39, .8);
    border: 1px solid rgba(148, 163, 184, .14);
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stMetric"]:hover {
    border: 1px solid rgba(100, 180, 255, .35);
}


/* ==========================================================
   DATAFRAMES
   ========================================================== */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(148, 163, 184, .12);
    border-radius: 12px;
}


/* ==========================================================
   FOOTER
   ========================================================== */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. DATABASE CONFIGURATION
# ============================================================

SERVER = r"LAPTOP-HSERDTUR\SQLEXPRESS"
DATABASE = "DBA_Performance_Lab"


def get_connection():
    """
    Creates and returns a connection to SQL Server.

    Trusted_Connection=yes means Windows Authentication
    is being used.
    """

    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )

    return pyodbc.connect(connection_string)


def run_query(query):
    """
    Executes a SELECT query against SQL Server
    and returns the result as a Pandas DataFrame.
    """

    conn = get_connection()

    try:
        return pd.read_sql(query, conn)

    finally:
        conn.close()


# ============================================================
# 4. SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🗄️ DBA LAB")

    st.caption("SQL Server Monitoring")

    st.divider()

    st.markdown("### Environment")

    st.write("**Server**")
    st.code(SERVER)

    st.write("**Database**")
    st.code(DATABASE)

    st.divider()

    st.markdown("### Stack")

    st.write("🔹 SQL Server")
    st.write("🔹 Python")
    st.write("🔹 pyodbc")
    st.write("🔹 Pandas")
    st.write("🔹 Streamlit")
    st.write("🔹 Plotly")

    st.divider()

    if st.button(
        "🔄 Refresh Database",
        use_container_width=True
    ):
        st.rerun()

    st.caption(
        f"Last refresh\n"
        f"{datetime.now().strftime('%d %b %Y - %H:%M:%S')}"
    )


# ============================================================
# 5. CONNECTION TEST
# ============================================================

try:

    server_info = run_query("""
    SELECT
        @@SERVERNAME AS ServerName,
        DB_NAME() AS DatabaseName,
        @@VERSION AS SQLServerVersion;
    """)

except Exception as error:

    st.error("SQL Server connection failed.")

    st.exception(error)

    st.stop()


# ============================================================
# 6. HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">'
    'SQL Server Command Center'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Database Health • Performance • Storage • '
    'Indexing • Workload • Architecture'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 7. DATABASE STATUS
# ============================================================

database_status = run_query("""
SELECT
    name AS DatabaseName,
    state_desc AS DatabaseStatus,
    recovery_model_desc AS RecoveryModel,
    user_access_desc AS UserAccess
FROM sys.databases
WHERE name = 'DBA_Performance_Lab';
""")


status = database_status.iloc[0]["DatabaseStatus"]
recovery_model = database_status.iloc[0]["RecoveryModel"]
user_access = database_status.iloc[0]["UserAccess"]


# ============================================================
# 8. CORE COUNTS
# ============================================================

counts = run_query("""
SELECT
    (SELECT COUNT(*) FROM Customers) AS Customers,
    (SELECT COUNT(*) FROM Products) AS Products,
    (SELECT COUNT(*) FROM Orders) AS Orders,
    (SELECT COUNT(*) FROM OrderItems) AS OrderItems;
""")


customers = int(counts.iloc[0]["Customers"])
products = int(counts.iloc[0]["Products"])
orders = int(counts.iloc[0]["Orders"])
order_items = int(counts.iloc[0]["OrderItems"])


# ============================================================
# 9. INDEX INFORMATION
# ============================================================

indexes = run_query("""
SELECT
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    i.type_desc AS IndexType,
    i.is_unique AS IsUnique
FROM sys.indexes i
WHERE
    OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1
    AND i.name IS NOT NULL
ORDER BY
    TableName,
    IndexName;
""")


index_count = len(indexes)


# ============================================================
# 10. INDEX USAGE
# ============================================================

index_usage = run_query("""
SELECT
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,

    ISNULL(s.user_seeks, 0) AS UserSeeks,
    ISNULL(s.user_scans, 0) AS UserScans,
    ISNULL(s.user_lookups, 0) AS UserLookups,
    ISNULL(s.user_updates, 0) AS UserUpdates

FROM sys.indexes i

LEFT JOIN sys.dm_db_index_usage_stats s
    ON i.object_id = s.object_id
    AND i.index_id = s.index_id
    AND s.database_id = DB_ID()

WHERE
    OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1
    AND i.name IS NOT NULL

ORDER BY
    TableName,
    IndexName;
""")


# ============================================================
# 11. DATABASE STORAGE
# ============================================================

database_size = run_query("""
SELECT
    name AS FileName,

    CASE type
        WHEN 0 THEN 'DATA'
        WHEN 1 THEN 'LOG'
    END AS FileType,

    CAST(
        size * 8.0 / 1024
        AS DECIMAL(10,2)
    ) AS SizeMB

FROM sys.database_files;
""")


total_size = float(database_size["SizeMB"].sum())

data_size = float(
    database_size.loc[
        database_size["FileType"] == "DATA",
        "SizeMB"
    ].sum()
)

log_size = float(
    database_size.loc[
        database_size["FileType"] == "LOG",
        "SizeMB"
    ].sum()
)


# ============================================================
# 12. TABLE ROW COUNTS
# ============================================================

table_rows = run_query("""
SELECT
    t.name AS TableName,
    SUM(p.rows) AS TotalRows

FROM sys.tables t

INNER JOIN sys.partitions p
    ON t.object_id = p.object_id

WHERE
    p.index_id IN (0,1)

GROUP BY
    t.name

ORDER BY
    TotalRows DESC;
""")


# ============================================================
# 13. TABLE STORAGE
# ============================================================

table_storage = run_query("""
SELECT

    t.name AS TableName,

    SUM(p.rows) AS TotalRows,

    CAST(
        SUM(a.total_pages) * 8.0 / 1024
        AS DECIMAL(12,2)
    ) AS TotalSizeMB,

    CAST(
        SUM(a.used_pages) * 8.0 / 1024
        AS DECIMAL(12,2)
    ) AS UsedSizeMB

FROM sys.tables t

INNER JOIN sys.indexes i
    ON t.object_id = i.object_id

INNER JOIN sys.partitions p
    ON i.object_id = p.object_id
    AND i.index_id = p.index_id

INNER JOIN sys.allocation_units a
    ON p.partition_id = a.container_id

GROUP BY
    t.name

ORDER BY
    TotalSizeMB DESC;
""")


# ============================================================
# 14. ORDER STATUS
# ============================================================

order_status = run_query("""
SELECT
    ISNULL(Status, 'Unknown') AS Status,
    COUNT(*) AS TotalOrders

FROM Orders

GROUP BY
    Status

ORDER BY
    TotalOrders DESC;
""")


if not order_status.empty:

    order_status["Percentage"] = (
        order_status["TotalOrders"]
        / order_status["TotalOrders"].sum()
        * 100
    )


# ============================================================
# 15. ORDER ACTIVITY OVER TIME
# ============================================================

orders_over_time = run_query("""
SELECT
    CAST(OrderDate AS DATE) AS OrderDate,
    COUNT(*) AS TotalOrders

FROM Orders

GROUP BY
    CAST(OrderDate AS DATE)

ORDER BY
    OrderDate;
""")


# ============================================================
# 16. HEALTH SCORE
# ============================================================
#
# This is a LAB health score.
#
# It is NOT an official SQL Server health score.
#
# The idea is to demonstrate how monitoring rules can
# be translated into a simple operational score.
# ============================================================

health_score = 100

health_findings = []


# ------------------------------------------------------------
# DATABASE ONLINE CHECK
# ------------------------------------------------------------

if status != "ONLINE":

    health_score -= 60

    health_findings.append(
        "Database is not ONLINE."
    )


# ------------------------------------------------------------
# INDEX CHECK
# ------------------------------------------------------------

if index_count == 0:

    health_score -= 20

    health_findings.append(
        "No indexes detected."
    )


# ------------------------------------------------------------
# DATA CHECK
# ------------------------------------------------------------

if orders == 0:

    health_score -= 10

    health_findings.append(
        "Orders table contains no records."
    )


if customers == 0:

    health_score -= 10

    health_findings.append(
        "Customers table contains no records."
    )


# ------------------------------------------------------------
# LOG SIZE CHECK
# ------------------------------------------------------------

if data_size > 0:

    log_to_data_ratio = log_size / data_size

else:

    log_to_data_ratio = 0


if log_to_data_ratio > 3:

    health_score -= 10

    health_findings.append(
        "Transaction log is more than "
        "3x the size of the data file."
    )


health_score = max(
    0,
    min(100, health_score)
)


# ============================================================
# 17. HEALTH LABEL
# ============================================================

if health_score >= 90:

    health_label = "HEALTHY"
    health_icon = "🟢"

elif health_score >= 70:

    health_label = "WARNING"
    health_icon = "🟡"

else:

    health_label = "CRITICAL"
    health_icon = "🔴"


# ============================================================
# 18. HEALTH BANNER
# ============================================================


st.markdown(
    f"""
<div class="health-banner">
    <strong>{health_icon} DATABASE HEALTH: {health_label}</strong>
    &nbsp;&nbsp; | &nbsp;&nbsp;
    Health Score: <strong>{health_score}/100</strong>
    &nbsp;&nbsp; | &nbsp;&nbsp;
    Status: <strong>{status}</strong>
    &nbsp;&nbsp; | &nbsp;&nbsp;
    Recovery: <strong>{recovery_model}</strong>
    &nbsp;&nbsp; | &nbsp;&nbsp;
    Access: <strong>{user_access}</strong>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 19. MAIN KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "👥 Customers",
        f"{customers:,}"
    )


with col2:

    st.metric(
        "📦 Products",
        f"{products:,}"
    )


with col3:

    st.metric(
        "🧾 Orders",
        f"{orders:,}"
    )


with col4:

    st.metric(
        "🔗 Order Items",
        f"{order_items:,}"
    )


with col5:

    st.metric(
        "⚡ Indexes",
        f"{index_count:,}"
    )


# ============================================================
# 20. HEALTH OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">'
    'System Health Overview'
    '</div>',
    unsafe_allow_html=True
)


left, right = st.columns(
    [1, 2]
)


# ============================================================
# 21. HEALTH GAUGE
# ============================================================

with left:

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=health_score,

            number={
                "suffix": "/100",
                "font": {
                    "size": 42
                }
            },

            title={
                "text": "Database Health Score",
                "font": {
                    "size": 16
                }
            },

            gauge={

                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "thickness": 0.65
                },

                "steps": [

                    {
                        "range": [0, 60]
                    },

                    {
                        "range": [60, 85]
                    },

                    {
                        "range": [85, 100]
                    }

                ]
            }
        )
    )


    gauge.update_layout(

        height=300,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        }
    )


    st.plotly_chart(
        gauge,
        use_container_width=True
    )


# ============================================================
# 22. TABLE VOLUME
# ============================================================

with right:

    fig_tables = px.bar(

        table_rows,

        x="TotalRows",

        y="TableName",

        orientation="h",

        title="Table Volume",

        text="TotalRows"
    )


    fig_tables.update_traces(

        texttemplate="%{text:,}",

        textposition="outside",

        hovertemplate=(
            "<b>%{y}</b><br>"
            "Rows: %{x:,}"
            "<extra></extra>"
        )
    )


    fig_tables.update_layout(

        height=300,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        },

        yaxis={
            "categoryorder": "total ascending"
        },

        margin=dict(
            l=20,
            r=50,
            t=50,
            b=20
        )
    )


    st.plotly_chart(
        fig_tables,
        use_container_width=True
    )


# ============================================================
# 23. STORAGE & WORKLOAD
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Storage & Workload'
    '</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2)


# ============================================================
# 24. DATABASE STORAGE
# ============================================================

with left:

    storage_chart = px.pie(

        database_size,

        names="FileType",

        values="SizeMB",

        hole=.65,

        title=(
            f"Database Storage — "
            f"{total_size:.0f} MB"
        )
    )


    storage_chart.update_traces(

        textinfo="percent+label",

        hovertemplate=(
            "<b>%{label}</b><br>"
            "%{value:.2f} MB<br>"
            "%{percent}"
            "<extra></extra>"
        )
    )


    storage_chart.update_layout(

        height=340,

        paper_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        },

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )


    st.plotly_chart(
        storage_chart,
        use_container_width=True
    )


    c1, c2 = st.columns(2)


    c1.metric(
        "💾 Data File",
        f"{data_size:.0f} MB"
    )


    c2.metric(
        "📜 Transaction Log",
        f"{log_size:.0f} MB"
    )


# ============================================================
# 25. ORDER WORKLOAD
# ============================================================

with right:

    status_chart = px.bar(

        order_status,

        x="Status",

        y="TotalOrders",

        title="Order Workload by Status",

        text="TotalOrders"
    )


    status_chart.update_traces(

        texttemplate="%{text:,}",

        textposition="outside",

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Orders: %{y:,}"
            "<extra></extra>"
        )
    )


    status_chart.update_layout(

        height=340,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        },

        xaxis_title="Status",

        yaxis_title="Orders",

        margin=dict(
            l=30,
            r=20,
            t=60,
            b=40
        )
    )


    st.plotly_chart(
        status_chart,
        use_container_width=True
    )


# ============================================================
# 26. ORDER STATUS BREAKDOWN
# ============================================================

if not order_status.empty:

    status_columns = st.columns(
        len(order_status)
    )

    for column, row in zip(
        status_columns,
        order_status.itertuples()
    ):

        with column:

            st.metric(

                str(row.Status),

                f"{int(row.TotalOrders):,}",

                f"{row.Percentage:.1f}% of orders"
            )


# ============================================================
# 27. ACTIVITY & TABLE STORAGE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Database Activity & Capacity'
    '</div>',
    unsafe_allow_html=True
)


left, right = st.columns(
    [1.4, 1]
)


# ============================================================
# 28. ORDERS OVER TIME
# ============================================================

with left:

    if not orders_over_time.empty:

        activity_chart = px.line(

            orders_over_time,

            x="OrderDate",

            y="TotalOrders",

            title="Order Activity Over Time",

            markers=False
        )


        activity_chart.update_traces(

            line={
                "width": 2
            },

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Orders: %{y:,}"
                "<extra></extra>"
            )
        )


        activity_chart.update_layout(

            height=340,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font={
                "color": "white"
            },

            xaxis_title="",

            yaxis_title="Orders",

            hovermode="x unified",

            margin=dict(
                l=30,
                r=20,
                t=60,
                b=40
            )
        )


        st.plotly_chart(
            activity_chart,
            use_container_width=True
        )


# ============================================================
# 29. TABLE STORAGE CHART
# ============================================================

with right:

    if not table_storage.empty:

        storage_by_table_chart = px.bar(

            table_storage,

            x="TableName",

            y="TotalSizeMB",

            title="Storage by Table",

            text="TotalSizeMB"
        )


        storage_by_table_chart.update_traces(

            texttemplate="%{text:.1f} MB",

            textposition="outside",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Storage: %{y:.2f} MB"
                "<extra></extra>"
            )
        )


        storage_by_table_chart.update_layout(

            height=340,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font={
                "color": "white"
            },

            xaxis_title="",

            yaxis_title="MB",

            margin=dict(
                l=30,
                r=20,
                t=60,
                b=40
            )
        )


        st.plotly_chart(
            storage_by_table_chart,
            use_container_width=True
        )


# ============================================================
# 30. INDEX ACTIVITY
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Index Performance'
    '</div>',
    unsafe_allow_html=True
)


index_activity = index_usage.copy()


if not index_activity.empty:

    index_activity["Reads"] = (

        index_activity["UserSeeks"]
        + index_activity["UserScans"]
        + index_activity["UserLookups"]

    )


    useful_indexes = index_activity.sort_values(

        by="Reads",

        ascending=False

    ).head(10)


    index_chart = px.bar(

        useful_indexes,

        x="IndexName",

        y=[
            "UserSeeks",
            "UserScans",
            "UserLookups"
        ],

        title="Index Read Activity",

        barmode="group"
    )


    index_chart.update_layout(

        height=350,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        },

        xaxis_title="",

        yaxis_title="Operations",

        legend_title="Operation",

        margin=dict(
            l=30,
            r=20,
            t=60,
            b=80
        )
    )


    st.plotly_chart(
        index_chart,
        use_container_width=True
    )


# ============================================================
# 31. DATABASE ARCHITECTURE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Database Architecture'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
"""
<div class="architecture">

<pre style="font-size:15px; line-height:1.55">

                         ┌───────────────────────┐
                         │      SQL SERVER       │
                         │  DBA_Performance_Lab  │
                         └───────────┬───────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  │                                     │
                  ▼                                     ▼
        ┌───────────────────┐                 ┌──────────────────┐
        │ RELATIONAL MODEL  │                 │ DBA MONITORING   │
        └─────────┬─────────┘                 │      LAYER       │
                  │                           └────────┬─────────┘
                  │                                    │
       ┌──────────┴──────────┐               ┌─────────┴──────────┐
       │                     │               │                    │
       ▼                     ▼               ▼                    ▼
┌─────────────┐       ┌─────────────┐   sys.databases       sys.indexes
│  Customers  │       │  Products   │   sys.partitions      sys.database_files
└──────┬──────┘       └──────┬──────┘   index usage         table storage
       │                     │
       │ 1:M                 │
       ▼                     │
┌─────────────┐              │
│   Orders    │              │
└──────┬──────┘              │
       │                     │
       │ 1:M                 │
       ▼                     │
┌────────────────────────────┴────┐
│           OrderItems            │
└────────────────┬────────────────┘
                 │
                 ▼
          ┌─────────────┐
          │   pyodbc    │
          │ SQL → Python│
          └──────┬──────┘
                 │
                 ▼
          ┌─────────────┐
          │   Pandas    │
          │ DataFrames  │
          └──────┬──────┘
                 │
                 ▼
        ┌───────────────────┐
        │ Streamlit + Plotly│
        │   DBA COMMAND     │
        │      CENTER       │
        └───────────────────┘

</pre>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 32. DBA DIAGNOSTICS
# ============================================================

st.markdown(
    '<div class="section-title">'
    'DBA Diagnostics'
    '</div>',
    unsafe_allow_html=True
)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "⚡ Indexes",
        "📈 Index Usage",
        "📊 Tables",
        "💽 Table Storage",
        "💾 Database Files",
        "🔧 Server"
    ]
)


# ------------------------------------------------------------
# INDEXES
# ------------------------------------------------------------

with tab1:

    st.dataframe(
        indexes,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# INDEX USAGE
# ------------------------------------------------------------

with tab2:

    st.dataframe(
        index_usage,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# TABLE ROWS
# ------------------------------------------------------------

with tab3:

    st.dataframe(
        table_rows,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# TABLE STORAGE
# ------------------------------------------------------------

with tab4:

    st.dataframe(
        table_storage,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# DATABASE FILES
# ------------------------------------------------------------

with tab5:

    st.dataframe(
        database_size,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# SERVER
# ------------------------------------------------------------

with tab6:

    st.write(
        "**Server:**",
        server_info.iloc[0]["ServerName"]
    )

    st.write(
        "**Database:**",
        server_info.iloc[0]["DatabaseName"]
    )

    st.write(
        "**Database Status:**",
        status
    )

    st.write(
        "**Recovery Model:**",
        recovery_model
    )

    st.write(
        "**User Access:**",
        user_access
    )

    st.write(
        "**SQL Server Version:**"
    )

    st.code(
        server_info.iloc[0]["SQLServerVersion"]
    )


# ============================================================
# 33. HEALTH DIAGNOSTICS
# ============================================================

with st.expander(
    "🩺 Health Score Diagnostics"
):

    st.write(
        f"### Current Score: {health_score}/100"
    )


    if not health_findings:

        st.success(
            "No major health warnings detected "
            "by the current lab monitoring rules."
        )

    else:

        st.warning(
            "The following conditions affected "
            "the database health score:"
        )

        for finding in health_findings:

            st.write(
                f"• {finding}"
            )


    st.caption(
        "This score is a custom educational metric "
        "for the DBA Performance Lab and is not an "
        "official Microsoft SQL Server health score."
    )


# ============================================================
# 34. PROJECT SKILLS
# ============================================================

with st.expander(
    "🎓 What this project demonstrates"
):

    st.markdown("""
### Database Administration

- SQL Server monitoring
- Database health inspection
- Storage monitoring
- Transaction log awareness
- Database status monitoring
- Recovery model inspection
- Index monitoring
- Index usage analysis

### SQL Engineering

- Relational data modelling
- Primary Keys
- Foreign Keys
- Referential integrity
- JOIN operations
- Query tuning
- Execution plans
- Clustered indexes
- Nonclustered indexes
- Covering indexes
- SQL Server Dynamic Management Views

### Python

- SQL Server connectivity with `pyodbc`
- SQL query execution
- Pandas DataFrames
- Data transformation
- Automated monitoring

### Data Visualization

- Streamlit
- Plotly
- KPI dashboards
- Health gauges
- Workload visualisation
- Storage analysis
- Operational monitoring

### Performance Engineering

- `SET STATISTICS IO`
- `SET STATISTICS TIME`
- Index Scan vs Index Seek
- Query-plan analysis
- Index usage statistics
- Query optimisation

### Architecture

This project demonstrates the complete path:

`SQL Server → pyodbc → Python → Pandas → Streamlit → Plotly`

The SQL Server database remains the source of truth.

Python extracts and processes the monitoring information.

Streamlit and Plotly expose that information through the DBA Command Center.
""")


# ============================================================
# 35. FOOTER
# ============================================================

st.divider()


footer1, footer2 = st.columns(
    [2, 1]
)


with footer1:

    st.caption(
        "DBA Performance Lab | "
        "SQL Server • Python • Database Administration • "
        "Performance Engineering"
    )


with footer2:

    st.caption(
        f"Dashboard generated "
        f"{datetime.now().strftime('%d %b %Y %H:%M')}"
    )
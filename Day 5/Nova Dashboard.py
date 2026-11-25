import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NOVA | Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* MAIN BACKGROUND */

    .stApp {
        background-color: #0B1020;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #11182B;
        border-right: 1px solid #26314D;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    /* ALL HEADINGS */

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* NORMAL TEXT */

    p, label {
        color: #E2E8F0;
    }

    /* MAIN TITLE */

    .main-title {
        font-size: 36px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 0px;
    }

    /* SUBTITLE */

    .subtitle {
        color: #CBD5E1 !important;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* SECTION TITLE */

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-top: 15px;
    }

    /* STREAMLIT WIDGET LABELS */

    [data-testid="stWidgetLabel"] {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* METRIC CARDS */

    div[data-testid="stMetric"] {
        background-color: #151C30;
        border: 1px solid #26314D;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #CBD5E1 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 13px;
    }

    /* CHART TEXT */

    .js-plotly-plot .plotly text {
        fill: #FFFFFF !important;
    }

    /* DATAFRAME TEXT */

    [data-testid="stDataFrame"] {
        color: #FFFFFF;
    }

    /* FOOTER */

    .footer {
        color: #CBD5E1 !important;
        text-align: center;
        font-size: 13px;
        padding-top: 25px;
    }

    /* DOWNLOAD BUTTON */

    .stDownloadButton button {
        background-color: #7C3AED;
        color: white;
        border-radius: 8px;
        border: none;
    }

    .stDownloadButton button:hover {
        background-color: #6D28D9;
        color: white;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SAMPLE DATA GENERATOR
# --------------------------------------------------

@st.cache_data
def generate_data():

    np.random.seed(42)

    number_of_records = 1000

    start_date = date.today() - timedelta(days=365)

    dates = pd.date_range(
        start=start_date,
        end=date.today(),
        periods=number_of_records
    )

    products = [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Smart Watch",
        "Tablet"
    ]

    regions = [
        "North",
        "South",
        "East",
        "West"
    ]

    customers = [
        "Customer A",
        "Customer B",
        "Customer C",
        "Customer D",
        "Customer E"
    ]

    df = pd.DataFrame({

        "Date": dates,

        "Product": np.random.choice(
            products,
            number_of_records
        ),

        "Region": np.random.choice(
            regions,
            number_of_records
        ),

        "Customer": np.random.choice(
            customers,
            number_of_records
        ),

        "Quantity": np.random.randint(
            1,
            10,
            number_of_records
        ),

        "Unit Price": np.random.randint(
            500,
            50000,
            number_of_records
        )

    })

    df["Revenue"] = (
        df["Quantity"] * df["Unit Price"]
    )

    df["Order ID"] = [
        f"ORD-{10000 + i}"
        for i in range(number_of_records)
    ]

    return df


df = generate_data()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚀 NOVA")

st.sidebar.caption(
    "Business Intelligence Platform"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Sales Analytics",
        "Product Analytics",
        "Transactions"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader(
    "Dashboard Filters"
)

min_date = df["Date"].min().date()

max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_products = st.sidebar.multiselect(
    "Select Products",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date, end_date = selected_dates

else:

    start_date = min_date

    end_date = max_date


filtered_df = df[

    (df["Date"].dt.date >= start_date)

    &

    (df["Date"].dt.date <= end_date)

    &

    (df["Region"].isin(selected_regions))

    &

    (df["Product"].isin(selected_products))

].copy()


# --------------------------------------------------
# COMMON CALCULATIONS
# --------------------------------------------------

total_revenue = filtered_df["Revenue"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_units = filtered_df["Quantity"].sum()

average_order_value = (

    total_revenue / total_orders

    if total_orders > 0

    else 0

)

previous_revenue = df["Revenue"].sum()

revenue_growth = (

    ((total_revenue - previous_revenue)
     / previous_revenue) * 100

    if previous_revenue > 0

    else 0

)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">NOVA Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your business performance at a glance'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Showing data from {start_date} to {end_date}"
)


# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":

    st.markdown(
        '<div class="section-title">'
        'Performance Overview'
        '</div>',
        unsafe_allow_html=True
    )

    # KPI CARDS

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Revenue",
            f"₹{total_revenue:,.0f}",
            f"{revenue_growth:.1f}%"
        )

    with col2:

        st.metric(
            "Total Orders",
            f"{total_orders:,}",
            "Orders"
        )

    with col3:

        st.metric(
            "Units Sold",
            f"{total_units:,}",
            "Units"
        )

    with col4:

        st.metric(
            "Average Order Value",
            f"₹{average_order_value:,.0f}",
            "Per order"
        )

    st.markdown("---")

    # REVENUE TREND

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Revenue Trend")

        monthly_revenue = (

            filtered_df
            .set_index("Date")
            .resample("MS")["Revenue"]
            .sum()
            .reset_index()

        )

        fig = px.area(
            monthly_revenue,
            x="Date",
            y="Revenue",
            title="Monthly Revenue",
            color_discrete_sequence=["#8B5CF6"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151C30",
            plot_bgcolor="#151C30",
            height=350,
            font=dict(
                color="#FFFFFF",
                size=14
            ),
            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Revenue by Region")

        region_revenue = (

            filtered_df
            .groupby("Region")["Revenue"]
            .sum()
            .reset_index()

        )

        fig = px.pie(
            region_revenue,
            names="Region",
            values="Revenue",
            hole=0.55,
            color_discrete_sequence=[
                "#8B5CF6",
                "#06B6D4",
                "#F59E0B",
                "#EC4899"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151C30",
            height=350,
            font=dict(
                color="#FFFFFF",
                size=14
            ),
            margin=dict(
                l=10,
                r=10,
                t=30,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # PRODUCT PERFORMANCE

    st.subheader("Top Performing Products")

    product_revenue = (

        filtered_df
        .groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )

    )

    fig = px.bar(
        product_revenue,
        x="Product",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="Purples",
        text_auto=".2s"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151C30",
        plot_bgcolor="#151C30",
        height=350,
        font=dict(
            color="#FFFFFF",
            size=14
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # RECENT ORDERS

    st.subheader("Recent Transactions")

    recent_orders = (

        filtered_df
        .sort_values(
            "Date",
            ascending=False
        )
        .head(10)

    )

    st.dataframe(
        recent_orders[
            [
                "Order ID",
                "Date",
                "Customer",
                "Product",
                "Region",
                "Revenue"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# SALES ANALYTICS PAGE
# --------------------------------------------------

elif page == "Sales Analytics":

    st.title("📈 Sales Analytics")

    st.write(
        "Explore revenue and order performance."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Sales by Region")

        region_sales = (

            filtered_df
            .groupby("Region")["Revenue"]
            .sum()
            .reset_index()

        )

        fig = px.bar(
            region_sales,
            x="Region",
            y="Revenue",
            color="Region",
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151C30",
            plot_bgcolor="#151C30",
            font=dict(
                color="#FFFFFF",
                size=14
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Orders by Product")

        product_orders = (

            filtered_df
            .groupby("Product")["Order ID"]
            .nunique()
            .reset_index()

        )

        product_orders.columns = [
            "Product",
            "Orders"
        ]

        fig = px.bar(
            product_orders,
            x="Product",
            y="Orders",
            color="Orders",
            color_continuous_scale="Teal"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151C30",
            plot_bgcolor="#151C30",
            font=dict(
                color="#FFFFFF",
                size=14
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Daily Revenue")

    daily_revenue = (

        filtered_df
        .groupby(
            filtered_df["Date"].dt.date
        )["Revenue"]
        .sum()
        .reset_index()

    )

    daily_revenue.columns = [
        "Date",
        "Revenue"
    ]

    fig = px.line(
        daily_revenue,
        x="Date",
        y="Revenue",
        markers=True,
        color_discrete_sequence=["#06B6D4"]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151C30",
        plot_bgcolor="#151C30",
        height=400,
        font=dict(
            color="#FFFFFF",
            size=14
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# PRODUCT ANALYTICS PAGE
# --------------------------------------------------

elif page == "Product Analytics":

    st.title("🛍️ Product Analytics")

    product_summary = (

        filtered_df
        .groupby("Product")
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )

    )

    st.subheader("Product Performance")

    st.dataframe(
        product_summary,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Product Revenue Comparison")

    fig = px.bar(
        product_summary,
        x="Product",
        y="Revenue",
        color="Quantity",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151C30",
        plot_bgcolor="#151C30",
        height=400,
        font=dict(
            color="#FFFFFF",
            size=14
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Quantity vs Revenue")

    fig = px.scatter(
        product_summary,
        x="Quantity",
        y="Revenue",
        size="Orders",
        color="Product",
        hover_name="Product"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151C30",
        plot_bgcolor="#151C30",
        font=dict(
            color="#FFFFFF",
            size=14
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# TRANSACTIONS PAGE
# --------------------------------------------------

elif page == "Transactions":

    st.title("📋 Transactions")

    st.write(
        "Search, review, and download transaction data."
    )

    search_text = st.text_input(
        "Search Order ID or Customer"
    )

    transaction_df = filtered_df.copy()

    if search_text:

        transaction_df = transaction_df[

            transaction_df["Order ID"].str.contains(
                search_text,
                case=False,
                na=False
            )

            |

            transaction_df["Customer"].str.contains(
                search_text,
                case=False,
                na=False
            )

        ]

    st.metric(
        "Matching Transactions",
        len(transaction_df)
    )

    st.dataframe(
        transaction_df.sort_values(
            "Date",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    # CSV DOWNLOAD

    csv_data = transaction_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name="transactions.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    '<div class="footer">'
    'NOVA Analytics Dashboard | Built with Streamlit'
    '</div>',
    unsafe_allow_html=True
)
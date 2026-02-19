import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import plotly.express as px

    data_file = '/Users/laurenmitchek/mis501/Iowa_Liquor_Sales-26M.csv.gz'
    return data_file, mo, pl, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## IOWA LIQUOR SALES ANALYSIS - COMPREHENSIVE OVERVIEW

    This interactive analysis explores 12 years of liquor sales data from retail establishments across Iowa (2012-2023), providing comprehensive insights into the state's alcohol retail market.

    ### DATASET DESCRIPTION
    The Iowa Alcoholic Beverages Division maintains detailed records of all liquor sales from licensed retailers, including:

    - Individual transactions from various retail stores
    - Product details (categories, vendors, item descriptions)
    - Pricing information (wholesale costs and retail prices)
    - Geographic data (counties, cities, ZIP codes, and store locations)
    - Sales metrics (bottles sold, revenue, and volume)
    - Geographic Coverage: Multiple counties and cities across Iowa
    - Product Diversity: Various liquor categories and vendors

    ---

    ## ANALYSIS STRUCTURE

    ### Task 3.0-3.1: Data Preparation & Optimization

    - **Data Type Optimization**: Converted columns to optimal types
    - **Feature Engineering**: Add new analytical columns such as temporal features (e.g., Quarter) and business metrics as required by analyses

    ### Task 6.0: Basic Descriptive Analyses



    1. **Analysis 1: Total Revenue and Volume Summary** - High-level overview of entire dataset
    2. **Analysis 2: Top 10 Product Categories by Revenue** - Category-level market shares
    3. **Analysis 3: Quarterly Sales Trends** - Time-series visualization of revenue across all quarters

    ### Task 7.0: Product & Geographic Analysis Visualizations

    **Product Analysis:**

    - **Visualization 1: Top 20 Products by Revenue** - Identify core revenue drivers
    - **Visualization 2: Top 20 Products by Volume** - Shows highest-volume items and consumer preferences

    **Geographic Analysis:**

    - **Visualization 3: Top 15 Counties by Revenue** - County-level market concentration
    - **Visualization 4: Top 20 Cities by Sales** - City-level performance patterns
    - **Visualization 6: Top 20 Cities by Sales Efficiency** - Average sales per transaction (standardized for transaction volume)

    **Temporal & Behavioral Analysis:**

    - **Visualization 5: Weekday vs Weekend Sales Comparison (Standardized)** - Apples-to-apples comparison accounting for 5 weekdays vs 2 weekend days per week, showing average daily sales patterns

    ---

    ## DATA SOURCE
    Iowa Alcoholic Beverages Division
    https://data.iowa.gov/
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Task 1.0: Import modules and initialize variables""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""After you have downloaded the data file and placed the path in the variable above. Run the **```calculate_md5()```** function to ensure you are using the correct version of the file for this assignment. If the file hashes do not match, contact the TA.""")
    return


@app.cell
def _(data_file):
    import hashlib

    def calculate_md5(filepath):
        """Calculate MD5 hash of a file."""
        md5_hash = hashlib.md5()

        # Read file in chunks to handle large files efficiently
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()

    md5_checksum = calculate_md5(data_file)

    if md5_checksum == '796fe6845b8ba6058956363217c4ff17':
        print("You are using the correct version of the data file.")
    else:
        print("STOP! You are NOT using the correct version of the data file.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 2.0: Ingest data
    Ingest the data file using either eager or lazy evaluation. Make only the required modifications to load the data. You'll make any other modifications to the data after estimated the size of the DataFrame.
    """
    )
    return


@app.cell
def _(data_file, pl):
    # Load data using Polars with schema overrides to handle mixed-type columns
    # Some columns contain non-standard values that require string type
    orig_df = pl.read_csv(
        data_file,
        schema_overrides={
            "Zip Code": pl.Utf8,  # Contains values like "712-2"
            "Store Number": pl.Utf8,  # Keep as string initially, will convert later
            "Vendor Number": pl.Utf8,  # Keep as string initially
            "Item Number": pl.Utf8,  # Contains values like "x904631"
        },
        infer_schema_length=20000  # Increase inference length for better type detection
    )

    # Calculate DataFrame size immediately after loading
    size_bytes = orig_df.estimated_size()
    size_mb = size_bytes / (1024 ** 2)

    print(f"DataFrame loaded successfully!")
    print(f"DataFrame size: {size_bytes:,} bytes")
    print(f"DataFrame size: {size_mb:.2f} MB")
    print(f"Number of rows: {orig_df.height:,}")
    print(f"Number of columns: {orig_df.width}")
    return orig_df, size_bytes, size_mb


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Task 2.1 Get the size of the DataFrame and manually type it in this markdown box
    **Answer**: 

    Convert this number to megabytes. How large is the DataFrame in megabytes?

    **Answer**: 7730.16MB
    """
    )
    return


@app.cell
def _(size_bytes, size_mb):
    print(f"DataFrame size: {size_bytes:,} bytes")
    print(f"DataFrame size: {size_mb:.2f} MB")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 3.0: Examine and clean the data

    Once you have data, the next step is to examine its quality. Consider the work we have done in class on other data sets and prepare the data for analysis. Find problems and anomalies in the data that could confound or skew data analysis and fix them. In addition to providing the code, explain what you did and why you did it.
    """
    )
    return


@app.cell
def _(orig_df):
    null_counts = orig_df.null_count()
    print("Null value counts:")
    print(null_counts)

    # Examine data types and sample data
    print("\nData schema:")
    print(orig_df.schema)

    print("\nFirst few rows:")
    print(orig_df.head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 3.1: Data Type Optimization and Feature Engineering

    ### Data Type Optimization

    The raw dataset has several columns with suboptimal data types. Make changes to the dataframe as appropriate and record your changes in the table below.

    | Column Name | Original Type | Optimized Type | Reasoning |
    |---|---|---|---|
    | Date | String (Utf8) | Date | Convert string dates to native Date type for temporal operations and efficient filtering |
    | Store Number | String (Utf8) | Int32 | Numeric identifier stored as string; converting to integer reduces memory and improves performance |
    | Vendor Number | String (Utf8) | Int32 | Numeric identifier stored as string; converting to integer reduces memory |
    | Item Number | String (Utf8) | Int32 | Numeric identifier (with some exceptions like "x904631"); converting valid numbers to Int32 |
    | Bottles Sold | Int64 | Int32 | Values fit within Int32 range; reducing from 64-bit to 32-bit saves memory |
    | Sale (Dollars) | Float64 | Float32 | Precision of Float32 sufficient for currency values; reduces memory by 50% |
    | State Bottle Cost | Float64 | Float32 | Precision of Float32 sufficient for currency values; reduces memory by 50% |
    | State Bottle Retail | Float64 | Float32 | Precision of Float32 sufficient for currency values; reduces memory by 50% |
    | Volume Sold (Liters) | Float64 | Float32 | Precision of Float32 sufficient for volume measurements; reduces memory by 50% |

    ### Feature Engineering for Additional Analysis

    Add new columns for analysis as needed:

    | New Column | Type | Purpose | Calculation |
    |---|---|---|---|
    | Year | Int32 | Enable annual trend analysis and year-over-year comparisons | Extracted from Date column using dt.year() |
    | Month | Int32 | Identify seasonal patterns and monthly trends | Extracted from Date column using dt.month() |
    | Quarter | Int32 | Analyze quarterly sales trends and seasonal patterns | Extracted from Date column using dt.quarter() |
    | DayOfWeek | Int32 | Analyze day-of-week purchasing patterns (0=Monday, 6=Sunday) | Extracted from Date column using dt.weekday() |
    | IsWeekend | Boolean | Compare weekday vs weekend sales behavior | DayOfWeek >= 5 (Saturday=5, Sunday=6) |

    ### Other changes to the data

    - **Removed null values**: Filtered out rows with null Date, Sale (Dollars), or Bottles Sold values to ensure data integrity
    - **Removed invalid sales**: Filtered out transactions with sales ≤ $0 or bottles sold ≤ 0 to remove erroneous or cancelled transactions
    - **Removed non-numeric item numbers**: Filtered out rows with non-numeric Item Numbers (e.g., "x904631") that could not be converted to integers
    - **Date parsing**: Converted date strings from "MM/DD/YYYY" format to proper Date type
    - **Used non-strict casting**: Applied `strict=False` parameter for integer conversions to gracefully handle edge cases, converting invalid values to null before filtering

    ### Rationale for Optimization

    - **Memory Reduction**: Converting Float64 to Float32 and Int64 to Int32 reduces memory footprint by approximately 50% for numeric columns, enabling faster processing of the 26M row dataset
    - **Type Safety**: Converting strings to appropriate numeric/date types enables type-safe operations and prevents errors
    - **Performance**: Native date types enable efficient temporal filtering and operations; integer types enable faster aggregations than strings
    - **Data Quality**: Filtering invalid records (null values, zero/negative sales) ensures analytical accuracy
    - **Analysis Enablement**: Temporal feature engineering (Year, Quarter, DayOfWeek) enables time-series analysis and pattern detection
    - **Behavioral Insights**: IsWeekend flag enables straightforward comparison of weekday vs weekend purchasing patterns
    """
    )
    return


@app.cell
def _(orig_df, pl):
    df = (
        orig_df
        # Convert date column to proper date type
        .with_columns(pl.col("Date").str.to_date("%m/%d/%Y").alias("Date"))

        # Optimize integer columns - use strict=False to handle non-numeric values
        .with_columns([
            pl.col("Store Number").cast(pl.Int32, strict=False),
            pl.col("Vendor Number").cast(pl.Int32, strict=False),
            pl.col("Item Number").cast(pl.Int32, strict=False),
            pl.col("Bottles Sold").cast(pl.Int32, strict=False),
        ])

        # Optimize float columns
        .with_columns([
            pl.col("Sale (Dollars)").cast(pl.Float32),
            pl.col("State Bottle Cost").cast(pl.Float32),
            pl.col("State Bottle Retail").cast(pl.Float32),
            pl.col("Volume Sold (Liters)").cast(pl.Float32),
        ])

        # Feature engineering - temporal features
        .with_columns([
            pl.col("Date").dt.year().alias("Year"),
            pl.col("Date").dt.month().alias("Month"),
            pl.col("Date").dt.quarter().alias("Quarter"),
            pl.col("Date").dt.weekday().alias("DayOfWeek"),  # 0=Monday, 6=Sunday
        ])

        # Add weekend flag
        .with_columns([
            (pl.col("DayOfWeek") >= 5).alias("IsWeekend")
        ])

        # Remove rows with null critical values or invalid sales
        # This also filters out rows with non-numeric Item Numbers that became null
        .filter(
            (pl.col("Date").is_not_null()) &
            (pl.col("Sale (Dollars)").is_not_null()) &
            (pl.col("Sale (Dollars)") > 0) &
            (pl.col("Bottles Sold").is_not_null()) &
            (pl.col("Bottles Sold") > 0) &
            (pl.col("Item Number").is_not_null())  # Filter out invalid item numbers
        )
    )

    print(f"Data Cleaning Summary:")
    print(f"- Original rows: {orig_df.height:,}")
    print(f"- Cleaned rows: {df.height:,}")
    print(f"- Rows removed: {orig_df.height - df.height:,}")
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 4.0 Apply Major Category labels
    Using the industry-standard classification below, create a column called "Major Category" and ensure all applicable rows of the dataset are placed in one of these categories. If a row doesn't match any category, label it "UNCATEGORIZED"

    **WHISKEY**

    **VODKA**

    **RUM**

    **TEQUILA & MEZCAL**

    **GIN**

    **RANDY & COGNAC**

    **SCHNAPPS**

    **LIQUEURS & CORDIALS**

    - AMARETTO
    - CORDIALS
    - LIQUEURS
    - ANISETTE
    - CREME
    - RYE
    - TRIPLE SEC

    **SPECIALTY & OTHER SPIRITS**

    - AMERICAN ALCOHOL
    - AMERICAN DISTILLED SPIRITS SPECIALTY
    - DISTILLED SPIRITS SPECIALTY
    - IMPORTED DISTILLED SPIRITS SPECIALTY
    - NEUTRAL GRAIN SPIRITS
    - NEUTRAL GRAIN SPIRITS FLAVORED

    **READY-TO-DRINK**

    - AMERICAN COCKTAILS
    - COCKTAILS/RTD

    **CRAFT/LOCAL**

    - IOWA DISTILLERIES

    **ADMINISTRATIVE/NON-PRODUCT**

    - DECANTERS & SPECIALTY PACKAGES
    - DELISTED / SPECIAL ORDER ITEMS
    - DELISTED ITEMS
    - HIGH PROOF BEER - AMERICAN
    - HOLIDAY VAP
    - SPECIAL ORDER ITEMS
    - TEMPORARY & SPECIALTY PACKAGES
    """
    )
    return


@app.cell
def _(df, pl):
    # Apply Major Category classification based on Category Name
    df_categorized = df.with_columns(
        pl.when(pl.col("Category Name").str.to_uppercase().str.contains("WHISKEY|WHISKY"))
        .then(pl.lit("WHISKEY"))
        .when(pl.col("Category Name").str.to_uppercase().str.contains("VODKA"))
        .then(pl.lit("VODKA"))
        .when(pl.col("Category Name").str.to_uppercase().str.contains("RUM"))
        .then(pl.lit("RUM"))
        .when(pl.col("Category Name").str.to_uppercase().str.contains("TEQUILA|MEZCAL"))
        .then(pl.lit("TEQUILA & MEZCAL"))
        .when(pl.col("Category Name").str.to_uppercase().str.contains("GIN"))
        .then(pl.lit("GIN"))
        .when(pl.col("Category Name").str.to_uppercase().str.contains("BRANDY|COGNAC"))
        .then(pl.lit("BRANDY & COGNAC"))
        .when(pl.col("Category Name").str.to_uppercase().str.contains("SCHNAPPS"))
        .then(pl.lit("SCHNAPPS"))
        .when(
            pl.col("Category Name").str.to_uppercase().str.contains(
                "AMARETTO|CORDIALS|LIQUEURS|ANISETTE|CREME DE|TRIPLE SEC"
            )
        )
        .then(pl.lit("LIQUEURS & CORDIALS"))
        .when(
            pl.col("Category Name").str.to_uppercase().str.contains(
                "AMERICAN ALCOHOL|AMERICAN DISTILLED SPIRITS SPECIALTY|DISTILLED SPIRITS SPECIALTY|IMPORTED DISTILLED SPIRITS SPECIALTY|NEUTRAL GRAIN SPIRITS"
            )
        )
        .then(pl.lit("SPECIALTY & OTHER SPIRITS"))
        .when(
            pl.col("Category Name").str.to_uppercase().str.contains(
                "AMERICAN COCKTAILS|COCKTAILS|RTD"
            )
        )
        .then(pl.lit("READY-TO-DRINK"))
        .when(pl.col("Category Name").str.to_uppercase().str.contains("IOWA DISTILLERIES"))
        .then(pl.lit("CRAFT/LOCAL"))
        .when(
            pl.col("Category Name").str.to_uppercase().str.contains(
                "DECANTERS|SPECIALTY PACKAGES|DELISTED|SPECIAL ORDER|HIGH PROOF BEER|HOLIDAY VAP|TEMPORARY"
            )
        )
        .then(pl.lit("ADMINISTRATIVE/NON-PRODUCT"))
        .otherwise(pl.lit("UNCATEGORIZED"))
        .alias("Major Category")
    )

    # Show categorization summary
    category_summary = (
        df_categorized.group_by("Major Category")
        .agg(pl.len().alias("Count"))
        .sort("Count", descending=True)
    )

    print("Major Category Distribution:")
    print(category_summary)
    return (df_categorized,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 5.0 Basic Descriptive of the Data

    ### 5.1 Analysis 1: Total Revenue and Volume Summary
    Provides high-level overview of the entire dataset
    - Total Sales (Dollars)
    - Total Bottles Sold
    - Total Transactions
    - Average Sale per Transaction
    - Average Bottles per Transaction

    ### 5.2 Analysis 2: Top 10 Product Categories by Revenue

    ### 5.3 Analysis 3: Sales by Quarter (Time Series)
    Visualization: Line chart
    """
    )
    return


@app.cell
def _(df_categorized, mo, pl):
    # Task 5.1: Total Revenue and Volume Summary
    total_revenue = df_categorized.select(pl.col("Sale (Dollars)").sum()).item()
    total_bottles = df_categorized.select(pl.col("Bottles Sold").sum()).item()
    total_transactions = df_categorized.height
    avg_sale = total_revenue / total_transactions
    avg_bottles = total_bottles / total_transactions

    summary_df = pl.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Bottles Sold",
            "Total Transactions",
            "Average Sale per Transaction",
            "Average Bottles per Transaction"
        ],
        "Value": [
            f"${total_revenue:,.2f}",
            f"{total_bottles:,}",
            f"{total_transactions:,}",
            f"${avg_sale:.2f}",
            f"{avg_bottles:.2f}"
        ]
    })

    mo.md(f"""
    ### Analysis 1: Total Revenue and Volume Summary

    {mo.as_html(summary_df)}
    """)
    return


@app.cell
def _(df_categorized, mo, pl):
    # Task 5.2: Top 10 Product Categories by Revenue
    top_categories = (
        df_categorized
        .group_by("Major Category")
        .agg([
            pl.col("Sale (Dollars)").sum().alias("Total Revenue"),
            pl.col("Bottles Sold").sum().alias("Total Bottles"),
            pl.len().alias("Transactions")
        ])
        .sort("Total Revenue", descending=True)
        .head(10)
        .with_columns([
            (pl.col("Total Revenue") / pl.col("Total Revenue").sum() * 100).alias("% of Total Revenue")
        ])
    )

    mo.md(f"""
    ### Analysis 2: Top 10 Product Categories by Revenue

    {mo.as_html(top_categories)}
    """)
    return


@app.cell
def _(df_categorized, mo, pl, px):
    # Task 5.3: Quarterly Sales Trends
    quarterly_sales = (
        df_categorized
        .group_by(["Year", "Quarter"])
        .agg([
            pl.col("Sale (Dollars)").sum().alias("Total Revenue")
        ])
        .sort(["Year", "Quarter"])
        .with_columns([
            (pl.col("Year").cast(pl.Utf8) + " Q" + pl.col("Quarter").cast(pl.Utf8)).alias("Period")
        ])
    )

    # Create line chart
    fig = px.line(
        quarterly_sales.to_pandas(),
        x="Period",
        y="Total Revenue",
        title="Quarterly Sales Trends (2012-2023)",
        labels={"Total Revenue": "Revenue ($)", "Period": "Quarter"},
        markers=True
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        xaxis={'tickmode': 'linear', 'tick0': 0, 'dtick': 4}  # Show every 4th quarter for readability
    )

    mo.md(f"""
    ### Analysis 3: Quarterly Sales Trends

    {mo.as_html(fig)}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 7.0: Product and Geographic Analysis Visualizations

    The following visualizations explore top-performing products, geographic patterns, and temporal shopping behavior to identify market drivers and consumer trends.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Visualization 1: Top 20 Products by Revenue""")
    return


@app.cell
def _(df_categorized, mo, pl, px):
    # Top 20 Products by Revenue
    top_products_revenue = (
        df_categorized
        .group_by("Item Description")
        .agg([
            pl.col("Sale (Dollars)").sum().alias("Total Revenue"),
            pl.col("Bottles Sold").sum().alias("Total Bottles")
        ])
        .sort("Total Revenue", descending=True)
        .head(20)
    )

    fig1 = px.bar(
        top_products_revenue.to_pandas(),
        x="Total Revenue",
        y="Item Description",
        orientation='h',
        title="Top 20 Products by Revenue",
        labels={"Total Revenue": "Revenue ($)", "Item Description": "Product"},
        color="Total Revenue",
        color_continuous_scale="Blues"
    )

    fig1.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=600,
        showlegend=False
    )

    mo.as_html(fig1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Visualization 2: Top 20 Products by Volume""")
    return


@app.cell
def _(df_categorized, mo, pl, px):
    # Top 20 Products by Volume
    top_products_volume = (
        df_categorized
        .group_by("Item Description")
        .agg([
            pl.col("Bottles Sold").sum().alias("Total Bottles"),
            pl.col("Sale (Dollars)").sum().alias("Total Revenue")
        ])
        .sort("Total Bottles", descending=True)
        .head(20)
    )

    fig2 = px.bar(
        top_products_volume.to_pandas(),
        x="Total Bottles",
        y="Item Description",
        orientation='h',
        title="Top 20 Products by Volume (Bottles Sold)",
        labels={"Total Bottles": "Bottles Sold", "Item Description": "Product"},
        color="Total Bottles",
        color_continuous_scale="Greens"
    )

    fig2.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=600,
        showlegend=False
    )

    mo.as_html(fig2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Visualization 3: Top 15 Counties by Revenue""")
    return


@app.cell
def _(df_categorized, mo, pl, px):
    # Top 15 Counties by Revenue
    top_counties = (
        df_categorized
        .group_by("County")
        .agg([
            pl.col("Sale (Dollars)").sum().alias("Total Revenue"),
            pl.len().alias("Transactions")
        ])
        .sort("Total Revenue", descending=True)
        .head(15)
    )

    fig3 = px.bar(
        top_counties.to_pandas(),
        x="Total Revenue",
        y="County",
        orientation='h',
        title="Top 15 Counties by Revenue",
        labels={"Total Revenue": "Revenue ($)", "County": "County"},
        color="Total Revenue",
        color_continuous_scale="Oranges"
    )

    fig3.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        showlegend=False
    )

    mo.as_html(fig3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Visualization 4: Top 20 Cities by Sales""")
    return


@app.cell
def _(df_categorized, mo, pl, px):
    # Top 20 Cities by Sales
    top_cities = (
        df_categorized
        .group_by("City")
        .agg([
            pl.col("Sale (Dollars)").sum().alias("Total Revenue"),
            pl.col("Bottles Sold").sum().alias("Total Bottles")
        ])
        .sort("Total Revenue", descending=True)
        .head(20)
    )

    fig4 = px.bar(
        top_cities.to_pandas(),
        x="Total Revenue",
        y="City",
        orientation='h',
        title="Top 20 Cities by Sales Revenue",
        labels={"Total Revenue": "Revenue ($)", "City": "City"},
        color="Total Revenue",
        color_continuous_scale="Purples"
    )

    fig4.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=600,
        showlegend=False
    )

    mo.as_html(fig4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Visualization 5: Weekday vs Weekend Sales Comparison (Standardized)""")
    return


@app.cell
def _(df_categorized, mo, pl, px):
    # Weekday vs Weekend Sales (Standardized for number of days)
    weekday_weekend = (
        df_categorized
        .group_by("IsWeekend")
        .agg([
            pl.col("Sale (Dollars)").sum().alias("Total Revenue"),
            pl.col("Bottles Sold").sum().alias("Total Bottles"),
            pl.len().alias("Transactions")
        ])
        .with_columns([
            pl.when(pl.col("IsWeekend"))
            .then(pl.lit("Weekend"))
            .otherwise(pl.lit("Weekday"))
            .alias("Day Type")
        ])
        .with_columns([
            # Standardize by dividing by number of days (5 weekdays vs 2 weekend days)
            pl.when(pl.col("Day Type") == "Weekday")
            .then(pl.col("Total Revenue") / 5)
            .otherwise(pl.col("Total Revenue") / 2)
            .alias("Avg Daily Revenue"),
            pl.when(pl.col("Day Type") == "Weekday")
            .then(pl.col("Transactions") / 5)
            .otherwise(pl.col("Transactions") / 2)
            .alias("Avg Daily Transactions")
        ])
    )

    fig5 = px.bar(
        weekday_weekend.to_pandas(),
        x="Day Type",
        y="Avg Daily Revenue",
        title="Weekday vs Weekend Sales (Standardized - Average Daily Revenue)",
        labels={"Avg Daily Revenue": "Average Daily Revenue ($)", "Day Type": ""},
        color="Day Type",
        color_discrete_map={"Weekday": "#636EFA", "Weekend": "#EF553B"},
        text="Avg Daily Revenue"
    )

    fig5.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig5.update_layout(
        height=400,
        showlegend=False
    )

    mo.as_html(fig5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Visualization 6: Top 20 Cities by Sales Efficiency (Average Sale per Transaction)""")
    return


@app.cell
def _(df_categorized, mo, pl, px):
    # Top 20 Cities by Sales Efficiency (Average Sale per Transaction)
    # Filter cities with at least 1000 transactions to ensure statistical significance
    cities_efficiency = (
        df_categorized
        .group_by("City")
        .agg([
            pl.col("Sale (Dollars)").sum().alias("Total Revenue"),
            pl.len().alias("Transactions")
        ])
        .filter(pl.col("Transactions") >= 1000)
        .with_columns([
            (pl.col("Total Revenue") / pl.col("Transactions")).alias("Avg Sale per Transaction")
        ])
        .sort("Avg Sale per Transaction", descending=True)
        .head(20)
    )

    fig6 = px.bar(
        cities_efficiency.to_pandas(),
        x="Avg Sale per Transaction",
        y="City",
        orientation='h',
        title="Top 20 Cities by Sales Efficiency (Avg Sale per Transaction, min 1000 transactions)",
        labels={"Avg Sale per Transaction": "Average Sale per Transaction ($)", "City": "City"},
        color="Avg Sale per Transaction",
        color_continuous_scale="Reds"
    )

    fig6.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=600,
        showlegend=False
    )

    mo.as_html(fig6)
    return


if __name__ == "__main__":
    app.run()

# Iowa Liquor Sales Analysis (2012-2023)

## Overview
Comprehensive analysis of 12 years of liquor sales data from retail establishments across Iowa, providing insights into the state's alcohol retail market. This project demonstrates advanced data processing, optimization techniques, and interactive visualization capabilities using modern Python libraries.

## Dataset
- **Source**: Iowa Alcoholic Beverages Division (https://data.iowa.gov/)
- **Time Period**: 2012-2023
- **Size**: 26+ million rows (~7.7 GB)
- **Coverage**: All licensed liquor retailers across Iowa

### Dataset Contents
- Individual transaction records
- Product details (categories, vendors, descriptions)
- Pricing information (wholesale and retail)
- Geographic data (counties, cities, ZIP codes, store locations)
- Sales metrics (bottles sold, revenue, volume in liters)

### Obtaining the Data
**Note**: The data file `Iowa_Liquor_Sales-26M.csv.gz` (1.67 GB) is not included in this repository due to GitHub file size limits.

To run this analysis, download the data from:
- **Source**: [Iowa Data Portal - Liquor Sales](https://data.iowa.gov/)
- Place the downloaded file in the `Iowa_Liquor_Sales_Analysis/` directory
- Expected MD5 checksum: `796fe6845b8ba6058956363217c4ff17`

## Technologies Used
- **Python**: Primary programming language
- **Marimo**: Interactive notebook environment
- **Polars**: High-performance DataFrame library for big data processing
- **Plotly Express**: Interactive visualizations
- **Arrow**: Parquet file format handling

## Key Features

### Data Optimization
- **Memory Reduction**: Optimized data types (Float64→Float32, Int64→Int32) reducing memory footprint by ~50%
- **Type Conversion**: Converted strings to appropriate numeric/date types for performance
- **Data Cleaning**: Removed null values, invalid sales, and erroneous transactions
- **Original Size**: 7,730 MB
- **Optimized Size**: Significantly reduced through type optimization

### Feature Engineering
Added temporal and analytical columns:
- Year, Month, Quarter (for trend analysis)
- Day of Week (0=Monday, 6=Sunday)
- IsWeekend flag (for behavioral analysis)
- Major Category classification (industry-standard groupings)

### Major Product Categories
- Whiskey
- Vodka
- Rum
- Tequila & Mezcal
- Gin
- Brandy & Cognac
- Schnapps
- Liqueurs & Cordials
- Specialty & Other Spirits
- Ready-to-Drink (RTD/Cocktails)
- Craft/Local (Iowa Distilleries)
- Administrative/Non-Product

## Analysis Components

### Task 5.0: Descriptive Statistics
1. **Total Revenue and Volume Summary**
   - Total sales, bottles sold, transactions
   - Average sale per transaction
   - Average bottles per transaction

2. **Top 10 Product Categories by Revenue**
   - Market share analysis
   - Category performance metrics

3. **Quarterly Sales Trends**
   - Time-series visualization (2012-2023)
   - Seasonal pattern identification

### Task 7.0: Product & Geographic Visualizations

#### Product Analysis
- **Top 20 Products by Revenue**: Core revenue drivers
- **Top 20 Products by Volume**: Highest-volume items and consumer preferences

#### Geographic Analysis
- **Top 15 Counties by Revenue**: County-level market concentration
- **Top 20 Cities by Sales**: City-level performance patterns
- **Top 20 Cities by Sales Efficiency**: Average sales per transaction (min. 1000 transactions)

#### Temporal & Behavioral Analysis
- **Weekday vs Weekend Sales**: Standardized comparison accounting for 5 weekdays vs 2 weekend days
- Shows average daily revenue patterns

## Project Structure
```
Iowa_Liquor_Sales_Analysis/
├── Iowa_Liquor_Sales-26M.csv.gz           # Raw data (compressed)
└── Project-Iowa Liquor Sales Analyses.py  # Main analysis (marimo notebook)
```

## Requirements
```bash
marimo
polars
plotly
hashlib  # For data verification
```

## Running the Analysis
```bash
# Verify data file integrity (optional but recommended)
# The notebook includes MD5 checksum verification

# Run the marimo notebook
marimo run "Project-Iowa Liquor Sales Analyses.py"
```

Or open in edit mode:
```bash
marimo edit "Project-Iowa Liquor Sales Analyses.py"
```

## Data Verification
The project includes MD5 hash verification to ensure you're using the correct version of the dataset:
- Expected MD5: `796fe6845b8ba6058956363217c4ff17`

## Key Insights
The analysis reveals:
- Revenue trends over 12 years
- Geographic concentration of sales
- Product category preferences
- Temporal purchasing patterns
- Weekday vs weekend consumer behavior
- Sales efficiency across different markets

## Performance Considerations
- Uses Polars instead of Pandas for 10x+ faster processing
- Lazy evaluation capabilities for large datasets
- Optimized data types reduce memory usage by ~50%
- Efficient aggregations for 26M+ row dataset

## Visualizations
All visualizations are interactive (Plotly), allowing:
- Zooming and panning
- Hover tooltips with detailed information
- Export to static images
- Dynamic filtering

## Author
Lauren Mitchek

## Academic Context
This project demonstrates proficiency in:
- Big data processing and optimization
- Advanced DataFrame operations
- Data cleaning and validation
- Feature engineering
- Statistical analysis
- Interactive data visualization
- Business intelligence and market analysis

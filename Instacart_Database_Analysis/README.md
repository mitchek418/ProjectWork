# Instacart Database Analysis

## Overview
SQL-based analysis of Instacart shopping behavior, exploring customer ordering patterns, product preferences, reorder behaviors, and temporal trends. This project demonstrates advanced SQL querying techniques including window functions, CTEs, views, and complex aggregations.

## Dataset
The analysis uses the Instacart Market Basket Analysis dataset, which includes:

### Tables
- **orders**: Order-level information (user_id, order timing, days since prior order)
- **order_products**: Products in each order (with reorder flags, cart position)
- **products**: Product catalog (names, categories)
- **aisles**: Product aisle information
- **departments**: Product department information

### Data Files
- `orders.csv` - Order metadata (104 MB)
- `order_products.csv` - Current order products
- `order_products_prior.csv` - Prior order products (551 MB)
- `products.csv` - Product catalog
- `aisles.csv` - Aisle definitions
- `departments.csv` - Department definitions

### Obtaining the Data
**Note**: The large CSV files (`orders.csv`, `order_products.csv`, `order_products_prior.csv`) are not included in this repository due to GitHub file size limits.

To run this analysis, download the Instacart Market Basket Analysis dataset from:
- **Source**: [Kaggle - Instacart Market Basket Analysis](https://www.kaggle.com/c/instacart-market-basket-analysis/data)
- Place the downloaded CSV files in the `Instacart_Database_Analysis/` directory
- The smaller files (`products.csv`, `aisles.csv`, `departments.csv`) are included in this repository

## Technologies Used
- **MySQL**: Database management system
- **SQL**: Advanced querying with window functions, CTEs, and aggregations

## Project Structure
```
Instacart_Database_Analysis/
├── create_instacart.sql          # Database schema and data loading
├── InstacartDB_analysis.sql      # Analysis queries (15 questions)
├── orders.csv                    # Order data
├── order_products.csv            # Current order products
├── order_products_prior.csv      # Prior order products
├── products.csv                  # Product catalog
├── aisles.csv                    # Aisle definitions
└── departments.csv               # Department definitions
```

## Analysis Questions

### 1. Order Frequency Analysis
- How frequently do users place orders?
- Categorizes users by ordering frequency (weekly, bi-weekly, monthly)
- Creates `user_frequency` view for downstream analysis

### 2. Products per Order by User Category
- Compares average products per order between weekly and monthly shoppers
- Reveals shopping pattern differences

### 3. Top Reordered Products (Weekly Users)
- Identifies top 5 products most frequently reordered by weekly shoppers
- Shows customer loyalty patterns

### 4. Reorder Count vs Cart Position
- Examines relationship between reorder frequency and add-to-cart order
- Samples products for statistical significance

### 5. User Segmentation by Reorder Interval
- Segments users into 5 categories by average days between orders
- Provides distribution of user ordering patterns

### 6. Department Performance
- Most/least products ordered by department (total units)
- Most/least unique products ordered by department
- Reveals departmental popularity

### 7. Never-Ordered Products
- Identifies products that have never been purchased
- Includes aisle and department context

### 8. Top-Selling Product Aisles
- Identifies aisles containing the most top 100 products
- Creates `top_100_products` view
- Shows aisle-level market concentration

### 9. Single-Order Products in Top Aisles
- Products ordered only once in the highest-performing aisle
- Identifies underperforming items in popular aisles

### 10. First-in-Cart Products
- Top 10 products most often added to cart first
- Shows shopping priority patterns

### 11. Reorder Likelihood of Top Products
- Are top 10 most-ordered products likely to be reordered?
- Calculates reorder ratios (>60% = likely)
- Creates `top_10_ordered` view

### 12. Organic vs Non-Organic
- Compares sales volume between organic and non-organic products
- Market share analysis

### 13. Top Products per Department
- Top 5 products by order count for each department
- Uses window functions (ROW_NUMBER with PARTITION BY)

### 14. Weekday Order Patterns
- Identifies weekdays with highest/lowest order volumes
- Shows temporal ordering patterns

### 15. Prime Reorder Times
- Top 3 weekday + hour combinations for reorders
- Reveals optimal times for customer engagement

## SQL Techniques Demonstrated

### Advanced Features
- **Window Functions**: ROW_NUMBER, PARTITION BY
- **CTEs (Common Table Expressions)**: Subquery organization
- **Views**: Reusable query components
- **User Variables**: Dynamic filtering (@top_aisle_id)
- **Aggregations**: COUNT, SUM, AVG, ROUND
- **CASE Statements**: Conditional logic
- **JOINs**: Multiple table relationships (INNER, LEFT)
- **Filtering**: Complex WHERE conditions
- **Grouping**: Multi-level GROUP BY
- **Ordering**: Multiple sort criteria

### Data Analysis Patterns
- User segmentation
- Temporal pattern analysis
- Market basket analysis
- Product performance metrics
- Customer behavior profiling

## Setup Instructions

### 1. Create Database
```sql
CREATE DATABASE instacart;
USE instacart;
```

### 2. Load Data
Run the `create_instacart.sql` script to:
- Create table schemas
- Import CSV data
- Set up proper data types and indexes

### 3. Run Analysis
Execute queries from `InstacartDB_analysis.sql` individually or in sequence.

## Requirements
- MySQL 8.0+ (for window function support)
- CSV data files
- Sufficient disk space (~2-3 GB for full dataset)

## Key Insights
The analysis reveals:
- Customer ordering frequency patterns
- Reorder behavior by user segment
- Department and aisle popularity
- Temporal shopping patterns
- Product loyalty metrics
- Cart composition patterns
- Organic vs conventional preferences

## Performance Considerations
- Views created for frequently used queries
- Sampling used where appropriate (e.g., every 100th product)
- Indexed columns for faster joins
- Optimized aggregations

## Use Cases
This analysis provides insights valuable for:
- Inventory management
- Marketing campaign timing
- Product recommendation systems
- Customer segmentation strategies
- Reorder prediction models
- Promotional planning

## Author
Lauren Mitchek

## Academic Context
This project demonstrates proficiency in:
- Complex SQL querying
- Database design and management
- Window functions and advanced SQL features
- Customer behavior analysis
- E-commerce analytics
- Data-driven decision making

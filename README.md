# Project Work Portfolio

A collection of data analysis and programming projects demonstrating proficiency in Python, R, SQL, and modern data science tools.

## Author
**Lauren Mitchek**

## Repository Overview
This repository contains academic and personal projects showcasing skills in:
- Data analysis and visualization
- Statistical modeling and regression
- Database design and SQL querying
- Big data processing and optimization
- Interactive notebook development
- Machine learning and predictive analytics

## Projects

### 1. NCAA Football 2017 Analysis
**Directory**: `NCAA_Football_2017/`
**Technologies**: Python, Marimo, Polars, JSON

Analysis of 2017 NCAA football season data, exploring game statistics, team performance, and player metrics. Demonstrates data ingestion from JSON files, pattern matching with regex, and statistical analysis using modern Python libraries.

**Key Features**:
- 15+ analytical questions answered
- Field goal success rate analysis
- Drive efficiency metrics
- Rare event detection (safeties)
- Interactive marimo notebook

[View Full Documentation →](NCAA_Football_2017/README.md)

---

### 2. Iowa Liquor Sales Analysis (2012-2023)
**Directory**: `Iowa_Liquor_Sales_Analysis/`
**Technologies**: Python, Marimo, Polars, Plotly

Comprehensive analysis of 26+ million liquor sales transactions from Iowa retailers. Demonstrates big data processing, memory optimization, and interactive visualization.

**Key Features**:
- 7.7 GB dataset processing
- 50% memory reduction through type optimization
- Geographic and temporal trend analysis
- Industry-standard product categorization
- Interactive Plotly visualizations

[View Full Documentation →](Iowa_Liquor_Sales_Analysis/README.md)

---

### 3. Instacart Database Analysis
**Directory**: `Instacart_Database_Analysis/`
**Technologies**: MySQL, SQL

SQL-based analysis of e-commerce shopping behavior, exploring customer ordering patterns, product preferences, and reorder behaviors.

**Key Features**:
- 15 complex SQL queries
- Window functions and CTEs
- User segmentation by shopping frequency
- Product performance metrics
- Temporal pattern analysis

[View Full Documentation →](Instacart_Database_Analysis/README.md)

---

### 4. Chicago Crime Seasonality Analysis (2015-2024)
**Directory**: `Chicago_Crime_Seasonality/` and `R_Final_Project/`
**Technologies**: R, Tidyverse, MASS, Arrow

Statistical analysis of 10 years of Chicago crime data using negative binomial regression and ANOVA to understand seasonal patterns and special event impacts.

**Key Features**:
- Negative binomial regression modeling
- ANOVA with post-hoc testing
- Crime categorization and aggregation
- Event impact analysis (marathons, festivals)
- Comprehensive model diagnostics

[View Full Documentation →](Chicago_Crime_Seasonality/README.md)

---

## Technical Skills Demonstrated

### Programming Languages
- **Python**: Data analysis, visualization, automation
- **R**: Statistical modeling, regression, ANOVA
- **SQL**: Complex queries, database design, optimization

### Data Analysis Libraries
- **Python**: Polars, Pandas, Plotly, Marimo
- **R**: Tidyverse (dplyr, ggplot2), MASS, caret, lubridate

### Data Processing
- **Formats**: JSON, CSV, Parquet
- **Techniques**: Data cleaning, feature engineering, type optimization
- **Scale**: Multi-million row datasets

### Statistical Methods
- Regression analysis (negative binomial)
- ANOVA and post-hoc testing
- Hypothesis testing
- Model diagnostics and validation
- Train/test split methodology

### Database Technologies
- MySQL database design
- Complex JOIN operations
- Window functions (PARTITION BY, ROW_NUMBER)
- Views and CTEs
- Query optimization

### Visualization
- Interactive Plotly visualizations
- ggplot2 statistical graphics
- Time series analysis
- Geographic visualizations
- Comparative analysis plots

## Project Structure
```
ProjectWork/
├── README.md (this file)
├── NCAA_Football_2017/
│   ├── README.md
│   ├── 2017 Alabama football JSON/
│   └── 2017 NCAA Football assignment_v2.py
├── Iowa_Liquor_Sales_Analysis/
│   ├── README.md
│   ├── Iowa_Liquor_Sales-26M.csv.gz
│   └── Project-Iowa Liquor Sales Analyses.py
├── Instacart_Database_Analysis/
│   ├── README.md
│   ├── create_instacart.sql
│   ├── InstacartDB_analysis.sql
│   └── [CSV data files]
├── Chicago_Crime_Seasonality/
│   ├── README.md
│   └── chicago_crime_seasonality_2015_2024.parquet
└── R_Final_Project/
    ├── README.md
    └── Final_Project 1.R
```

## Getting Started

Each project folder contains:
- **README.md**: Detailed project documentation
- **Code**: Analysis scripts and notebooks
- **Data**: Dataset files (where applicable)

### Important Note on Data Files
Due to GitHub file size limits (100 MB), large data files are **not included** in this repository. Each project README contains instructions for obtaining the required datasets:
- **Iowa Liquor Sales**: Download from Iowa Data Portal
- **Instacart Database**: Download from Kaggle
- **Chicago Crime**: Download from Chicago Data Portal
- **NCAA Football**: Data included in repository (JSON files)

To explore a specific project, navigate to its directory and read the project-specific README for:
- Detailed methodology
- Data download instructions
- Setup instructions
- Running the analysis
- Key findings and insights

## Technologies Summary

| Project | Languages | Key Libraries | Dataset Size |
|---------|-----------|--------------|--------------|
| NCAA Football | Python | Marimo, Polars, JSON | ~1 GB |
| Iowa Liquor Sales | Python | Marimo, Polars, Plotly | 7.7 GB (26M rows) |
| Instacart | SQL | MySQL | ~2-3 GB |
| Chicago Crime | R | Tidyverse, MASS, Arrow | 162 MB (10 years) |

## Academic Context
These projects were completed as part of coursework in:
- Data Analytics
- Database Management
- Statistical Analysis
- Business Intelligence

They demonstrate practical application of:
- Real-world data analysis
- Statistical rigor
- Code documentation
- Reproducible research
- Data-driven decision making

## Contact
For questions or collaboration opportunities, please reach out via GitHub.

## License
These projects are for educational and portfolio purposes.

---

**Last Updated**: February 2026

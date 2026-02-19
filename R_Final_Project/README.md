# R Final Project - Chicago Crime Seasonality Analysis

## Overview
This folder contains the R analysis script for the Chicago Crime Seasonality project. The script performs statistical analysis on Chicago crime data (2015-2024) using negative binomial regression and ANOVA techniques.

## Project Components
- **Analysis Script**: `Final_Project 1.R`
- **Data Source**: `chicago_crime_seasonality_2015_2024.parquet` (located in `../Chicago_Crime_Seasonality/`)

## Related Project
This script analyzes data from the **Chicago Crime Seasonality** project. For complete project documentation, dataset description, and detailed findings, see:
- `../Chicago_Crime_Seasonality/README.md`

## What This Script Does

### Data Processing
1. Loads parquet file with Chicago crime data
2. Filters to 2015-2024 time period
3. Converts temporal variables to factors
4. Creates crime categories (Non-Violent, Violent, Human Trafficking/Sex, Special Event)
5. Aggregates incident-level data to daily counts

### Statistical Analysis
1. **Exploratory Data Analysis**
   - Time series plots with trend lines
   - Distribution plots by day, month, season, weekend

2. **Regression Modeling**
   - Four negative binomial models (by crime category + total)
   - Predictors: day, month, season, weekend, special events
   - 80/20 train/test split
   - Performance evaluation (RMSE, AIC)

3. **ANOVA Testing**
   - Tests for monthly differences in crime rates
   - Controls for weekend and seasonal effects
   - Tukey HSD post-hoc tests

4. **Model Diagnostics**
   - Residual plots
   - VIF for multicollinearity
   - Goodness-of-fit tests

## Requirements
```r
install.packages(c("arrow", "tidyverse", "lubridate", "caret",
                   "broom", "knitr", "car", "MASS"))
```

## Running the Script
```r
# Ensure you're in the correct directory or update the data path
source("Final_Project 1.R")
```

Or run interactively in RStudio.

## Key Technologies
- **R**: Statistical computing
- **Tidyverse**: Data manipulation (dplyr, ggplot2)
- **MASS**: Negative binomial regression
- **caret**: Machine learning tools
- **arrow**: Parquet file reading

## Output
The script generates:
- Multiple visualizations (ggplot2 graphics)
- Model summaries and diagnostics
- Summary tables (knitr)
- Performance metrics for all models

## Academic Context
Demonstrates proficiency in:
- Advanced regression modeling
- Statistical hypothesis testing
- Data visualization in R
- Reproducible analysis
- Working with large datasets

## Author
Lauren Mitchek

## Note
This is the analysis component of a two-part project:
1. **Data**: `Chicago_Crime_Seasonality/` folder
2. **Analysis**: This folder (`R_Final_Project/`)

For full project documentation, see the main Chicago Crime Seasonality README.

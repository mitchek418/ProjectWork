# Chicago Crime Seasonality Analysis (2015-2024)

## Overview
Statistical analysis of Chicago crime data examining seasonal patterns, temporal trends, and the impact of special events on crime rates. This project uses advanced regression modeling and ANOVA techniques to understand crime patterns across different time periods and categories.

## Dataset
- **Time Period**: 2015-2024 (10 years)
- **Format**: Parquet file (optimized columnar storage)
- **Source**: Chicago Police Department crime records
- **File**: `chicago_crime_seasonality_2015_2024.parquet` (~162 MB compressed)

### Dataset Features
- **Temporal Variables**: Date, time, year, month, day of week, quarter
- **Crime Details**: Primary type, description, location
- **Categorical Variables**: Season, weekend flag
- **Event Indicators**: Marathon, Lollapalooza, special events, river events

### Obtaining the Data
**Note**: The data file `chicago_crime_seasonality_2015_2024.parquet` (154 MB) is not included in this repository due to GitHub file size limits.

To run this analysis, download the Chicago crime data from:
- **Source**: [Chicago Data Portal - Crimes](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
- Filter for years 2015-2024 and export as CSV or use the provided parquet file if available
- Place the file in the `Chicago_Crime_Seasonality/` directory
- The R script in `R_Final_Project/` expects this file to be present

## Technologies Used
- **R**: Statistical programming language
- **Libraries**:
  - `arrow`: Parquet file reading
  - `tidyverse`: Data manipulation and visualization (dplyr, ggplot2)
  - `lubridate`: Date/time handling
  - `caret`: Train/test split
  - `MASS`: Negative binomial regression
  - `car`: ANOVA and VIF diagnostics
  - `broom`: Model output tidying
  - `knitr`: Publication-quality tables

## Crime Categories

### Classification System
1. **Non-Violent Crimes**
   - Theft
   - Robbery
   - Narcotics
   - Burglary

2. **Violent Crimes**
   - Battery
   - Assault
   - Criminal Damage
   - Homicide

3. **Special Event Crimes**
   - Arson
   - Gambling
   - Other Offenses

4. **Human Trafficking/Sex Crimes**
   - Criminal Sexual Assault
   - Domestic Violence
   - Prostitution
   - Kidnapping
   - Stalking
   - Human Trafficking

5. **Other**: All remaining crime types

## Analysis Components

### 1. Exploratory Data Analysis
- **Time Series Visualization**: Total daily crime counts (2015-2024) with trend line
- **Day of Week Patterns**: Boxplots showing crime distribution by weekday
- **Monthly Patterns**: Crime counts across all months
- **Seasonal Patterns**: Crime distribution by season (Winter, Spring, Summer, Fall)
- **Weekend vs Weekday**: Comparative analysis of crime rates

### 2. Statistical Modeling

#### Negative Binomial Regression Models
Four separate models built for:
1. Non-Violent Crime Counts
2. Violent Crime Counts
3. Human Trafficking/Sex Crime Counts
4. Total Crime Counts

#### Model Predictors
- Day of week (Monday-Sunday)
- Month (January-December)
- Weekend flag (Weekday/Weekend)
- Season (Winter, Spring, Summer, Fall)
- Marathon event (binary)
- Special event (binary)
- Lollapalooza event (binary)
- River event (binary)

#### Model Performance Metrics
- **RMSE** (Root Mean Squared Error): Prediction accuracy
- **AIC** (Akaike Information Criterion): Model quality
- **Deviance**: Goodness of fit
- **Theta**: Dispersion parameter

### 3. ANOVA Testing

#### Research Questions
1. Is there a significant difference in non-violent crime counts between months controlling for weekend?
2. Is there a significant difference in non-violent crime counts between months controlling for season?
3. Is there a significant difference in violent crime counts between months controlling for weekend?
4. Is there a significant difference in violent crime counts between months controlling for season?

#### Post-Hoc Analysis
- Tukey HSD tests for significant month effects
- Pairwise comparisons of monthly crime rates

### 4. Model Diagnostics
- Residual plots (4-panel diagnostic plots)
- Variance Inflation Factors (VIF) for multicollinearity
- Aliased coefficient detection
- Deviance goodness-of-fit tests
- Theta parameter estimation

## Project Structure
```
Chicago_Crime_Seasonality/
└── chicago_crime_seasonality_2015_2024.parquet    # Crime data
```

```
R_Final_Project/
└── Final_Project 1.R    # Analysis script
```

**Note**: The R script in `R_Final_Project` analyzes the parquet file from `Chicago_Crime_Seasonality`. These folders represent the same project with data and code separated.

## Running the Analysis

### Prerequisites
Install required R packages:
```r
install.packages(c("arrow", "tidyverse", "lubridate", "caret",
                   "broom", "knitr", "car", "MASS"))
```

### Execution
1. Ensure the parquet file path is correct in the script:
```r
crime_data <- read_parquet("chicago_crime_seasonality_2015_2024.parquet")
```

2. Run the entire script in R:
```r
source("Final_Project 1.R")
```

Or run interactively in RStudio line-by-line.

## Key Findings

### Temporal Patterns
- Crime rates vary significantly by season
- Weekend vs weekday patterns differ by crime type
- Certain months show consistently higher crime rates

### Event Impact
- Special events (marathons, Lollapalooza, river events) impact crime rates
- Effects vary by crime category

### Model Performance
- Negative binomial regression appropriately handles overdispersion in count data
- Separate models for crime categories reveal different predictor importance
- Temporal variables (month, day, season) are significant predictors

### Statistical Significance
- Month is a significant factor in crime rates
- Weekend/weekday distinction affects crime patterns
- Seasonal effects confirmed through ANOVA

## Visualizations Generated

### EDA Plots
1. Time series with LOESS smoothing
2. Boxplots by day of week (faceted by crime type)
3. Boxplots by month (faceted by crime type)
4. Boxplots by season (faceted by crime type)
5. Weekend vs weekday comparison (faceted by crime type)

### Statistical Plots
1. Bar charts of mean crime counts by month with error bars
2. 4-panel diagnostic plots for regression models

### Summary Tables
1. Crime category distribution
2. Model performance metrics
3. Season summary statistics
4. Weekend/weekday summary statistics

## Data Aggregation
- Raw incident-level data aggregated to daily counts
- Stratified by crime category
- Preserves temporal and event variables for modeling

## Train/Test Split
- 80% training data
- 20% test data
- Stratified sampling maintains temporal distribution
- Set seed (123) for reproducibility

## Statistical Methods

### Why Negative Binomial Regression?
- Crime counts are overdispersed (variance > mean)
- Poisson regression assumes variance = mean (violated)
- Negative binomial accommodates overdispersion via theta parameter
- Appropriate for count data with excess zeros

### Why ANOVA?
- Tests differences across multiple groups (months, seasons)
- Controls for confounding variables (weekend, season)
- Identifies which temporal factors drive crime variation

## Author
Lauren Mitchek

## Academic Context
This project demonstrates proficiency in:
- Advanced statistical modeling in R
- Regression analysis for count data
- ANOVA and post-hoc testing
- Model diagnostics and validation
- Data visualization with ggplot2
- Reproducible research practices
- Working with modern data formats (Parquet)
- Feature engineering for temporal data
- Handling large datasets efficiently

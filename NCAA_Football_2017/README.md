# 2017 NCAA Football Data Analysis

## Overview
This project analyzes NCAA football game data from the 2017 season using Python. The analysis focuses on game statistics, player performance, team metrics, and interesting patterns discovered in the season's data.

## Dataset
- **Source**: ESPN game data in JSON format
- **Coverage**: 2017 NCAA Football season (regular season + bowl games)
- **Format**: JSON files organized by week (Week 1-15 + Bowl)
- **Teams**: Multiple NCAA football teams with focus on Alabama Crimson Tide

## Technologies Used
- **Python**: Primary programming language
- **Marimo**: Interactive notebook environment
- **Polars**: High-performance DataFrame library for data analysis
- **Regex**: Pattern matching for text extraction
- **JSON**: Data ingestion and file I/O

## Key Concepts Demonstrated
- Data ingestion from JSON files
- Data manipulation with DataFrames
- Statistical analysis and aggregations
- Pattern matching with regular expressions
- Data quality assessment
- Exploratory data analysis

## Project Structure
```
NCAA_Football_2017/
├── 2017 Alabama football JSON/    # Game data organized by week
│   ├── Week 1/
│   ├── Week 2/
│   ├── ...
│   └── Bowl/
└── 2017 NCAA Football assignment_v2.py    # Main analysis script (marimo notebook)
```

## Analysis Questions Answered
1. **Game Count**: Total number of games in the dataset
2. **Data Structure**: Top-level keys and data organization
3. **Team Consistency**: Verification of team name consistency across files
4. **Team List**: Alphabetically sorted list of all teams
5. **Data Reliability**: Assessment of data quality and completeness
6. **Field Goal Analysis**: Alabama's field goal success rate vs. league average
7. **Safety Occurrences**: Games with safeties and teams involved
8. **Longest Plays**: Identification of season's longest plays
9. **Alabama Performance**: First and last offensive plays, punt statistics
10. **Punt Statistics**: Distance analysis (longest, shortest, median)
11. **Offensive Performance**: Team-level drive efficiency using Polars
12. **Video Highlights**: Extraction of video URLs from game data

## Requirements
```bash
marimo
polars
```

## Running the Analysis
```bash
# Run the marimo notebook
marimo run "2017 NCAA Football assignment_v2.py"
```

Or open in edit mode:
```bash
marimo edit "2017 NCAA Football assignment_v2.py"
```

## Key Findings
The analysis reveals comprehensive insights into the 2017 NCAA football season, including:
- Team performance metrics
- Field goal success rates
- Drive efficiency statistics
- Rare event occurrences (safeties)
- Player performance patterns

## Data Files
The `2017 Alabama football JSON` directory contains weekly game data organized by:
- Regular season weeks (Week 1-15)
- Bowl game(s)
- Each week has "full" folders containing complete game JSON files

## Output
The analysis generates a JSON file containing answers to all analytical questions, suitable for automated grading or reporting.

## Author
Lauren Mitchek

## Academic Context
This project was completed as part of MIS 501 coursework, demonstrating proficiency in Python programming, data analysis, and working with real-world sports data.

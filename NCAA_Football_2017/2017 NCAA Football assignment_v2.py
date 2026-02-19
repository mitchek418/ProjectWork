import marimo

__generated_with = "0.15.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pathlib
    import json
    import os
    import re
    import statistics
    return json, mo, os, re, statistics


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # MIS 501 Football Data Analysis Assignment

    ## Overview
    This project analyzes NCAA football game data from the 2017 season using Python. You will practice data ingestion, manipulation, analysis, and reporting skills.

    ## Key Concepts Used
    * **Basic Python**: syntax, len() function, variables, conditionals, loops
    * **Data structures**: lists, dictionaries, and sets
    * **Data analysis**: polars library for DataFrames and aggregations
    * **Pattern matching**: regex for extracting text patterns
    * **File I/O**: JSON file reading and writing
    * **File system**: pathlib for file access

    ## Dataset Information
    You have been provided JSON files containing football game data from the 2017 season.

    **Important Notes:**
    - Use only JSON files in the 'full' folders (not 'flattened')
    - If the provided data conflicts with real-world statistics, use the provided data
    - 'Season' includes all games provided (regular season + bowl games)
    - You are free to use any and all AI available to you.
    - Do not collaborate with others or use others' individual work on this assignment.

    ## Assignment Objectives
    Answer the questions below and output your results to a JSON file with:
    - **Keys**: Question identifiers (e.g., 'q1', 'q2', 'q3.1')
    - **Values**: Your answers in appropriate data types

    ## Deliverables
    - Submit a JSON file named: `mis511_python_project_[netid].json`
    - Submit your .py file
    """
    )
    return


@app.cell
def _():
    # Example: How to structure your answer file
    example_answer_file = {}
    example_answer_file['q1'] = 'yes'  # String answer
    example_answer_file['q2'] = 42      # Numeric answer
    example_answer_file['q3'] = ['item1', 'item2']  # List answer
    print(example_answer_file)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## Setup: Import Required Libraries
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Data Loading
    Load all game data from JSON files organized by week.
    """
    )
    return


@app.cell
def _(json, os):
    def load_game_data():
        # Initialize dictionary to store all game data
        game_dict = {}
        game_weeks = [
            "Bowl", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5",
            "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 11",
            "Week 12", "Week 13", "Week 14", "Week 15"
        ]
        for week in game_weeks:
            week_path = f'2017 Alabama football JSON/{week}/full'

            for file in os.listdir(week_path):

                game_dict[file] = {}


                with open(f'{week_path}/{file}', 'r') as path:
                    json_bytes = path.read()
                    game_data = json.loads(json_bytes)
                    game_dict[file].update(game_data)

        return game_dict

    game_dict = load_game_data()
    return (game_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## Question 1
    **How many games are in the data set?**
    """
    )
    return


@app.cell
def _(game_dict):
    # Count the number of games in the dataset
    q1 = len(game_dict)
    print(f"Number of games in dataset: {q1}")
    return (q1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 2
    **What are the top-level keys for each game file?**

    These keys represent the main data categories available for each game.
    """
    )
    return


@app.cell
def _(game_dict):
    # Get the top-level keys from any game file
    # Get the first game in the dictionary
    first_game_file = list(game_dict.keys())[0]
    q2 = list(game_dict[first_game_file].keys())
    print(f"Top-level keys: {q2}")
    return (q2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Data Quality Check

    Real-world data often contains irregularities or errors. Key questions to consider:
    - Are team names consistent across files? (e.g., "Texas A&M" vs "Texas A and M")
    - Are there duplicate games in the dataset?
    - Are all teams in the season represented?

    We'll examine file names and team references to assess data quality.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 3
    **Are all teams referenced consistently? (yes/no)**
    """
    )
    return


@app.cell
def _(game_dict, re):
    def check_team_consistency():
        # Check if teams are referenced consistently
        # Extract team names from filenames and compare with team names in game data
        teams_from_filenames = set()
        teams_from_gamedata = set()

        for filename, game_data in game_dict.items():
            match = re.search(r' - (.+) vs (.+)\.json', filename)
            if match:
                teams_from_filenames.add(match.group(1))
                teams_from_filenames.add(match.group(2))
            if 'teams' in game_data:
                for team_data in game_data['teams']:
                    if 'team' in team_data and 'displayName' in team_data['team']:
                        teams_from_gamedata.add(team_data['team']['displayName'])

        inconsistencies = []
        for team in teams_from_filenames:
            found = False
            for gd_team in teams_from_gamedata:
                if team.replace('_', '&') == gd_team or team.replace('_', ' and ') == gd_team or team == gd_team:
                    found = True
                    break
            if not found:
                inconsistencies.append(team)

        return 'no' if inconsistencies else 'yes'

    q3 = check_team_consistency()
    print(f"Teams referenced consistently? {q3}")
    return (q3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Question 3.1
    **Provide a Python list of all teams in the dataset, sorted alphabetically.**
    """
    )
    return


@app.cell
def _(game_dict):
    def get_all_teams():
        # Get all unique teams from the game data and sort alphabetically
        teams = set()

        for game_data in game_dict.values():
            if 'teams' in game_data:
                for team_data in game_data['teams']:
                    if 'team' in team_data and 'displayName' in team_data['team']:
                        teams.add(team_data['team']['displayName'])

        return sorted(list(teams))

    q3_1 = get_all_teams()
    print(f"Number of unique teams: {len(q3_1)}")
    print(f"Teams: {q3_1}")
    return (q3_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 4
    **Does the data seem reliable?**

    - **q4**: 'yes' or 'no'
    - **q4.1**: Provide 1-2 sentences with quantifiable reasons from the dataset.
      If you cleaned any data, explain what and why.
    """
    )
    return


@app.cell
def _(game_dict):
    def assess_data_reliability():
        # Assess data reliability by checking for duplicates and consistency
        # Check if all game IDs are unique (they should be from the filenames)
        game_ids = []
        for filename in game_dict.keys():
            game_id = filename.split(' - ')[0]
            game_ids.append(game_id)
        unique_ids = len(set(game_ids))
        total_ids = len(game_ids)
        games_with_complete_data = 0
        for game_data in game_dict.values():
            if 'gameInfo' in game_data and 'drives' in game_data and 'scoringPlays' in game_data:
                games_with_complete_data += 1
        has_duplicates = unique_ids != total_ids
        completeness_rate = games_with_complete_data / total_ids

        q4 = 'yes' if not has_duplicates and completeness_rate > 0.95 else 'no'
        q4_1 = f"The dataset contains {total_ids} games with {unique_ids} unique game IDs. {games_with_complete_data} games ({completeness_rate*100:.1f}%) have complete data including gameInfo, drives, and scoringPlays sections."
        return q4, q4_1

    q4, q4_1 = assess_data_reliability()
    print(f"Data seems reliable? {q4}")
    print(f"{q4_1}")
    return q4, q4_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 5
    **How many unique teams are represented in the data?**
    """
    )
    return


@app.cell
def _(q3_1):
    # Count unique teams (use the list from q3_1)
    q5 = len(q3_1)
    print(f"Number of unique teams: {q5}")
    return (q5,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 6
    **Alabama Field Goal Analysis**

    Alabama fans often assume their kicker will miss field goals. Does the 2017 season
    data support this perception? Compare Alabama's field goal success rate to other teams.

    - **q6**: 'yes' or 'no' (Does Alabama miss more often than others?)
    - **q6.1**: Provide quantifiable evidence from the dataset
    """
    )
    return


@app.cell
def _(game_dict):
    def analyze_field_goals():
        # Analyze field goal success rates
        # Count field goal attempts from drives
        alabama_fg_attempts = {'made': 0, 'missed': 0}
        all_teams_fg = {}

        for game_data in game_dict.values():
            if 'drives' in game_data and 'previous' in game_data['drives']:
                for drive in game_data['drives']['previous']:
                    team_data = drive.get('team', {})
                    team_name = team_data.get('displayName') if isinstance(team_data, dict) else team_data
                    if team_name and 'plays' in drive:
                        if team_name not in all_teams_fg:
                            all_teams_fg[team_name] = {'made': 0, 'missed': 0}

                        for play in drive['plays']:
                            if 'type' in play and 'text' in play:
                                play_type_data = play.get('type', {})
                                play_type = play_type_data.get('text', '') if isinstance(play_type_data, dict) else str(play_type_data)
                                play_text = play['text']
                                if 'field goal' in play_type.lower():
                                    # Check play_type for "good" or "missed", not play_text
                                    if 'good' in play_type.lower():
                                        all_teams_fg[team_name]['made'] += 1
                                        if team_name == 'Alabama Crimson Tide':
                                            alabama_fg_attempts['made'] += 1
                                    elif 'missed' in play_type.lower() or 'no good' in play_type.lower():
                                        all_teams_fg[team_name]['missed'] += 1
                                        if team_name == 'Alabama Crimson Tide':
                                            alabama_fg_attempts['missed'] += 1
        alabama_total_attempts = alabama_fg_attempts['made'] + alabama_fg_attempts['missed']
        alabama_success_rate = alabama_fg_attempts['made'] / alabama_total_attempts if alabama_total_attempts > 0 else 0
        all_rates = []
        for team, stats in all_teams_fg.items():
            total = stats['made'] + stats['missed']
            if total > 0:
                success_rate = stats['made'] / total
                all_rates.append(success_rate)

        avg_rate = sum(all_rates) / len(all_rates) if all_rates else 0
        q6 = 'yes' if alabama_success_rate < avg_rate else 'no'
        q6_1 = f"Alabama attempted {alabama_total_attempts} field goals, making {alabama_fg_attempts['made']} and missing {alabama_fg_attempts['missed']} for a {alabama_success_rate*100:.1f}% success rate. The average success rate across all teams was {avg_rate*100:.1f}%."
        return q6, q6_1

    q6, q6_1 = analyze_field_goals()
    print(f"Does Alabama miss more field goals than average? {q6}")
    print(f"{q6_1}")
    return q6, q6_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 7
    **Safety Occurrences**

    A *safety* occurs when the offensive player with the ball is tackled or downs
    the ball in their own end zone. The defensive team scores 2 points and receives
    possession.

    **In how many games did a safety occur?**
    """
    )
    return


@app.cell
def _(game_dict):
    def count_safety_games():
        # Count games where a safety occurred
        games_with_safety = 0

        for game_data in game_dict.values():
            has_safety = False
            if 'scoringPlays' in game_data:
                for play in game_data['scoringPlays']:
                    if 'scoringType' in play:
                        scoring_type_data = play.get('scoringType', {})
                        scoring_type = scoring_type_data.get('name', '') if isinstance(scoring_type_data, dict) else str(scoring_type_data)
                        if scoring_type == 'safety' or 'safety' in scoring_type.lower():
                            has_safety = True
                            break
            if has_safety:
                games_with_safety += 1

        return games_with_safety

    q7 = count_safety_games()
    print(f"Number of games with a safety: {q7}")
    return (q7,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 8
    **Which team(s) scored the most safeties?**

    Include all teams if there is a tie.
    """
    )
    return


@app.cell
def _(game_dict):
    def track_safeties():
        # Track safeties scored and given up by each team
        safeties_scored = {}  
        safeties_given_up = {}  

        for game_data in game_dict.values():
            if 'scoringPlays' in game_data:
                for play in game_data['scoringPlays']:
                    if 'scoringType' in play:
                        scoring_type_data = play.get('scoringType', {})
                        scoring_type = scoring_type_data.get('name', '') if isinstance(scoring_type_data, dict) else str(scoring_type_data)
                        if scoring_type == 'safety' or 'safety' in scoring_type.lower():
                            # The team that scored the safety
                            team_data = play.get('team', {})
                            scoring_team = team_data.get('displayName') if isinstance(team_data, dict) else team_data
                            if scoring_team:
                                safeties_scored[scoring_team] = safeties_scored.get(scoring_team, 0) + 1

                            if 'teams' in game_data:
                                for team_info in game_data['teams']:
                                    team_obj = team_info.get('team', {})
                                    team_name = team_obj.get('displayName') if isinstance(team_obj, dict) else team_obj
                                    if team_name and team_name != scoring_team:
                                        safeties_given_up[team_name] = safeties_given_up.get(team_name, 0) + 1

        return {'scored': safeties_scored, 'given_up': safeties_given_up}

    safety_dict = track_safeties()
    return (safety_dict,)


@app.cell
def _(safety_dict):
    # Find team(s) that scored the most safeties
    if safety_dict['scored']:
        max_safeties = max(safety_dict['scored'].values())
        teams_with_most = [team for team, count in safety_dict['scored'].items() if count == max_safeties]
        q8 = teams_with_most if len(teams_with_most) > 1 else teams_with_most[0]
    else:
        q8 = []
    print(f"Team(s) that scored the most safeties: {q8}")
    return (q8,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 9
    **Which three teams gave up the most safeties?**
    """
    )
    return


@app.cell
def _(safety_dict):
    # Find the three teams that gave up the most safeties
    if safety_dict['given_up']:
        sorted_teams = sorted(safety_dict['given_up'].items(), key=lambda x: x[1], reverse=True)
        top_3_teams = [team for team, count in sorted_teams[:3]]
        q9 = top_3_teams
    else:
        q9 = []
    print(f"Top 3 teams that gave up the most safeties: {q9}")
    return (q9,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 10
    **Find the longest play(s) in the 2017 season**

    For example: a 99-yard interception return or touchdown pass.

    If multiple plays tie for longest, show all of them with:
    - Team matchup
    - Quarter
    - Clock time
    - Play description
    """
    )
    return


@app.cell
def _(game_dict, re):
    def find_longest_plays():
        # Find the longest play(s) in the season
        longest_plays = []
        max_yards = 0

        for filename, game_data in game_dict.items():
            match = re.search(r' - (.+) vs (.+)\.json', filename)
            matchup = match.group(0) if match else filename

            if 'drives' in game_data and 'previous' in game_data['drives']:
                for drive in game_data['drives']['previous']:
                    if 'plays' in drive:
                        for play in drive['plays']:
                            yardage = 0

                            # Get yardage from statYardage, but validate it's realistic
                            if 'statYardage' in play:
                                stat_yards = abs(play['statYardage'])
                                # Filter out unrealistic values (max play in football is ~109 yards)
                                if stat_yards <= 110:
                                    yardage = stat_yards

                            # If statYardage is missing or unrealistic, try to extract from text
                            if yardage == 0 and 'text' in play:
                                yards_match = re.search(r'(\d+)\s*yd', play['text'], re.IGNORECASE)
                                if yards_match:
                                    yardage = int(yards_match.group(1))

                            if yardage > max_yards:
                                max_yards = yardage
                                period_data = play.get('period', {})
                                quarter = period_data.get('number', 'Unknown') if isinstance(period_data, dict) else period_data
                                clock_data = play.get('clock', {})
                                clock = clock_data.get('displayValue', 'Unknown') if isinstance(clock_data, dict) else clock_data
                                longest_plays = [{
                                    'matchup': matchup,
                                    'quarter': quarter,
                                    'clock': clock,
                                    'description': play.get('text', 'No description'),
                                    'yards': yardage
                                }]
                            elif yardage == max_yards and yardage > 0:
                                period_data = play.get('period', {})
                                quarter = period_data.get('number', 'Unknown') if isinstance(period_data, dict) else period_data
                                clock_data = play.get('clock', {})
                                clock = clock_data.get('displayValue', 'Unknown') if isinstance(clock_data, dict) else clock_data
                                longest_plays.append({
                                    'matchup': matchup,
                                    'quarter': quarter,
                                    'clock': clock,
                                    'description': play.get('text', 'No description'),
                                    'yards': yardage
                                })

        return longest_plays

    q10 = find_longest_plays()
    print(f"Longest play(s) in the season:")
    for play in q10:
        print(f"  {play['yards']} yards - {play['description']}")
        print(f"  Matchup: {play['matchup']}, Q{play['quarter']} at {play['clock']}")
    return (q10,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 11
    **Alabama's First and Last Offensive Plays**

    Provide the yardage and description for:
    - Alabama's FIRST offensive play of the season
    - Alabama's LAST offensive play of the season
    """
    )
    return


@app.cell
def _(json, os):
    # Find Alabama's first and last offensive plays
    # Need to identify all Alabama games and find first/last plays chronologically

    def get_alabama_plays():
        game_weeks_order = [
            "Week 1", "Week 2", "Week 3", "Week 4", "Week 5",
            "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 11",
            "Week 12", "Week 13", "Week 14", "Week 15", "Bowl"
        ]

        alabama_plays = []

        for week in game_weeks_order:
            week_path = f'2017 Alabama football JSON/{week}/full'
            if os.path.exists(week_path):
                for file in os.listdir(week_path):
                    if 'Alabama' in file:
                        filepath = f'{week_path}/{file}'
                        with open(filepath, 'r') as f:
                            game_data = json.load(f)

                        if 'drives' in game_data and 'previous' in game_data['drives']:
                            for drive in game_data['drives']['previous']:
                                team_data = drive.get('team', {})
                                team_name = team_data.get('displayName', '') if isinstance(team_data, dict) else str(team_data)
                                if 'Alabama' in team_name and 'plays' in drive:
                                    for play in drive['plays']:
                                        play_type_data = play.get('type', {})
                                        play_type = play_type_data.get('text', '') if isinstance(play_type_data, dict) else str(play_type_data)
                                        if play_type not in ['Kickoff', 'Timeout', 'End Period', 'End of Half']:
                                            alabama_plays.append({
                                                'week': week,
                                                'description': play.get('text', ''),
                                                'yardage': play.get('statYardage', 0)
                                            })

        first_play = alabama_plays[0] if alabama_plays else None
        last_play = alabama_plays[-1] if alabama_plays else None

        return {
            'first_play': first_play,
            'last_play': last_play
        }

    q11 = get_alabama_plays()
    print(f"Alabama's first and last offensive plays:")
    if q11['first_play']:
        print(f"  First play ({q11['first_play']['week']}): {q11['first_play']['description']}")
        print(f"    Yardage: {q11['first_play']['yardage']}")
    if q11['last_play']:
        print(f"  Last play ({q11['last_play']['week']}): {q11['last_play']['description']}")
        print(f"    Yardage: {q11['last_play']['yardage']}")
    return (q11,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 12
    **How many times did Alabama punt in the 2017 season?**
    """
    )
    return


@app.cell
def _(game_dict):
    def count_alabama_punts():
        # Count Alabama punts
        alabama_punts = 0

        for game_data in game_dict.values():
            if 'drives' in game_data and 'previous' in game_data['drives']:
                for drive in game_data['drives']['previous']:
                    team_data = drive.get('team', {})
                    team_name = team_data.get('displayName', '') if isinstance(team_data, dict) else str(team_data)
                    if 'Alabama' in team_name and 'plays' in drive:
                        for play in drive['plays']:
                            play_type_data = play.get('type', {})
                            play_type = play_type_data.get('text', '') if isinstance(play_type_data, dict) else str(play_type_data)
                            if 'punt' in play_type.lower():
                                alabama_punts += 1

        return alabama_punts

    q12 = count_alabama_punts()
    print(f"Alabama punted {q12} times in the 2017 season")
    return (q12,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 13
    **Punt Distance Statistics**

    Calculate the longest, shortest, and median punt distance across all punts.
    Return as a dictionary with labeled values.
    """
    )
    return


@app.cell
def _(game_dict, re, statistics):
    def calculate_punt_statistics():
        # Calculate punt distance statistics
        punt_distances = []

        for game_data in game_dict.values():
            if 'drives' in game_data and 'previous' in game_data['drives']:
                for drive in game_data['drives']['previous']:
                    if 'plays' in drive:
                        for play in drive['plays']:
                            play_type_data = play.get('type', {})
                            play_type = play_type_data.get('text', '') if isinstance(play_type_data, dict) else str(play_type_data)
                            play_text = play.get('text', '')
                            if 'punt' in play_type.lower():
                                yards_match = re.search(r'punt.*?(\d+)\s*yds?', play_text, re.IGNORECASE)
                                if yards_match:
                                    distance = int(yards_match.group(1))
                                    punt_distances.append(distance)

        if punt_distances:
            return {
                'longest': max(punt_distances),
                'shortest': min(punt_distances),
                'median': statistics.median(punt_distances)
            }
        else:
            return {'longest': 0, 'shortest': 0, 'median': 0}

    q13 = calculate_punt_statistics()
    print(f"Punt distance statistics:")
    print(f"  Longest: {q13['longest']} yards")
    print(f"  Shortest: {q13['shortest']} yards")
    print(f"  Median: {q13['median']} yards")
    return (q13,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Question 14
    **Offensive Performance Analysis Using Polars**

    Use the polars library to analyze offensive performance across all teams.

    Create a DataFrame of all drives and calculate per-team statistics:
    - Total number of drives
    - Average yards per drive
    - Touchdown percentage (% of drives ending in TD)
    - Turnover percentage (% of drives ending in turnover)

    Show the top 10 teams ranked by average yards per drive.
    """
    )
    return


@app.cell
def _(game_dict):
    def analyze_offensive_performance():
        # Offensive performance analysis using Polars
        import polars as pl
        drives_data = []

        for game_data in game_dict.values():
            if 'drives' in game_data and 'previous' in game_data['drives']:
                for drive in game_data['drives']['previous']:
                    team_data = drive.get('team', {})
                    team_name = team_data.get('displayName', '') if isinstance(team_data, dict) else str(team_data)
                    if team_name:
                        yards = drive.get('yards', 0)
                        result_data = drive.get('result', {})
                        result = result_data.get('text', '') if isinstance(result_data, dict) else str(result_data)
                        ended_in_td = 'touchdown' in result.lower() or 'TD' in result
                        ended_in_turnover = any(keyword in result.lower() for keyword in ['interception', 'fumble', 'turnover', 'downs'])

                        drives_data.append({
                            'team': team_name,
                            'yards': yards,
                            'touchdown': ended_in_td,
                            'turnover': ended_in_turnover
                        })
        df_drives = pl.DataFrame(drives_data)
        team_stats = df_drives.group_by('team').agg([
            pl.count('yards').alias('total_drives'),
            pl.mean('yards').alias('avg_yards_per_drive'),
            (pl.sum('touchdown') / pl.count('yards') * 100).alias('td_percentage'),
            (pl.sum('turnover') / pl.count('yards') * 100).alias('turnover_percentage')
        ]).sort('avg_yards_per_drive', descending=True).head(10)

        return team_stats.to_dicts()

    q14 = analyze_offensive_performance()
    print(f"Top 10 teams by average yards per drive:")
    for i, team in enumerate(q14, 1):
        print(f"  {i}. {team['team']}: {team['avg_yards_per_drive']:.2f} avg yards/drive")
        print(f"     Total drives: {team['total_drives']}, TD%: {team['td_percentage']:.1f}%, Turnover%: {team['turnover_percentage']:.1f}%")
    return (q14,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Bonus Question (5 points)
    **Locate and retrieve a video highlight URL from one of the games.**
    """
    )
    return


@app.cell
def _(game_dict):
    # Video highlight URL - extracted from JSON data
    def get_video_from_data():
        # Search through games for videos
        for filename, game_data in game_dict.items():
            if 'videos' in game_data and len(game_data['videos']) > 0:
                video = game_data['videos'][0]
                if 'links' in video and 'web' in video['links']:
                    return {
                        'url': video['links']['web']['href'],
                        'headline': video.get('headline', 'No headline'),
                        'description': video.get('description', 'No description'),
                        'game': filename
                    }
        return None

    bonus_data = get_video_from_data()
    bonus = bonus_data['url'] if bonus_data else "No video found"
    print(f"Video highlight URL: {bonus}")
    if bonus_data:
        print(f"  Headline: {bonus_data['headline']}")
        print(f"  From game: {bonus_data['game']}")
    return (bonus,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## Generate Answer File
    Compile all answers into a JSON file for submission.
    """
    )
    return


@app.cell
def _(
    bonus,
    q1,
    q10,
    q11,
    q12,
    q13,
    q14,
    q2,
    q3,
    q3_1,
    q4,
    q4_1,
    q5,
    q6,
    q6_1,
    q7,
    q8,
    q9,
):
    # Compile all answers into a single dictionary
    answer_file = {
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'q3.1': q3_1,
        'q4': q4,
        'q4.1': q4_1,
        'q5': q5,
        'q6': q6,
        'q6.1': q6_1,
        'q7': q7,
        'q8': q8,
        'q9': q9,
        'q10': q10,
        'q11': q11,
        'q12': q12,
        'q13': q13,
        'q14': q14,  
        'Bonus': bonus
    }
    return (answer_file,)


@app.cell
def _(answer_file, json):
    # Write answer file to JSON with pretty formatting
    output_filename = "mis511_python_project_lmitchek.json"

    with open(output_filename, "w") as outfile:
        json.dump(answer_file, outfile, indent=3)

    print(f"Answer file saved to: {output_filename}")
    return


if __name__ == "__main__":
    app.run()

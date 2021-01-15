import pandas as pd
import numpy as np



def average_data():
    game_data = pd.read_csv('game-data.csv')

    game_data['scheduled'] = pd.to_datetime(game_data['scheduled'])
    years = game_data['scheduled'].dt.year

    game_data = game_data.drop(columns = ['id', 'scheduled', 'away_team.points', 'home_team.points'])
    game_data = game_data.drop(columns = [
                                'away_team.statistics.goal_efficiency.team.td', 'away_team.statistics.passing.team.td',
                                'away_team.statistics.receiving.team.td', 'home_team.statistics.goal_efficiency.team.td',
                                'home_team.statistics.passing.team.td', 'home_team.statistics.receiving.team.td',
                                'home_team.statistics.redzone_efficiency.team.td', 'home_team.statistics.rushing.team.td',
                                'away_team.statistics.rushing.team.td', 'away_team.statistics.passing.team.td_pct',
                                'home_team.statistics.passing.team.td_pct'])

    away_data = game_data.iloc[:, :121]
    home_data = game_data.iloc[:, 121:]


    away_data = away_data.assign(year = years)
    home_data = home_data.assign(year = years)


    away_data = away_data.groupby(['away_team.id', 'year']).mean().reset_index()
    home_data = home_data.groupby(['home_team.id', 'year']).mean().reset_index()

    return away_data, home_data


#input_array = [away team, home team, year]
def get_inputs(input_array, away_data, home_data):
    year = int(input_array[-1]) - 1
    away_team = str(input_array[0])
    home_team = str(input_array[1])

    away_stats = away_data[(away_data['year'] == year) & (away_data['away_team.id'] == away_team)]
    home_stats = home_data[(home_data['year'] == year) & (home_data['home_team.id'] == home_team)]

    away_stats = away_stats.drop(columns = ['year', 'away_team.id'])
    home_stats = home_stats.drop(columns = ['year', 'home_team.id'])

    return np.concatenate((away_stats.to_numpy().flatten(), home_stats.to_numpy().flatten()))




def avg_across_n_games(input_array, data, n, away_col = [], home_col = []):

    game_data = data.drop(columns = ['id', 'away_team.points', 'home_team.points'])
    game_data = game_data.sort_values('scheduled', ascending = False, ignore_index = True)

    game_data['scheduled'] = pd.to_datetime(game_data['scheduled'])
    dates = game_data['scheduled']

    game_data = game_data.drop(columns = ['scheduled', 'away_team.statistics.goal_efficiency.team.td',
    'away_team.statistics.passing.team.td','away_team.statistics.receiving.team.td',
    'home_team.statistics.goal_efficiency.team.td','home_team.statistics.passing.team.td',
    'home_team.statistics.receiving.team.td','home_team.statistics.redzone_efficiency.team.td',
    'home_team.statistics.rushing.team.td','away_team.statistics.rushing.team.td',
    'away_team.statistics.passing.team.td_pct','home_team.statistics.passing.team.td_pct'])

    away_team = str(input_array[0])
    home_team = str(input_array[1])
    day = int(input_array[2])
    month = int(input_array[3])
    year = int(input_array[4])

    game_data_years = game_data[(dates.dt.year < year)]
    game_data_months = game_data[(dates.dt.year == year) & (dates.dt.month < month)]
    game_data_days = game_data[(dates.dt.year == year) & (dates.dt.month == month) & (dates.dt.day < day)]


    #game_data = game_data[(dates.dt.year == 2018)]
    game_data = pd.concat([game_data_years, game_data_months, game_data_days])



    away_data = game_data.iloc[:, 0:121]
    home_data = game_data.iloc[:, 121:]

    team1 = away_data[away_data['away_team.id'] == away_team]
    team2 = home_data[home_data['home_team.id'] == home_team]

    team1_avg = team1.drop(columns = ['away_team.id']).iloc[:n, :].mean()
    team2_avg = team2.drop(columns = ['home_team.id']).iloc[:n, :].mean()

    if away_col:
        team1_avg = team1_avg[away_col]
    if home_col:
        team2_avg = team2_avg[home_col]


    return np.concatenate([team1_avg.to_numpy().flatten(), team2_avg.to_numpy().flatten()])



game_data = pd.read_csv('game-data.csv')

test_array = np.array([['KC', 'ATL', 10, 10, 2017], ['NE', 'OAK', 30, 9, 2019]])

stats = np.apply_along_axis(avg_across_n_games, 1, test_array, game_data, 5,
away_col = ['away_team.remaining_challenges', 'away_team.remaining_timeouts'], home_col = ['home_team.statistics.defense.team.int'])

print(stats)

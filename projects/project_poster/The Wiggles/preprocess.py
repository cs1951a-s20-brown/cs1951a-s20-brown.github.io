import pandas as pd
import numpy as np
import tensorflow as tf
from game_test import avg_across_n_games, get_inputs, average_data
from sklearn.preprocessing import MinMaxScaler


def preprocess(filename, mode = 'shuffle', away_col = [], home_col = []):
    np.random.seed(0)
    scaler = MinMaxScaler()
    df = pd.read_csv(filename)

    df['home_wins'] = 0
    for i in range(len(df)):
        # this also has ties going to hometeam.... check
        if df.loc[i, 'home_team.points'] >= df.loc[i, 'away_team.points']:
            df.loc[i, 'home_wins'] = 1

    df['scheduled'] = pd.to_datetime(df['scheduled'])
    df['year'] = df['scheduled'].dt.year
    df['day'] = df['scheduled'].dt.day
    df['month'] = df['scheduled'].dt.month

    df = df.sort_values('scheduled')

    input_df = df.drop(columns=['away_team.id', 'home_team.id',
                           'away_team.points', 'home_team.points', 'id', 'scheduled', 'home_wins',
                           'away_team.statistics.goal_efficiency.team.td', 'away_team.statistics.passing.team.td',
                           'away_team.statistics.receiving.team.td', 'home_team.statistics.goal_efficiency.team.td',
                           'home_team.statistics.passing.team.td', 'home_team.statistics.receiving.team.td',
                           'home_team.statistics.redzone_efficiency.team.td', 'home_team.statistics.rushing.team.td',
                           'away_team.statistics.rushing.team.td', 'away_team.statistics.passing.team.td_pct',
                           'home_team.statistics.passing.team.td_pct'])


    total_col = away_col + home_col + ['year', 'month', 'day']

    if (away_col) or (home_col):
        input_df = input_df.loc[:, total_col]

    df_no_2019 = input_df[input_df.year != 2019].drop(columns = ['year', 'day', 'month'])
    df_only_2019 = input_df[input_df.year == 2019].drop(columns = ['year', 'day', 'month'])


    for i in range(len(df_no_2019)):
        no_2019_labels = df[df['year'] != 2019]['home_wins'].to_numpy()

    for i in range(len(df_no_2019)):
        only_2019_labels = df[df['year'] == 2019]['home_wins'].to_numpy()

    features_no_2019 = df_no_2019.to_numpy()
    features_only_2019 = df_only_2019.to_numpy()

    df_test = df[df.year == 2019]
    num_ex = len(no_2019_labels)

    all_together_scale = scaler.fit_transform(np.concatenate((features_no_2019, features_only_2019), axis = 0))
    features_no_2019 = all_together_scale[:num_ex]
    features_only_2019 = all_together_scale[num_ex:]

    indices = np.arange(num_ex)
    np.random.shuffle(indices)

    x_train = features_no_2019[indices, :]
    y_train = no_2019_labels[indices]

    num_test = len(only_2019_labels)
    split = round(num_test * 0.5)

    indices = np.arange(num_test)
    np.random.shuffle(indices)

    shuf_test = features_only_2019[indices, :]
    shuf_testl = only_2019_labels[indices]

    x_val = shuf_test[:split,:]
    y_val = shuf_testl[:split]

    x_test = shuf_test[split:]
    y_test = shuf_testl[split:]


    x_avg = df_test[['away_team.id', 'home_team.id', 'day', 'month', 'year']].to_numpy()[indices][split:]

    #away_data, home_data = average_data()
    #avg_stats = np.apply_along_axis(get_inputs, 1, x_avg, away_data, home_data)

    avg_stats = np.apply_along_axis(avg_across_n_games, 1, x_avg,
    df.drop(columns = ['home_wins', 'year', 'month', 'day']), 5, away_col = away_col, home_col = home_col)
    print('avg_stats', avg_stats.shape)

    df_no_2019.to_csv('game-data-no-2019.csv')
    df_only_2019.to_csv('game-data-only-2019.csv')




    return x_train, x_test, x_val, y_train, y_test, y_val, avg_stats

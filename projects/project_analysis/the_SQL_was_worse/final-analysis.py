import sqlite3
import numpy as np
import pandas as pd
import json
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures
import matplotlib.pylab as plt
#import seaborn as sns


def split_data(data, prob):
    test = []
    train = []
    for entry in data:
        if random.random() < prob:
            test.append(entry)
        else:
            train.append(entry)
    return train, test

def train_test_split(x, y, test_pct):
    x_tr = []
    x_te = []
    y_tr = []
    y_te = []
    xy_list = list(zip(x, y))
    train_data, test_data = split_data(xy_list, test_pct)
    for i in range(len(train_data)):
        x_tr.append(train_data[i][0])
        y_tr.append(train_data[i][1])
    for j in range(len(test_data)):
        x_te.append(test_data[j][0])
        y_te.append(test_data[j][1])
    return x_tr, x_te, y_tr, y_te

def get_region(birthplace):
    birthplace_string = json.dumps(birthplace).lower().strip('"') # e.g. "La Jolla, Ca" or "Ilford, Essex, England"
    if birthplace_string.endswith((', ca', ', or', ', wa', ', nv', ', hi', ', ak')):
        return 'far west'
    elif birthplace_string.endswith((', mt', ', id', ', wy', ', ut', ', co')):
        return 'rocky mountain'
    elif birthplace_string.endswith((', az', ', nm', ', tx', ', ok')):
        return 'southwest'
    elif birthplace_string.endswith((', nd', ', sd', ', ne', ', ks', ', mn', ', ia', ', mo')):
        return 'plains'
    elif birthplace_string.endswith((', wi', ', mi', ', il', ', in', ', oh')):
        return 'great lakes'
    elif birthplace_string.endswith((', ar', ', la', ', ky', ', wv', ', va', ', tn', ', nc', ', ms', ', al', ', ga', ', sc', ', fl')):
        return 'southeast'
    elif birthplace_string.endswith((', ny', ', pa', ', nj', ', md', ', de', ', dc')) or birthplace_string == 'new york city':
        return 'mideast'
    elif birthplace_string.endswith((', vt', ', nh', ', me', ', ct', ', ri', ', ma')):
        return 'new england'
    elif birthplace_string == 'na':
        return np.nan
    else:
        return 'international'

if __name__=='__main__':

    random.seed(1)
    p = 0.2

    def load_file(file_path):

        # Create dataframes
        actor_success_threshold = []
        conn = sqlite3.connect(file_path)
        df_allmovies = pd.read_sql_query("SELECT * FROM allmovies ORDER BY release_date", conn)
        df_dems = pd.read_sql_query("SELECT * FROM demographics", conn)

        # Add a new 'region' column to the demographics dataframe. Entry may be NaN.
        df_dems['region'] = df_dems['birthplace'].map(lambda x: get_region(x))

        # Create the dependent variable
        try:
            y = pd.read_csv('actor_success_threshold.csv')
        except IOError as e:
        	print('No actor_success_threshold.csv file found, generating new file...')
	        actors = df_dems[['entity']].values
	        for actor in actors:
	            count = 0
	            for row in df_allmovies.itertuples():
	                row_string = json.dumps(row[8])
	                found = row_string.find(actor[0])
	                rating = float(row[6] or 0.0)
	                revenue = float(row[5] or 0.0)
	                if found != -1:
	                    count += 1
	                    if rating > 7.5:
	                        break
	            actor_success_threshold.append(count)
	        y = pd.DataFrame(actor_success_threshold, columns=['actor_success_threshold'])
	        y.to_csv('actor_success_threshold.csv', index=False)

	    # Select independent variables
        X_race = pd.get_dummies(df_dems['race_ethnicity'].apply(json.dumps), drop_first=True)
        X_region = pd.get_dummies(df_dems['region'], drop_first=True)
        X_sexuality = pd.get_dummies(df_dems['sexual_orientation'].apply(json.dumps), drop_first=True)
       	X = X_sexuality

        # Plotting
        df_for_plot = pd.concat((df_dems, y), axis=1)
        # https://seaborn.pydata.org/tutorial/categorical.html
        #sns.set(style="ticks", color_codes=True)
        # sns.catplot(x="race_ethnicity", y="actor_success_threshold", kind="box", data=df_for_plot)
        #sns.catplot(x="sexual_orientation", kind="count", data=df_for_plot)
        plt.show()

        X = X.values
        y = y.values
        return X, y

    X, y = load_file("data/oscars.db")


    x_train, x_test, y_train, y_test = train_test_split(X, y, p)

    x_train = sm.add_constant(x_train)
    model = sm.OLS(y_train, x_train)
    ret = model.fit()
    train_predictions = ret.predict(x_train)
    print('Train MSE: ', eval_measures.mse(y_train, train_predictions, axis = 0))
    x_test = sm.add_constant(x_test)
    test_predictions = ret.predict(x_test)
    print('Test MSE: ', eval_measures.mse(y_test, test_predictions, axis = 0))

    print(ret.summary())
    print('R-Squared: ', ret.rsquared)

    fig, ax = plt.subplots()
    fig = sm.graphics.plot_fit(ret, 0, ax=ax)
    ax.set_ylabel("Credits to Success")
    ax.set_title("Multiple Linear Regression")
    fig.savefig('regression.png', dpi=125)
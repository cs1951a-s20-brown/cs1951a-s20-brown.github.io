import numpy as np
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, LSTM
from preprocess import preprocess
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.svm import SVC
import pandas as pd
import random

import seaborn as sns
from sklearn import metrics
#from seqModel import preprocess


def main(mod_type = 'dense'):
    tf.random.set_seed(25)
    np.random.seed(25)
    random.seed(25)
    input_size = 100  # Size of team statistic input vectors
    num_classes = 2  # Number of classes/possible labels
    batch_size = 100
    learning_rate = 0.0001
    MAX_NUM_OF_EPOCHS = 500

    print("Got to main!")



    x_train, x_test, x_validation, y_train, y_test, y_validation, x_avg = preprocess(
        'game-data.csv', mode = 'shuffle')

    num_examples = len(x_train)

    print("finished preprocessing...")

    model = Sequential()


    model.add(Dense(input_size, activation='relu', input_dim=232))
    #model.add(Dropout(0.3))
    model.add(Dense(1, activation='sigmoid'))


    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print("START OF TRAIN")

    history = model.fit(x_train, y_train, epochs=200, batch_size=batch_size, validation_data = (x_validation, y_validation))


    train_scores = history.history['accuracy']
    val_scores = history.history['val_accuracy']

    plt.plot(range(200), train_scores, label = 'training')
    plt.plot(range(200), val_scores, label = 'validation')

    plt.ylabel('Accuracy')
    plt.xlabel('No. epoch')

    plt.legend(loc="upper left")

    plt.show()

    scoreVal = model.evaluate(x_validation, y_validation, batch_size=batch_size)
    scoreTest = model.evaluate(x_test, y_test, batch_size=batch_size)
    print("\nscoreVal: ", scoreVal)
    print("scoreTest: ", scoreTest)


    score_avg = model.evaluate(x_avg, y_test, batch_size = batch_size)
    print('Score Avg: ', score_avg)

    x_random_train = np.random.randint(0, 10, (1673, 232))
    y_random_train = np.random.randint(0, 10, 1673)

    logReg = LogisticRegression(random_state=0).fit(x_random_train, y_random_train)
    print("Logistic Regression Score Avg Without Training: ", logReg.score(x_avg, y_test))

    logReg = LogisticRegression(random_state=0).fit(x_train, y_train)
    print("\nLogistic Regression Score: ", logReg.score(x_test, y_test))

    #logReg = LogisticRegression(random_state=0).fit(x_train, y_train)
    predictions = logReg.predict(x_avg)
    scoreAvg = logReg.score(x_avg, y_test)
    print("Logistic Regression Score Avg: ", scoreAvg)
    cm = metrics.confusion_matrix(y_test, predictions)

    plt.figure(figsize=(9,9))
    sns.heatmap(cm, annot=True, fmt=".3f", linewidths=0.1, square = True, cmap = 'Blues_r');
    plt.ylabel('Actual label');
    plt.xlabel('Predicted label');
    all_sample_title = 'Accuracy Score: {0}'.format(scoreAvg)
    plt.title(all_sample_title, size = 15);
    #plt.show()

    coefficients = logReg.coef_
    reshapedCoefficients = np.squeeze(np.transpose(coefficients))
    topTenFeatures = np.argsort(np.absolute(reshapedCoefficients))[-10:]
    print("topTenFeatures", topTenFeatures)
    df = pd.read_csv('game-data.csv')
    input_df = df.drop(columns=['away_team.id', 'home_team.id',
                           'away_team.points', 'home_team.points', 'id', 'scheduled',
                                'away_team.statistics.goal_efficiency.team.td', 'away_team.statistics.passing.team.td',
                                'away_team.statistics.receiving.team.td', 'home_team.statistics.goal_efficiency.team.td',
                                'home_team.statistics.passing.team.td', 'home_team.statistics.receiving.team.td',
                                'home_team.statistics.redzone_efficiency.team.td', 'home_team.statistics.rushing.team.td',
                                'away_team.statistics.rushing.team.td', 'away_team.statistics.passing.team.td_pct', 'home_team.statistics.passing.team.td_pct'])

    topTenColumns = input_df.columns[topTenFeatures].to_numpy()
    print("topTenColumns: ", topTenColumns)
    heatMapDf = input_df[topTenColumns]
    myCorr = heatMapDf.corr()
    plt.figure(figsize=(12,12))
    sns.heatmap(myCorr, annot=True, fmt=".1f", linewidths=0.1, square = True)
    plt.ylabel('Features');
    plt.xlabel('Features');
    plt.show()



    svm = SVC(random_state = 0).fit(x_train, y_train)
    print("\nSVM Score: ", svm.score(x_test, y_test))
    print("SVM Score Avg: ", svm.score(x_avg, y_test))

    # top ten feature columns
    away_col = ['away_team.statistics.fumbles.team.lost', 'away_team.statistics.kickoffs.team.ret', 'away_team.statistics.fourth_down_efficiency.team.att', 'away_team.statistics.passing.team.rating']
    home_col = ['home_team.statistics.kickoffs.team.kicks', 'home_team.statistics.kickoffs.team.yds', 'home_team.statistics.kickoffs.team.net_yds', 'home_team.statistics.passing.team.cmp_pct',
    'home_team.statistics.fourth_down_efficiency.team.att',
    'home_team.statistics.passing.team.rating']

    # removed feature columns with high correlation (removed only one from each pair of correlated features)
    away_col2 = ['away_team.statistics.fumbles.team.lost', 'away_team.statistics.kickoffs.team.ret', 'away_team.statistics.fourth_down_efficiency.team.att', 'away_team.statistics.passing.team.rating']
    home_col2 = ['home_team.statistics.kickoffs.team.kicks',
    'home_team.statistics.fourth_down_efficiency.team.att',
    'home_team.statistics.passing.team.rating']

    x_train, x_test, x_validation, y_train, y_test, y_validation, x_avg = preprocess(
        'game-data.csv', mode = 'shuffle', away_col = away_col, home_col = home_col)

    logReg2 = LogisticRegression(random_state=0).fit(x_train, y_train)
    scoreAvg2 = logReg2.score(x_avg, y_test)
    print("Logistic Regression2 Score Avg: ", scoreAvg2)

    x_train, x_test, x_validation, y_train, y_test, y_validation, x_avg = preprocess(
        'game-data.csv', mode = 'shuffle', away_col = away_col2, home_col = home_col2)

    logReg3 = LogisticRegression(random_state=0).fit(x_train, y_train)
    scoreAvg3 = logReg3.score(x_avg, y_test)
    print("Logistic Regression Correlated Values Removed Score Avg: ", scoreAvg3)

if __name__ == '__main__':
    main()

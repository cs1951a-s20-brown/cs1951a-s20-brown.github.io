import numpy as np
import pandas as pd
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures
from sklearn.model_selection import train_test_split




def load_file(file_path):
    df = pd.read_csv(file_path, delimiter=',')
    df = df.dropna()
    X = df[['donationamount', 'candidatewonlost']]
    y = df['percentchangeinstockprice']
    return X, y



X, y = load_file("data/consolidated-donation-data.csv")


file = open("data/consolidated-donation-data.csv", 'r')
# get the line reader past the bull shit header
line = file.readline()
line = file.readline()

candsToComps = dict()
compsToCands = dict()
# 0 for comps 1 for reps
# label is cand name or stock ticker
# type (comp/cand) 0/1
# name/ticker
# type, id, cand win lost, percent change, neighbors
# candidate,donationamount,candidatewonlost,companystockticker,percentchangeinstockprice
links = []
while line:
    line = line.split(",")
    if len(line) == 6:
        candName = line[0] + "," + line[1]
        candName = candName.replace('"', '')
        companyTicker = line[4]
        donationAmount = line[2]
        links.append([companyTicker, candName, donationAmount])
        if candName not in candsToComps:
            candsToComps[candName] = []
        else:
            currList = candsToComps[candName]
            currList.append(companyTicker)
            candsToComps[candName] = currList
        if companyTicker not in compsToCands:
            compsToCands[companyTicker] = [candName]
        else:
            currList = compsToCands[companyTicker]
            currList.append(candName)
            compsToCands[companyTicker] = currList
        line = file.readline()
    else:
        # fucking mark gladney didnt have a comma in his name like everyone else
        candName = line[0]
        candName = candName.replace('"', '')
        companyTicker = line[3]
        if candName not in candsToComps:
            candsToComps[candName] = []
        else:
            currList = candsToComps[candName]
            currList.append(companyTicker)
            candsToComps[candName] = currList
        if companyTicker not in compsToCands:
            compsToCands[companyTicker] = [candName]
        else:
            currList = compsToCands[companyTicker]
            currList.append(candName)
            compsToCands[companyTicker] = currList
        line = file.readline()



#nodes.csv
with open('nodes.csv', 'w', newline='') as csvfile:
    myCsvWriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    #type,id,candidatewinlost,percentchangeinstockprice
    file = open("data/consolidated-donation-data.csv", 'r')
    myCsvWriter.writerow(['type', 'id', 'candidatewinlost', 'percentchangeinstockprice', 'neighbors'])
    #clear the bullshit
    line = file.readline()
    line = file.readline()
    comps = set()
    cands = set()
    while line:
        line = line.split(",")
        # print(line)
        # print(len(line))
        if len(line) == 6:
            candName = line[0] + "," + line[1]
            candName = candName.replace('"', '')
            wonLost = line[3]
            companyTicker = line[4]
            percentChange = line[5]
            if companyTicker not in comps:
                comps.add(companyTicker)
                myCsvWriter.writerow(['0', companyTicker, "", percentChange[:-2], compsToCands[companyTicker]])
            if candName not in cands:
                cands.add(candName)
                myCsvWriter.writerow(['1', candName, wonLost, "", candsToComps[candName]])
            line = file.readline()
        else:
            # fucking mark gladney didnt have a comma in his name like everyone else
            candName = line[0]
            candName = candName.replace('"', '')
            wonLost = line[2]
            companyTicker = line[3]
            percentChange = line[4]
            if companyTicker not in comps:
                comps.add(companyTicker)
                myCsvWriter.writerow(['0', companyTicker, "", percentChange, compsToCands[companyTicker]])
            if candName not in cands:
                cands.add(candName)
                myCsvWriter.writerow(['1', candName, wonLost, "", candsToComps[candName]])
            line = file.readline()

#links.csv
with open('links.csv', 'w', newline='') as csvfile:
    myCsvWriter = csv.writer(csvfile, delimiter=',')
    myCsvWriter.writerow(['target', 'source', 'donationamount'])
    for line in links:
        myCsvWriter.writerow([line[0], line[1], line[2]])

import requests
import sqlite3
import urllib
import os, glob
import pandas as pd


degree_dict = {11:  'farming agri', 13:  'environmental work', 14:  'architecture', 15:  'ethnic civ studies', 19:  'communications', 20:  'Communication technologies', 21:  'Computer science', 22: 'COSMETOLOGY SERVICES AND CULINARY ARTS', 23:  'Education', 24:  'Engineering', 25:  'Engineering Technologies', 26:  'Linguistics', 29:  'family consumer Sciences', 32:  'Legal', 33:  'Literature', 34:  'Liberal arts', 35:  'Library science', 36:  'Biology', 37:  'Math', 38:  'Military Tech', 40:  'Interdisciplinary Science', 41:  'Parks rec', 48:  'Philosophy religion', 49:  'Philosophy religion', 50:  'Physical Sciences', 51: 'Nuclear Technologies',52:  'Psychology', 53: 'Criminal Justice and Fire Protection', 54:  'Public work', 55: 'Social Sciences', 56:  'Construction', 57:  'Misc technology', 59:  'Transportation', 60:  'Fine Arts', 61:  'Medical', 62:  'Business', 64:  'History'}
occp_dict = {0: 'Manager', 50: 'Business', 80: 'Finance', 100: 'Computer Science', 130: 'Engineering', 160: 'Sciences', 200: 'Social Worker', 210: 'Legal', 220: 'Education', 260: 'Entertainment', 300: 'Medical', 360: 'Health Aides', 370: 'Public Defense Workers', 400: 'Food', 420: 'Cleaning', 430: 'Personal Work', 470: 'Sales',  500: 'Clerks', 600: 'Forestry', 620: 'Contractors', 680: 'Extraction', 700: 'Repairers', 770: 'Production', 900: 'transportation', 980: 'Military', 990: 'Unemployed'}
wkw_dict = {1:51, 2:48.5, 3:43.5, 4:33, 5:20, 6:7}

def round_down(x, l):
    import bisect

    if x in l:
        return x
    i = bisect.bisect_right(l,x)
    return l[i-1]


def clean_data():

    data = pd.read_csv("data/trimmed_data.csv")
    d1 = data[data.WAGP > 0]
    d1["YOEP"].fillna(2019, inplace = True) 
    d1["YOEP"] = d1["YOEP"].apply(yoep_to_exp)
    d1["Approximate weeks worked"] = d1["WKW"].apply(weeks_worked)
    d1["Approximate hours worked"] = hours_worked(d1['WKW'], d1['WKHP'])
    d1["Degree"] = d1["FOD1P"].apply(categorize_degree)
    d1["Degree 2"] = d1["FOD2P"].apply(categorize_degree)
    d1["Occupation"] = d1["OCCP"].apply(categorize_occp)

    d1.to_csv('analysis_data.csv')


def weeks_worked(wkw):
    return wkw_dict[wkw]

def hours_worked(wkw, wkhp):
    k = wkw[1]
    
    annual_hours = wkw_dict[k]*wkhp
    return annual_hours

def yoep_to_exp(yoep):
    return 2018 - yoep

def categorize_degree(fod1p):
    import math
    if math.isnan(fod1p):
        return "No Degree"
    degree = str(fod1p)[0:2]
    k = int(degree)
    return degree_dict[k]

def categorize_occp(occp):
    
    
    occp  = str(occp/10)

    k = float(occp)
    l = list(occp_dict.keys())
    k = round_down(k, l)
    return occp_dict[k]



clean_data()

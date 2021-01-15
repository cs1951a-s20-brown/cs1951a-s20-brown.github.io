#from bs4 import BeautifulSoup
import requests
import sqlite3
import urllib

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]




def download_csvs():
    url ='https://www2.census.gov/programs-surveys/acs/data/pums/2018/1-Year/csv_p'
    import requests, zipfile, io

    for state in states:
        zipurl = url + state.lower() + '.zip'
        print(zipurl)
        r = requests.get(zipurl)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()

def merge_csvs():


    import os, glob
    import pandas as pd

    path ="data"
    allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    frame = pd.concat(list_)
    frame.to_csv('data/merged_data.csv', encoding='utf-8', index=False)



def filter_nulls():
    import pandas as pd 
  
    
    data = pd.read_csv("data/merged_data.csv") 

    bool_series = pd.notnull(data["FOD1P"]) 
    data[bool_series].to_csv('data.csv', encoding='utf-8', index=False)


def trim_cols(columns):
    import pandas as pd

    df = pd.read_csv("data/data.csv", usecols = columns)
    df.to_csv('trimmed_data.csv', encoding='utf-8', index=False)
    
  
   
columns = ['REGION', 'ST', 'WAGP', 'FOD1P', 'FOD2P', 'SCHG', 'SCHL', 'SEX', 'YOEP', 'WKHP', 'WKW', 'OCCP']

trim_cols(columns)

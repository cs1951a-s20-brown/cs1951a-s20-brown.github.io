import numpy as np
import pandas as pd
import sqlite3
import re
import requests
from io import StringIO
from os import listdir
from preprocess_zillow import add_to_db, read_data

# DATA PROCESSING
def process_airbnb_data(df, cols_to_keep, money_cols):
    # Select certain columns from the downloaded CSV
    df = df[cols_to_keep]

    # Remove rows with no zipcodes
    df = df.dropna(subset = ['zipcode'])
    # Extracts zip codes using a regex
    df['zipcode'] = df['zipcode'].map(lambda x: re.findall('\\d{5}|$', x)[0] if isinstance(x, str) else x)
    df = df[df['zipcode'] != '']
    # Finally changes the type now that we've removed zip codes that can't be parsed into integers, like 12345-6789
    df['zipcode'] = df['zipcode'].astype(int, copy=False)

    # Now we convert any column in money_cols to FLOAT
    for col in money_cols:
        df[col] = df[col].str.replace('$', '').str.replace(',', '')
        df[col] = df[col].astype(float, copy=False)

    return df
    
def main():
    local_csv_files = ['./data/airbnb/' + file_name for file_name in listdir('./data/airbnb/')]
    path_to_db = './data/housing.db'
    cols_to_keep = ['id', 'last_scraped', 'street', 'neighbourhood_cleansed', 'city', 'state', 'zipcode', 'latitude', 'longitude', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'price', 'weekly_price', 'monthly_price', 'security_deposit', 'cleaning_fee', 'minimum_nights', 'maximum_nights', 'calendar_updated', 'availability_30', 'availability_60', 'availability_90']
    money_cols = ['price', 'weekly_price', 'monthly_price', 'security_deposit', 'cleaning_fee']

    all_cities_df = pd.DataFrame()
    for path in local_csv_files:
        df = read_data(path)
        print("Finished reading data from {}".format(path))

        df = process_airbnb_data(df, cols_to_keep, money_cols)
        print("Finished processing data from {}".format(path))

        all_cities_df = all_cities_df.append(df)

    add_to_db(all_cities_df, path_to_db, 'airbnb')
    print("Finished processing data from {}".format(path))




if __name__ == "__main__":
    main()
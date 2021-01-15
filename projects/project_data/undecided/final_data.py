import numpy as np
import csv
import random
import math
import pandas as pd
from statsmodels.tools import eval_measures
from bs4 import BeautifulSoup
import requests
import sqlite3
import matplotlib as plt
   

conn = sqlite3.connect('final_data.db')
c = conn.cursor()

# saving rate of each country year 2000 - 2018
df = pd.read_csv('savings.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "savings";')
c.execute('CREATE TABLE savings(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# turn df into sql, taken from https://datatofish.com/pandas-dataframe-to-sql/
df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
# df = df.sample(frac=0.1, replace=True, random_state=1)
df.to_sql('savings',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM savings''')
# for row in c.fetchall():
#     print(row)

# unemployment rate of each country year 2000 - 2018
df = pd.read_csv('unemployment.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "unemployment";')
c.execute('CREATE TABLE unemployment(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('unemployment',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM unemployment''')
# for row in c.fetchall():
#     print(row)

# percentage of each gender of each country year 2000 - 2018
c.execute('DROP TABLE IF EXISTS "gender";')
c.execute('CREATE TABLE gender(country text PRIMARY KEY, zero_male real, one_male real, two_male real, three_male real, four_male real, five_male real, six_male real, seven_male real, eight_male real, nine_male real, ten_male real, eleven_male real, twelve_male real, thirteen_male real, fourteen_male real, fifteen_male real, sixteen_male real, seventeen_male real, eighteen_male real, \
	zero_female real, one_female real, two_female real, three_female real, four_female real, five_female real, six_female real, seven_female real, eight_female real, nine_female real, ten_female real, eleven_female real, twelve_female real, thirteen_female real, fourteen_female real, fifteen_female real, sixteen_female real, seventeen_female real, eighteen_female real)')
conn.commit()
li = []
df = pd.read_csv('male.csv', header=0, escapechar='\\')
li.append(df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']])
df = pd.read_csv('female.csv', header=0, escapechar='\\')
df = df[['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# rename female's columns so we can concatenate the dataframe
df.columns = ['2000f','2001f','2002f','2003f','2004f','2005f','2006f','2007f','2008f','2009f','2010f','2011f','2012f','2013f','2014f','2015f','2016f','2017f','2018f']
li.append(df)
df = pd.concat(li, axis=1)
df.to_sql('gender',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM gender''')
# for row in c.fetchall():
#     print(row)

#total population for each country, year 2000 - 2018
df = pd.read_csv('total_population.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "total_population";')
c.execute('CREATE TABLE total_population(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('total_population',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM total_population''')
# for row in c.fetchall():
#     print(row)

#population density for each country, year 2000 - 2018
df = pd.read_csv('population_density.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "population_density";')
c.execute('CREATE TABLE population_density(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('population_density',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM population_density''')
# for row in c.fetchall():
#     print(row)

#nominal gdp for each country, year 2000 - 2018
df = pd.read_csv('nominal_gdp.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "nominal_gdp";')
c.execute('CREATE TABLE nominal_gdp(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('nominal_gdp',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM nominal_gdp''')
# for row in c.fetchall():
#     print(row)

#nominal gdp per capita for each country, year 2000 - 2018
df = pd.read_csv('nominal_gdp_per_capita.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "nominal_gdp_per_capita";')
c.execute('CREATE TABLE nominal_gdp_per_capita(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('nominal_gdp_per_capita',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM nominal_gdp_per_capita''')
# for row in c.fetchall():
#     print(row)

#gdp growth for each country, year 2000 - 2018
df = pd.read_csv('gdp_growth.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "gdp_growth";')
c.execute('CREATE TABLE gdp_growth(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('gdp_growth',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM gdp_growth''')
# for row in c.fetchall():
#     print(row)

# age dependency ratio of working age, for each country, year 2000 - 2018
df = pd.read_csv('age_old.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "age_old";')
c.execute('CREATE TABLE age_old(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('age_old',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM age_old''')
# for row in c.fetchall():
#     print(row)

# age dependency ratio of young, for each country, year 2000 - 2018
df = pd.read_csv('age_young.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "age_young";')
c.execute('CREATE TABLE age_young(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('age_young',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM age_young''')
# for row in c.fetchall():
#     print(row)

# literacy rate of young, for each country, year 2000 - 2018
df = pd.read_csv('literacy_rate.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "literacy_rate";')
c.execute('CREATE TABLE literacy_rate(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('literacy_rate',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM literacy_rate''')
# for row in c.fetchall():
#     print(row)

# educational attainment, for each country, year 2000 - 2018
df = pd.read_csv('education.csv', header=0, escapechar='\\')
c.execute('DROP TABLE IF EXISTS "education";')
c.execute('CREATE TABLE education(country text PRIMARY KEY, zero real, one real, two real, three real, four real, five real, six real, seven real, eight real, nine real, ten real, eleven real, twelve real, thirteen real, fourteen real, fifteen real, sixteen real, seventeen real, eighteen real)')
conn.commit()
df = df[['Country Name','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
# df = df.drop([df.index[7], df.index[61], df.index[62], df.index[63], df.index[64], df.index[65], df.index[68], df.index[73], df.index[74], df.index[95], df.index[98], df.index[102], df.index[103], df.index[104], df.index[105], df.index[107], df.index[110], df.index[128], df.index[135], df.index[136], df.index[139], df.index[140], df.index[142], df.index[153], df.index[156], df.index[161], df.index[170], df.index[181], df.index[183], df.index[196], df.index[197], df.index[198], df.index[218], df.index[230], df.index[231], df.index[236], df.index[238], df.index[240], df.index[241], df.index[249], df.index[259]])
df.to_sql('education',conn,if_exists='replace',index=False)
# c.execute('''SELECT * FROM education''')
# for row in c.fetchall():
#     print(row)



#Now we want to draw the curve for all the saving_rating data for all year to find out if there are any outliers to delete
# saving_data_testing_outliers = []

# a1 = df['saving_rate_2000']
# saving_data_testing_outliers.append(a1)
# plt.plot(a1,label='2000')
# #...maybe add a loop here...)
# a19 = df['saving_rate_2018']
# saving_data_testing_outliers.append(a19)
# plt.plot(a19,label='2018')
# plt.xlabel("along each year")
# plt.ylabel("saving rate")
# plt.legend()
# plt.show()





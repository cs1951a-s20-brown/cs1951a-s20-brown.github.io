import requests
import urllib
import os, glob
import pandas as pd
import statsmodels.api as sm

data = pd.read_csv("data/analysis_data.csv")
ind = [ 'SEX','YOEP', 'SCHL']
wkw_dict = {1:51, 2:48.5, 3:43.5, 4:33, 5:20, 6:7}

X = data[ind]
X = sm.tools.add_constant(X)
y = data['WAGP']/(data['Approximate hours worked'])
model = sm.OLS(y, X).fit()
predictions = model.predict(X)

print('OLS results of regressing hourly wage on sex, years of industry experience, and educational attainment')
print(model.summary())
#print(model.pvalues)
X1= data['SEX']
X1 = sm.tools.add_constant(X1)
model1 = sm.OLS(y, X1).fit()
predictions = model1.predict(X1)
print('OLS results of regressing hourly wage on sex')
print(model1.summary())
#print(model1.pvalues)

men = data.loc[data['SEX']== 1]
women =  data.loc[data['SEX'] == 2]
xmen = men[ind]
xmen = sm.tools.add_constant(xmen)
ymen = men['WAGP']/men['Approximate hours worked']
xwomen = women[ind]
xwomen = sm.tools.add_constant(xwomen)
ywomen = women['WAGP']/women['Approximate hours worked']
'''
print('men avg wagp / approximate hours worked: ')
print((men['WAGP']/men['Approximate hours worked']).mean())

print('women avg wagp / appz hours worked : ')
print((women['WAGP']/women['Approximate hours worked']).mean())


model2 = sm.OLS(ymen, xmen).fit()
predictions = model2.predict(xmen)
print(model2.summary())
model3 = sm.OLS(ywomen, xwomen).fit()
predictions = model3.predict(xwomen)
print(model3.summary())
'''
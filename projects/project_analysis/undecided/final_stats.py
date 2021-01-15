import numpy as np
import pandas as pd
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures
from statsmodels.tools.eval_measures import mse
import math

def split_data(data, prob):
	data = data.iloc[np.random.permutation(len(data))]
	data.reset_index(drop=True)
	split_idx = math.ceil(len(data)*prob)
	test_data = data[:split_idx]
	train_data = data[split_idx:]
	return train_data, test_data

def train_test_split(x, y, test_pct, file_name):
	x.insert(1,'y',y)
	train_data, test_data = split_data(x,test_pct)
	x_train = train_data[[file_name]]
	y_train = train_data['y']
	x_test = test_data[[file_name]]
	y_test = test_data['y']
	return x_train, x_test, y_train, y_test


if __name__=='__main__':
	random.seed(1)
	p = 0.2

	def load_xfile(file_path, file_name):
		with open(file_path, 'rb') as f:
			df_2018 = pd.read_csv(f,usecols=['2018'])
			df_2018.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2017 = pd.read_csv(f,usecols=['2017'])
			df_2017.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2016 = pd.read_csv(f,usecols=['2016'])
			df_2016.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2015 = pd.read_csv(f,usecols=['2015'])
			df_2015.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2014 = pd.read_csv(f,usecols=['2014'])
			df_2014.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2013 = pd.read_csv(f,usecols=['2013'])
			df_2013.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2012 = pd.read_csv(f,usecols=['2012'])
			df_2012.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2011 = pd.read_csv(f,usecols=['2011'])
			df_2011.columns = [file_name]
		with open(file_path, 'rb') as f:
			df_2010 = pd.read_csv(f,usecols=['2010'])
			df_2010.columns = [file_name]
		df_all = pd.concat([df_2018, df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011,df_2010])
		
		return df_all


	# def load_xfile(file_path, file_name):
	# 	with open(file_path, 'rb') as f:
	# 		df_2018 = pd.read_csv(f,usecols=['2018'])
	# 		df_2018.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2017 = pd.read_csv(f,usecols=['2017'])
	# 		df_2017.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2016 = pd.read_csv(f,usecols=['2016'])
	# 		df_2016.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2015 = pd.read_csv(f,usecols=['2015'])
	# 		df_2015.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2014 = pd.read_csv(f,usecols=['2014'])
	# 		df_2014.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2013 = pd.read_csv(f,usecols=['2013'])
	# 		df_2013.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2012 = pd.read_csv(f,usecols=['2012'])
	# 		df_2012.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2011 = pd.read_csv(f,usecols=['2011'])
	# 		df_2011.columns = [file_name]
	# 	with open(file_path, 'rb') as f:
	# 		df_2010 = pd.read_csv(f,usecols=['2010'])
	# 		df_2010.columns = [file_name]
	# 	df_all = pd.concat([df_2018, df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011,df_2010])
	# 	X = df_all[[file_name]]
	# 	X = sm.add_constant(X)
	# 	return X

	def load_yfile(file_path):
		with open(file_path, 'rb') as f:
			df_2018 = pd.read_csv(f,usecols=['2018'])
			df_2018.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2017 = pd.read_csv(f,usecols=['2017'])
			df_2017.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2016 = pd.read_csv(f,usecols=['2016'])
			df_2016.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2015 = pd.read_csv(f,usecols=['2015'])
			df_2015.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2014 = pd.read_csv(f,usecols=['2014'])
			df_2014.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2013 = pd.read_csv(f,usecols=['2013'])
			df_2013.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2012 = pd.read_csv(f,usecols=['2012'])
			df_2012.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2011 = pd.read_csv(f,usecols=['2011'])
			df_2011.columns = ['savings']
		with open(file_path, 'rb') as f:
			df_2010 = pd.read_csv(f,usecols=['2010'])
			df_2010.columns = ['savings']
		df_all=pd.concat([df_2018, df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011,df_2010],ignore_index=True)
		y = df_all['savings'].values
		return y

	file_unemployment = load_xfile("../project_data/unemployment.csv", 'unemployment')
	file_male = load_xfile("../project_data/male.csv", 'male')
	
	trial = file_unemployment + file_male

	print(trial)
	trial = file_unemployment[['male', 'unemployment']]
	X = trial
	X = sm.add_constant(X)





	# X = load_xfile("../project_data/unemployment.csv", 'unemployment')
	y = load_yfile("../project_data/savings.csv")

	x_train, x_test, y_train, y_test = train_test_split(X, y, p, 'unemployment')

	model = sm.OLS(y_train, x_train, missing='drop')
	results_train = model.fit()

	print(results_train.summary())


	

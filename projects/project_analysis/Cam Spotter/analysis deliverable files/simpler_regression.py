import numpy as np
import pandas as pd
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures

def split_data(data, prob):
    """input:
     data: a list of pairs of x,y values
     prob: the fraction of the dataset that will be testing data, typically prob=0.2
     output:
     two lists with training data pairs and testing data pairs
     """
    #TODO: Split data into fractions [prob, 1 - prob]. You can re-use the code from part I.
    size = len(data)
    train, test = [], []
    for i in range(size):
        if random.random() > prob:
            train.append(data[i])
        else:
            test.append(data[i])
    return train, test

def train_test_split(x, y, test_pct):
    """input:
    x: list of x values, y: list of independent values, test_pct: percentage of the data that is testing data=0.2.

    output: x_train, x_test, y_train, y_test lists
    """

    #TODO: Split the features X and the labels y into x_train, x_test and y_train, y_test as specified by test_pct.
    #You can re-use code from part I.
    train, test = split_data(list(zip(X,y)), p)
    x_train, x_test, y_train, y_test = [], [], [], []
    for pair in train:
        x_train.append(pair[0])
        y_train.append(pair[1])
    for pair in test:
        x_test.append(pair[0])
        y_test.append(pair[1])
    return x_train, x_test, y_train, y_test



if __name__=='__main__':

	# DO not change this seed. It guarantees that all students perform the same train and test split
    random.seed(1)
	# Setting p to 0.2 allows for a 80% training and 20% test split
    p = 0.2

	#############################################
	# TODO: open csv and read data into X and y #
	#############################################
    def load_file(file_path):
        """input: file_path: the path to the data file
		   output: X: array of independent variables values, y: array of the dependent variable values
		"""
		#TODO:
		#1. Use pandas to load data from the file. Here you can also re-use most of the code from part I.
		#2. Select which independent variables best predict the dependent variable count.
        x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, \
        x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, \
        x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, \
        x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, \
        x58, x59, x60, x61, x62, x63, x64, x65, x66, x67, x68, x69, x70, x71, \
        x72, x73, x74, x75, x76, x77, x78, x79, x80, x81, x82, x83, x84, x85, \
        x86, x87, x88, x89, x90, x91, x92, x93, x94, x95, x96, x97, x98, x99, \
        x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111, x112, x113, \
        y = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], []
        with open(file_path,'rb') as f:
            df = pd.read_csv(f)
        x1_raw, x2_raw, x3_raw= df['READ_PHONE_STATE'], df['GET_ACCOUNTS'], df['RECEIVE_SMS']
        x4_raw, x5_raw, x6_raw, x7_raw= df['READ_SMS'], df['USE_CREDENTIALS'], df['MANAGE_ACCOUNTS'], df['WRITE_SMS']
        x8_raw, x9_raw, x10_raw, x11_raw= df['READ_SYNC_SETTINGS'], df['AUTHENTICATE_ACCOUNTS'], df['WRITE_HISTORY_BOOKMARKS'], df['INSTALL_PACKAGES']
        x12_raw, x13_raw, x14_raw, x15_raw= df['CAMERA'], df['WRITE_SYNC_SETTINGS'], df['READ_HISTORY_BOOKMARKS'], df['INTERNET']
        x16_raw, x17_raw, x18_raw, x19_raw= df['RECORD_AUDIO'], df['NFC'], df['ACCESS_LOCATION_EXTRA_COMMANDS'], df['WRITE_APN_SETTINGS']
        x20_raw, x21_raw, x22_raw, x23_raw= df['BIND_REMOTEVIEWS'], df['READ_PROFILE'], df['MODIFY_AUDIO_SETTINGS'], df['READ_SYNC_STATS']
        x24_raw, x25_raw, x26_raw, x27_raw= df['BROADCAST_STICKY'], df['WAKE_LOCK'], df['RECEIVE_BOOT_COMPLETED'], df['RESTART_PACKAGES']
        x28_raw, x29_raw, x30_raw, x31_raw= df['BLUETOOTH'], df['READ_CALENDAR'], df['READ_CALL_LOG'], df['SUBSCRIBED_FEEDS_WRITE']
        x32_raw, x33_raw, x34_raw, x35_raw= df['READ_EXTERNAL_STORAGE'], df['VIBRATE'], df['ACCESS_NETWORK_STATE'], df['SUBSCRIBED_FEEDS_READ']
        x36_raw, x37_raw, x38_raw, x39_raw= df['CHANGE_WIFI_MULTICAST_STATE'], df['WRITE_CALENDAR'], df['MASTER_CLEAR'], df['UPDATE_DEVICE_STATS']

        x40_raw, x41_raw, x42_raw, x43_raw= df['WRITE_CALL_LOG'], df['DELETE_PACKAGES'], df['GET_TASKS'], df['GLOBAL_SEARCH']
        x44_raw, x45_raw, x46_raw, x47_raw= df['DELETE_CACHE_FILES'], df['WRITE_USER_DICTIONARY'], df['REORDER_TASKS'], df['WRITE_PROFILE']
        x48_raw, x49_raw, x50_raw, x51_raw= df['SET_WALLPAPER'], df['BIND_INPUT_METHOD'], df['READ_SOCIAL_STREAM'], df['READ_USER_DICTIONARY']
        x52_raw, x53_raw, x54_raw, x55_raw= df['PROCESS_OUTGOING_CALLS'], df['CALL_PRIVILEGED'], df['BIND_WALLPAPER'], df['RECEIVE_WAP_PUSH']
        x56_raw, x57_raw, x58_raw, x59_raw= df['DUMP'], df['BATTERY_STATS'], df['ACCESS_COARSE_LOCATION'], df['SET_TIME']
        x60_raw, x61_raw, x62_raw, x63_raw= df['WRITE_SOCIAL_STREAM'], df['WRITE_SETTINGS'], df['REBOOT'], df['BLUETOOTH_ADMIN']
        x64_raw, x65_raw, x66_raw, x67_raw= df['BIND_DEVICE_ADMIN'], df['WRITE_GSERVICES'], df['KILL_BACKGROUND_PROCESSES'], df['STATUS_BAR']
        x68_raw, x69_raw, x70_raw, x71_raw= df['PERSISTENT_ACTIVITY'], df['CHANGE_NETWORK_STATE'], df['RECEIVE_MMS'], df['SET_TIME_ZONE']
        x72_raw, x73_raw, x74_raw, x75_raw= df['CONTROL_LOCATION_UPDATES'], df['BROADCAST_WAP_PUSH'], df['BIND_ACCESSIBILITY_SERVICE'], df['ADD_VOICEMAIL']
        x76_raw, x77_raw, x78_raw, x79_raw= df['CALL_PHONE'], df['BIND_APPWIDGET'], df['FLASHLIGHT'], df['READ_LOGS']

        x80_raw, x81_raw, x82_raw, x83_raw= df['SET_PROCESS_LIMIT'], df['MOUNT_UNMOUNT_FILESYSTEMS'], df['BIND_TEXT_SERVICE'], df['INSTALL_LOCATION_PROVIDER']
        x84_raw, x85_raw, x86_raw, x87_raw= df['SYSTEM_ALERT_WINDOW'], df['MOUNT_FORMAT_FILESYSTEMS'], df['CHANGE_CONFIGURATION'], df['CLEAR_APP_USER_DATA']
        x88_raw, x89_raw, x90_raw, x91_raw= df['CHANGE_WIFI_STATE'], df['READ_FRAME_BUFFER'], df['ACCESS_SURFACE_FLINGER'], df['BROADCAST_SMS']
        x92_raw, x93_raw, x94_raw, x95_raw= df['EXPAND_STATUS_BAR'], df['INTERNAL_SYSTEM_WINDOW'], df['SET_ACTIVITY_WATCHER'], df['WRITE_CONTACTS']
        x96_raw, x97_raw, x98_raw, x99_raw= df['BIND_VPN_SERVICE'], df['DISABLE_KEYGUARD'], df['ACCESS_MOCK_LOCATION'], df['GET_PACKAGE_SIZE']
        x100_raw, x101_raw, x102_raw, x103_raw = df['MODIFY_PHONE_STATE'], df['CHANGE_COMPONENT_ENABLED_STATE'], df['CLEAR_APP_CACHE'], df['SET_ORIENTATION']
        x104_raw, x105_raw, x106_raw, x107_raw = df['READ_CONTACTS'], df['DEVICE_POWER'], df['HARDWARE_TEST'], df['ACCESS_WIFI_STATE']
        x108_raw, x109_raw, x110_raw, x111_raw = df['WRITE_EXTERNAL_STORAGE'], df['ACCESS_FINE_LOCATION'], df['SET_WALLPAPER_HINTS'], df['SET_PREFERRED_APPLICATIONS']
        x112_raw, x113_raw = df['WRITE_SECURE_SETTINGS'], df['SEND_SMS']

        y_raw = df['class']
        for i in range(len(df.index)):
            x1.append(x1_raw[i])
            x2.append(x2_raw[i])
            x3.append(x3_raw[i])
            x4.append(x4_raw[i])
            x5.append(x5_raw[i])
            x6.append(x6_raw[i])
            x7.append(x7_raw[i])
            x8.append(x8_raw[i])
            x9.append(x9_raw[i])
            x10.append(x10_raw[i])
            x11.append(x11_raw[i])
            x12.append(x12_raw[i])
            x13.append(x13_raw[i])
            x14.append(x14_raw[i])
            x15.append(x15_raw[i])
            x16.append(x16_raw[i])
            x17.append(x17_raw[i])
            x18.append(x18_raw[i])
            x19.append(x19_raw[i])
            x20.append(x20_raw[i])
            x21.append(x21_raw[i])
            x22.append(x22_raw[i])
            x23.append(x23_raw[i])
            x24.append(x24_raw[i])
            x25.append(x25_raw[i])
            x26.append(x26_raw[i])
            x27.append(x27_raw[i])
            x28.append(x28_raw[i])
            x29.append(x29_raw[i])
            x30.append(x30_raw[i])
            x31.append(x31_raw[i])
            x32.append(x32_raw[i])
            x33.append(x33_raw[i])
            x34.append(x34_raw[i])
            x35.append(x35_raw[i])
            x36.append(x36_raw[i])
            x37.append(x37_raw[i])
            x38.append(x38_raw[i])
            x39.append(x39_raw[i])
            x40.append(x40_raw[i])
            x41.append(x41_raw[i])
            x42.append(x42_raw[i])
            x43.append(x43_raw[i])
            x44.append(x44_raw[i])
            x45.append(x45_raw[i])
            x46.append(x46_raw[i])
            x47.append(x47_raw[i])
            x48.append(x48_raw[i])
            x49.append(x49_raw[i])
            x50.append(x50_raw[i])
            x51.append(x51_raw[i])
            x52.append(x52_raw[i])
            x53.append(x53_raw[i])
            x54.append(x54_raw[i])
            x55.append(x55_raw[i])
            x56.append(x56_raw[i])
            x57.append(x57_raw[i])
            x58.append(x58_raw[i])
            x59.append(x59_raw[i])
            x60.append(x60_raw[i])
            x61.append(x61_raw[i])
            x62.append(x62_raw[i])
            x63.append(x63_raw[i])
            x64.append(x64_raw[i])
            x65.append(x65_raw[i])
            x66.append(x66_raw[i])
            x67.append(x67_raw[i])
            x68.append(x68_raw[i])
            x69.append(x69_raw[i])
            x70.append(x70_raw[i])
            x71.append(x71_raw[i])
            x72.append(x72_raw[i])
            x73.append(x73_raw[i])
            x74.append(x74_raw[i])
            x75.append(x75_raw[i])
            x76.append(x76_raw[i])
            x77.append(x77_raw[i])
            x78.append(x78_raw[i])
            x79.append(x79_raw[i])
            x80.append(x80_raw[i])
            x81.append(x81_raw[i])
            x82.append(x82_raw[i])
            x83.append(x83_raw[i])
            x84.append(x84_raw[i])
            x85.append(x85_raw[i])
            x86.append(x86_raw[i])
            x87.append(x87_raw[i])
            x88.append(x88_raw[i])
            x89.append(x89_raw[i])
            x90.append(x90_raw[i])
            x91.append(x91_raw[i])
            x92.append(x92_raw[i])
            x93.append(x93_raw[i])
            x94.append(x94_raw[i])
            x95.append(x95_raw[i])
            x96.append(x96_raw[i])
            x97.append(x97_raw[i])
            x98.append(x98_raw[i])
            x99.append(x99_raw[i])
            x100.append(x100_raw[i])
            x101.append(x101_raw[i])
            x102.append(x102_raw[i])
            x103.append(x103_raw[i])
            x104.append(x104_raw[i])
            x105.append(x105_raw[i])
            x106.append(x106_raw[i])
            x107.append(x107_raw[i])
            x108.append(x108_raw[i])
            x109.append(x109_raw[i])
            x110.append(x110_raw[i])
            x111.append(x111_raw[i])
            x112.append(x112_raw[i])
            x113.append(x113_raw[i])

            if y_raw[i] == 'S':
                y.append(1)
            else:
                y.append(0)
        X = list(zip(x1, x2, x4, x10, x15, x18, x19, x22, x29, x30, x31, x34, \
            x35, x36, x40, x44, x60, x61, x64, x68, x69, x71, x72, x73, x75, \
            x77, x80, x81, x83, x85,  x87, x89, x90, x94, x98, x101, x106, x113))
        return X, y

    X, y = load_file("data/drebin215dataset5560malware9476benign.csv")



	##################################################################################
	# TODO: use train test split to split data into x_train, x_test, y_train, y_test #
	#################################################################################
    x_train, x_test, y_train, y_test = train_test_split(X, y, p)

	##################################################################################
	# TODO: Use StatsModels to create the Linear Model and Output R-squared
	#################################################################################
    x_train = sm.add_constant(x_train)
    model = sm.OLS(y_train, x_train)
    results = model.fit()


	# Prints out the Report
	# TODO: print R-squared, test MSE & train MSE
    print('r-squared')
    print(results.rsquared)

    x_test = sm.add_constant(x_test)
    test_pred = results.predict(x_test)
    print('MSE test')
    print(eval_measures.mse(y_test,test_pred))

    train_pred = results.predict(x_train)
    print('MSE train')
    print(eval_measures.mse(y_train,train_pred))

    print('Summary')
    print(results.summary())

#     r-squared
# 0.4610741855183632
# MSE test
# 0.12307815170253002
# MSE train
# 0.12598380510417417

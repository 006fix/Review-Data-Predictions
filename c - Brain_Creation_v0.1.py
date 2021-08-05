# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 19:56:48 2021

@author: Alan
"""


import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import json
import time
from sklearn import preprocessing

input_size = 250000
test_size = int(input_size/10)
work_size = int(0.9*input_size)

inpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Brain_Dataset_v0.1_combined.csv"



temp_dataset = pd.read_csv(inpath)
temp_dataset_check = temp_dataset.head(100)
#print(temp_dataset_check.columns.tolist())
working_set = temp_dataset.iloc[:, 2:803]
temp_check2 = working_set.head(100)
to_rejoin = temp_dataset['check_label']

#normalise by column
#normalise by row

min_max_scaler = preprocessing.MinMaxScaler()

#row division
x1 = working_set.values
x_mod = min_max_scaler.fit_transform(x1)

row_df = pd.DataFrame(x_mod)

#column division
x2 = x1.T
x_mod2 = min_max_scaler.fit_transform(x2)
x_mod2_T = x_mod2.T

column_df = pd.DataFrame(x_mod2_T)

row_df['check_label'] = to_rejoin
column_df['check_label'] = to_rejoin
#column_df2 = pd.concat([column_df, to_rejoin], axis=1)

row_df_check = row_df.head(100)


#this works for the row version
early_dataset = row_df.drop(row_df[row_df.check_label > 0].index)
mid_dataset_temp = row_df.drop(row_df[row_df.check_label == 0].index)
mid_dataset = mid_dataset_temp.drop(mid_dataset_temp[mid_dataset_temp.check_label == 2].index)
late_dataset = row_df.drop(row_df[row_df.check_label < 2].index)

early_test = early_dataset.head(test_size)
mid_test = mid_dataset.head(test_size)
late_test = late_dataset.head(test_size)

early_work = early_dataset.tail(work_size)
mid_work = mid_dataset.tail(work_size)
late_work = late_dataset.tail(work_size)

check_set = pd.concat([early_test, mid_test, late_test], axis = 0)
work_set = pd.concat([early_work, mid_work, late_work], axis = 0)

check_labels = check_set['check_label']
work_labels = work_set['check_label']

checking3 = check_set.head(100)

final_work = work_set.drop(columns=['check_label'])
final_check = check_set.drop(columns=['check_label'])

outpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Brain_Dataset_v0.1"
end = ".csv"
work_lab = "_work_labels"
check_lab = "_check_labels"
work_data = "_work_data"
check_data = "_check_data"
rows_str = "_rows"

#this works for the column version

early_dataset2 = column_df.drop(column_df[column_df.check_label > 0].index)
mid_dataset_temp2 = column_df.drop(column_df[column_df.check_label == 0].index)
mid_dataset2 = mid_dataset_temp.drop(mid_dataset_temp[mid_dataset_temp.check_label == 2].index)
late_dataset2 = column_df.drop(column_df[column_df.check_label < 2].index)

early_test2 = early_dataset2.head(test_size)
mid_test2 = mid_dataset2.head(test_size)
late_test2 = late_dataset2.head(test_size)

early_work2 = early_dataset2.tail(work_size)
mid_work2 = mid_dataset2.tail(work_size)
late_work2 = late_dataset2.tail(work_size)

check_set2 = pd.concat([early_test2, mid_test2, late_test2], axis = 0)
work_set2 = pd.concat([early_work2, mid_work2, late_work2], axis = 0)

check_labels2 = check_set['check_label']
work_labels2 = work_set['check_label']

checking4 = check_set2.head(100)

final_work2 = work_set2.drop(columns=['check_label'])
final_check2 = check_set2.drop(columns=['check_label'])

cols_str = "_cols"

final_work.to_csv(outpath+work_data+rows_str+end)
final_check.to_csv(outpath+check_data+rows_str+end)
check_labels.to_csv(outpath+check_lab+rows_str+end)
work_labels.to_csv(outpath+work_lab+rows_str+end)

final_work2.to_csv(outpath+work_data+cols_str+end)
final_check2.to_csv(outpath+check_data+cols_str+end)
check_labels2.to_csv(outpath+check_lab+cols_str+end)
work_labels2.to_csv(outpath+work_lab+cols_str+end)





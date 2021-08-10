# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 18:59:49 2021

@author: Alan
"""

import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import json
import time


inpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Brain_Dataset_v0.1_file"

num_target = 250000
num_early = 0
num_mid = 0
num_late = 0
early_datasets = []
mid_datasets = []
late_datasets = []

for i in range(8):
    print(i)
    if (num_late < num_target) or (num_mid < num_target) or (num_early < num_target):
        file_name = inpath + str(i) + ".csv"
        temp_dataset = pd.read_csv(file_name)
        early_dataset = temp_dataset.drop(temp_dataset[temp_dataset.check_label > 0].index)
        mid_dataset_temp = temp_dataset.drop(temp_dataset[temp_dataset.check_label == 0].index)
        mid_dataset = mid_dataset_temp.drop(mid_dataset_temp[mid_dataset_temp.check_label == 2].index)
        late_dataset = temp_dataset.drop(temp_dataset[temp_dataset.check_label < 2].index)
        early_rows = len(early_dataset.index)
        print(early_rows)
        mid_rows = len(mid_dataset.index)
        print(mid_rows)
        late_rows = len(late_dataset.index)
        print(late_rows)
        if early_rows + num_early <= num_target:
            early_datasets.append(early_dataset)
        else:
            if num_early < num_target:
                dif = num_target - num_early
                subset_e = early_dataset.head(dif)
                early_datasets.append(subset_e)
        if mid_rows + num_mid <= num_target:
            mid_datasets.append(mid_dataset)
        else:
            if num_mid < num_target:
                dif = num_target - num_mid
                subset_m = mid_dataset.head(dif)
                mid_datasets.append(subset_m)
        if late_rows + num_late <= num_target:
            late_datasets.append(late_dataset)
        else:
            if num_late < num_target:
                dif = num_target - num_late
                subset_l = late_dataset.head(dif)
                late_datasets.append(subset_l)
        num_early += early_rows
        num_mid += mid_rows
        num_late += late_rows
    
all_datasets = early_datasets + mid_datasets + late_datasets

df_final = pd.concat(all_datasets, axis = 0)
    
outpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Brain_Dataset_v0.1_combined.csv"

df_final.to_csv(outpath)
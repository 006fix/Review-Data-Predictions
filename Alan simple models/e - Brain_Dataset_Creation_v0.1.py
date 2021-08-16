# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 15:32:02 2021

@author: Alan
"""

import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import json
import time



punc = string.punctuation


inpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Usable_Set_of_400_words.csv"
#top 400 inc and dec words that are not real words from nltk dataframe

word_series = pd.read_csv(inpath)

word_list = word_series['0']
word_list_fin = word_list.tolist()

year_vals = ['2020','2013','2016','2011','2008','2019','2009','2014','2021','2004','2005','2006','2018','2010','2015','2017','2003','2000','2001','2002','1998','1999','2012','2007']
#above is true for the first 8 files (0 through 7)
year_vals_low = ['1998','1999','2000','2001','2002','2003']
year_vals_mid = ['2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014']
year_vals_late = ['2015','2016','2017','2018','2019','2020','2021']

sourcepath_base = "C:/Users/Alan/Desktop/Review Data/Review_Data_Preprocessed"
sourcepath_second = "/pre_processed_group_"
second = ".txt"

def generate_dataframe(file_num, word_check_list):
    global label_list
    label_list = []
    result_list = []
    count = 0
    time_start = time.time()
    i = file_num
    with open(sourcepath_base + sourcepath_second + str(i) + second) as f:
            line = f.readline()
            while line:
                try:
                    checkvar = line
                    if count%10000 == 0:
                        timenow = time.time()
                        timetaken = round((timenow - time_start)/60, 2)
                        print(f"You have completed " + str(count) + " lines worth of data")
                        print("There were " + str(timetaken) + " minutes elapsed since start")
                    count += 1
                    line= f.readline()
                    jsonfile = json.loads(line)
                    json_line_review = jsonfile['review_detail']
                    json_line_data = jsonfile['review_year']
                    if json_line_data in year_vals_low:
                        label_list.append(0)
                        print("0 added")
                    elif json_line_data in year_vals_mid:
                        label_list.append(1)
                        print("1 added")
                    elif json_line_data in year_vals_late:
                        label_list.append(2)
                        print("2 added")
                    else:
                        print("AN ERROR HAS OCCURED AT LINE " + str(count))
                        print(json_line_data)
                    for j in range(len(punc)):
                         json_line_review = json_line_review.replace(punc[j], "")
                    json_line_lower = json_line_review.lower()
                    list_results = []
                    for k in range(len(word_check_list)):
                        checkval = word_check_list[k]
                        findcount = json_line_lower.count(checkval)
                        list_results.append(findcount)
                    result_list.append(list_results)
                except:
                    print("An exception occured at line number" + str(count))
    return label_list, result_list


for i in range(8):
    x0 = generate_dataframe(i, word_list_fin)
    
    results_df = pd.DataFrame(x0[1])
    results_df['sum'] = results_df.sum(axis=1)
    
    c = [results_df['sum'] > 0]
    v = ['keep']
    results_df['filter'] = np.select(c,v,'remove')
    
    results_df['check_label'] = x0[0]
    
    results_df_check2 = results_df['sum']
    
    results_df2 = results_df.drop(results_df[results_df.filter == 'remove'].index)
    
    outpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Brain_Dataset_v0.1_file" + str(i) + ".csv"
    
    results_df.to_csv(outpath)







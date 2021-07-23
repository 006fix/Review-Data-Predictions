# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 19:39:24 2021

@author: Alan
"""

import pandas as pd
import json
import os
import sys

sourcepath = r"C:\Users\Alan\Desktop\Review Data"
dirs = os.listdir(sourcepath)

json_storage = {}

for file in dirs:
    json_loc = sourcepath + r"\\" + file
    json_open = open(json_loc)
    json_storage[file] = json.load(json_open)
    
#while number of files in directory = 1, will only run once
#num files in directory can be changed later, will retain functionality
#writes each new file to its own dictionary, keys accessible through
# for file in dirs loop
    
   
date_storage = []    
for file in dirs:
    date_storage_sub = []
    for j in range(len(json_storage[file])):
        date_storage_sub.append(json_storage[file][j]['review_date'])
        del json_storage[file][j]['review_date']
    date_storage.append(date_storage_sub)

#looks through the entirety of all the files, generates list of lists
#containing all of the dates, split by input file
#then deletes the dates from all entires

file_num_holder = -1
#will iterate by 1 on each loop, lets you access upper list in list of lists
#based on iterations on file in dirs

replacement_count = []
#will hold records of replacement count, and location (to allow checking)
#could easily modify below to always write values to this dict to generate
#a column for match found

#print(date_storage[0][1][-4:])
#print(json_storage['part-01.json'][45]['review_detail'])


for file in dirs:
    file_num_holder += 1
    for date in range(len(date_storage[file_num_holder])):
        single_date = date_storage[file_num_holder][date][-4:]
        #above pulls last 4 digits of date string (aka year)
        temphold = json_storage[file][date]['review_detail']
        if temphold.count(single_date) > 0:
            match_found = [temphold.count(single_date), date]
            replacement_count.append(match_found)
        temphold2 = temphold.replace(single_date, 'QQQQ')
        temphold3 = {'review_detail': temphold2}
        json_storage[file][date].update(temphold3)
        
#print(json_storage['part-01.json'][45]['review_detail'])

#upon review, doing the same to the titles is a waste of time, their formatting
#is highly variable and complex

final_digit_storage = []
for file in dirs:
    final_digit_sub = []
    for k in range(len(json_storage[file])):
        final_digit_sub.append(json_storage[file][k]['review_id'][-1])
    final_digit_storage.append(final_digit_sub)
    
    
    
#below indicates that the count of final digit is a valid method for subsetting    
print(final_digit_storage[0].count("0"))
print(final_digit_storage[0].count("1"))
print(final_digit_storage[0].count("2"))
print(final_digit_storage[0].count("3"))
print(final_digit_storage[0].count("4"))
print(final_digit_storage[0].count("5"))
print(final_digit_storage[0].count("6"))
print(final_digit_storage[0].count("7"))
print(final_digit_storage[0].count("8"))
print(final_digit_storage[0].count("9"))

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 19:39:24 2021

@author: Alan
"""

import pandas as pd
import json
import os
import sys
import nltk
from nltk.util import ngrams

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


#examing 1, 2, 3 ngram counts as a function of set size
#will split into where count = 0 and all others to compare

sourcepath2 = r"C:\Users\Alan\Desktop\Text_Output"
string_storage = ""



file_num_holder = -1
iterations_completed = -1
dirs2 = os.listdir(sourcepath2)
files_found = 0
max_val = 0

for file in dirs2:
    files_found += 1
    
    
    
output_loc_list = []    
if files_found > 0:
    for file in dirs2:
        detloc_start = file.index("[")
        detloc_end = file.index("]")
        outputval = int(file[detloc_start+1:detloc_end])
        output_loc_list.append(outputval)
        print(outputval)
        
if files_found > 0:
    output_loc_list.sort(reverse=True)
    max_val = output_loc_list[0]
    
counter = 0
complete_count = 0
print(len(json_storage["part-01.json"]))

for file in dirs:
    for string2 in range((1000*max_val), len(json_storage[file])):
        counter+=1
        if string2 == (len(json_storage[file]) - 1):
            string_storage += json_storage[file][string2]['review_detail']
            string_storage += " "
            string_storage += "gotolocfind" + str(string2)
            string_storage += " "
            text_filename = sourcepath2 + r"\\" + "(" + str(file) + ")_" + "test[" + str(1+ int(((string2+1)/1000))) + "].txt"
            string_storage.encode("ascii",errors="ignore")
            f1 = open(text_filename, "w+", encoding="utf-8")
            print(counter)
            print(string2)
            f1.write(string_storage)
            f1.close()
            string_storage = ""
        if counter < 1000:
            string_storage += json_storage[file][string2]['review_detail']
            string_storage += " "
            string_storage += "gotolocfind" + str(string2)
            string_storage += " "
        else:
            string_storage += json_storage[file][string2]['review_detail']
            string_storage += " "
            string_storage += "gotolocfind" + str(string2)
            string_storage += " "
            text_filename = sourcepath2 + r"\\" + "(" + str(file) + ")_" + "test[" + str(int(((string2+1)/1000))) + "].txt"
            string_storage.encode("ascii",errors="ignore")
            f1 = open(text_filename, "w+", encoding="utf-8")
            print(counter)
            print(string2)
            f1.write(string_storage)
            f1.close()
            string_storage = ""
            counter = 0
            complete_count += 1
            print("There have been " + str(complete_count) + " files created.")

            
print("This step has finished!")



# def extract_ngrams(data, num):
#     n_grams = ngrams(nltk.word_tokenize(data), num)
#     return n_grams
            
# zerosplitn1 = extract_ngrams(string_storage0, 1)
# zerosplitn2 = extract_ngrams(string_storage0, 2)
# zerosplitn3 = extract_ngrams(string_storage0, 3)
# othsplitn1 = extract_ngrams(string_storage1t9, 1)
# othsplitn2 = extract_ngrams(string_storage1t9, 2)
# othsplitn3 = extract_ngrams(string_storage1t9, 3)

# print(len(zerosplitn1))
# print(len(zerosplitn2))
# print(len(zerosplitn3))
# print(len(othsplitn1))
# print(len(othsplitn2))
# print(len(othsplitn3))















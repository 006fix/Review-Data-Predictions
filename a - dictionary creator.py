# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 19:16:13 2021

@author: Alan
"""
import os
import sys
import json
import string
import pandas as pd

punc = string.punctuation

def ngram_maker(overall_dict, ngram_len, string_temp):
    string_split = string_temp.split()
    modified_len = len(string_split) - (ngram_len - 1)
    for i in range(modified_len):
        holder_val = string_split[i:i+ngram_len]
        holder_val_join = " ".join(holder_val)
        try:
            holdval = overall_dict[holder_val_join] + 1
            new_entry = {holder_val_join: holdval}
            overall_dict.update(new_entry)
        except:
            holdval = 1
            new_entry = {holder_val_join: holdval}
            overall_dict.update(new_entry)
    return overall_dict


sourcepath_base = "C:/Users/Alan/Desktop/Review Data/Review_Data_Preprocessed"
sourcepath_second = "/pre_processed_group_"
second = ".txt"
lines = ""
overall_dict = {}
year_dict= {}
count = 0
finding_total = 0


# for i in range(8):
#     print(i)
#     with open(sourcepath_base + sourcepath_second + str(i) + second) as f:
#         for line in f:
#             finding_total += 1
            
# print(finding_total)
                
    
#is the double usage of i in the interior going to cause problems???????
def make_dicts(number_files, ngram_len, dict_list):
    global checkvar
    global count
    for i in range(number_files):
        with open(sourcepath_base + sourcepath_second + str(i) + second) as f:
                line = f.readline()
                while line:
                    try:
                        checkvar = line
                        if count%10000 == 0:
                            print(f"You have completed " + str(count) + " lines worth of data")
                        count += 1
                        line= f.readline()
                        jsonfile = json.loads(line)
                        json_line_review = jsonfile['review_detail']
                        json_line_data = jsonfile['review_year']
                        year_group_val = 99
                        if count%100000 == 0:
                            print(json_line_data)
                        if json_line_data in year_vals_low:
                            year_group_val = 0
                        elif json_line_data in year_vals_mid:
                            year_group_val = 1
                        elif json_line_data in year_vals_late:
                            year_group_val = 2
                        current_dict = list_of_dicts[year_group_val]
                        #pull out review year and review details
                        for j in range(len(punc)):
                            json_line_review = json_line_review.replace(punc[j], "")
                        #strip all punctuation from the review
                        ngram_maker(current_dict, ngram_len, json_line_review)
                    except:
                        print("An exception occured at line number" + str(count))
    return dict_list

year_dict = {'2020': 98630, '2013': 18207, '2016': 19943, '2011': 15587, '2008': 17273, '2019': 65219, '2009': 15731, '2014': 19762, '2021': 3445, '2004': 17667, '2005': 21131, '2006': 23982, '2018': 49363, '2010': 15827, '2015': 20997, '2017': 26295, '2003': 17854, '2000': 10969, '2001': 13560, '2002': 16890, '1998': 2626, '1999': 12634, '2012': 16025, '2007': 18889}
year_vals = ['2020','2013','2016','2011','2008','2019','2009','2014','2021','2004','2005','2006','2018','2010','2015','2017','2003','2000','2001','2002','1998','1999','2012','2007']
#above is true for the first 8 files (0 through 7)
year_vals_low = ['1998','1999','2000','2001','2002','2003']
year_vals_mid = ['2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014']
year_vals_late = ['2015','2016','2017','2018','2019','2020','2021']

word_dict_low = {}
word_dict_mid = {}
word_dict_high = {}
list_of_dicts = [word_dict_low, word_dict_mid, word_dict_high]

x = make_dicts(8, 1, list_of_dicts)

dict_words_tot = [0,0,0]

for i in range(3):
    dict_temp = list_of_dicts[i]
    new_dict = {key:value for key, value in dict_temp.items() if value > 50}
    list_of_dicts[i] = new_dict


for i in range(3):
    print(i)
    for key in list_of_dicts[i]:
        orig_val = dict_words_tot[i]
        new_val = orig_val + list_of_dicts[i][key]
        dict_words_tot[i] = new_val
        
valid_word_dict = {}
valid_word_list = []
for key in list_of_dicts[1]:
    for i in range(2):
        try:
            x = list_of_dicts[1+i][key]
            update_val = {key:[0,0,0]}
            valid_word_dict.update(update_val)
            valid_word_list.append(key)
        except:
            y = 1
            
dict_of_results = {}

for i in range(3):
    print(i)
    for key in list_of_dicts[i]:
        holdval = 0
        if key in valid_word_list:
            holdval = list_of_dicts[i][key]
            values = valid_word_dict[key]
            values[i] = holdval
            update_val = {key:values}
            dict_of_results.update(update_val)
            
output_list = []            
for key in dict_of_results:
    holder_list = []
    holder_list.append(key)
    for i in range(3):
        holder_list.append(dict_of_results[key][i])
    output_list.append(holder_list)
            
final_dataframe = pd.DataFrame(output_list, columns = ['word', 'early_count', 'mid_count', 'late_count'])
output_loc = r"C:\Users\Alan\Desktop\Review Data\Dataframes\comparison_dict.csv"
final_dataframe.to_csv(output_loc, encoding = 'utf-8', index=False)




            
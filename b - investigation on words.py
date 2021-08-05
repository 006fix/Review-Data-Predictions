# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 21:33:09 2021

@author: Alan
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import words

#nltk.download('words')

low_words = 94445311
mid_words = 429138181
late_words = 319233536
tot_words = low_words + mid_words + late_words
low_words_rel = low_words/tot_words
mid_words_rel = mid_words/tot_words
late_words_rel = late_words/tot_words

low_modfac = 1/low_words_rel
mid_modfac = 1/mid_words_rel
late_modfac = 1/late_words_rel

path = r"C:\Users\Alan\Desktop\Review Data\Dataframes\comparison_dict.csv"
import_df = pd.read_csv(path)

import_df = import_df.drop(import_df[import_df.early_count < 1].index)
import_df = import_df.drop(import_df[import_df.late_count < 1].index)


import_df['low_mod'] = import_df['early_count'] * low_modfac
import_df['mid_mod'] = import_df['mid_count'] * mid_modfac
import_df['late_mod'] = import_df['late_count'] * late_modfac

import_df['low_to_mid'] = import_df['low_mod'] / import_df['mid_mod']
import_df['mid_to_high'] = import_df['mid_mod'] / import_df['late_mod']

c = [
     (import_df['low_mod'] < import_df['mid_mod']) & (import_df['mid_mod'] < import_df['late_mod']),
     (import_df['low_mod'] > import_df['mid_mod']) & (import_df['mid_mod'] > import_df['late_mod'])
     ]

v = ['always_inc', 'always_dec']

import_df['changes'] = np.select(c,v,'remove')

import_df = import_df.drop(import_df[import_df.changes == 'remove'].index)

import_df['combined_variance'] = abs(1-import_df['low_to_mid']) + abs(1-import_df['mid_to_high'])


import_df_inc = import_df.drop(import_df[import_df.changes == 'always_dec'].index)


import_df_inc['mid_to_low'] = import_df_inc['mid_mod'] / import_df_inc['low_mod']
import_df_inc['high_to_mid'] = import_df_inc['late_mod'] / import_df_inc['mid_mod']
import_df_inc['combined_variance2'] = abs(1-import_df_inc['mid_to_low']) + abs(1-import_df_inc['high_to_mid'])


import_df_inc['lowercase'] = import_df_inc['word'].str.lower()
import_df['lowercase'] = import_df['word'].str.lower()

import_df_dec = import_df.drop(import_df[import_df.changes == 'always_inc'].index)

####commenting out the below for now to trial other approach
# c1 = [
#       import_df['lowercase'] == import_df['word']
#       ]

# v1 = ['matches']

# import_df['only_lowercase'] = np.select(c1, v1, "remove")

# c2 = [
#       import_df_inc['lowercase'] == import_df_inc['word']
#       ]

# v2 = ['matches']

# import_df_inc['only_lowercase'] = np.select(c2, v2, "remove")

# import_df = import_df.drop(import_df[import_df.only_lowercase == 'remove'].index)
# import_df_inc = import_df_inc.drop(import_df_inc[import_df_inc.only_lowercase == 'remove'].index)
###commenting out above for now to trial other approach

#above was interesting, but lets try a new idea
#import nltk list of words
#set words col to lowercase
#make nltk list of words a dataframe, add col of val 1
#left merge
#filter to where newcol is blank

trial_list = words.words()

onelist = []
for i in range(len(trial_list)):
    onelist.append("remove")
    
combined_dataframe = []
combined_dataframe.append(trial_list)
combined_dataframe.append(onelist)
combined_dataframeT = np.asarray(combined_dataframe).T

words_df = pd.DataFrame(combined_dataframeT, columns=['lowercase', 'ones'])

incorp_words_dec = pd.merge(import_df_dec, words_df, how='left')
incorp_words_inc = pd.merge(import_df_inc, words_df, how='left')

incorp_words_dec['ones'] = incorp_words_dec['ones'].fillna('keep')
incorp_words_inc['ones'] = incorp_words_inc['ones'].fillna('keep')


incorp_words_dec2 = incorp_words_dec.drop(incorp_words_dec[incorp_words_dec.ones == 'remove'].index)
incorp_words_inc2 = incorp_words_inc.drop(incorp_words_inc[incorp_words_inc.ones == 'remove'].index)

c1 = [
      incorp_words_dec2['lowercase'] == incorp_words_dec2['word']
      ]

v1 = ['matches']

incorp_words_dec2['only_lowercase'] = np.select(c1, v1, "remove")

c2 = [
      incorp_words_inc2['lowercase'] == incorp_words_inc2['word']
      ]

v2 = ['matches']

incorp_words_inc2['only_lowercase'] = np.select(c2, v2, "remove")

incorp_words_dec3 = incorp_words_dec2.drop(incorp_words_dec2[incorp_words_dec2.only_lowercase == 'remove'].index)
incorp_words_inc3 = incorp_words_inc2.drop(incorp_words_inc2[incorp_words_inc2.only_lowercase == 'remove'].index)

incorp_words_dec4 = incorp_words_dec3.sort_values(by=['combined_variance'],ascending = False)
incorp_words_inc4 = incorp_words_inc3.sort_values(by=['combined_variance2'],ascending = False)

dataset1 = incorp_words_dec4['word'].head(400)
dataset2 = incorp_words_inc4['word'].head(400)

list1 = dataset1.tolist()
list2 = dataset2.tolist()
list3 = list1 + list2

outpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Usable_Set_of_400_words.csv"

series_comb = pd.Series(list3)

series_comb.to_csv(outpath)
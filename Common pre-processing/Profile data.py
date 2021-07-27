# Code to generate some profile statistics of the feed data
#
# Created by Greg on 27/07/21
#

import json
from pathlib import Path
import time
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# Define data source and target
pre_processed_data_source_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/pre_processed")
files_to_load = ["pre_processed_group_0.txt", "pre_processed_group_1.txt", "pre_processed_group_2.txt", "pre_processed_group_3.txt", "pre_processed_group_4.txt", "pre_processed_group_5.txt",  "pre_processed_group_6.txt", "pre_processed_group_7.txt"]
# Use the below instead of the above for testing			 
# files_to_load = ["pre_processed_group_0.txt"]

# Open a couter to store the years
review_by_year = Counter()

# Read in the text corpus
# This is now a list of JSONs, so needs to be read in accordingly
startTime = time.time()
process_count = 0

for current_file in files_to_load:
    print(f"Starting analysis of {current_file}...")
    file_to_read = pre_processed_data_source_folder / current_file
    with open(file_to_read, mode='r') as file:
        
        process_count_file = 0
        
        for line in file:
            process_count_file +=1
            review = json.loads(line.strip())
            
            # Add the year to the review_by_year Counter
            review_by_year[review['review_year']] += 1
        
        print(f"Analysed {process_count_file} reviews")
        process_count += process_count_file

print(f"File analysis complete after {time.time() - startTime:.2f} seconds. {process_count} reviews reviewed")

print (f"The review years are {sorted(review_by_year.most_common())}")

review_by_year_df = pd.DataFrame.from_dict(review_by_year, orient='index').reset_index()
review_by_year_df = review_by_year_df.rename(columns={'index':'year', 0:'reviews'})
review_by_year_df.sort_values(by='year', inplace=True)
review_by_year_df.plot(kind='bar', x='year')
plt.show()
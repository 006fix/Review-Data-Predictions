# Code to prep the data for the BOW model
#
# Created by Greg on 27/07/21
#
# Takes as input one or more files in the format generated by Data Preprocessing
# Creates a balanced data set in a single file including all fields in the original

import json
from pathlib import Path
import time

# Define data source and target
pre_processed_data_source_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/pre_processed")
# files_to_load = ["pre_processed_group_0.txt", "pre_processed_group_1.txt", "pre_processed_group_2.txt", "pre_processed_group_3.txt", "pre_processed_group_4.txt", "pre_processed_group_5.txt",  "pre_processed_group_6.txt", "pre_processed_group_7.txt"]
# Use the below instead of the above for testing			 
files_to_load = ["pre_processed_group_0.txt"]

data_target_file = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW/BOW_training_data.txt")

# Create the counters
target_volume_per_year = 1000
year_counter = {}
for year in range (1998,2022): # Note that index must be one higher than the years required as thats how the for loop works
    year_counter[str(year)] = target_volume_per_year

# Define a corpus sub-set
corpus_sub_set = []

# Read in the text corpus
# This is now a list of JSONs, so needs to be read in accordingly
startTime = time.time()
target_count = 0

for current_file in files_to_load:
    print(f"Starting processing of {current_file}...")
    file_to_read = pre_processed_data_source_folder / current_file
    with open(file_to_read, mode='r') as file:
        
        for line in file:

            review = json.loads(line.strip())
            if (year_counter[review['review_year']] > 0 ):
                corpus_sub_set.append(review)
                year_counter[review['review_year']] = year_counter[review['review_year']] -1
                
                if (year_counter[review['review_year']] == 0):
                    print(f"Found target number for {review['review_year']}")

                target_count += 1

            if (target_count >= target_volume_per_year * 24 ):
                break # Stop when enough data found

print(f"Data prep selection complete after {time.time() - startTime:.2f} seconds. {target_count} reviews selected")

# Write the result as a set of lines each of which is a JSON (allows streamed reading if required)
with open(data_target_file, 'w', encoding='utf-8') as f:
    for review in corpus_sub_set:
        f.write(json.dumps(review))
        f.write('\n')
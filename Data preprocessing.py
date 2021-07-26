# Alternate pre-processing trial
#
# Created by Greg on 24/07/21

import pandas as pd
import json
from pathlib import Path
import sys
import time
import re
import zlib # used for a simple hash

# Define data source and target
data_source_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/raw")
# Enumerate the failenames rather than reading the directory, so outcome is fully predictable
# files_to_load = ["part-01.json", "part-02.json", "part-03.json", "part-04.json", "part-05.json", "part-06.json"]
files_to_load = ["sample.json"]

data_target_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/pre_processed")
data_target_filename_prefix = "pre_processed_group_"
data_target_filename_suffix = ".txt"
target_files = {}

# Define the regex to use for year matching
# Base on starting with 19 or 20, then two digits
# regex compiled as it will be used many times over
year_pattern_regex = re.compile(r"(19|20)\d{2}")

# Notes on preprocessing
# 1) For simplicity later on, add a column with the target review year
# 2) Remove any instances of any year from the description.  May be making this harder than it needs to be, but really tests the word based reviews
# 3) Split the data into 10 target files, based on last digit in a hash of the movie name (so all reviews for one movi end in eth same file)
# 4) Write out as a set of lines, each of which is a JSON object (rather than a JSON list) .. so allows easy line by line use later
#
# NOT included (for ref.)
# 1) Removal of instances of the film name.  Could be an issue if names are in reviews in both build and test set, though we could split
# the set by film (using last digit of a hash of name for example)

# Open the set of output files, in append mode
for x in range(10):
     data_target_filename = data_target_filename_prefix + str(x) + data_target_filename_suffix
     data_target_file = data_target_folder / data_target_filename
     target_files[x] = open(data_target_file, 'a')
print(f"Opened output files ...")

startTime = time.time()
process_count = 0
update_count = 10000
for current_file in files_to_load:
    print(f"Starting load of {current_file}...")
    file_to_read = data_source_folder / current_file
    with open(file_to_read, mode='r') as file:

        # Note that this loads the entire JSON file into memory, and JSON structure kind of makes that 'normal'
        # But structure is simple as its just an array of objects, so could be possible to parse and read if reqd.
        # See https://stackoverflow.com/questions/10382253/reading-rather-large-json-files-in-python 
        new_reviews = json.load(file)
        
        for review in new_reviews:

            # Use a hash of 'movie' to determine the right sub group.  This puts all reviws for a given movie in one file
            target_index_hash = str(zlib.adler32(bytearray(review['movie'], 'utf-8')))
            sub_group = int(target_index_hash[-1:])
            
            # Add a column with the year
            review['review_year'] = review['review_date'][-4:]

            # Replace any occurrances of a year in the 'review_summary' and'review_detail' fields with QQQQ
            review['review_summary'] = year_pattern_regex.sub('QQQQ',review['review_summary'])
            review['review_detail'] = year_pattern_regex.sub('QQQQ',review['review_detail'])
            review['movie'] = year_pattern_regex.sub('QQQQ',review['movie'])

            # Write to correct sub-group
            target_files[sub_group].write(json.dumps(review))
            target_files[sub_group].write('\n')

            # Add to count
            process_count += 1
            update_count -= 1
            if (update_count == 0):
                print(f"Finished pre-processing {process_count} rows")
                update_count = 10000

    print(f"Finished pre-processing of {current_file} at {time.time() - startTime:.2f} total seconds elapsed")
print(f"Pre-processing complete after {time.time() - startTime:.2f} seconds")

# Close the set of output files
for x in range(10):
     target_files[x].close()

print(f"Total reviews pre-processed: {process_count:,}")

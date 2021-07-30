# Data pre-processior
#
# Created by Greg on 24/07/21

import json
from pathlib import Path
import time
import re
import zlib # used for a simple hash

# Define data source and target
data_source_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/raw")
# Enumerate the failenames rather than reading the directory, so outcome is fully predictable
files_to_load = ["part-01.json", "part-02.json", "part-03.json", "part-04.json", "part-05.json", "part-06.json"]
# Use the below instead of the above for testing
# files_to_load = ["sample.json"]

data_target_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/pre_processed")
data_target_filename_prefix = "pre_processed_group_"
data_target_filename_suffix = ".txt"
target_files = {}

# Define the regex to use for year matching
# Base on starting with 19 or 20, then two digits
# regex compiled as it will be used many times over
# Note that there is a unicode en-dash that looks confusingly like it has got left over 
# It appers as \u2013 - see https://www.fileformat.info/info/unicode/char/2013/index.htm 
year_pattern_regex = re.compile(r"(19|20)\d{2}")

# Define the regex to use in matching film title
# Splits string into two search blocks, with the first being the title
# The second is a whitespace followed by an open bracket followed by four digits, then any other characters (which may be none), then a closing bracket
# Matching the four digits ensures a year follows the bracket
title_pattern_regex = re.compile(r"(.*)(\s\(\d{4}.*\))")

# Notes on preprocessing
# 1) For simplicity later on, add a column with the target review year
# 2) Replaces any instances of any year from the summary and detail with QQQQ
# 3) Replaces instances of the title (case insensitive) with TTTT
# 4) Split the data into 10 target files, based on last digit in a hash of the movie name (so all reviews for one movie end in the same file)
# 5) Write out as a set of lines, each of which is a JSON object (rather than a JSON list) .. so allows easy line by line use later

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
            review['movie_hidden_years'] = year_pattern_regex.sub('QQQQ',review['movie'])

            # Replace any occurances of the movie title with TTTT
            title_search_group = title_pattern_regex.match(review['movie'])
            if (title_search_group):
                title_search = title_pattern_regex.match(review['movie']).group(1)
                # Use a regex sub function to ensure case insensitivity
                # Effctively like below but case insensitive
                # review['review_summary'] = review['review_summary'].replace(title_search, "TTTT")
                specific_title_regex = re.compile(re.escape(title_search), re.IGNORECASE)
                review['review_summary'] = specific_title_regex.sub('TTTT',review['review_summary'])
                review['review_detail'] = specific_title_regex.sub('TTTT',review['review_detail'])

            # Write to correct sub-group
            target_files[sub_group].write(json.dumps(review))
            target_files[sub_group].write('\n')

            # Add to count
            process_count += 1
            update_count -= 1
            if (update_count == 0):
                print(f"Finished pre-processing {process_count} rows", end='\r')
                update_count = 10000

    print(f"Finished pre-processing of {current_file} at {time.time() - startTime:.2f} total seconds elapsed")
print(f"Pre-processing complete after {time.time() - startTime:.2f} seconds")

# Close the set of output files
for x in range(10):
     target_files[x].close()

print(f"Total reviews pre-processed: {process_count:,}")

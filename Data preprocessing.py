# Alternate pre-processing trial
#
# Created by Greg on 24/07/21

import pandas as pd
import json
from pathlib import Path
import sys
import time

# Load data into dataframe
data_folder = Path("C:/Users/gregp/Documents/kaggle/input/imdb-review-dataset/")
# Enumerate the failenames rather than reading the directory, so outcome is fully predictable
# files_to_load = ["part-01.json", "part-02.json", "part-03.json", "part-04.json", "part-05.json", "part-06.json"]
files_to_load = ["sample.json"]
reviews_json = list()

startTime = time.time()
for current_file in files_to_load:
    print(f"Starting load of {current_file}...")
    file_to_read = data_folder / current_file
    with open(file_to_read, mode='r') as file:
        new_reviews = json.load(file)
        for review in new_reviews:
            reviews_json.append(review)
    print(f"Finished load of {current_file} at {time.time() - startTime:.2f} total seconds elapsed")
print(f"Loading complete after {time.time() - startTime:.2f} seconds, {len(reviews_json):,} items in reviews_json")

reviews_total_count = len(reviews_json)
print(f"Total reviews in the working data: {reviews_total_count:,}")


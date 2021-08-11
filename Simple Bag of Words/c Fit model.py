# Code to fit a model
#
# Created by Greg on 27/07/21
#
# Takes as input one or more files in the format generated by Data Preprocessing
# And, the tokenized dictionary generated in 'Tokenization.py'

import json
from pathlib import Path
import time
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.utils import to_categorical
from numpy import array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
import matplotlib.pyplot as plt

startTime = time.time()

# Load dictonary source
tokenized_dictionary = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW/tokenized_dictionary.json")
with open(tokenized_dictionary) as f:
    tokenizer = tokenizer_from_json(f.read())
print(f"Loaded tokenized dictionary based on {tokenizer.document_count} reviews, and including {len(tokenizer.word_index)} words")

# Define training data source
data_source_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW")
training_files_to_load = ["BOW_training_data.txt"]

# Define the target
model_save_file = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW/saved_model.tf")

# Load the training data
training_texts = []
training_outcomes = []
process_count = 0
# non_number_count = 0
for current_file in training_files_to_load:
    print(f"Starting load of training data by {current_file}...")
    file_to_read = data_source_folder / current_file
    with open(file_to_read, mode='r') as file:        
        for line in file:
            review = json.loads(line.strip())
            # Use both the review summary and the review detail
            # Temporarily switch to using the rating (in bins of positive,neutral, negative) rather than year, since year not proving easy
            # Training outcomes are zero based by subtracting 1998
            # training_outcomes.append (int(review['review_year'])-1998)
            # if (review['rating'] == None):
            #     non_number_count += 1
            #     continue
            # elif (int(review['rating'])>6):
            #     training_outcomes.append (2)
            # elif (int(review['rating'])<4):
            #     training_outcomes.append (0)
            # else:
            #     training_outcomes.append (1)

            # Load the training texts
            training_texts.append (review['review_detail'])

            # Load the outcomes
            training_outcomes.append (review['bin_id'])

            process_count += 1

print(f"{process_count} items of training data loaded after {time.time() - startTime:.2f} seconds")
# print(f"Found {non_number_count} ratings that have a non string rating")

# Define test data source
data_source_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW")
test_files_to_load = ["BOW_test_data.txt"]

# Load the training data
test_texts = []
test_outcomes = []
process_count = 0
# non_number_count = 0
for current_file in test_files_to_load:
    print(f"Starting load of training data by {current_file}...")
    file_to_read = data_source_folder / current_file
    with open(file_to_read, mode='r') as file:        
        for line in file:
            review = json.loads(line.strip())
           
            # Load the test texts
            test_texts.append (review['review_detail'])

            # Load the outcomes
            test_outcomes.append (review['bin_id'])

            process_count += 1

print(f"{process_count} items of test data loaded after {time.time() - startTime:.2f} seconds")

# Set the desired dictionary size
max_words = 1500
tokenizer.num_words = max_words

# Build the tokenized training texts
print(f"Tokenizing training texts, using dictionary of {max_words}")
# Uses TFDIF mode as a guess for what will work best
Xtrain = tokenizer.texts_to_matrix(training_texts, mode='freq')
print(f"Tokenizing training texts complete after {time.time() - startTime:.2f} seconds")
print(f"Training texts shape is {Xtrain.shape}")
print(f"Training texts example is {Xtrain[0]}")

# Buld the target training matrix
# Target is an ordinal variable -
# But, for initial version treat as a classification
# Uses the Keras to_categorical model
Ytrain = array(training_outcomes)
print(f"Training outcomes shape is {Ytrain.shape}")

# Build the tokenized test texts
print(f"Tokenizing test texts, using dictionary of {max_words}")
Xtest = tokenizer.texts_to_matrix(test_texts, mode='freq')
print(f"Tokenizing test texts complete after {time.time() - startTime:.2f} seconds")
print(f"Test texts shape is {Xtest.shape}")
print(f"Test texts example is {Xtest[0]}")

# Buld the target test matrix
# Target is an ordinal variable -
# But, for initial version treat as a classification
# Uses the Keras to_categorical model
Ytest = array(test_outcomes)
print(f"Test outcomes shape is {Ytest.shape}")

# create model
print(f"{time.time() - startTime:.2f} : Creating model")
model = Sequential()
model.add(BatchNormalization(input_dim=max_words))
model.add(Dense(100, activation='relu'))
# model.add(Dense(50, activation='relu'))
# 24 ouput options (now 3 during check vs. rating )
model.add(Dense(3, activation='softmax'))

# Compile model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(f"{time.time() - startTime:.2f} : Model compiled")

# fit model.  Include a 0.2 validation split
history = model.fit(Xtrain, Ytrain, validation_split=0.2, epochs=35, verbose=2)
print(f"{time.time() - startTime:.2f} : Model fitted")

# Evaluate the model on the test data
print("Checking against test set")
loss, acc = model.evaluate(Xtest, Ytest, verbose=2)
print('Test Accuracy: %f' % (acc))
print('Test Loss: %f' % (loss))

# Show metrics - model build progress
plt.plot (history.history['accuracy'])
plt.plot (history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')
plt.show()

# Save the model
model.save(model_save_file)
print(f"{time.time() - startTime:.2f} : Model Saved")
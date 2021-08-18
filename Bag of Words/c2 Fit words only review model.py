# Code to fit a model
#
# Created by Greg on 12/08/21
#
# Takes as input one or more files in the format generated by Data Preprocessing
# And, the tokenized dictionary generated in 'Tokenization.py'
# Model in this case uses a tokenized version of the review, not just word frequency

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
from numpy import array, argmax, atleast_2d, concatenate, random
import numpy
from sklearn.metrics import confusion_matrix
from sklearn.utils.validation import check_memory
from tensorflow.keras.layers import BatchNormalization, Dense, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.constraints import MaxNorm
from tensorflow.python.keras.layers.core import Dropout

startTime = time.time()

# Load dictonary source
tokenized_dictionary = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW/tokenized_dictionary.json")
with open(tokenized_dictionary) as f:
    tokenizer = tokenizer_from_json(f.read())
print(f"Loaded tokenized dictionary based on {tokenizer.document_count} reviews, and including {len(tokenizer.word_index)} words")

# Loads the data
def load_data (data_source_folder, files_to_load, texts, outcomes):
    
    #Load the data
    for current_file in files_to_load:
        file_to_read = data_source_folder / current_file
        with open(file_to_read, mode='r') as file:        
            for line in file:
                review = json.loads(line.strip())
                
                data_item = {}
                texts.append (review['review_detail'])
                outcomes.append (review['bin_id'])

data_source_folder = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW")

# Load the training data
training_files_to_load = ["BOW_training_data.txt"]
training_texts = []
training_outcomes = []
load_data (data_source_folder, training_files_to_load, training_texts, training_outcomes)
print(f"Time {time.time() - startTime:.2f} : {len(training_outcomes)} items loaded")

# Load the test data
test_files_to_load = ["BOW_test_data.txt"]
test_texts = []
test_outcomes = []
load_data (data_source_folder, test_files_to_load, test_texts, test_outcomes)
print(f"Time {time.time() - startTime:.2f} : {len(test_outcomes)} items loaded")

# Set the desired dictionary size
max_words = 1500
tokenizer.num_words = max_words

# Build the tokenized training texts
max_review_words = 1500
print(f"Tokenizing training texts, with length of {max_review_words} and dictionary of {max_words}")
full_reviews = tokenizer.texts_to_sequences(training_texts)
tokenised_training_texts = pad_sequences(full_reviews, max_review_words, padding='post')
print(f"Tokenizing training texts complete after {time.time() - startTime:.2f} seconds")
print(f"Training texts shape is {tokenised_training_texts.shape}")
print(f"Training texts example is {tokenised_training_texts[0]}")

# Buld the target training matrix
training_outcomes_np = array(training_outcomes)
print(f"Training outcomes shape is {training_outcomes_np.shape}")

training = concatenate((atleast_2d(training_outcomes_np).T, tokenised_training_texts), axis=1)
print(f"Training data shape is {training.shape}")

# Buld the target training matrix
# Target is an ordinal variable -
# But, for initial version treat as a classification
# Uses the Keras to_categorical model
Ytrain = array(training_outcomes)
print(f"Training outcomes shape is {Ytrain.shape}")

# Build the tokenized test texts
print(f"Tokenizing training texts, with length of {max_review_words} and dictionary of {max_words}")
full_reviews = tokenizer.texts_to_sequences(test_texts)
Xtest = pad_sequences(full_reviews, max_review_words, padding='post')
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
model.add(Dense(500, activation='relu', kernel_constraint=MaxNorm(3), input_shape=(max_review_words,)))
model.add(Dropout(0.1))
model.add(Dense(70, activation='relu', kernel_constraint=MaxNorm(3)))
model.add(Dropout(0.1))
model.add(Dense(30, activation='relu', kernel_constraint=MaxNorm(3)))
model.add(Dropout(0.1))
model.add(Dense(4, activation='softmax'))

# Compile model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(f"{time.time() - startTime:.2f} : Model compiled")

# Shuffle the training data
rng = random.default_rng()
rng.shuffle(training)

# fit model.  Include a 0.2 validation split
history = model.fit(training[:,1:], training[:,0:1], validation_split=0.2, epochs=35, verbose=2)
print(f"{time.time() - startTime:.2f} : Model fitted")

# Evaluate the model on the test data
print("Checking against test set")
loss, acc = model.evaluate(Xtest, Ytest, verbose=0)
print('Test Accuracy: %f' % (acc))
print('Test Loss: %f' % (loss))

test_predictions = model.predict(Xtest)
test_predictions=argmax(test_predictions, axis=1)
cm = confusion_matrix (Ytest, test_predictions)
print('Confusion matrix.  True labels on rows, predicted on columns')
print(cm)

# Show metrics - model build progress
plt.plot (history.history['accuracy'])
plt.plot (history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')
plt.show()

# Save the model
model_save_file = Path("C:/Users/gregp/Documents/kaggle/imdb-review-dataset/simple_BOW/saved_model.tf")
model.save(model_save_file)
print(f"{time.time() - startTime:.2f} : Model Saved")
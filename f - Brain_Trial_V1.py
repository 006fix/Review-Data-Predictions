# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 00:05:58 2021

@author: Alan
"""

import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import json
import time
from sklearn import preprocessing

inpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Brain_Dataset_v0.1"
end = ".csv"
work_lab = "_work_labels"
check_lab = "_check_labels"
work_data = "_work_data"
check_data = "_check_data"
rows_str = "_rows"
cols_str = "_cols"

#this is the check for rows
final_work = pd.read_csv((inpath+work_data+rows_str+end), index_col=0)
final_check = pd.read_csv((inpath+check_data+rows_str+end), index_col=0)
check_labels = pd.read_csv((inpath+check_lab+rows_str+end), index_col=0)
work_labels = pd.read_csv((inpath+work_lab+rows_str+end), index_col=0)

work_use = final_work.to_numpy().astype(np.float32)
check_use = final_check.to_numpy().astype(np.float32)
work_lab = work_labels.to_numpy().astype(np.float32)
check_lab = check_labels.to_numpy().astype(np.float32)



model = tf.keras.Sequential([
    tf.keras.layers.Dense(1600, activation='relu'),
    tf.keras.layers.Dropout(0.16),
    tf.keras.layers.Dense(800, activation='relu'),
    tf.keras.layers.Dropout(0.12),
    tf.keras.layers.Dense(400, activation='relu'),
    tf.keras.layers.Dropout(0.08),
    tf.keras.layers.Dense(200, activation='relu'),
    tf.keras.layers.Dropout(0.03),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(3)
    ])

model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(work_use, work_lab, validation_split=0.1,batch_size=32,epochs=25)

model.summary()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

probability_model = tf.keras.Sequential([model,tf.keras.layers.Softmax()])

predictions = probability_model.predict(check_use)

master_list = []
for i in range(len(check_lab)):
    hold_list = []
    hold_list.append(check_lab[i])
    predicted_val = np.argmax(predictions[i])
    hold_list.append(predicted_val)
    if check_lab[i] == predicted_val:
        correct_results = 1
    else:
        correct_results = 0
    hold_list.append(correct_results)
    master_list.append(hold_list)
    
    
output_df = pd.DataFrame(master_list, columns=['true_label', 'predicted_label', 'correct_flag'])

outpath = r"C:\Users\Alan\Desktop\Review Data\Dataframes\Brain_Dataset_v0.1_trial_1_output_CHECK.csv"
output_df.to_csv(outpath)

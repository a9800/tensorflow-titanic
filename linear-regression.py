from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import clear_output
from six.moves import urllib

import tensorflow.compat.v2.feature_column as fc

import tensorflow as tf

# A Linear regression AI model to calculate who would survive a simulated Titanic

# Load dataset.
dftrain = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv') # training data
dfeval  = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv')  # testing data
y_train = dftrain.pop('survived')
y_eval  = dfeval.pop('survived')

# Categorical data must be encoded from strings to integers in order to make them easier to handle

CATEGORICAL_COLUMNS = ['sex','parch','class','deck','embark_town','alone']

NUMERIC_COLUMNS = ['age', 'n_siblings_spouses' ,'fare']

feature_columns = []


for feature_name in CATEGORICAL_COLUMNS:
    # gets a list of all unique values from that feature name
    vocabulary = dftrain[feature_name].unique()
    # create a feature column with the feature name and the different vocablary associated to it
    feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name,vocabulary))

for feature_name in NUMERIC_COLUMNS:
    feature_columns.append(tf.feature_column.numeric_column(feature_name,dtype=tf.float32))


# The input function takes the pandas dataframe above and converts it to a tf.data.Dataset object 

def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
  def input_function():  # inner function, this will be returned
    ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))  # create tf.data.Dataset object with data and its label
    if shuffle:
      ds = ds.shuffle(1000)  # randomize order of data
    ds = ds.batch(batch_size).repeat(num_epochs)  # split dataset into batches of 32 and repeat process for number of epochs
    return ds  # return a batch of the dataset
  return input_function  # return a function object for use

train_input_fn = make_input_fn(dftrain, y_train)  # here we will call the input_function that was returned to us to get a dataset object we can feed to the model
eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=1, shuffle=False)

linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)

# Training the model 

linear_est.train(train_input_fn)  # train
result = linear_est.evaluate(eval_input_fn)  # get model metrics/stats by testing on testing data

clear_output()  # clears console output
print("Accuracy = ", result['accuracy'])  # the result variable is a dict of stats about our model

prediction = list(linear_est.predict(eval_input_fn))
print(dfeval.loc[0])
print(prediction[0]['probabilities'][0])


# -*- coding: utf-8 -*-

from __future__ import print_function
from hyperopt import Trials, STATUS_OK, tpe, rand
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.metrics import accuracy_score
from hyperas import optim
from hyperas.distributions import choice, uniform, conditional
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import pandas as pd
import numpy as np
from keras import models
from keras import layers
import numpy as np
from keras import optimizers
from keras import callbacks
from sklearn.utils import shuffle
from keras import backend as K

def read_data():

  df = pd.read_csv('../../inputs/final_processed_data.csv')

  df['height'] = df['height'] / df['height'].max()
  df['matches_year1'] = df['matches_year1'] / df['matches_year1'].max()
  df['matches_year2'] = df['matches_year2'] / df['matches_year2'].max()
  df['goals_year1'] = df['goals_year1'] / df['goals_year1'].max()
  df['goals_year2'] = df['goals_year2'] / df['goals_year2'].max()
  df['goals_per_match_year1'] = df['goals_per_match_year1'] / df['goals_per_match_year1'].max()
  df['goals_per_match_year2'] = df['goals_per_match_year2'] / df['goals_per_match_year2'].max()
  df['goals_per_match_year3'] = df['goals_per_match_year3'] / df['goals_per_match_year3'].max()

  data = shuffle(df, random_state=42)
  data = data.drop('name', 1)

  data = data.sort_values(by=['goals_per_match_year3'])

  y = data[['goals_per_match_year3']].values.astype('float32')

  data = data.drop('goals_per_match_year3', 1)
  x = data.values.astype('float32')

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
  x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=42)

  return x_train, x_val, x_test, y_train, y_val, y_test

def create_model(x_train, y_train, x_val, y_val, layer_sizes):

  def coeff_determination(y_true, y_pred):
    SS_res = K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return (1 - SS_res / (SS_tot + K.epsilon()))

  model = models.Sequential()

  model.add(layers.Dense({{choice([np.power(2, 0), np.power(2, 1), np.power(2, 2), np.power(2, 3),
                                   np.power(2, 4), np.power(2, 5), np.power(2, 6), np.power(2, 7)])}}, 
            activation={{choice(['relu','selu','tanh','softmax','softplus','linear',None])}}, 
            input_shape=(len(data.columns),)))

  model.add(layers.Dense({{choice([np.power(2, 0), np.power(2, 1), np.power(2, 2), np.power(2, 3),
                                   np.power(2, 4), np.power(2, 5), np.power(2, 6), np.power(2, 7)])}}, 
            activation={{choice(['relu','selu','tanh','softmax','softplus','linear',None])}}))

  model.add(layers.Dense({{choice([np.power(2, 0), np.power(2, 1), np.power(2, 2), np.power(2, 3),
                                   np.power(2, 4), np.power(2, 5), np.power(2, 6), np.power(2, 7)])}}, 
            activation={{choice(['relu','selu','tanh','softmax','softplus','linear',None])}}))

  model.add(layers.Dense(1, activation={{choice(['relu','selu','tanh','softmax','softplus','linear',None])}}))

  RMS = optimizers.Adamax(lr={{choice([0.0001, 0.001, 0.01, 0.1])}}, beta_1=0.9, beta_2=0.999)

  model.compile(optimizer=RMS,
                loss={{choice(['mean_absolute_error','mean_squared_error','mean_absolute_percentage_error',
                               'mean_squared_logarithmic_error','hinge','squared_hinge','logcosh'])}},
                metrics=[coeff_determination])

  model.fit(x_train, y_train, epochs={{choice([25, 50, 75, 100, 500])}}, 
            batch_size={{choice([10, 16, 20, 32, 64])}}, validation_data=(x_val, y_val))

  score, acc = model.evaluate(x_val, y_val, verbose=0)
  print('Validation accuracy:', acc)

  return {'loss': -acc, 'status': STATUS_OK, 'model': model}

if __name__ == '__main__':

  best_run, best_model, space = optim.minimize(model=create_model, data=read_data, algo=tpe.suggest, max_evals=15,
                                               trials=Trials(), eval_space=True, return_space=True)

  print("Best performing model chosen hyper-parameters:")
  print(best_run)

  print ("4 layers")


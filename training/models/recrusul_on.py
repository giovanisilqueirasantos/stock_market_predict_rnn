import numpy as np
import pandas as pd
from collections import deque
from random import shuffle
from time import time
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from get_data import GetData

SEQ_LEN = 3
EPOCHS = 10
BATCH_SIZE = 3
NAME = f"RECRUSUL_ON-SEQ-{SEQ_LEN}-EPOCHS-{EPOCHS}-BATCH_SIZE-{BATCH_SIZE}-TIME-{int(time())}"

def preprocess_df(df):          
  df.dropna(inplace=True)
  
  sequential_data = []
  prev_days = deque(maxlen=SEQ_LEN)
  
  for i in df.values:
      prev_days.append([n for n in i[:-1]])
      if len(prev_days) == SEQ_LEN:
        sequential_data.append([np.array(prev_days), i[-1]])
      
  shuffle(sequential_data)
  
  x = []
  y = []
  
  for seq, target in sequential_data:
      x.append(seq)
      y.append(target)
      
  return np.array(x), y

data = GetData('mongodb://root:root@stock_price_mongo/admin', 27017, 'stock_price', 'recrusul_on')
df = data.get_all_processed_data()

times = df.index.values
last_pct = times[-int(0.2*len(times))]

validation_df = df[(df.index >= last_pct)]
df = df[(df.index < last_pct)]
x_train, y_train = preprocess_df(df)
x_test, y_test = preprocess_df(validation_df)

model = Sequential()

model.add(LSTM(128, input_shape=(x_train.shape[1:]), activation='relu', return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(LSTM(128, input_shape=(x_train.shape[1:]), activation='relu', return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(LSTM(128, input_shape=(x_train.shape[1:]), activation='relu'))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(2, activation='softmax'))

opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

model.compile(loss='sparse_categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

tesorboard = TensorBoard(log_dir=f'../logs/{NAME}')

filepath = "RNN_Final-{epoch:02d}-{val_acc:.3f}"
checkpoint = ModelCheckpoint("../check_points/recrusul_on/{}.model".format(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max'))

history = model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(x_test, y_test), callbacks=[tesorboard, checkpoint])

model.save('../store/recrusul_on.h5')
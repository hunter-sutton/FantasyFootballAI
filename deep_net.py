import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from keras.callbacks import EarlyStopping
from keras.regularizers import l2
from keras.layers import Dropout

df = pd.read_csv("player_stats.csv", index_col=0)

# drop the rows where position is "QB" or "K"
df = df[df.position != 'QB']
df = df[df.position != 'K']

# read in columns_to_drop.csv where each row is a column to drop
columns_to_drop = pd.read_csv("columns_to_drop.csv", header=None)

label = LabelEncoder()
df['position'] = label.fit_transform(df['position'])

df.fillna(0, inplace=True)

# if the column name contains a string from columns_to_drop, drop it
for col in df.columns:
	for string in columns_to_drop[0]:
		if string in col:
			df = df.drop([col], axis=1)
			break

# drop the rows with 25% or more missing values
df = df.dropna(thresh=df.shape[1] * 0.50, axis=0)

df.to_csv("player_stats_trimmed.csv")

# split the dataframe into X and y
X = df.loc[:, ~df.columns.str.startswith('14_')]
y = df['14_pointsScored']

# # split X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True)

# Scale the data
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the model
model = Sequential()

# Input layer and first hidden layer with Dropout regularisation
model.add(Dense(units=64, activation='relu', input_shape=(X_train_scaled.shape[1],)))
model.add(Dropout(0.1))  # Dropout 10% of the neurons

# Second hidden layer with Dropout regularisation
model.add(Dense(units=32, activation='relu'))
model.add(Dropout(0.1))  # Dropout 10% of the neurons

# Output layer
model.add(Dense(units=1, activation='linear'))  # Use linear activation function for regression

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Callback for early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5)

# Fit the model to the training data
history = model.fit(
    X_train_scaled, y_train,
    validation_split=0.2,
    epochs=100,
    callbacks=[early_stopping],
    batch_size=32,  
    verbose=1
)

# Evaluate the model
train_loss = model.evaluate(X_train_scaled, y_train, verbose=0)
test_loss = model.evaluate(X_test_scaled, y_test, verbose=0)

print(f'Train Loss: {train_loss}')
print(f'Test Loss: {test_loss}')

# Plot the validation and training loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'])
plt.show()
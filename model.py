# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 00:35:32 2019

@author: 91727
"""
#import dataset and divide into input and output set.
import numpy as np
import pandas as pd
dataset = pd.read_csv('final.csv', encoding = "ISO-8859-1", error_bad_lines=False)
x = dataset.iloc[1:,1:7].values
y = dataset.iloc[1:,7:8].values

#deal with missing data, replace missing data with average
from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values = 0, strategy = 'mean', axis = 0)
imputer = imputer.fit(x[:, 2:3])
x[:, 2:3] = imputer.transform(x[:, 2:3])

imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
imputer = imputer.fit(y[:, 0:1])
y[:, 0:1] = imputer.transform(y[:, 0:1])

# Encoding categorical data
# Encoding the Independent Variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelencoder_x = LabelEncoder()
x[:, 0] = labelencoder_x.fit_transform(x[:, 0])

labelencoder_x = LabelEncoder()
x[:, 5] = labelencoder_x.fit_transform(x[:, 5])

for i in range(len(x)):
    s = x[i][3]
    s = s.replace(",", "")
    x[i][3] = float(s)

onehotencoder = OneHotEncoder(categorical_features = [0])
x = onehotencoder.fit_transform(x).toarray()

onehotencoder = OneHotEncoder(categorical_features = [37])
x = onehotencoder.fit_transform(x).toarray()

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

#fit the model and train it (random forest)
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 500, random_state = 0)
regressor.fit(x_train, y_train)

#predict the output upon testing dataset
y_pred = regressor.predict(x_test)

#plot the graph to visualize the accuracy.
import matplotlib.pyplot as plt
plt.figure(1,figsize=(13.5, 10))
plt.plot(y_test, color = "red")
plt.plot(y_pred, color = "blue")
plt.show()

importances = regressor.feature_importances_
indices = np.argsort(importances)
features = []
for i in range(0,43):
    features.append(i)
    
indices_value = []
for i in range(0,len(indices)):
    indices_value.append(features[indices[i]])
plt.figure(1,figsize=(13.5, 10))
plt.barh(range(len(indices)), importances[indices], color='#5485C0', align='center')
plt.yticks(range(len(indices)), indices_value)
plt.xlabel('Relative Importance')
plt.savefig('Features Importance.png')
    

print("Success")
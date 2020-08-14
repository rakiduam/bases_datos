# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 22:25:29 2020


idea general, porque usar sklearn, posee funciones de machine learn
ademas tiene ventajas como la capacidad de "normalizar" datos y generar
sets rapidos de entrenamiento y validacion.

idea general:
    generar un script que sea relativamente simple, que permite incluir una
    regresion de tipo multiple o simple, que realice un analisis de tipo
    k-folds.

solo generar una funcion que realice el crossvalidation

K-Folds Cross Validation

fuentes de info:
    - https://medium.com/dunder-data/from-pandas-to-scikit-learn-a-new-exciting-workflow-e88e2271ef62
    - https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
    - https://blog.usejournal.com/a-quick-introduction-to-k-nearest-neighbors-algorithm-62214cea29c7

conceptos:
    - https://en.wikipedia.org/wiki/Ordinary_least_squares

@author: fanr
"""
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import statsmodels.api as sm # import statsmodels
import statsmodels.api as sm


# ejemplos de realizar regresion multiple con distintos modelos en este caso
# primero se carga el dataset y luego se usara statsmodels y asi.

data = datasets.load_boston()
type(data)
print(data.DESCR)
data.feature_names
data.target

# define the data/PREDICTORS as the pre-set feature names
df = pd.DataFrame(data.data, columns=data.feature_names)

# Put the TARGET (housing value -- MEDV) in another DataFrame
target = pd.DataFrame(data.target, columns=["MEDV"])

## Without a constant

X = df["RM"]
y = target["MEDV"]

# Note the difference in argument order
model = sm.OLS(y, X).fit()
predictions = model.predict(X) # make the predictions by the model

# Print out the statistics
model.summary()
model.rsquared
model.rsquared_adj
model.ssr

# The coefficient of 3.6534 means that as the RM variable increases by 1,
# the predicted value of MDEV increases by 3.6534.

# constante forzando pasar por 0. en pp puede hacer sentido.

X = df["RM"] ## X usually means our input variables (or independent variables)
y = target["MEDV"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model
# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)
# Print out the statistics
model.summary()

X = df[['RM', 'LSTAT']]
y = target['MEDV']

model = sm.OLS(y, X).fit()
predictions = model.predict(X)
model.summary()



from sklearn import datasets ## imports datasets from scikit-learn
data = datasets.load_boston() ## loads Boston dataset from datasets library
# define the data/predictors as the pre-set feature names
df = pd.DataFrame(data.data, columns=data.feature_names)
# Put the target (housing value -- MEDV) in another DataFrame
target = pd.DataFrame(data.target, columns=["MEDV"])

X = df
y = target['MEDV']

lm = linear_model.LinearRegression()
model = lm.fit(X,y)

predictions = lm.predict(X)
print(predictions)[0:5]

# salida de informacion arroja el R2
lm.score(X,y)

# Load the Diabetes dataset
columns = “age sex bmi map tc ldl hdl tch ltg glu”.split() # Declare the columns names
diabetes = datasets.load_diabetes() # Call the diabetes dataset from sklearn
df = pd.DataFrame(diabetes.data, columns=columns) # load the dataset as a pandas data frame
y = diabetes.target # define the target variable (dependent variable) as y


# create training and testing vars
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2)
print X_train.shape, y_train.shape
print X_test.shape, y_test.shape(353, 10) (353,)
(89, 10) (89,)

# fit a model
lm = linear_model.LinearRegression()model = lm.fit(X_train, y_train)
predictions = lm.predict(X_test)

predictions[0:5]
array([ 205.68012533,   64.58785513,  175.12880278,  169.95993301,
        128.92035866])


## The line / model
plt.scatter(y_test, predictions)
plt.xlabel(“True Values”)
plt.ylabel(“Predictions”)

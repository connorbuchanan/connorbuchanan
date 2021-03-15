# -*- coding: utf-8 -*-
"""
Connor Buchanan
version 1.0 - 1/13/2021

Process to create and choose the best model. Iterates through all possible data point combinations
"""

# Load libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from matplotlib import pyplot
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import sqlite3
import matplotlib as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier


#connect to database to gather all relevant data points
conn = sqlite3.connect('C:\Users\conno\OneDrive\Documents\Gambling Project\SQL\Soccer.db')
c = conn.cursor()

"""
#create query string
queryString = "SELECT * FROM MATCH M JOIN POINTS P ON M.URL_ID=P.URL_ID JOIN GOALS G ON M.URL_ID=G.URL_ID JOIN OPP_GOALS OG " \
                +"ON M.URL_ID=OG.URL_ID  " \
                +"WHERE M.RESULT IS NOT NULL"
"""

#Test as if draws don't exist
#create query string
queryString = "SELECT * FROM MATCH M JOIN POINTS P ON M.URL_ID=P.URL_ID JOIN GOALS G ON M.URL_ID=G.URL_ID JOIN OPP_GOALS OG " \
                +"ON M.URL_ID=OG.URL_ID JOIN CHANCES C ON M.URL_ID=C.URL_ID JOIN SHOTS S ON M.URL_ID=S.URL_ID JOIN OPP_SHOTS OP " \
                +"ON M.URL_ID=OP.URL_ID JOIN OTHER_STATS OS ON M.URL_ID=OS.URL_ID WHERE M.RESULT IS NOT NULL AND M.RESULT != 'DRAW'"




#return dataframe and close connection
statDF = pd.read_sql_query(queryString,conn)
conn.close() 

#delete duplicated URL_ID columns
statDF = statDF.loc[:,~statDF.columns.duplicated()]

del statDF['LEAGUE']

"""
#create list of all predictive columns
colList = list(statDF.columns)
del colList[0:5]

#create list of all possible data point combinations
comboList = []
for subset in itertools.combinations(colList, 20):
    comboList.append(subset)
"""

"""MODEL PREP AND SETUP"""
#split out valiation dataset
X = statDF
y = statDF['RESULT']

X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=6)

#specify columns to be used for training
#X_train_data = X_train.loc[:,['HOME_BIG_SIX'	,'AWAY_BIG_SIX'	,'H_PTS_V_OPPTYPE_5'	,'H_PTS_V_OPPTYPE_10'	,'H_PTS_HOME_V_OPPTYPE_5'	,'H_PTS_HOME_V_OPPTYPE_10'	,'H_XPTS_V_OPPTYPE_5'	,'H_XPTS_V_OPPTYPE_10'	,'H_XPTS_HOME_V_OPPTYPE_5'	,'H_XPTS_HOME_V_OPPTYPE_10'	,'A_PTS_V_OPPTYPE_5'	,'A_PTS_V_OPPTYPE_10'	,'A_PTS_AWAY_V_OPPTYPE_5'	,'A_PTS_AWAY_V_OPPTYPE_10'	,'A_XPTS_V_OPPTYPE_5'	,'A_XPTS_V_OPPTYPE_10'	,'H_G_V_OPPTYPE_5'	,'H_G_V_OPPTYPE_10'	,'H_G_HOME_V_OPPTYPE_5'	,'H_G_HOME_V_OPPTYPE_10'	,'H_XG_V_OPPTYPE_5'	,'H_XG_V_OPPTYPE_10'	,'H_XG_HOME_V_OPPTYPE_5'	,'H_XG_HOME_V_OPPTYPE_10'	,'A_G_V_OPPTYPE_5'	,'A_G_V_OPPTYPE_10'	,'A_G_AWAY_V_OPPTYPE_5'	,'A_G_AWAY_V_OPPTYPE_10'	,'A_XG_V_OPPTYPE_5'	,'A_XG_V_OPPTYPE_10']]
#X_validation_data = X_validation.loc[:,['HOME_BIG_SIX'	,'AWAY_BIG_SIX'	,'H_PTS_V_OPPTYPE_5'	,'H_PTS_V_OPPTYPE_10'	,'H_PTS_HOME_V_OPPTYPE_5'	,'H_PTS_HOME_V_OPPTYPE_10'	,'H_XPTS_V_OPPTYPE_5'	,'H_XPTS_V_OPPTYPE_10'	,'H_XPTS_HOME_V_OPPTYPE_5'	,'H_XPTS_HOME_V_OPPTYPE_10'	,'A_PTS_V_OPPTYPE_5'	,'A_PTS_V_OPPTYPE_10'	,'A_PTS_AWAY_V_OPPTYPE_5'	,'A_PTS_AWAY_V_OPPTYPE_10'	,'A_XPTS_V_OPPTYPE_5'	,'A_XPTS_V_OPPTYPE_10'	,'H_G_V_OPPTYPE_5'	,'H_G_V_OPPTYPE_10'	,'H_G_HOME_V_OPPTYPE_5'	,'H_G_HOME_V_OPPTYPE_10'	,'H_XG_V_OPPTYPE_5'	,'H_XG_V_OPPTYPE_10'	,'H_XG_HOME_V_OPPTYPE_5'	,'H_XG_HOME_V_OPPTYPE_10'	,'A_G_V_OPPTYPE_5'	,'A_G_V_OPPTYPE_10'	,'A_G_AWAY_V_OPPTYPE_5'	,'A_G_AWAY_V_OPPTYPE_10'	,'A_XG_V_OPPTYPE_5'	,'A_XG_V_OPPTYPE_10']]

"""Change this section for desired columns"""
X_train_data = X_train.iloc[:,5:]
X_validation_data = X_validation.iloc[:,5:]


"""Stepwise model building"""
"""Univariate feature selection"""
from sklearn.feature_selection import SelectKBest, chi2
X_5_best= SelectKBest(chi2, k=35).fit(X_train_data, Y_train)             
mask = X_5_best.get_support() #list of booleans for selected features
new_feat = [] 
for bool, feature in zip(mask, X_train_data.columns):
    if bool:
        new_feat.append(feature)
print('The best features are:{}'.format(new_feat))


"""Recursive feature elimination"""
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
estimator = RandomForestClassifier(random_state = 42)
selector = RFE(estimator, 5, step=1)
selector = selector.fit(X_train_data, Y_train)
rfe_mask = selector.get_support() #list of booleans for selected features
new_features = [] 
for bool, feature in zip(rfe_mask, X_train_data.columns):
    if bool:
        new_features.append(feature)
new_features # The list of your 5 best features


"""Recursive feature elimination with cross-validation"""
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier
cv_estimator = RandomForestClassifier(random_state =1)
cv_estimator.fit(X_train_data, Y_train)
cv_selector = RFECV(cv_estimator,cv= 5, step=1,scoring='accuracy')
cv_selector = cv_selector.fit(X_train_data, Y_train)
rfecv_mask = cv_selector.get_support() #list of booleans
rfecv_features = [] 
for bool, feature in zip(rfecv_mask, X_train_data.columns):
    if bool:
        rfecv_features.append(feature)
print('Optimal number of features :', cv_selector.n_features_)
print('Best features :', rfecv_features)
n_features = X_train_data.shape[1]
#plt.figure(figsize=(8,8))
#plt.barh(range(n_features), cv_estimator.feature_importances_, align='center') 
#plt.yticks(np.arange(n_features), X_train_data.columns.values) 
#plt.xlabel('Feature importance')
#plt.ylabel('Feature')
#plt.show()



#select based on stepwise
X_train_data = X_train.loc[:,['HOME_BIG_SIX'	,'AWAY_BIG_SIX'	,'H_PTS_5'	,'H_G_5'	,'H_OPP_G_5'	,'H_XPTS_5'	,'H_XG_5'	,'H_OPP_XG_5'	,'A_PTS_5'	,'A_G_5'	,'A_OPP_G_5'	,'A_XPTS_5'	,'A_XG_5'	,'A_OPP_XG_5'	,'H_DEEP_5'	,'H_PPDA_5'	,'A_DEEP_5'	,'A_PPDA_5'	,'H_SHT_5'	,'A_SHT_5']]
X_validation_data = X_validation.loc[:,['HOME_BIG_SIX'	,'AWAY_BIG_SIX'	,'H_PTS_5'	,'H_G_5'	,'H_OPP_G_5'	,'H_XPTS_5'	,'H_XG_5'	,'H_OPP_XG_5'	,'A_PTS_5'	,'A_G_5'	,'A_OPP_G_5'	,'A_XPTS_5'	,'A_XG_5'	,'A_OPP_XG_5'	,'H_DEEP_5'	,'H_PPDA_5'	,'A_DEEP_5'	,'A_PPDA_5'	,'H_SHT_5'	,'A_SHT_5']]


# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
models.append(('RF',RandomForestClassifier()))
models.append(('GBST',GradientBoostingClassifier()))
models.append(('NN', MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)))

models = []
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('NN', MLPClassifier(hidden_layer_sizes=(15,15,15), max_iter=10000)))


"""Evaluate each model and combo of dataset"""
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=21, shuffle=True)
	cv_results = cross_val_score(model, X_train_data, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
    
    
# Compare Algorithms
pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()



#predict
model = MLPClassifier(hidden_layer_sizes=(15,15,15), max_iter=10000)
model.fit(X_train_data, Y_train)
predictions = model.predict(X_validation_data)
probPredict = model.predict_proba(X_validation_data)


# Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))


#add results of model to dataframe
resultsDF = X_validation[['URL_ID','EVENT_DATE','HOME_TEAM','AWAY_TEAM','RESULT']].copy()
resultsDF['Pred'] = predictions
resultsDF['HOME_PROB'],resultsDF['AWAY_PROB'] = probPredict[:,1],probPredict[:,0]
print(resultsDF.head())

#export the model predictions to a .csv for further analysis
#resultsDF.to_csv('Predictions.csv')

#save model for later use
#import pickle
#pickle.dump(model, open('Global_NN_v1', 'wb'))


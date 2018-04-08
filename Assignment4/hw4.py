# File house-votes-84.txt (attached) contains 435 records of UnitedStates representatives.  
# Each record shows how the representative voted on each of 16 different issues (columns in the file).
# Based on the voting records, guess the party affiliation of the representative 
# (there are only two parties represented in the United States Congress: Democratic and Republican).
# Your tasks:
# 1) Create a classification model of your choice (naive Bayes, logistic regression, Bayesian network, neural networks, etc.)
# 2) Find overall classification accuracy
# 3) Report sensitivity and specificity for each of the two parties
# 4) Measure positive and negative predictive value for each of the two parties
# 5) Plot ROC curve of your model
# http://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html


# Please use the five-fold cross-validation method in your tests.


import matplotlib.pyplot as plt # https://matplotlib.org/api/pyplot_summary.html
from mpl_toolkits.mplot3d import Axes3D
import numpy as np # https://docs.scipy.org/doc/numpy/reference/
import pandas as pd # https://pandas.pydata.org/pandas-docs/stable/
import scipy.special as spec # https://docs.scipy.org/doc/scipy/reference/special.html
import scipy.stats as st # https://docs.scipy.org/doc/scipy/reference/stats.html
import seaborn as sns # https://seaborn.pydata.org/api.html



print('Load house-votes-84.txt into Pandas DataFrame')
votes_ori = pd.read_csv('house-votes-84.txt', sep='\s+')
votes_ori = np.array(votes_ori)
votes = np.array(votes_ori,copy=True)

party = votes[:,0:1]
rep_idx = (party == 'republican')
party[rep_idx] = 0

dem_idx = (party == 'democrat')
party[dem_idx] = 1
party = party.astype(int)

N = party.shape[0]

vote_input = votes[:,1:]
vote_input[vote_input=='n'] = 0
vote_input[vote_input=='y'] = 1
vote_input[vote_input=='w'] = 2
vote_input = vote_input.astype(int)



# 1) Create a classification model of your choice (logistic regression)
# use the five-fold cross-validation method in your tests.
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(vote_input, party, test_size=0.2, random_state=0)

# print(x_test.shape)
# print(x_train.shape)
# print(y_test.shape)
# print(y_train.shape)

from sklearn.linear_model import LogisticRegression
logisticRegr = LogisticRegression()
logisticRegr.fit(x_train, y_train.ravel())


from sklearn import cross_validation

scores = cross_validation.cross_val_score(logisticRegr, vote_input, party.ravel(), cv=5)
print(scores)

# 2) Find overall classification accuracy
y_pdt_all  = logisticRegr.predict(vote_input)
err = np.sum(y_pdt_all != party.ravel())
print("err num is %d" %err)
print("err is %f" %(err / N))

# 3) Report sensitivity and specificity for each of the two parties
# (number of) positive samples (P)
# (number of) negative samples (N)
# (number of) true positive (TP)
# eqv. with hit
# (number of) true negative (TN)
# eqv. with correct rejection

# (number of) false positive (FP)
# eqv. with false alarm, Type I error
# (number of) false negative (FN)

# sensitivity or true positive rate (TPR)
# eqv. with hit rate, recall
# TPR = TP / P = TP / (TP + FN)

# specificity (SPC) or true negative rate
# SPC = TN / N = TN / (TN + FP)


# "true positive" is the event that the test makes a positive prediction, 
# and the subject has a positive result under the gold standard, and 
# "false positive" is the event that the test makes a positive prediction, 
# and the subject has a negative result under the gold standard.

# "true negative" is the event that the test makes a negative prediction, 
# and the subject has a negative result under the gold standard, 
# and a "false negative" is the event that the test makes a negative prediction, 
# and the subject has a positive result under the gold standard.





Pos = np.sum(party == 1)
Neg = np.sum(party == 0)


Pos_pdt = y_pdt_all == 1
Neg_pdt = y_pdt_all == 0

TP = np.sum(party.ravel()[Pos_pdt] == 1)
FP = np.sum(party.ravel()[Pos_pdt] == 0)

TN = np.sum(party.ravel()[Neg_pdt] == 0)
FN = np.sum(party.ravel()[Neg_pdt] == 1)

print(TP,FP,TN,FN)




# print(Pos, Neg)
crt_idx = party.ravel() == y_pdt_all
TP = np.sum(party[crt_idx] == 1)
TN = np.sum(party[crt_idx] == 0)
print(TP,TN)
# print(TP,TN)
TPR = TP / Pos
SPC = TN / Neg
print("sensitivity is %5f, specificity is %5f" %(TPR, SPC))


# 4) Measure positive and negative predictive value for each of the two parties
y_val = logisticRegr.decision_function(vote_input)

# 5) Plot ROC curve of your model
#  true positive rate (TPR) against the false positive rate (FPR)
from sklearn import metrics
fpr, tpr, thresholds = metrics.roc_curve(party, y_val, pos_label=1)
# print(fpr,tpr,thresholds)
# print(fpr.shape,tpr.shape,thresholds.shape)

# http://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html

plt.figure()
plt.plot(fpr, tpr, color='darkorange')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.show()




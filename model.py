import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# sklearn imports
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer

# tree classifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

# rainforest classifier
from sklearn.ensemble import RandomForestClassifier

# linear regession classifier
from sklearn.linear_model import LogisticRegression

# KNN classifier
from sklearn.neighbors import KNeighborsClassifier
import wrangle as w

def model_df():
    df = w.clean_df()
    
    # Keep columns
    df = df[["state", "breach_type", "location", "multi_breached_location", "summer"]]
    
    # create dummies
    dummy_df = pd.get_dummies(df[["state", "location"]],
                            drop_first=True)
    df = pd.concat([df, dummy_df], axis=1)
    df = df.drop(columns=["state","location"])

    return df

def create_x_y(train, validate, test, target):
    """
    This function creates x and y variables for either a decision tree or a random forest, 
    by using the unsplit df, target variable columns name and column to drop, for multiple columns that need to be 
    dropped create a list of the columns0
    The arguments taken in are train, validate, test, target, drop_col=[])
    The function returns x_train, y_train, x_validate, y_validate, x_test, y_test
    """
    # separates train target variable
    x_train = train.drop(columns=[target])
    y_train = train[target]
    # validate 
    x_validate = validate.drop(columns=[target])
    y_validate = validate[target]

    # test
    x_test = test.drop(columns=[target])
    y_test = test[target]
    
    return x_train, y_train, x_validate, y_validate, x_test, y_test

# final test model

def best_model(x_train, y_train, x_validate, y_validate, x_test, y_test):
    '''
    ! WARNING!: Only use this for your final model 
    This function provides a quick print output of the baseling accuracy train, validation, test scores based on your classifier, for easy viewing.
    The function takes the following arguments: object name (clf), x_train, y_train, x_validate, y_validate, x_test, y_test
    '''
    rf = RandomForestClassifier(random_state=3, min_samples_leaf=5, max_depth=6)
    rf = rf.fit(x_train, y_train)
    # model.fit(x, y)
    print(f'''
    Accuracy of {rf} on training set: {round(rf.score(x_train, y_train), 2)}
    Accuracy of {rf} on validation set: {round(rf.score(x_validate, y_validate), 2)}
    Accuracy of {rf} on test set: {round(rf.score(x_test, y_test), 2)}
    ''')


####################################### Decision Tree model functions

def best_tree(x_train, y_train, x_validate, y_validate):
    '''
    This function provides a quick print output of the train and validation scores based on the decision trees, for easy viewing.
    The function takes the following arguments: logit, x_train, y_train, x_validate, y_validate
    '''
    tree = DecisionTreeClassifier(max_depth=7, random_state=3)

    # model.fit(x, y)
    tree = tree.fit(x_train, y_train)

    print(f'''
    Accuracy of Decision Tree classifier on training set: {round(tree.score(x_train, y_train), 2)}
    Accuracy of Decision Tree classifier on validation set: {round(tree.score(x_validate, y_validate),2)}
    ''')




######################################## Random Forest model functions 

def best_forest(x_train, y_train, x_validate, y_validate):
    '''
    This function provides a quick print output of the train and validation scores based on the random forest, for easy viewing.
    The function takes the following arguments: logit, x_train, y_train, x_validate, y_validate
    '''
    rf = RandomForestClassifier(random_state=3, min_samples_leaf=5, max_depth=6)

    # model.fit(x, y)
    rf = rf.fit(x_train, y_train)

    print(f'''
    Accuracy of Random Forest on training set: {round(rf.score(x_train, y_train), 2)}
    Accuracy of Random Forest on validation set: {round(rf.score(x_validate, y_validate),2)}
    ''')


#################################### Logistic Regression model functions 
def logit_accuracy(x_train, y_train, x_validate, y_validate):
    '''
    This function provides a quick print output of the train and validation scores based on the logisitics regression, for easy viewing.
    The function takes the following arguments: logit, x_train, y_train, x_validate, y_validate
    '''
    logit = LogisticRegression()

    # model fit 
    logit.fit(x_train, y_train)
    print(f'''

    Accuracy of Logistic Regression on training set: {round(logit.score(x_train, y_train), 2)}
    Accuracy of Logistic Regression on validation set: {round(logit.score(x_validate, y_validate), 2)}
    ''')


####################### KNN model functions
def best_knn(x_train, y_train, x_validate, y_validate):
    '''
    This function provides a quick print output of the train and validation scores based on the KNN model, for easy viewing.
    The function takes the following arguments: logit, x_train, y_train, x_validate, y_validate
    '''
    knn = KNeighborsClassifier(n_neighbors = 10)
    knn.fit(x_train, y_train)
    print(f'''
    Accuracy of KNN on training set: {round(knn.score(x_train, y_train),2)}
    Accuracy of KNN on validation set: {round(knn.score(x_validate, y_validate),2)}
    ''')
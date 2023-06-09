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
    """
    Preprocesses the data and creates a DataFrame suitable for modeling.

    Returns:
    -------
    df : pandas DataFrame
        Preprocessed DataFrame containing selected columns and dummy variables.

    Usage:
    ------
    df = model_df()
    """
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
    rf = RandomForestClassifier(random_state=3, min_samples_leaf=1, max_depth=10)
    rf = rf.fit(x_train, y_train)
    # model.fit(x, y)
    print(f'''
    Accuracy of {rf} on training set: {round(rf.score(x_train, y_train), 2)}
    Accuracy of {rf} on validation set: {round(rf.score(x_validate, y_validate), 2)}
    Accuracy of {rf} on test set: {round(rf.score(x_test, y_test), 2)}
    ''')


####################################### Decision Tree model functions
def depth_check(x_train, y_train, x_validate, y_validate):
    """
    Evaluate decision tree classifiers with varying max_depth values on training and validation data.

    Parameters:
        x_train (array-like): Training data features.
        y_train (array-like): Training data target labels.
        x_validate (array-like): Validation data features.
        y_validate (array-like): Validation data target labels.

    Returns:
        pandas.DataFrame: DataFrame containing the max_depth, train_accuracy, validate_accuracy, and difference columns.

    Raises:
        None

    Example:
        scores = depth_check(x_train, y_train, x_validate, y_validate)
    """
    scores_all = []
    for x in range(1,5):

        tree = DecisionTreeClassifier(max_depth=x, random_state=3)
        tree.fit(x_train, y_train)
        train_accuracy = tree.score(x_train, y_train)

        #evaluate on validate
        validate_accuracy = tree.score(x_validate, y_validate)

        scores_all.append([x, round(train_accuracy, 6), round(validate_accuracy, 6)])
        
    scores = pd.DataFrame(scores_all, columns=['max_depth','train_accuracy','validate_accuracy'])
    
    scores['difference'] = round(scores.train_accuracy - scores.validate_accuracy, 6)
    return scores


def best_tree(x_train, y_train, x_validate, y_validate):
    '''
    This function provides a quick print output of the train and validation scores based on the decision trees, for easy viewing.
    The function takes the following arguments: logit, x_train, y_train, x_validate, y_validate
    '''
    tree = DecisionTreeClassifier(max_depth=3, random_state=3)

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
    rf = RandomForestClassifier(random_state=3, min_samples_leaf=1, max_depth=10)

    # model.fit(x, y)
    rf = rf.fit(x_train, y_train)

    print(f'''
    Accuracy of Random Forest on training set: {round(rf.score(x_train, y_train), 2)}
    Accuracy of Random Forest on validation set: {round(rf.score(x_validate, y_validate),2)}
    ''')

def leaf_check(x_train, y_train, x_validate, y_validate):
    '''
    This function takes in: x_train, y_train, x_validate, y_validate
    Which then runs through a range of (1,11)-min_samples_leaf and descending (1,11) for max_depth to help determine the best parameters
    '''
    scores_all = []

    for x in range(1,11):

        #make it
        rf = RandomForestClassifier(random_state=3, min_samples_leaf=x, max_depth=11-x)
        #fit it
        rf.fit(x_train, y_train)
        #transform it
        train_acc = rf.score(x_train, y_train)

        #evaluate on my validate data
        val_acc = rf.score(x_validate, y_validate)

        scores_all.append([x, 11-x, round(train_acc, 4), round(val_acc, 4)])

    scores_df = pd.DataFrame(scores_all, columns=['min_samples_leaf','max_depth','train_acc','val_acc'])
    scores_df['difference'] = round(scores_df.train_acc - scores_df.val_acc, 3)
    return scores_df


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
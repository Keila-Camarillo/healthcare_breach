#data wrangling imports
import pandas as pd
import numpy as np

#vizualizations 
import matplotlib.pyplot as plt
import seaborn as sns

#stats
from scipy import stats
import wrangle as w

def entity_type_barplot(df):
    '''
    This function creates a custom bar chart for comparing the indivdual affected for homes in the Orange, LA, and Ventura.
    '''
    fig, ax =plt.subplots()

    plt.title("Average Number of Affected for Business Associates")

    colors = ['#D8BFD8', '#66CDAA', '#FFDAB9']
    sns.set_palette(colors)

    sns.barplot(x="entity_type", y="number_affected", data=df)

    plt.xlabel("Entities")
    plt.ylabel("Individual Affected")
#     tick_label = ["Los Angeles", "Ventura", "Orange"]
#     ax.set_xticklabels(tick_label)
    property_value_average = df.number_affected.mean()
    plt.axhline(property_value_average, label="number_affected Average", color='DarkSlateBlue')
    plt.legend()

    plt.show()

def cross_function(train, target_variable, feature_variable, alpha=0.05):
    '''
    This function will take the train, target_variable, feature_variable, null_hypothesis, alternative_hypothesis, alpha=0.05
    and print the results and the p-value
    '''
    observed = pd.crosstab(train[target_variable], train[feature_variable])

    chi2, p, degf, expected = stats.chi2_contingency(observed)

    if p < alpha:
        print(f'''Reject the null hypothesis: Sufficient''')
    else:
        print(f''' Fail to reject the null: Insufficient evidence''')
    print(f" chi^2 = {chi2} p = {p}")


def trim_legend(df, column_name, categories):
    """
    Categorizes a column in a DataFrame based on a list of categories.

    Args:
        df (pandas.DataFrame): The DataFrame containing the column to be categorized.
        column_name (str): The name of the column to be categorized.
        categories (list): A list of categories to use for categorization.

    Returns:
        pandas.DataFrame: The modified DataFrame with the categorized column.

    Example:
        # Define the list of categories
        category_list = ['Network Server', 'Email', 'Paper/Films', 'Electronic Medical Record', 'Other']

        # Call the function to categorize a column
        top_5 = categorize_column(train, 'location', category_list)
    """
    categorized_column = df[column_name].apply(lambda x: x.strip() if isinstance(x, str) else x)
    categorized_column = categorized_column.apply(lambda x: x if x in categories else 'Other')
    df[column_name] = categorized_column
    return df

def plot_stacked_bar(df,yaxis,legend,title,xlabel,ylabel,limit=0,legendnames=None,figsize=None, palette="Pastel1"):
    """
    Plot the top 5 locations of breaches based on the provided DataFrame.

    Parameters:
    
top_5 (DataFrame): DataFrame containing breach data with categorized location and breach type columns.

    Returns:
    
None"""
    lvalues = df.loc[:,legend]
    if limit > 0 and limit < len(lvalues.unique()):
        lvcounts = lvalues.value_counts().reset_index()
        lcats =  list(lvcounts.loc[:,'index'][:limit])
        df = trim_legend(df,legend,lcats)
        lcats.append("Other")
    else:
        lcats = list(lvalues.value_counts().reset_index().loc[:,'index'].unique())

    ycats = df.loc[:,yaxis].sort_values(ascending=False).unique()
    myOrd = df.loc[:,legend].replace({k: v for v, k in enumerate(lcats)})
    myOrd.value_counts()
    data= {}
    for ndx in range(0,len(ycats)):
        data[ycats[ndx]]= myOrd[df.loc[:,yaxis] == ycats[ndx]].dropna().value_counts()

    sns.set_palette(palette)
    plotdata = pd.DataFrame(data).T
#     plotdata = Tpose.div(Tpose.sum(axis=1), axis=0) * 100

    plotdata.plot(kind='barh',figsize=figsize, stacked=True)
    plt.legend((lcats,legendnames)[legendnames!=None], bbox_to_anchor=(1.05, 1))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()


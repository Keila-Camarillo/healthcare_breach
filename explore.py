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
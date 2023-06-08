import pandas as pd 
from sklearn.model_selection import train_test_split


# create seasons 
def get_season(month):
    '''
    Returns the season based on the input month.

    Parameters:
        month (int): The month for which the season is to be determined.

    Returns:
        str: The season corresponding to the input month. Possible values are 'Winter', 'Spring', 'Summer',
             'Autumn', or 'Unknown' if the month is not within the valid range of 1 to 12.
    '''
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Unknown'

def clean_df():
    '''
    Cleans the breach_report.csv DataFrame.

    Reads the 'breach_report.csv' file and performs the following cleaning operations:
    1. Adjusts column names to lowercase and underscored.
    2. Drops the 'web_description' column.
    3. Converts the 'breach_submission_date' column to the datetime64 data type.
    4. Adds a 'month' column derived from the 'breach_submission_date'.
    5. Creates a 'multi_breached_location' column indicating if multiple locations are present.
    6. Converts boolean values in the 'multi_breached_location' column to 1 or 0.
    7. Converts the 'month' column to the integer data type.
    8. Adds a 'season' column based on the 'month' using the get_season function.
    9. Renames columns 'type_of_breach' to 'breach' and duplicates it as 'breach_type'.
    10. Drops the 'type_of_breach' and 'month' columns.
    11. Creates dummy variables for columns 'season', 'business_associate_present', and 'breach'.
    12. Concatenates the dummy variables with the original DataFrame.

    Returns:
    - The cleaned DataFrame.

    Example:
    clean_df()
    '''

    df = pd.read_csv('breach_report.csv') 

    # adjust column names - lowercase and underscored
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_")

    # dropped Web Descs column
    df = df.drop(columns=["web_description"])

    # dates are obj will change to date 
    df.breach_submission_date = df.breach_submission_date.astype('datetime64')

    # add month columns
    df["month"] = df.breach_submission_date.dt.strftime("%m")

    # create columns for multiple locations -- encoded 

    # Check if commas exist in the 'Column1' and create a new column 'Has_Comma'
    df['multi_breached_location'] = df['location_of_breached_information'].str.contains(',')

    # Convert boolean values to 1 or 0
    df['multi_breached_location'] = df['multi_breached_location'].astype(int)

    # change month to int
    df[["month"]] = df[["month"]].astype("int")

    # add season column
    df['season'] = df['month'].apply(get_season)

    # rename column
    df["breach"] = df.type_of_breach
    df["breach_type"] = df.type_of_breach
    df = df.drop(columns=["type_of_breach", "month"])

    # create dummies
    dummy_df = pd.get_dummies(df[["season", "business_associate_present", "breach"]])
                            # drop_first=True)
    df = pd.concat([df, dummy_df], axis=1)


    # rename columns
    df = df.rename(columns={"name_of_covered_entity": "entity_name", "covered_entity_type": "entity_type", "individuals_affected": "number_affected", "breach_submission_date": "date", "location_of_breached_information": "location", "season_Spring": "spring", "season_Summer": "summer", "season_Winter": "winter", "breach_Hacking/IT Incident": "hacking_or_it_incident", "breach_Improper Disposal": "improper_disposal", "breach_Theft": "theft", "breach_Loss": "loss", "breach_Unauthorized Access/Disclosure": "unauthorized_access_or_disclosure", "business_associate_present_Yes": "business_associate"})
#     df.columns = df.columns.str.lower()
    # drop entity name
    df = df.drop(columns=['entity_name', 'breach'])

    # fix nans for state column
    df.state = df.state.fillna('PR')

    # df for modeling

    # Display the modified DataFrame
    df = pd.DataFrame(df)
    return df

def split_data(df, target_variable="breach_type"):
    '''
    Takes in two arguments the dataframe name and the ("target_variable" - must be in string format) to stratify  and 
    return train, validate, test subset dataframes will output train, validate, and test in that order.
    '''
    train, test = train_test_split(df, #first split
                                   test_size=.2, 
                                   random_state=123, 
                                   stratify= df[target_variable])
    train, validate = train_test_split(train, #second split
                                    test_size=.25, 
                                    random_state=123, 
                                    stratify=train[target_variable])
    return train, validate, test


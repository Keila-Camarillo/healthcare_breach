import pandas as pd 
from sklearn.model_selection import train_test_split

# create seasons 
def get_season(month):
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

    # add year column
    df["year"] = df.breach_submission_date.dt.strftime("%Y")

    # add day column
    df["day"] = df.breach_submission_date.dt.strftime("%A")

    # create columns for multiple locations -- encoded 

    # Check if commas exist in the 'Column1' and create a new column 'Has_Comma'
    df['multi_breached_location'] = df['location_of_breached_information'].str.contains(',')

    # Convert boolean values to 1 or 0
    df['multi_breached_location'] = df['multi_breached_location'].astype(int)

    # change month and year to and int
    df[["month", "year"]] = df[["month", "year"]].astype("int")
    
    # add season column
    df['season'] = df['month'].apply(get_season)

    # create dummies
    dummy_df = pd.get_dummies(df[["season", "business_associate_present"]],
                            drop_first=True)
    df = pd.concat([df, dummy_df], axis=1)

    # add day number column
    df["day_number"] = df.breach_submission_date.dt.strftime("%w")

    # rename columns
    df = df.rename(columns={"name_of_covered_entity": "entity_name", "covered_entity_type": "entity_type", "individuals_affected": "number_affected", "breach_submission_date": "date", "type_of_breach": "breach_type", "location_of_breached_information": "location", "season_Spring": "spring", "season_Summer": "summer", "season_Winter": "winter", "business_associate_present_Yes": "business_associate"})
    
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


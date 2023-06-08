
# Healthcare Breaches

Machine Learning Classification Model for Healthcare Breach Types

## Project Description

The healthcare breach dataset is utilized in this project to find drivers for breach types. The project aims to discover the key factors contributing to breach types in healthcare facilities and develop a machine learning model to classify these facilities based on the probability of a breach type occurrence. Breach types refer to security incidents where unauthorized parties gain access to sensitive or confidential data. By analyzing the drivers of breach types, this project seeks to enhance our understanding of the contributing elements and aims to enable healthcare facilities to take proactive steps toward protecting sensitive patient information.  

## Project Goal

- Discover drivers of breach types in the healthcare breach dataset.
- Develop a machine learning model to classify healthcare facilities based on the probability of a breach type occurrence.
- Gain insights into the elements that contribute to breach types.

## Initial Thoughts

The initial hypothesis suggests that drivers of breaches will include elements such as state, entity type, season, location, and multi-breach location.

# The Plan 

## Acquire

- Dataset: The project acquires the healthcare breach dataset from the U.S. Department of Health and Human Services Office for Civil Rights ([Link](https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf)).
- The dataset contains 867 rows and 9 columns before cleaning.
- Each row represents a healthcare facility, and each column represents a feature of those facilities.

## Prepare

- Prepare Actions:
  - Renamed columns to promote readability.
  - Checked for null values in the data (identified nulls within the state column, originating from Puerto Rico).
  - Verified appropriate data types for each column.
  - Added the multi_breach_location and season columns.
  - Removed features:
    - Name of Covered Entity
    - Web Description
  - Encoded categorical variables.
  - Split data into train, validate, and test sets (approximately 60/20/20 split), stratifying on 'breach_type'.
  - Outliers have not been removed in this iteration of the project.

## Explore

- Explore data in search of drivers of breaches
- Answer the following initial questions:
    * Are States Related to the Type of Breach?
    * Are Multiple Locations Related to the Breach type?
    * Is the Summer Season Related to the Breach type?
    * Is Season Related to the Breach Type?
    * Is a Business Associate Present Related  to the Breach type?

## Modeling

- Develop a Model to predict type of breach
    - Use drivers identified in explore to build predictive models of different types
    - Evaluate models on train and validate data
    - Select the best model based on lowest RMSE and highest R2
    - Evaluate the best model on test data

- Draw conclusions

# Data Dictionary

**Table: Healthcare Breach**

| Feature            |  Definition                                                                                          |
|-----------------------|-------------------------------------------------------------------------------------------------------|
| Name of Covered Entity| Name for each healthcare facility                                                                     |
| State                 | State where the healthcare facility is located                                                        |
| Covered Entity Type   | HIPAA covered entities: Healthcare Provider, Businees Associate, Health Plan                          |
| Individual Affected   | Number of individuals affected by the breach                                                        |
| Location of Breached Information | Where the breach occured                                                        |
| Breach Submission Date    | Date when the breach was submitted 
| Business Associate Present | If a business associate was present (A “business associate” is a person or entity, other than a member of the workforce of a covered entity, who performs functions or activities on behalf of, or provides certain services to, a covered entity that involve access by the business associate to protected health information.) |


**Note:** This data dictionary provides an overview of the columns/features present in the healthcare breach dataset. The dataset was acquired from the U.S. Department of Health and Human Services Office for Civil Rights and Data.World. The data was prepared by performing various actions such as renaming columns, handling nulls, checking data types, adding additional columns, removing irrelevant features, encoding categorical variables, and splitting the data into train, validate, and test sets.

Steps to Reproduce
1. Clone this repo.
2. Acquire the data from U.S. Department of Health and Human Services Office for Civil Rights and Data.World
3. Place the data in the file containing the cloned repo.
4. Run notebook.

## Takeaways and Conclusions
* "Location" was found to be a driver of "breach_type", Hacking/IT incidents and Unauthorized Access/Disclousre breachs appeared like they occured more in Network Servers.
* "State" was found to be a driver of "breach_type", some states only had Hacking/IT incidents breaches, possible as a result of not enough samples from the states.
* "Multiple Locations" was found to be a driver of "breach_type",  breaches with 'Multiple Locations' appeared more in theft breaches.
* "Summer" was found to be a driver of "breach_type", Loss and Theft appeared more in the 'Summer' than other seasons.
* "Season" was not found to be a driver of "breach_type"
* "Business Associate" was not found to be a driver of "breach_type"

# Recommendations

- Healthcare facilities that are more likely to experience hacking/IT incidents should prioritize investing in firewall protection, installing/updating SSL certificates, and using VPNs, particularly before the summer season.
- Theft incidents are more prevalent in the summertime. Conducting annual vigilance training in the spring can help educate employees on when and where to report incidents, thereby reducing or eliminating the threat.

# Next Steps

- Given more time, it would be beneficial to review each breach individually and assess its impact on the number of affected individuals. Additionally, exploring the effect of location on the number of affected individuals would provide further insights.


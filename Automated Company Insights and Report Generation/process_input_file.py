import os
import pandas as pd
import numpy as np
import warnings

# Filter out all warnings
warnings.filterwarnings("ignore")

def process_input_excel_to_output(input_excel_file):
    # Read Excel file into DataFrame
    df = pd.read_excel(input_excel_file)

    # Remove rows with NaN values in the 'Company Name' column
    df_cleaned = df.dropna(subset=['Company Name'])

    # df_cleaned dataframe columns might be strings that represent dates or already datetime objects
    # If they're strings representing dates, we will convert them to datetime objects first
    df_cleaned.columns = [pd.to_datetime(col, errors='ignore') if i in range(3, len(df_cleaned.columns)-1) else col for i, col in enumerate(df_cleaned.columns)]

    # Now convert those datetime objects to the desired string format
    df_cleaned.columns = [col.strftime('%b-%Y') if isinstance(col, pd.Timestamp) else col for col in df_cleaned.columns]

    # Reset index of cleaned DataFrame
    df_cleaned.reset_index(drop=True, inplace=True)

    # Extract date columns
    date_columns = df_cleaned.columns[3:-1]

    # Initialize a list to store the date range columns
    date_range_columns = []

    # Iterate over the range of indices to construct the date range columns
    for i in range(len(date_columns) - 1):
        start_month = date_columns[i]  # Extract the start month from the date columns name
        end_month = date_columns[i + 1]  # Extract the end month from the next date columns name
        new_date_column = f"{start_month} to {end_month}"  # Construct the new date column name
        date_range_columns.append(new_date_column)

    new_date_range_df = pd.DataFrame(columns=date_range_columns)

    # Concatenate the new DataFrame with the existing DataFrame along axis 1 (columns)
    concat_df1 = pd.concat([df_cleaned, new_date_range_df], axis=1)

    # Calculate the percentage change for the metrics 'Sales', 'Operating Profit', and 'Net Profit' across four quarters.
    concat_df1.iloc[:, 9] = (concat_df1.iloc[:, 4].values - concat_df1.iloc[:, 3].values) / concat_df1.iloc[:, 3].values*100
    concat_df1.iloc[:, 10] = (concat_df1.iloc[:, 5].values - concat_df1.iloc[:, 4].values) / concat_df1.iloc[:, 4].values*100
    concat_df1.iloc[:, 11] = (concat_df1.iloc[:, 6].values - concat_df1.iloc[:, 5].values) / concat_df1.iloc[:, 5].values*100
    concat_df1.iloc[:, 12] = (concat_df1.iloc[:, 7].values - concat_df1.iloc[:, 6].values) / concat_df1.iloc[:, 6].values*100

    # Filter DataFrame rows based on condition
    concat_df1_without_percentage = concat_df1.loc[concat_df1['Unit']!='Percentage']

    # Reset index
    concat_df1_without_percentage.reset_index(drop=True, inplace=True)

    # Filter DataFrame rows based on condition
    concat_df1_with_percentage = concat_df1.loc[concat_df1['Unit']=='Percentage']

    # set specific columns to NaN
    concat_df1_with_percentage.loc[concat_df1_with_percentage['Unit']=='Percentage', concat_df1_with_percentage.columns[9:]] = np.nan

    # Reset index
    concat_df1_with_percentage.reset_index(drop=True, inplace=True)

    # Calculate the percentage change for the metrics 'PAT Margin', 'Gross Profit Margin', and 'Operating Profit Margin' across four quarters.
    concat_df1_with_percentage.iloc[:, 9] = (concat_df1_with_percentage.iloc[:, 4].values - concat_df1_with_percentage.iloc[:, 3].values)
    concat_df1_with_percentage.iloc[:, 10] = (concat_df1_with_percentage.iloc[:, 5].values - concat_df1_with_percentage.iloc[:, 4].values)
    concat_df1_with_percentage.iloc[:, 11] = (concat_df1_with_percentage.iloc[:, 6].values - concat_df1_with_percentage.iloc[:, 5].values)
    concat_df1_with_percentage.iloc[:, 12] = (concat_df1_with_percentage.iloc[:, 7].values - concat_df1_with_percentage.iloc[:, 6].values)

    concat_df1_without_percentage.reset_index(drop=True, inplace=True)

    # Concatenate the new DataFrame with the existing DataFrame along axis 0 (Rows)
    final_df = pd.concat([concat_df1_without_percentage, concat_df1_with_percentage], axis=0)

    final_df.reset_index(drop=True, inplace=True)

    # Sort DataFrame by specified columns
    final_df = final_df.sort_values(by='Company Name')

    # Reset index
    final_df.reset_index(drop=True, inplace=True)

    # Set custom order for categorical data
    custom_order = final_df['Metrics'].unique()
    final_df['Metrics'] = pd.Categorical(final_df['Metrics'], categories=custom_order, ordered=True)
    final_sorted_df = final_df.sort_values(by=['Company Name', 'Metrics'])

    # Convert the last four columns to float
    for column in final_sorted_df.columns[-4:]:
        # Convert the column to float
        final_sorted_df[column] = final_sorted_df[column].astype(float)

    # Selecting float columns
    float_cols = final_sorted_df.select_dtypes(include=['float64']).columns

    # Rounding float columns to 2 decimal places
    final_sorted_df[float_cols] = final_sorted_df[float_cols].round(2)

    # To create a copy of final_sorted_df
    langchain_df = final_sorted_df.copy()

    # Select first three columns
    first_three_columns = langchain_df.iloc[:, :3]

    # Select last four columns
    last_five_columns = langchain_df.iloc[:, -5:]

    # Combine the two selections
    langchain_df_combined = pd.concat([first_three_columns, last_five_columns], axis=1)

    # Get unique unit values
    unit_values = langchain_df_combined['Unit'].unique()

    # Convert all unit values to lowercase
    langchain_df_combined['Unit'] = langchain_df_combined['Unit'].str.lower()

    # Iterate over unique unit values and replace them dynamically
    for unit in unit_values:
        langchain_df_combined['Unit'] = langchain_df_combined['Unit'].replace(unit.lower(), 'percentage')

    return final_sorted_df, langchain_df_combined

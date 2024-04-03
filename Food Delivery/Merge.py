import pandas as pd

# Read the contents of both CSV files into pandas DataFrames
df1 = pd.read_csv('Restaurant_grubhub_data.csv')
df2 = pd.read_csv('Restaurants_Info.csv')


# Merge the DataFrames using concat() method
CsvMerge = pd.merge(df1, df2, on = ['Restaurant_Link','Restaurant_ID'])

# # Write the merged DataFrame to a new CSV file
CsvMerge.to_csv('GrubHub Data.csv', index=False)

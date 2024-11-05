import dask.dataframe as dd

# Read the large CSV file with Dask
df = dd.read_csv('/Users/ramisafi/Downloads/stories_partition1.csv')

# Get the first 3 rows
first_3_rows = df.head(4)

# Convert to Pandas DataFrame and write to a new CSV file
first_3_rows.to_csv('/Users/ramisafi/Downloads/first_3_rows.csv', index=False)

print("First 3 rows written to new CSV file successfully!")

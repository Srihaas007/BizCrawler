import pandas as pd

# Path to the CSV file
file_path = 'data/output/real_estate_in_england.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Count the rows where the 'email' column contains valid data
# Check for non-empty, non-"N/A", and non-null entries
email_count = df[(df['email'].notnull()) & (df['email'] != 'N/A') & (df['email'].str.strip() != '')].shape[0]

print(f"Number of rows with valid email data: {email_count}")


import pandas as pd

# Path to the saved tab-delimited dataframe file
input_file = "../processingResults/processedFullDataFrame"

# Read the tab-separated file
# Assume first row has column names, first col = reporting date, second col = IDRSSD
df = pd.read_csv(input_file, sep="\t")

# Ensure reporting period end date is treated as datetime (optional but useful)
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])

# Convert IDRSSD to numeric just in case
df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors="coerce")

# Convert all remaining columns to numeric so they can be averaged
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Group by reporting date (first column) and compute mean across all other columns
# This will average each numeric column across rows (i.e., across IDRSSD) for each date
avg_df = df.groupby(df.columns[0], as_index=False).mean(numeric_only=True)

# Remove the IDRSSD column
avg_df = avg_df.drop('IDRSSD', axis=1)

# Convert columns to integers
cols_to_change_names = avg_df.iloc[:, 1:].columns
new_types = {col_name: 'int64' for col_name in cols_to_change_names}
avg_df = avg_df.astype(new_types)

# Print the resulting dataframe as tab-delimited text
print(avg_df.to_csv(sep="\t", index=False))

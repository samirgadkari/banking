
import os
import pandas as pd

# User parameters
root_dir = "../data/commonBanks"      # top directory containing subdirectories
info_numeric_file = "./commonBanksRSSD"  # file with numeric values (one per line or tab-delimited)
info_columns_file = "extractColumns"  # file with column names (one per line or tab-delimited)

# -------------------------------------------------------------------
# Read filter values
# -------------------------------------------------------------------
# Numeric values that must match the dataframe's second column
numeric_filter = (
    pd.read_csv(info_numeric_file, sep="\t", header=None)
      .iloc[:, 0]
      .dropna()
      .astype(float)
      .tolist()
)

# Column names that must match dataframe column names
column_filter = (
    pd.read_csv(info_columns_file, sep="\t", header=None)
      .iloc[:, 0]
      .dropna()
      .astype(str)
      .tolist()
)

all_results = []  # to collect per-subdirectory filtered DataFrames

# -------------------------------------------------------------------
# Process each subdirectory
# -------------------------------------------------------------------
for subdir_name in sorted(os.listdir(root_dir)):
    subdir_path = os.path.join(root_dir, subdir_name)
    if not os.path.isdir(subdir_path):
        continue

    subdir_dfs = []

    # Read and horizontally concatenate all files in this subdirectory
    for filename in sorted(os.listdir(subdir_path)):
        file_path = os.path.join(subdir_path, filename)
        if not os.path.isfile(file_path):
            continue

        try:
            # Read full tab-delimited file; assume first row has column names or let pandas assign
            df = pd.read_csv(file_path, sep="\t", dtype=str)
        except Exception as e:
            print(f"Skipping {file_path}: {e}")
            continue

        subdir_dfs.append(df)

    if not subdir_dfs:
        continue

    for id, df in enumerate(subdir_dfs):

        if id == 0:
            continue

        df.drop(labels=["Reporting Period End Date", "IDRSSD"], axis=1, 
                inplace=True, errors="ignore")

    # Concatenate columns side-by-side, aligning by index
    subdir_df = pd.concat(subdir_dfs, axis=1)

    # Ensure the second column exists
    if subdir_df.shape[1] < 2:
        print(f"Subdirectory {subdir_name} has fewer than 2 columns after concatenation; skipping.")
        continue

    # ----------------------------------------------------------------
    # Filter rows based on second column values
    # ----------------------------------------------------------------
    # Convert second column to numeric where possible for comparison
    second_col = pd.to_numeric(subdir_df.iloc[:, 1], errors="coerce")

    # Filter rows where second column is in numeric_filter
    row_mask = second_col.isin(numeric_filter)

    # ----------------------------------------------------------------
    # Filter columns based on column names
    # ----------------------------------------------------------------
    # Keep always the first two columns, plus any columns whose names are in column_filter
    cols_to_keep = list(subdir_df.columns[:2])  # always keep first two
    cols_to_keep += [col for col in subdir_df.columns[2:] if str(col) in column_filter]

    filtered_df = subdir_df.loc[row_mask, cols_to_keep]

    # Store this subdirectory's filtered result
    all_results.append(filtered_df)
    rows, cols = filtered_df.shape

# -------------------------------------------------------------------
# Concatenate all filtered subdirectory results vertically
# -------------------------------------------------------------------
if all_results:

    final_df = pd.concat(all_results, axis=0, ignore_index=True)

    # Print as tab-delimited text
    # If you prefer writing to a file, replace print(...) with final_df.to_csv("output.txt", sep="\t", index=False)
    print(final_df.to_csv(sep="\t", index=False))
else:
    print("No data matched the given filters or no valid files were found.")


import os
import pandas as pd

# Set this to your top-level directory that contains the sub-directories
root_dir = "../data/commonBanks"

common_values = None  # Will hold the running intersection of first-column values

# Iterate over sub-directories in alphabetical order
for subdir_name in sorted(os.listdir(root_dir)):
    subdir_path = os.path.join(root_dir, subdir_name)
    if not os.path.isdir(subdir_path):
        continue

    # Iterate over files in each sub-directory in alphabetical order
    for filename in sorted(os.listdir(subdir_path)):
        file_path = os.path.join(subdir_path, filename)

        if not os.path.isfile(file_path):
            continue

        if filename == "Readme.txt":
            continue

        try:
            # Read only the first column (0-based index) as strings from tab-delimited file
            df = pd.read_csv(
                file_path,
                sep="\t",
                header='infer',
                usecols=[1],  # This is the IDRSSD
                dtype=str
            )
        except Exception as e:
            # If a file cannot be read as expected, skip it
            print(f"Skipping {file_path}: {e}")
            continue

        # Get a set of non-null values from the first column
        col_values = set(df.iloc[:, 0].dropna())

        # Initialize or intersect with running set
        if common_values is None:
            common_values = col_values
        else:
            common_values &= col_values

# Print the final result
if common_values is None:
    print("No valid files processed.")
else:
    print("Common RSSD values in first column across all files:")
    for val in sorted(common_values):
        print(val)

    print("Number of common values: ", len(common_values))

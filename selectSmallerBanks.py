import pandas as pd

# 1. Read in the dataframe
df = pd.read_csv("../processingResults/processedFullDataframe", sep="\t")
print(f"{df.head()}")
print(f"{df.shape}")

# Ensure 'Reporting Period End Date' is in datetime format to extract the year
df["Reporting Period End Date"] = pd.to_datetime(
    df["Reporting Period End Date"]
)

# 2. Identify IDRSSDs for banks with RCFD2170 <= 70,000 ($70M) in 2025
# and RCFD2170 > 10,000 ($10M) in 2025
# (Filtering out banks ABOVE 70000 and below 10000 in 2025)
banks_2025 = df[df["Reporting Period End Date"].dt.year == 2025]
target_rssds = banks_2025[(banks_2025["RCFD2170"] <= 70000) &
                            (banks_2025["RCFD2170"] > 10000)][
    "IDRSSD"
].unique()

df = pd.read_csv("../processingResults/processedFullDataframe", sep="\t")
# Filter main dataframe to keep only those selected target banks
df_focus = df[df["IDRSSD"].isin(target_rssds)].copy()

# 3. Define the desired output columns
requested_columns = [
    "Reporting Period End Date",
    "IDRSSD",
    "RCFD2170",
    "RCON2170",
    "RIAD4340",
    "RCFD0010",
    "RCON0010",
    "RCFD2143",
    "RCON2143",
    "RCFD3163",
    "RCON3163",
    "RIAD4217",
    "RIADAF28",
    "RIAD4135",
]

# Ensure missing columns in the source data don't throw KeyErrors
existing_columns = [col for col in requested_columns if col in df_focus.columns]

# Create the final selected_banks dataframe
selected_banks = df_focus[existing_columns].copy()

# Display summary of filtered dataset
print(f"Total focus banks selected: {len(target_rssds)}")
print(f"Shape of selected_banks DataFrame: {selected_banks.shape}")
print(f"Selected banks (shape: {selected_banks.shape}: \n{selected_banks.head()}")

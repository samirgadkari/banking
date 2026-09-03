import numpy as np
import pandas as pd

# Path to the saved tab-delimited dataframe file
input_file = "../processingResults/commonBanksDataframe"
raroe_specific_companies_file = "../processingResults/raroeSpecificCompanies"
raroe_file = "../processingResults/raroe"

# Read the tab-separated file
# Assume first row has column names, first col = reporting date, second col = IDRSSD
ori_df = pd.read_csv(input_file, sep="\t")

# Remove columns we don't need
# RIAD4340 = Net income (bottom line net earnings)
# RCON3210 = Total equity capital
short_df = ori_df.loc[:, ["IDRSSD", "RIAD4340", "RCON3210"]].copy()

# Convert all columns to numeric so they can be averaged
for col in short_df.columns:
    short_df[col] = pd.to_numeric(short_df[col], errors="coerce")

short_df = short_df[short_df['RCON3210'] != 0]
short_df["ROE"] = short_df["RIAD4340"] / short_df["RCON3210"]
aggregates = short_df.groupby('IDRSSD')['ROE'].agg(['mean', 'std']).reset_index()
short_df = short_df.merge(aggregates, on='IDRSSD')
short_df['RAROE'] = short_df['mean'] - short_df['std']

df = short_df.groupby(by='IDRSSD', as_index=False).first()
df.sort_values(by='RAROE', ascending=False, inplace=True)
df.iloc[:10].to_csv(raroe_file, sep='\t', index=False)

selected_IDRSSD = df.iloc[:10]['IDRSSD']
df = ori_df[ori_df['IDRSSD'].isin(selected_IDRSSD)].copy()
df['ROE'] = df['RIAD4340'] / df['RCON3210']
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

df[['Reporting Period End Date', 'IDRSSD', 'RIAD4340', 'RCON3210', 'ROE']] \
        .to_csv(raroe_specific_companies_file, sep='\t', index=False)


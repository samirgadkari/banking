import numpy as np
import pandas as pd

# 1. Read in the dataframe
df = pd.read_csv("../processingResults/AllBanksDataframe", sep="\t")

# Ensure 'Reporting Period End Date' is in datetime format to extract the year
df["Reporting Period End Date"] = pd.to_datetime(
    df["Reporting Period End Date"]
)

# 2. Identify IDRSSDs for banks with RCFD2170 > 10,000 ($10M) and 
# RCFD2170 <= 7,000,000 ($7000M) in 2025
banks_2025 = df[df["Reporting Period End Date"].dt.year == 2025]
target_rssds = banks_2025[(banks_2025["RCFD2170"] > 10000) & 
                            (banks_2025["RCFD2170"] <= 7000000)][
    "IDRSSD"
].unique()

df = pd.read_csv("../processingResults/AllBanksDataframe", sep="\t")
# Filter main dataframe to keep only those selected target banks
selected_banks = df[df["IDRSSD"].isin(target_rssds)]. \
                    reset_index(drop=True). \
                    copy()

# Display summary of filtered dataset
print(f"Total focus banks selected: {len(target_rssds)}")
print(f"Shape of selected_banks DataFrame: {selected_banks.shape}")
print(f"Selected banks (shape: {selected_banks.shape}: \n{selected_banks}")
print(f"df.columns: {selected_banks.columns}")
sorted_dates = selected_banks["Reporting Period End Date"].sort_values()
unique_dates = pd.Series(sorted_dates).unique()
print(f"Selected unique dates: {unique_dates}")

d = np.array(['2006-03-31', '2006-06-30', '2006-09-30', '2006-12-31', '2007-03-31',
 '2007-06-30', '2007-09-30', '2007-12-31', '2008-03-31', '2008-06-30',
 '2008-09-30', '2008-12-31', '2009-03-31', '2009-06-30', '2009-09-30',
 '2009-12-31', '2010-03-31', '2010-06-30', '2010-09-30', '2010-12-31',
 '2011-03-31', '2011-06-30', '2011-09-30', '2011-12-31', '2012-03-31',
 '2012-06-30', '2012-09-30', '2012-12-31', '2013-03-31', '2013-06-30',
 '2013-09-30', '2013-12-31', '2014-03-31', '2014-06-30', '2014-09-30',
 '2014-12-31', '2015-03-31', '2015-06-30', '2015-09-30', '2015-12-31',
 '2016-03-31', '2016-06-30', '2016-09-30', '2016-12-31', '2017-03-31',
 '2017-06-30', '2017-09-30', '2017-12-31', '2018-03-31', '2018-06-30',
 '2018-09-30', '2018-12-31', '2019-03-31', '2019-06-30', '2019-09-30',
 '2019-12-31', '2020-03-31', '2020-06-30', '2020-09-30', '2020-12-31',
 '2021-03-31', '2021-06-30', '2021-09-30', '2021-12-31', '2022-03-31',
 '2022-06-30', '2022-09-30', '2022-12-31', '2023-03-31', '2023-06-30',
 '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30',
 '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30'])
d = np.flip(d)
dates = pd.to_datetime(d, format="%Y-%m-%d").to_pydatetime()


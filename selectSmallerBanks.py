import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

def make_grid(rows, cols):
    grid = []
    for _ in range(rows):
        grid.append(st.columns(cols))
    return grid

def print_group(g):
    for name, group in g:
        print(f"name: {name}\n")
        print(f"group: {group}")

def combine_cols(df, col1, col2, col3):
    # 2. Unified Asset Column (handling RCFD vs RCON)
    if col1 in df.columns and col2 in df.columns:
        df[col3] = df[col1].combine_first(df[col2])
    elif col1 in df.columns:
        df[col3] = df[col1]
    else:
        df[col3] = df[col2]

def cumulative_pct(df, col):
    df[col] = df[col].replace(0, np.nan)
    df["Initial"] = df.groupby("IDRSSD")[col].transform("first")
    df["Cumulative_" + col + "_Pct"] = (
        (df[col] - df["Initial"]) / df["Initial"]
    ) * 100

def growth_rates(selected_banks):

    # Load your dataframe from memory/variable
    df = selected_banks.copy()

    # 1. Clean date column and sort chronologically
    df["Reporting Period End Date"] = pd.to_datetime(
        df["Reporting Period End Date"]
    )
    df = df.sort_values(by=["IDRSSD", "Reporting Period End Date"])

    combine_cols(df, "RCFD2170", "RCON2170", "Total_Assets")

    cumulative_pct(df, "Total_Assets")

    df["Net_Income"] = df["RIAD4340"]
    cumulative_pct(df, "Net_Income")

    combine_cols(df, "RCFD2143", "RCON2143", "Goodwill")
    cumulative_pct(df, "Goodwill")

    st.set_page_config(layout="wide", page_title="Bank Analytics Dashboard")

    # st.title("Bank M&A & Growth Screener")

    # Create tabs
    tab1, tab2 = st.tabs(["Changes over time", "Filtered data"])

    with tab1:
        # Create a 2-row, 3-column matrix
        grid = make_grid(2, 2)

        with grid[0][0].container(border=True):
            # Plotly provides native interactive hover tooltips & zooming
            fig1 = px.line(
                df,
                x="Reporting Period End Date",
                y="Cumulative_Total_Assets_Pct",
                color="IDRSSD",
                title="Total Assets (%)",
            )
            st.plotly_chart(fig1, width='stretch')

        with grid[0][1].container(border=True):
            fig2 = px.line(
                df,
                x="Reporting Period End Date",
                y="Cumulative_Net_Income_Pct",
                color="IDRSSD",
                title="Net Income (%)",
            )
            st.plotly_chart(fig2, width='stretch')

        with grid[1][0].container(border=True):
            fig2 = px.line(
                df,
                x="Reporting Period End Date",
                y="Cumulative_Goodwill_Pct",
                color="IDRSSD",
                title="Goodwill (%)",
            )
            st.plotly_chart(fig2, width='stretch')

    with tab2:
        st.subheader("Filtered Bank Data Table")
        st.dataframe(df)

df = pd.read_csv("../processingResults/AllBanksDataframe", sep="\t")

# Ensure 'Reporting Period End Date' is in datetime format to extract the year
df["Reporting Period End Date"] = pd.to_datetime(
    df["Reporting Period End Date"]
)

# 2. Identify IDRSSDs for banks with RCFD2170 > 10,000 ($10M) and 
# RCFD2170 <= 7,000,000 ($7000M) in 2025
# RCFD2170 = total assets
banks_2025 = df[df["Reporting Period End Date"].dt.year == 2025]
target_rssds = banks_2025[(banks_2025["RCFD2170"] > 10000) & 
                            (banks_2025["RCFD2170"] <= 7000000)][
    "IDRSSD"
].unique()

# df = pd.read_csv("../processingResults/AllBanksDataframe", sep="\t")
# Filter main dataframe to keep only those selected target banks
selected_banks = df[df["IDRSSD"].isin(target_rssds)]. \
                    reset_index(drop=True). \
                    copy()

# Display summary of filtered dataset
print(f"Total focus banks selected: {len(target_rssds)}")
print(f"Shape of selected_banks DataFrame: {selected_banks.shape}")
print(f"Selected banks: {selected_banks.shape}: \n{selected_banks}")
print(f"df.columns: {selected_banks.columns}")
sorted_dates = selected_banks["Reporting Period End Date"].sort_values()
unique_dates = pd.Series(sorted_dates).unique()

unique_dates = pd.Series(pd.to_datetime(unique_dates, format="%Y-%m-%d").to_pydatetime())
print(f"Selected unique dates: {unique_dates.dt.date}")
growth_rates(selected_banks)


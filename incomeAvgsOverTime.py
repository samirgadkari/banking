
import pandas as pd
import plotly.graph_objects as go

# Path to your tab-delimited data file
input_file = "../processingResults/reportingPeriodAverages"

# Columns to plot
cols = [
    "RIAD4010", "RIAD4065", "RIAD4115", "RIADB488",
    "RIADB489", "RIAD4060", "RIAD4020", "RIAD4518"
]
updatedCols = {
        "RIAD4010": "Performing Loans and Leases", 
        "RIAD4065": "Leases", 
        "RIAD4115": "Interbank CDs etc.", 
        "RIADB488": "US Treasuries", 
        "RIADB489": "MBS", 
        "RIAD4060": "Other securities", 
        "RIAD4020": "Overnight lending and Reverse Repos", 
        "RIAD4518": "Non-performing Loans and Leases"}

# Read the tab-separated file
# First column is date (yyyy-mm-dd), first row has headers
df = pd.read_csv(input_file, sep="\t")

df.rename(columns=updatedCols, inplace=True)

# Ensure the date column is datetime (assume first column is the date)
date_col = df.columns[0]
df[date_col] = pd.to_datetime(df[date_col], format="%Y-%m-%d")
df = df[df[date_col].dt.month == 12]

# Keep only the date and the selected columns that actually exist in the file
available_cols = [c for c in updatedCols.values() if c in df.columns]
if not available_cols:
    raise ValueError("None of the requested columns are present in the file.")

plot_df = df[[date_col] + available_cols].copy()

# Sort by date for a chronological x-axis
plot_df = plot_df.sort_values(by=date_col)

# Create stacked bar chart
fig = go.Figure()

for col in available_cols:
    fig.add_bar(
        x=plot_df[date_col],
        y=plot_df[col],
        name=col
    )

fig.update_layout(
    barmode="stack",
    title="RIAD/B",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5,
    ),
)

fig.update_xaxes(title_text="Year")
fig.update_yaxes(title_text="Amount")

# Show the figure (in a script, this will open a window; in a notebook, it will render inline)
fig.show()

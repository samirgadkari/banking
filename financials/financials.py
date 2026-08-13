import os
import pandas as pd
import requests


def download_bank_data():
    url = "https://banks.data.fdic.gov/api/financials"

    # Define asset filter: $10M ($10,000k) to $70M ($70,000,000k)
    asset_min = 10000
    asset_max = 700000
    # Define year filter: e.g., 2020 through 2025
    start_year = 2000
    end_year = 2025

    # Request essential metrics + RSSDID identifier
    fields = "NAME,CERT,RSSDID,REPDTE,ASSET,INTINC,NONII,NONIX,INTEXP,ROE,ROA"

    all_records = []
    limit = 10000  # API max limit per page
    offset = 0

    print("Fetching bank financial data from FDIC API...")

    while True:
        params = {
            "filters": f"ASSET:[{asset_min} TO {asset_max}] AND YEAR:[{start_year} TO {end_year}]",
            "fields": fields,
            "limit": limit,
            "offset": offset,
            "sort_by": "REPDTE",
            "sort_order": "DESC",
            "format": "json",
        }

        response = requests.get(url, params=params)
        data = response.json().get("data", [])

        if not data:
            break

        # Extract underlying json payload
        records = [item["data"] for item in data]
        all_records.extend(records)

        # Check if another page exists
        if len(records) < limit:
            break

        offset += limit
        print(f"Retrieved {len(all_records)} records so far...")

    df = pd.DataFrame(all_records)
    print(f"Total records retrieved: {len(df)}")
    return df


def save_dataframes_by_rssd(df, output_dir="bank_data_by_rssd"):
    os.makedirs(output_dir, exist_ok=True)

    # Clean missing RSSD values if any exist
    df = df.dropna(subset=["RSSDID"])

    # Group dataframe by RSSD ID and save individual CSV files
    grouped = df.groupby("RSSDID")

    for rssd_id, group in grouped:
        # Cast RSSD ID to integer string (e.g., "1234567")
        rssd_str = str(int(rssd_id))
        filename = os.path.join(output_dir, f"rssd_{rssd_str}.csv")

        # Sort bank data chronologically by report date
        group_sorted = group.sort_values(by="REPDTE", ascending=True)
        group_sorted.to_csv(filename, index=False)

    print(f"Successfully saved {len(grouped)} individual bank CSV files to '{output_dir}/'.")


if __name__ == "__main__":
    df_banks = download_bank_data()
    print(f"df_banks.head:\n{df_banks.head()}")
    save_dataframes_by_rssd(df_banks)


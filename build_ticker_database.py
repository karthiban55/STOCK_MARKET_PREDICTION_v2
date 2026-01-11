# build_ticker_database.py
import pandas as pd
import urllib.request
import json

def build_database():
    """
    Downloads the latest list of all NASDAQ-traded stocks and saves them
    to a JSON file for our search endpoint to use.
    """
    print("Attempting to download latest stock ticker list from NASDAQ...")

    # The official source for the list of all traded symbols
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt"
    
    try:
        # Use urllib to download the file
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')

        print("Download successful. Processing file...")
        
        # The file is pipe-delimited (|). We read it into a pandas DataFrame.
        # We need to split the string data into lines first.
        lines = data.strip().split('\r\n')
        # We can use a list of lists to create the DataFrame
        rows = [line.split('|') for line in lines]
        # The first row is the header, the last row is a file creation timestamp
        df = pd.DataFrame(rows[1:-1], columns=rows[0])

        # We only care about the Symbol and Security Name
        df_clean = df[['Symbol', 'Security Name']].copy()

        # Let's filter out some test stocks and warrants that aren't useful
        df_clean = df_clean[df_clean['Symbol'].str.contains(r'^[A-Z]+$')]

        # Rename columns to match what our API expects
        df_clean.rename(columns={"Symbol": "ticker", "Security Name": "name"}, inplace=True)
        
        # Convert the cleaned DataFrame to a list of dictionaries
        tickers_list = df_clean.to_dict(orient='records')
        
        # Save the list to our JSON file
        with open("ticker_database.json", "w") as f:
            json.dump(tickers_list, f, indent=2)
            
        print(f"Success! ticker_database.json has been created with {len(tickers_list)} entries.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Could not build the ticker database. The search feature might not work correctly.")


if __name__ == "__main__":
    build_database()
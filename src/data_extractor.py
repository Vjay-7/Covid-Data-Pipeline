import requests
import pandas as pd
import json
from datetime import datetime

class COVIDDataExtractor:
    def __init__(self):
        self.base_url = "https://disease.sh/v3/covid-19"
    
    def fetch_global_data(self):
        """
        Fetch global COVID-19 statistics
        """
        try:
            response = requests.get(f"{self.base_url}/all")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching global data: {e}")
            return None
    
    def fetch_countries_data(self):
        """
        Fetch COVID-19 data for all countries
        """
        try:
            response = requests.get(f"{self.base_url}/countries")
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except requests.RequestException as e:
            print(f"Error fetching countries data: {e}")
            return None
    
    def save_raw_data(self, data, filename):
        """
        Save raw data to JSON file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"data/raw_{filename}_{timestamp}.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Raw data saved to {filepath}")
    
    def process_data(self, df):
        """
        Process and clean country-level data
        """
        cleaned_df = df[[
            'country', 
            'cases', 
            'todayCases', 
            'deaths', 
            'todayDeaths', 
            'recovered', 
            'active', 
            'critical',
            'continent'
        ]].copy()
        
        cleaned_df.columns = [
            'Country', 
            'Total_Cases', 
            'New_Cases', 
            'Total_Deaths', 
            'New_Deaths', 
            'Total_Recovered', 
            'Active_Cases', 
            'Critical_Cases',
            'Continent'
        ]
        
        return cleaned_df

def main():
    extractor = COVIDDataExtractor()
    
    # Fetch global data
    global_data = extractor.fetch_global_data()
    if global_data:
        extractor.save_raw_data(global_data, "global")
    
    # Fetch countries data
    countries_df = extractor.fetch_countries_data()
    if countries_df is not None:
        processed_df = extractor.process_data(countries_df)
        
        # Save processed data
        processed_df.to_csv('data/processed_covid_data.csv', index=False)
        print("Data processing complete.")

if __name__ == "__main__":
    main()
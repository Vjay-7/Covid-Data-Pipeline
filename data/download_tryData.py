import requests
import pandas as pd

# Method 1: disease.sh API
def fetch_covid_data():
    # Global Statistics
    global_stats = requests.get('https://disease.sh/v3/covid-19/all').json()
    
    # Country-wise Data
    countries_data = requests.get('https://disease.sh/v3/covid-19/countries').json()
    
    # Convert to DataFrame
    df = pd.DataFrame(countries_data)
    
    # Save to CSV
    df.to_csv('data/processed_covid_data.csv', index=False)

# Method 2: Johns Hopkins GitHub Data
def fetch_jhu_data():
    base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    
    # Example for a specific date (modify as needed)
    date = "03-01-2023"  # MM-DD-YYYY format
    url = f"{base_url}{date}.csv"
    
    df = pd.read_csv(url)
    df.to_csv('data/processed_covid_data.csv', index=False)

# Method 3: Kaggle Dataset (requires Kaggle API)
def fetch_kaggle_dataset():
    # Prerequisite: Install Kaggle CLI
    # pip install kaggle
    
    import subprocess
    
    # Download specific dataset
    subprocess.run([
        "kaggle", "datasets", "download", 
        "-d", "tanmoymitra1/covid-19-world-data"
    ])
    
fetch_covid_data()
    

    
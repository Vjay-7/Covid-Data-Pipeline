import pandas as pd
import sqlite3

class COVIDDataTransformer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.db_path = 'data/covid_analytics.db'
    
    def continent_analysis(self):
        """
        Aggregate data by continent
        """
        continent_summary = self.df.groupby('Continent').agg({
            'Total_Cases': 'sum',
            'Total_Deaths': 'sum',
            'Active_Cases': 'sum',
            'Country': 'count'
        }).reset_index()
        
        continent_summary.columns = [
            'Continent', 
            'Total_Continental_Cases', 
            'Total_Continental_Deaths', 
            'Total_Active_Cases',
            'Total_Countries'
        ]
        
        return continent_summary
    
    def top_affected_countries(self, top_n=10):
        """
        Get top N most affected countries
        """
        return self.df.nlargest(top_n, 'Total_Cases')[
            ['Country', 'Total_Cases', 'Total_Deaths']
        ]
    
    def save_to_sqlite(self):
        """
        Save transformed data to SQLite database
        """
        conn = sqlite3.connect(self.db_path)
        
        # Original data
        self.df.to_sql('country_covid_data', conn, if_exists='replace', index=False)
        
        # Continent analysis
        continent_summary = self.continent_analysis()
        continent_summary.to_sql('continent_summary', conn, if_exists='replace', index=False)
        
        # Top affected countries
        top_countries = self.top_affected_countries()
        top_countries.to_sql('top_affected_countries', conn, if_exists='replace', index=False)
        
        conn.close()
        print("Data saved to SQLite database successfully.")

def main():
    transformer = COVIDDataTransformer('data/processed_covid_data.csv')
    transformer.save_to_sqlite()
    
    # Display some insights
    print("\nContinent Analysis:")
    print(transformer.continent_analysis())
    
    print("\nTop 10 Most Affected Countries:")
    print(transformer.top_affected_countries())

if __name__ == "__main__":
    main()
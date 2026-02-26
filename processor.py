import pandas as pd
import numpy as np
import logging
import os

class DataProcessor:
    """
    Cleans and processes raw e-commerce data using Pandas and NumPy.
    """
    
    def __init__(self, input_file="data/raw_books_data.csv", output_file="data/clean_books_data.csv"):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Mapping dictionary for text-to-integer conversion
        self.rating_map = {
            'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'None': np.nan
        }

    def load_data(self):
        """Loads data from the raw CSV."""
        try:
            self.df = pd.read_csv(self.input_file)
            self.logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
        except FileNotFoundError:
            self.logger.error(f"File {self.input_file} not found. Please run scraper first.")
            raise

    def clean_prices(self):
        """Removes currency symbols and converts prices to floats."""
        self.logger.info("Cleaning price column...")
        # The price usually comes with an unusual currency symbol like Â£
        # We extract just the numeric part using regex
        self.df['Price'] = self.df['Price_Raw'].str.extract(r'(\d+\.\d+)').astype(float)
        self.df.drop(columns=['Price_Raw'], inplace=True)

    def process_ratings(self):
        """Converts string ratings ('Three') to numeric integers (3)."""
        self.logger.info("Converting text ratings to integers...")
        self.df['Rating'] = self.df['Rating_Text'].map(self.rating_map)
        self.df.drop(columns=['Rating_Text'], inplace=True)

    def flag_outliers(self):
        """Uses NumPy to calculate the Z-score and flag price outliers."""
        self.logger.info("Calculating Z-scores to flag price outliers...")
        prices = self.df['Price'].to_numpy()
        
        # Calculate mean and standard deviation
        mean_price = np.mean(prices)
        std_price = np.std(prices)
        
        # Calculate Z-score
        self.df['Price_Z_Score'] = (self.df['Price'] - mean_price) / std_price
        
        # Flag anything with a Z-score > 2 or < -2 as an outlier
        self.df['Is_Outlier'] = np.where(np.abs(self.df['Price_Z_Score']) > 2, True, False)

    def run_pipeline(self):
        """Executes the full cleaning pipeline."""
        if self.df is None:
            self.load_data()
            
        self.clean_prices()
        self.process_ratings()
        self.flag_outliers()
        
        # Drop missing values
        initial_len = len(self.df)
        self.df.dropna(subset=['Price', 'Rating'], inplace=True)
        self.logger.info(f"Dropped {initial_len - len(self.df)} rows with missing critical data.")
        
        self.save_data()
        return self.df

    def save_data(self):
        """Saves the cleaned DataFrame to a new CSV."""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        self.df.to_csv(self.output_file, index=False)
        self.logger.info(f"Cleaned data saved to {self.output_file}")
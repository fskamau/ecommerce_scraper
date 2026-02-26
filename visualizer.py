import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

class DataVisualizer:
    """
    Generates analytical plots from cleaned e-commerce data using Matplotlib.
    """
    
    def __init__(self, data_file="data/clean_books_data.csv", output_dir="plots/"):
        self.data_file = data_file
        self.output_dir = output_dir
        self.df = None
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self):
        """Loads the cleaned dataset."""
        try:
            self.df = pd.read_csv(self.data_file)
            self.logger.info("Cleaned data loaded for visualization.")
        except FileNotFoundError:
            self.logger.error("Clean data file not found. Run processor first.")
            raise

    def set_plot_style(self):
        """Configures the aesthetic style for all Matplotlib plots."""
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12

    def plot_price_distribution(self):
        """Creates a histogram showing the distribution of book prices."""
        self.logger.info("Generating Price Distribution Plot...")
        plt.figure()
        
        # Filter out outliers for a cleaner histogram
        normal_prices = self.df[self.df['Is_Outlier'] == False]['Price']
        
        plt.hist(normal_prices, bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Book Prices (Excluding Outliers)')
        plt.xlabel('Price (£)')
        plt.ylabel('Number of Books')
        plt.grid(axis='y', alpha=0.75)
        
        output_path = os.path.join(self.output_dir, 'price_distribution.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        self.logger.info(f"Saved plot to {output_path}")

    def plot_rating_vs_price(self):
        """Creates a scatter plot comparing star rating to price."""
        self.logger.info("Generating Rating vs. Price Plot...")
        plt.figure()
        
        # Group data by rating to get average price per rating
        avg_prices = self.df.groupby('Rating')['Price'].mean().reset_index()
        
        plt.plot(avg_prices['Rating'], avg_prices['Price'], marker='o', linestyle='-', color='coral')
        plt.title('Average Price by Star Rating')
        plt.xlabel('Star Rating (1-5)')
        plt.ylabel('Average Price (£)')
        plt.xticks([1, 2, 3, 4, 5])
        plt.grid(True, alpha=0.5)
        
        output_path = os.path.join(self.output_dir, 'rating_vs_price.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        self.logger.info(f"Saved plot to {output_path}")

    def generate_all_plots(self):
        """Runs the full visualization suite."""
        if self.df is None:
            self.load_data()
            
        self.set_plot_style()
        self.plot_price_distribution()
        self.plot_rating_vs_price()
        self.logger.info("All visualizations completed successfully.")
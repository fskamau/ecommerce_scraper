import logging
from scraper import EcommerceScraper
from processor import DataProcessor
from visualizer import DataVisualizer

def main():
    """
    Main execution controller for the E-Commerce ETL Pipeline.
    """
    print("="*50)
    print("🚀 Starting E-Commerce Data Pipeline")
    print("="*50)
    
    # 1. EXTRACT
    print("\n--- PHASE 1: EXTRACTION ---")
    scraper = EcommerceScraper(pages_to_scrape=5)
    scraper.run_scraper()
    scraper.save_to_csv()
    
    # 2. TRANSFORM
    print("\n--- PHASE 2: PROCESSING & CLEANING ---")
    processor = DataProcessor()
    processor.run_pipeline()
    
    # 3. LOAD / VISUALIZE
    print("\n--- PHASE 3: DATA VISUALIZATION ---")
    visualizer = DataVisualizer()
    visualizer.generate_all_plots()
    
    print("\n" + "="*50)
    print("✅ Pipeline Completed Successfully!")
    print("Check the '/data' and '/plots' folders for results.")
    print("="*50)

if __name__ == "__main__":
    main()
# 🛒 E-Commerce Data Scraper & Analyzer
> **A high-performance Python ETL pipeline for automated product intelligence.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458.svg)](https://pandas.pydata.org/)
[![BeautifulSoup](https://img.shields.io/badge/Scraper-BS4-green.svg)](https://www.crummy.com/software/BeautifulSoup/)

---

## 📖 Table of Contents
* [Executive Summary](#-executive-summary)
* [ETL Workflow](#-etl-workflow)
* [Technical Features](#-technical-features)
* [Project Structure](#-project-structure)
* [Installation & Setup](#-installation--setup)
* [Data Schema](#-data-schema)
* [Usage & Execution](#-usage--execution)
* [Statistical Methodology](#-statistical-methodology)
* [Troubleshooting](#-troubleshooting)
* [License](#-license)

---

## 🚀 Executive Summary
This project provides a production-ready solution for scraping, cleaning, and analyzing e-commerce data from the `books.toscrape.com` sandbox. Unlike simple scripts, this pipeline implements a structured **ETL (Extract, Transform, Load)** approach, ensuring data integrity through regex-based sanitization and statistical outlier detection.



---

## 🛠️ ETL Workflow

### 1. Extract (Scraping)
* **Engine:** `BeautifulSoup4` with `Requests`.
* **Logic:** Traverses 50+ pages of product listings.
* **Resilience:** Implements User-Agent rotation and error handling for 404/500 responses to prevent script termination during long crawls.

### 2. Transform (Data Cleaning)
* **Standardization:** Converts currency strings (e.g., `£51.77`) into `float64`.
* **Categorical Mapping:** Maps text-based ratings ("One", "Two", "Three"...) to a numerical scale ($1-5$).
* **Sanitization:** Removes non-ASCII characters from titles and normalizes whitespace.

### 3. Load & Visualize (Analysis)
* **Storage:** Persists the final dataset as a sanitized `.csv` and a `SQLite` database (optional).
* **Intelligence:** Generates distribution plots and correlation heatmaps to identify pricing trends relative to stock levels.

---

## ✨ Technical Features
* **Paginated Traversal:** Automatically detects the "Next" button to scrape the entire catalog.
* **Vectorized Operations:** Uses `NumPy` for fast mathematical transformations instead of slow Python loops.
* **Visual Storytelling:** Built-in `Matplotlib` / `Seaborn` templates for instant reporting.
* **Outlier Identification:** Uses the Interquartile Range (IQR) method to flag suspiciously priced items.

---

## 📂 Project Structure
```text
ecommerce-scraper/
├── data/
│   ├── raw_data.json          # Unprocessed scrape results
│   └── cleaned_books.csv      # Production-ready dataset
├── plots/
│   ├── price_distribution.png # Histogram of product prices
│   └── rating_analysis.png    # Scatter plot of ratings vs price
├── src/
│   ├── scraper.py             # BS4 extraction logic
│   ├── processor.py           # Pandas transformation logic
│   └── visualizer.py          # Matplotlib plotting scripts
├── main.py                    # Main pipeline entry point
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation

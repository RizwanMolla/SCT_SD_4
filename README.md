# 🛒 E-commerce Scraper

A modern desktop app to scrape product data from e-commerce category pages (tested with [books.toscrape.com](https://books.toscrape.com)). Built with Python, CustomTkinter, and BeautifulSoup.

![image](https://github.com/user-attachments/assets/1519b82e-ca98-424b-bda3-7eb36b039c5f)

![image](https://github.com/user-attachments/assets/ffb341cf-139b-443a-94f7-02596d4c035b)


## Features

- Enter any compatible e-commerce site URL
- Automatically loads and lists product categories
- Scrapes all products in a selected category (including pagination)
- Saves results as `products.csv`
- Clean, dark-themed GUI

## How to Run

1. **Install dependencies**  
   Make sure you have Python installed.  
   Install required packages:
   ```bash
   pip install customtkinter requests beautifulsoup4 pandas

2. **Run the game**
   ```bash
   python task4.py

## Usage
- Enter the website URL (default: https://books.toscrape.com/).
- Click Load Categories to fetch available categories.
- Select a category from the dropdown.
- Click Start Scraping.
- Wait for the status message to confirm completion.
- The scraped data will be saved as products.csv in the current folder.

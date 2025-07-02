import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("E-commerce Scraper")
app.geometry("650x500")

status = ctk.StringVar()
status.set("Enter website and load categories.")
category_urls = {}

def fetch_categories(site_url):
    try:
        response = requests.get(site_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cat_elements = soup.select("ul.nav-list ul li a")
        categories = {cat.text.strip(): site_url.rstrip('/') + "/" + cat["href"] for cat in cat_elements}
        return categories
    except Exception as e:
        status.set(f"Error: {str(e)}")
        return {}

def load_categories():
    global category_urls
    url = site_entry.get().strip()
    if not url:
        status.set("Please enter a website URL.")
        return
    status.set("Fetching categories...")
    category_urls = fetch_categories(url)
    if category_urls:
        dropdown.configure(values=list(category_urls.keys()))
        dropdown.set(list(category_urls.keys())[0])
        status.set("Categories loaded.")
    else:
        status.set("No categories found or invalid structure.")

def scrape_category(category_url, status_label):
    url = category_url
    all_data = []
    page = 1

    while True:
        status_label.set(f"Scraping page {page}...")
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        books = soup.select(".product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text
            rating = book.p["class"][1]
            all_data.append({"Title": title, "Price": price, "Rating": rating})

        next_btn = soup.select_one("li.next a")
        if next_btn:
            next_url = next_btn["href"]
            url = "/".join(url.split("/")[:-1]) + "/" + next_url
            page += 1
        else:
            break

    pd.DataFrame(all_data).to_csv("products.csv", index=False)
    status_label.set(f"Done! {len(all_data)} products saved to products.csv")

def start_scraping():
    category = dropdown.get()
    if not category:
        status.set("Please select a category.")
        return
    status.set("Starting scraper...")
    threading.Thread(target=scrape_category, args=(category_urls[category], status), daemon=True).start()

# UI Elements
ctk.CTkLabel(app, text="Custom E-commerce URL", font=("Arial", 16)).pack(pady=10)
site_entry = ctk.CTkEntry(app, width=500)
site_entry.insert(0, "https://books.toscrape.com/")
site_entry.pack(pady=5)

ctk.CTkButton(app, text="Load Categories", command=load_categories).pack(pady=10)

ctk.CTkLabel(app, text="Select Category", font=("Arial", 16)).pack(pady=5)
dropdown = ctk.CTkOptionMenu(app, values=[])
dropdown.pack(pady=10)

ctk.CTkButton(app, text="Start Scraping", command=start_scraping).pack(pady=20)

status_label = ctk.CTkLabel(app, textvariable=status, font=("Arial", 14), wraplength=500)
status_label.pack(pady=10)

app.mainloop()

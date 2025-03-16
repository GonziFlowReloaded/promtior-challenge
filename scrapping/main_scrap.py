from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error {response.status_code}: No se pudo acceder a la página")
        return None, None, None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Obtener todos los href de los enlaces
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    
    # Obtener todo el texto dentro del HTML
    text = soup.get_text(separator=' ', strip=True)
    
    return links, text, url

def save_to_mongo(data, db_name="scraper_db", collection_name="pages"):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(data)
    print(f"Datos guardados en MongoDB: {data['url']}")

def scrape_recursive(url, visited_urls, domain):
    if url in visited_urls:
        return
    
    visited_urls.add(url)
    sub_links, text, scraped_url = scrape_html(url)
    
    if text:
        data = {"url": scraped_url, "text": text, "url_encontradas": sub_links}
        save_to_mongo(data)
        
        if sub_links:
            for link in sub_links:
                parsed_link = urlparse(link)
                if parsed_link.netloc.endswith(domain):
                    scrape_recursive(link, visited_urls, domain)

# URL de inicio
start_url = "https://promtior.ai"
domain = "promtior.ai"
visited_urls = set()

scrape_recursive(start_url, visited_urls, domain)

print("Proceso finalizado.")

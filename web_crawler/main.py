from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from keybert import KeyBERT

def crawl(collection, starting_url):
    visited = set()
    q = [starting_url]
    model = KeyBERT('distilbert-base-nli-mean-tokens')

    while q and len(visited) < 1000:
        url = q.pop(0)
        x = requests.get(url)

        if x.status_code == 200:
            visited.add(url)
            text = x.text
            soup = BeautifulSoup(text, 'html.parser')
            relative_links = soup.find_all('a')

            keywords = model.extract_keywords(soup)
            print(keywords)

            # for link in relative_links:
            #     if link not in visited:
            #         q.append(link)



def main():
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)

    try:
        database = client.get_database("cs6675")
        web_crawler = database.get_collection("web_crawler")

        url = "https://www.cc.gatech.edu/"
        crawl(web_crawler, url)

    except Exception as e:
        raise Exception("Error connecting to database: ", e)
    

    

if __name__ == '__main__':
    main()


    
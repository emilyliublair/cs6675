from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import threading
import time
from urllib.parse import urljoin

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

db = client.get_database("cs6675")
web_crawler = db.get_collection("web_crawler_gui")

visited = set()
starting_url = input("Enter starting URL: ")
narrow_url = input("What would you like to limit your crawl to? ")
num = input("Maximum URLs to crawl: ")

start = time.time()
visited = set()
q = [starting_url]
q_lock = threading.Lock()
print("\nStarting Crawl...")

def crawl():
    while True and len(visited) < int(num) and len(q) > 0:
        url = None
        with q_lock:
            if len(q) > 0:
                url = q.pop(0)
        if url and url not in visited:
            try: 
                x = requests.get(url, timeout=5)

                if x.status_code == 200:
                    visited.add(url)
                    print(len(visited))
                    soup = BeautifulSoup(x.text, 'html.parser')
                    relative_links = soup.find_all('a')
                    text = soup.get_text(' ', strip=True)[:5000]

                    doc = {"url": url, "text": text}
                    web_crawler.update_one({"url": url}, {"$set": doc}, upsert=True)

                    for link in relative_links:
                        next_url = link.get("href")
                        if next_url and narrow_url in urljoin(url, next_url) and next_url not in visited:
                            with q_lock: 
                                q.append(urljoin(url, next_url))
            except:
                continue

def main():
    start = time.time()

    thread1 = threading.Thread(target = crawl)
    thread2 = threading.Thread(target = crawl)
    thread3 = threading.Thread(target = crawl)
    thread4 = threading.Thread(target = crawl)
    thread5 = threading.Thread(target = crawl)
    thread6 = threading.Thread(target = crawl)
    thread7 = threading.Thread(target = crawl)
    thread8 = threading.Thread(target = crawl)
    thread9 = threading.Thread(target = crawl)
    thread10 = threading.Thread(target = crawl)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()
    thread10.join()

    end = time.time()
    print("Crawl Finished! Here are your crawl statistics: ")
    
    s = end - start
    print(s)
    t = s / float(60)
    
    s = end - start
    t = s / float(60)
    num_crawled_url = len(visited)
    num_extracted_url = num_crawled_url + len(q)

    crawled_url_p_s = float(num_crawled_url) / t
    extracted_url_p_s = float(num_extracted_url) / t
    crawled_extracted = float(num_crawled_url) / num_extracted_url

    print("\nTotal time of execution (s): ", s)
    print("# URLs crawled: ", num_crawled_url)
    print("# URLs extracted: ", num_extracted_url)
    print("Crawl Speed (# URLs crawled per minute): ", crawled_url_p_s)
    print("# URLs Extracted Per Minute: ", extracted_url_p_s)
    print("Ratio of # URLs Crawled / # URLs to be crawled: ", crawled_extracted)

if __name__ == '__main__':
    main()
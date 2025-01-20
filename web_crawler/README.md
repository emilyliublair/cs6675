
# CS6675 Homework 1: Web Crawler

## Implementation
For Homework 1, I chose to complete option 1.2 and create my own web crawler from scratch. 

I chose https://www.cc.gatech.edu/ as my starting url and focused my crawl on CoC Georgia Tech links (includes "cc.gatech.edu" in the url). I used the `requests` python library to fetch the content of webpages, the `BeautifulSoup` library to parse the retrieved HTML, and limited my text retrieval to the first 5000 characters. For data storage, I explored 2 different approaches. 

### Option 1: Dictionary Storage (option1.ipynb)
The first option I took was to use a dictionary data structure for my inverted index. The structure of an entry looks like `{ keyword: [url1, url2, url3, ...] }`. To extract keywords, I chose to use the DistilBERT model. BERT is a state-of-the-art Transformer model that is used for various NLP tasks including search, sentiment analysis, etc. DistilBERT is a smaller version of BERT that runs 60% faster while preserving 95% performance of the original model. Since speed is an important aspect of web crawler performance, I chose to utilize the faster model. Using this approach, I was able to crawl 1000 urls in 26m 4s, giving me the following crawl statistics:

| Metric | Statistic |
| -------- | ------- |
| Total # Keywords Extracted (Unique) | 184 |
| # Keywords Extracted Per Minute | 7.058 |
| Crawl Speed (# URLs Crawled Per Minute) | 38.36 |
| # URLs Extracted Per Minute | 2565.959 |
| Ratio of # URLs Crawled / # URLs to be crawled | 0.0149 |

Note that the model will only extract the 5 most relevant keywords in the text, which is why the total number of keywords extracted is so low. Therefore, this approach can be useful for finding more relevant pages (URLs that are more focused on the keyword they are searching for) rather than pages that may just mention the keyword once or twice. The following is an example of the dictionary/inverted index used to store the keywords extracted:

`{'forbes': ['https://www.cc.gatech.edu/news/research-ai-safety-lands-recent-graduate-forbes-30-under-30', 'https://prod-cc.cc.gatech.edu/news/research-ai-safety-lands-recent-graduate-forbes-30-under-30', 'https://www.cc.gatech.edu/news/research-ai-safety-lands-recent-graduate-forbes-30-under-30#main-navigation', 'https://www.cc.gatech.edu/news/research-ai-safety-lands-recent-graduate-forbes-30-under-30#main-content', 'https://www.cc.gatech.edu/news/research-ai-safety-lands-recent-graduate-forbes-30-under-30#search-container']}`

### Option 2: MongoDB (option2.ipynb)
The second approach I explored was using MongoDB as my Web archive. This design decision was motivated by MongoDB's built-in Inverted Index, which allows for keyword and keyphrase lookup without the additional overhead of using an ML model for keyword extraction. Each document has 3 fields: `_id, url, text`. Using this approach, I was able to crawl 1000 urls in 5m 3s, giving me the following crawl statistics:

| Metric | Statistic |
| -------- | ------- |
| Crawl Speed (# URLs Crawled Per Minute) | 198.02 |
| # URLs Extracted Per Minute | 13219.60 |
| Ratio of # URLs Crawled / # URLs to be crawled | 0.0149 |

Documents/URLs could then be searched for within the MongoDB database with queries. For example, if someone wanted to search for links related to CS internships and career fairs, they could use the following query:
` 
  {
    "text": {
      "$regex": "(computer science.*internship|career fair)",
      "$options": "i"
    }
  }
`
and get the following response:
<img src="./images/mongodb_example_query.png" alt="Execution Time">

Note that the data stored on the MongoDB database has been exported as a json file and can be acccessed at cs6675.web_crawler.json. 

### Optimization (multithreaded.py)
Comparing the two options I explored, it is clear that the second option utilizing MongoDB was better in terms of speed. Option 2 also provided a better way for indexing -- enabling search with more keywords and the ability to search for keyphrases.

Thus, to further optimize my web crawler, I chose to incoporate multi-threading into my Option 2 implementation. I experimented with various thread numbers and arrived at the following conclusion: 

<img src="./images/threads_vs_time.png" alt="Threads vs Time" width="600">

### Crawl Comparisons
| Metric                                  | DistilBERT | MongoDB | 10-Threaded MongoDB |
|-----------------------------------------|------------|---------|---------------------|
| Total Execution Time (seconds)          | 1564       | 303     | 59                  |
| Crawl Speed (# URLs Crawled Per Minute) | 38.36      | 198.02  | 1016.95             |
| # URLs Extracted Per Minute             | 2565.959   | 13219.6 | 72729.304           |
| Ratio of # URLs Crawled / # URLs to be crawled | 0.0149     | 0.0149  | 0.0137              |

<img src="./images/exec_time.png" alt="Execution Time" width="400">
<img src="./images/crawl_speed.png" alt="Crawl Speed" width="400">
<img src="./images/extract_p_min.png" alt="Extraction per Minute" width="400">
<img src="./images/extract_v_crawled.png" alt="Extraction vs Crawled" width="400">


## Final Product
The final product can be accessed at webcrawler.py. It utilizes 10 threads and the MongoDB approach for storage. To use, you must create your own MongoDB collection and modify those values within the script (`uri, db, web_crawler`). Once you run the script, you will be prompted to enter a starting URL, a URL narrower, and maximum number of URLs you want to crawl. Once the script finishes, it will print out some crawl statistics including total time of execution, # of URLs crawled, and crawl speed. The following is an example execution:

    Enter starting URL: https://en.wikipedia.org/wiki/Web_crawler
    What would you like to limit your crawl to? en.wikipedia.org/wiki
    Maximum URLs to crawl: 200

    Starting Crawl...
    Crawl Finished! Here are your crawl statistics: 

    Total time of execution (s):  79.64573740959167
    # URLs crawled:  200
    # URLs extracted:  105249
    Crawl Speed (# URLs crawled per minute):  150.66719689326212
    # URLs Extracted Per Minute:  79287.85902909472
    Ratio of # URLs Crawled / # URLs to be crawled:  0.0019002555843760985
    
### Pros vs. Cons
**Pros**

1. Speed: with the utilization of 10 threads working in parallel, the web crawler is able to crawl URLs in extremely fast times.
2. Scalability: MongoDB databases are well-suited for high-throughput writes. With the added parallelism, this solution makes it easy to scale and crawl many pages. 
3. Usability: with MongoDB's built-in Inverted Index storage, it makes it easy for users to search for specific keywords and even keyphrases. 

**Cons**

1. Resource Utilization: having 10 threads working in parallel -- eaching making a GET request to some web server -- may put a lot of strain on the computer's CPU and also introduce traffic and high loads within the network. 
2. Server Strain: if the user ends up crawling on one specific server a lot (putting strain on the server), it could potentially lead to IP bans and rate-limiting.
3. MongoDB Storage Overhead: since the solution utilizes MongoDB for its Inverted Index storage, it forces the additional overhead of creating, configuring, and managing an additional database outside the current script on to the user.
4. Accuracy: since two different URLs can actually point to the same webpage, my web crawler may actually crawl the same page multiple times, which is bad for efficiency and skews statistics/metrics. This can be seen in the example inverted index output under option 1, where all the URLs related to the keyword "forbes" -- although different -- ultimately reference the same webpage. 

### Predictions
Using my 10-threaded script, I predict the following:

1. 10 million pages: 590000 seconds = 9833.33 minutes = 163.88 hours = 6.83 days
2. 1 billion pages: 59 million seconds = 983333.33 minutes = 16388.88 hours = 682.87 days = 1.87 years

## Discussion (Experience & Lessons)
This experience was very informative and provided a lot of learning opportunities. Firstly, I was exposed to various keyword extraction methods including DistilBERT, spaCy, and Rake. Reading and seeing examples of their implementations allowed me to learn more about the practical applications of modern NLP models. I also expanded my knowledge of the capabilities of MongoDB (Inverted Index structure, high write-throughput, keyword/keyphrase lookup, etc.) that could be helpful for future system designs/projects when considering the pros and cons of various data storages. Finally, I also gained experience with system architecture design and learned how to consider the trade-offs of different approaches.

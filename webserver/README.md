# CS6675 Homework 4: Web Server Technology

GitHub Link: https://github.com/emilyliublair/cs6675/tree/main/webserver

## Implementation
For Homework 4, I chose to complete option 2 and create my own web service that hosts 5 web pages and create various workloads to interact with the web service. 

### Web Service
The web service I created hosts 5 web pages, each containing different content. `/page1.html` contains 10 different images, `page2.html` contains 5 of the same video, `page3.html` contains a JavaScript animation, `page4.html` contains a script that computes 50,000 primes, and `page5.html` is a combination of all previous pages. You can view these pages in the `/tomcat/pages` folder. Note that the content in each page was chosen to be included due to being CPU-intensive, thus increasing server load.  

### Remote Client
<div style="display: flex; gap: 10px;">
    <img src="./images/images.PNG" width="200">
    <img src="./images/video.PNG" width="200">
    <img src="./images/animation.PNG" width="200">
</div>
<div style="display: flex; gap: 10px;">
    <img src="./images/prime.PNG" width="200">
    <img src="./images/combined.PNG" width="200">
</div>


### Testing Web Server Performance
To test my web server performance, I used Locust: https://github.com/locustio/locust. You can view the locust file at `locustfile.py`, which can be run using the following command: `locust -f locustfile.py --host={host}`. Then, using it's web-based UI, I tested my web service using 100 total users with a ramp up of 10 (users started per second), and ran it until 50,000 requests had been completed. 

<img src=./images/locust.png>

I received the following results:

<img src=./images/table.png>

<img src=./images/charts.png>

Since the results contain a lot of information, a summary of the notable statistics (average latency and throughput) are displayed in the following table:

| Page         | Avg Latency (s) | Throughput (RPS) |
|-------------|----------------|------------------|
| /page1.html | 0.00670        | 63.4             |
| /page2.html | 0.00676        | 66.2             |
| /page3.html | 0.00670        | 62.1             |
| /page4.html | 0.00672        | 66.5             |
| /page5.html | 0.00675        | 64.5             |
| **Aggregated** | **0.00673**  | **322.7**        |

### Stress Test
To create a stress test of my web service, I modified my inputs into Locust to have 10,000 users with a ramp up of 500 (users spawned per second), and ran it until 500,000 requests had been completed. I received the following results:

<img src=./images/stress_table.png>

<img src=./images/stress_charts.png>

A summary of the notable statistics are displayed in the following table:

| Page         | Avg Latency (s) | Throughput (RPS) |
|-------------|----------------|------------------|
| /page1.html | 4.59461        | 126.9            |
| /page2.html | 4.74248        | 126.0            |
| /page3.html | 4.67431        | 120.9            |
| /page4.html | 4.54698        | 126.5            |
| /page5.html | 4.57405        | 126.6            |
| **Aggregated** | **4.62651**  | **627.0**        |

With the increased number of users, we see that the average latency for each page increased by over 4 seconds per each request, and the throughput for each page more than doubled. Interestingly, however, Locust reported 0 failures of the 500,000 requests that were sent -- indicating that the server was able to handle the increased load without dropping requests at the cost of significantly higher response times. It should also be noted that within a minute of running the workload, CPU usage reached over 90%, indicating high saturation and stress on the web server:

<img src=./images/high_cpu.png>

### Web Access Cache
According to the Apache Tomcat 11 Configuration (https://tomcat.apache.org/tomcat-11.0-doc/config/resources.html), web caching is enabled by default. Thus, for the previous results, I added the following line into the `context.xml` file to disable caching: `<Resources cachingAllowed="false"/>`. On the other hand, the results in this section were obtained with the line omitted, enabling caching on my web server. I received the following results:

**Initial Web Server Performance Test**
<img src=./images/cache_table.png>

<img src=./images/cache_charts.png>

A summary of the notable statistics are displayed in the following table:

| Page          | Avg Latency (s) | Throughput (RPS) |
|--------------|----------------|-----------------|
| /page1.html  | 0.00448        | 67.2            |
| /page2.html  | 0.00435        | 64.6            |
| /page3.html  | 0.00439        | 63.9            |
| /page4.html  | 0.00443        | 66.2            |
| /page5.html  | 0.00438        | 62.9            |
| **Aggregated** | **0.00441**    | **324.8**        |

Compared the non-cache results, we see that the average latency decreased by around .002 seconds per request, and the average throughput remained the same, differing by only 2 requests per second. Thus, for relatively small numbers of requests, it seems that caching does not have a significant impact on performance.

**Stress Test**
<img src=./images/stress_cache_table.png>

<img src=./images/stress_cache_charts.png>

A summary of the notable statistics are displayed in the following table:

| Page          | Avg Latency (s) | Throughput (RPS) |
|--------------|----------------|-----------------|
| /page1.html  | 4.20212        | 157.1           |
| /page2.html  | 4.26750        | 151.8           |
| /page3.html  | 4.38066        | 155.6           |
| /page4.html  | 4.19760        | 152.4           |
| /page5.html  | 4.28256        | 159.4           |
| **Aggregated** | **4.26607**    | **776.3**       |

Compared to the non-cache results, we see that the average latency decreased by almost 0.4 seconds per request, and the throughput increased by over 150 requests per second. This is a significant performance boost, highlighting the importance/impact of caching in optimizing web server performance. However, it should be noted that the content within pages 3 and 4 cannot be fully cached. Page 3 contains JavaScript code that dynamically generates an animation at runtime, meaning it does not produce static assets that can be effectively cached. While the JavaScript file itself can be cached, the rendered animation remains dynamic. Page 4 executes prime number computations on page load. Similarly, while the JavaScript file itself can be cached, the computations are generated dynamically and are not stored. These two caveats limit the effectiveness of caching on my web server's performance. The performance of Page 5, which is a combination of all pages, is also thus limited. 

## Learnings
1. One of the key learnings I gained from this homework assignment was using Locust as a way to test web server performance. Prior to this assignment, I had experience with developing web applications specifically focusing on developing features, functionality, and user experience. I had never delved into performance testing -- especially under high load or stress -- since the applications I was developing were relatively small in scale and unlikely to experience heavy traffic in real-world use. This assignment gave me hands-on experience in simulating high traffic and analyzing server performance, which I believe will be invaluable for future experiences. 
2. Another key insight I gained from this experience was introducing caching into web servers. Similar to the previous learning, since my experience with web applications never involved high traffic, introducing caching had never been a topic that cross my mind. However, this homework assignment gave me first-hand experience about the benefits of caching and its impact on performance. At the same time, it also introduced to me some limitations of caching, and how one would modify their web server content to take the most advantage of caching. 
3. The last learning I gained from this homework assignment was the experience of creating and hosting an Apache web server. Prior to this homework, my experience with web servers was limited to Netlify -- a platform that abstracts the intracacies of web server hosting from users. Although I did not interact a lot with the server files, this assignment gave me a small preview of the complexities involved with configuring and managing a web server. 

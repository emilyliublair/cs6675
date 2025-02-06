# CS6675 Homework 2: Peer to Peer System

Github Link: https://github.com/emilyliublair/cs6675/tree/main/peer2peer

## Implementation
For Homework 2, I chose to complete option 1.2 and join a full-fledge P2P network as a client. The P2P system I chose was BitTorrent (https://www.bittorrent.com/) and used its Web API (https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)#get-global-transfer-info) to perform queries and measurements. 

### How to Use
To use my script, download BitTorrent and either download a .torrent file or enter a magnet link in the application to join a network. Then, under 'Tools' -> 'Options' -> 'Web UI', enable 'Web User Interface. After, change the variables `QB_URL`, `USERNAME`, and `PASSWORD` according what you configure in the application. Then, just run `python peer2peer.py` to begin measuring the system. 

My script offers 5 possible measurements to the user:

**Option 1: Membership Establishment (Hand-Shake) Cost**

Pressing `1` allows you to measure the memership establishment cost of the network. It prints out the time it takes the login and establish an initial connection with peers (can be leechs or seeds). An example output is as follows:

<img src=./images/member_establishment.png>

**Option 2: Membership Maintenance Cost**

Pressing `2` allows you to measure the membership maintenance cost of the network. I define membership maintenance cost as the number of peer changes (polled every 5 seconds) within a specified duration. An example output is as follows:

<img src=./images/membership_maintenance.png>

**Option 3: One-hop Dynamics**

Pressing `3` allows you to measure the one-hop dynamics of the network. More specifically, it prints the average lifetime of a peer within a specified duration. An example output is as follows:

<img src=./images/peer_lifetime.png>

**Option 4: Query Latency & Throughput**

Pressing `4` allows you to measure the latency and throughput of varying number of query loads. Entering a comma-separated list of number of query loads, it will print out th average latency and throughput of each load. Note that each load has both fake queries (queries that will not find any content) and real queries. A real query is run in intervals of 10. An example output is as follows:

<img src=./images/query_latency_throughput.png>

**Option 5: Seed : Leech Ratio**

Pressing `5` allows you to measure the seed to leech ratio of the system within a specified duration. An example output is as follows:

<img src=./images/seed_leech.png>

Note: the above measurements were made on the following torrent: enwiki-20241201-pages-articles-multistream.xml.bz2

## Observations
Here are 3 observations I made based on the 5 example measurements that I provided above. 

**Observation 1**

From option 2, we see 61 peer changes in 60 seoncds, which is a relatively high peer turnover rate. This indicates that at the time, the network was extremely dynamic. At the same time, option 3 shows an average peer lifetime of 1.51 seconds. This makes sense as a short lifetime would contribute to high peer churn (peers joining and leaving the network frequently). Note that having a high peer churn rate can negatively impact the system due to increased membership maintenance costs, unreliable resource availability, and higher latency (due to having to reroute queries).

**Observation 2**

From option 4, we see that despite the query load increasing from 10 to 20 to 40, the average latency remained around 22.38-22.49 seconds. Since the latency remains the same despite the increasing query loads, this indicates that the network is not easily congested. Option 5 shows the ratio of seeds to leechs. From the measurement, we see a constant 0 seeds and a maximum of 4 leechs at a time. With such a small amount of peers, I can infer that (at least at that instance) the network does not increase congestion with increased load likely due to an underutilized network rather than an efficient system design (i.e. effective query routing, caching, etc.). 

**Observation 3**

From option 4, we see that throughput increases from 3.99 queries/sec under a 10 load to 5.04 queries/sec under a 40 load. This suggests that the system is good/efficient at handling high query loads. Aligning with observation 2, this suggests that the network has untapped capacity at lower loads (meaning it is underutilized) and depicts better performance when more queries are running likely due to better reliance of available peers. 

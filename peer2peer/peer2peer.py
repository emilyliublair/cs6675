import requests
import time

# qBittorrent Web API credentials, CHANGE ACCORDINGLY
QB_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "adminadmin"


def login(username, password):
    session = requests.Session()
    login_data = {"username": username, "password": password}
    response = session.post(f"{QB_URL}/api/v2/auth/login", data=login_data)
    if response.status_code == 200:
        # print("Successfully logged in")
        return session
    else:
        print("Login unsuccessful")
        return None
    

def measure_membership_establishment(username, password):
    start_time = time.time()
    session = requests.Session()
    login_data = {"username": username, "password": password}
    response = session.post(f"{QB_URL}/api/v2/auth/login", data=login_data)

    if response.status_code == 200:
        while True:
            data = session.post(f"{QB_URL}/api/v2/sync/maindata").json()
            torrent = list(data["torrents"].keys())[0]
            if data["torrents"][torrent]["num_leechs"] > 0 or data["torrents"][torrent]["num_seeds"] > 0:
                break  # Peers found
            
            time.sleep(1)

        establishment_time = time.time() - start_time
        print(f"Membership Establishment Time: {establishment_time:.2f} sec")
        return establishment_time
    else:
        print("Login unsuccessful")
        return None
    

def measure_membership_maintenance(session, duration):
    start_time = time.time()
    peer_changes = 0
    prev_peers = set()

    torrent = session.post(f"{QB_URL}/api/v2/torrents/info").json()[0]
    torrent_hash = torrent["hash"]

    while time.time() - start_time < duration:
        torrent_peers_data = session.post(f"{QB_URL}/api/v2/sync/torrentPeers", data={
            "hash": torrent_hash
        }).json()

        current_peers = set(torrent_peers_data["peers"].keys())

        if prev_peers:
            peer_changes += len(prev_peers.symmetric_difference(current_peers))

        prev_peers = current_peers
        time.sleep(5)

    print(f"Membership Maintenance Cost: {peer_changes} peer changes in {duration} sec")
    return peer_changes


def measure_p2p_dynamics(session, duration):
    start_time = time.time()
    peer_history = {}

    torrent = session.post(f"{QB_URL}/api/v2/torrents/info").json()[0]
    torrent_hash = torrent["hash"]

    while time.time() - start_time < duration:
        torrent_peers_data = session.post(f"{QB_URL}/api/v2/sync/torrentPeers", data={
            "hash": torrent_hash
        }).json()
        current_peers = set(torrent_peers_data["peers"].keys())

        for peer_ip in current_peers:
            if peer_ip not in peer_history:
                peer_history[peer_ip] = {"first_seen": time.time(), "last_seen": time.time()}
            else:
                peer_history[peer_ip]["last_seen"] = time.time()

        time.sleep(1)

    
    peer_durations = {peer: info["last_seen"] - info["first_seen"] for peer, info in peer_history.items()}
    avg_lifetime = sum(peer_durations.values()) / len(peer_durations) if peer_durations else 0

    print(f"Average Peer Lifetime: {avg_lifetime:.2f} sec")
    return avg_lifetime


def query(session, query, category="all"):
    start_time = time.time()
    res = session.post(f"{QB_URL}/api/v2/search/start", data={
        "pattern": query,
        "plugins": "all",
        "category": category
    })

    if res.status_code == 200:
        search_id = res.json().get("id")
        
        while True:
            results = session.post(f"{QB_URL}/api/v2/search/results", data={"id": search_id})
            if results.json().get("status") == "Stopped":
                break
            time.sleep(1)
        
        latency = time.time() - start_time
        return latency, len(results.json().get("results", []))
    else:
        print("Query unsuccessful, status code: " + res.status_code)


def measure_query_latency(session, loads):
    results = {}
    real_queries = ["albert", "biology", "cats", "delaware", "elephant", "fox", "georgia", "house", "ice", "jelly"]
    for load in loads:
        total_latency = 0
        total_queries = 0
        for i in range(load):
            if i % 10 == 0:
                latency, found = query(session, real_queries[(i//10 ) - 1])
            else:
                latency, found = query(session, f"fake_query_{i}")
            total_latency += latency
            total_queries += found
        avg_latency = total_latency / load
        throughput = total_queries / (total_latency if total_latency > 0 else 1)

        results[load] = {
            "avg_latency": avg_latency,
            "throughput": throughput,
        }

    for load, data in results.items():
        print(f"Query Load: {load}")
        print(f"  Avg Latency: {data['avg_latency']:.2f} sec")
        print(f"  Throughput: {data['throughput']:.2f} queries/sec")
        print()


def get_seed_leech_ratio(session, duration):
    start_time = time.time()
    ratios = []
    print("# seeds : # leechs")
    
    while time.time() - start_time < duration:
        data = session.post(f"{QB_URL}/api/v2/sync/maindata").json()
        
        torrent = list(data["torrents"].keys())[0]
        ratios.append((data["torrents"][torrent]["num_seeds"], data["torrents"][torrent]["num_leechs"]))
        print(data["torrents"][torrent]["num_seeds"], " : ", data["torrents"][torrent]["num_leechs"])

        time.sleep(10)
    return ratios


def main():

    print("Measure your Peer-to-Peer System. Press 'q' to exit. ")
    print("Press (1) to measure your membership establishment cost (time to establish initial connections)")
    print("Press (2) to measure membership maintenance cost (how often peers change in a given timeframe).")
    print("Press (3) to measure one-hop dynamics (average peer lifetime).")
    print("Press (4) to measure query latency and throughput.")
    print("Press (5) to measure seed:leech ratio.")

    while True:
        user_input = input("Enter your choice (1-5) or 'q' to quit: ").strip().lower()

        if user_input == 'q':
            print("Exiting...")
            break
            
        elif user_input == '1':
            measure_membership_establishment(USERNAME, PASSWORD)

        elif user_input == '2':
            duration = input("Enter duration in seconds (default = 60): ").strip()
            duration = int(duration) if duration.isdigit() else 60
            session = login(USERNAME, PASSWORD)

            if session:
                    measure_membership_maintenance(session, duration)

        elif user_input == '3':
            duration = input("Enter duration in seconds (default = 60): ").strip()
            duration = int(duration) if duration.isdigit() else 60
            session = login(USERNAME, PASSWORD)

            if session:
                    measure_p2p_dynamics(session, duration)

        elif user_input == '4':
            query_input = input("Enter a comma-separated list of query counts (e.g., 10,20,40): ").strip()
            try:
                query_counts = [int(q.strip()) for q in query_input.split(",") if q.strip().isdigit()]
                session = login(USERNAME, PASSWORD)

                if session:
                    measure_query_latency(session, query_counts)
            except:
                print("Invalid input. Please enter a valid comma-separated list of numbers.")

        elif user_input == '5':
                duration = input("Enter duration in seconds (default = 60): ").strip()
                duration = int(duration) if duration.isdigit() else 60
                session = login(USERNAME, PASSWORD)

                if session:
                    get_seed_leech_ratio(session, duration)

        else:
            print("Invalid input. Please enter a number between 1 and 5 or 'q' to exit.")

if __name__ == "__main__":
    main()
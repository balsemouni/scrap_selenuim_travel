import threading
import queue
import requests

# Queue to hold all proxies
q = queue.Queue()
valid_proxies = []

# Read proxies from file
with open("proxy\proxy_list.txt", "r") as f:
    proxy_lines = f.read().splitlines()

    for line in proxy_lines:
        # Remove protocol part (e.g., http:// or https://)
        cleaned_proxy = line.split("://")[-1]
        q.put(cleaned_proxy)

# Function to check proxies
def check_proxies():
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get(
                "https://www.tripadvisor.com/Hotels",
                proxies={"http": proxy, "https": proxy},
                timeout=10
            )


            # Only consider valid if response is NOT the JS warning page
            if res.status_code == 200:
                if "enable JavaScript" not in res.text:
                    print(f"✅ Valid proxy: {proxy}")
                    valid_proxies.append(proxy)
                else:
                    print(f"❌ Proxy blocked by JS wall: {proxy}")
            else:
                print(f"❌ Non-200 status code: {proxy} | Status: {res.status_code}")

        except Exception as e:
            # Proxy didn't work
            pass
        q.task_done()

# Start multiple threads
for _ in range(10):
    t = threading.Thread(target=check_proxies, daemon=True)
    t.start()

# Wait until all tasks in the queue are processed
q.join()

# Optional: Save valid proxies to file
with open("valid_proxies.txt", "w") as f:
    for proxy in valid_proxies:
        f.write(proxy + "\n")

print("✅ Finished checking proxies.")
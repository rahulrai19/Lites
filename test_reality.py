import time
import requests
import sys

def test_cache(url):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer test-lites-key"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of Japan? Please answer in one word."}
        ]
    }
    
    print(f"Testing Lites API on {url}...")
    
    # Request 1 (Cache Miss)
    print("\n--- Request 1 (Expected Miss) ---")
    start = time.perf_counter()
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Failed to connect: HTTP {response.status_code}")
            print(response.text)
            return False
    except requests.exceptions.ConnectionError:
        print(f"Connection refused on {url}")
        return False
        
    duration1 = (time.perf_counter() - start) * 1000
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()['choices'][0]['message']['content']}")
    print(f"Latency: {duration1:.2f} ms")
    
    # Request 2 (Cache Hit)
    print("\n--- Request 2 (Expected Hit) ---")
    start2 = time.perf_counter()
    response2 = requests.post(url, json=payload, headers=headers)
    duration2 = (time.perf_counter() - start2) * 1000
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()['choices'][0]['message']['content']}")
    print(f"Latency: {duration2:.2f} ms")
    
    print("\n--- Results ---")
    print(f"Cache Hit was {duration1 / duration2:.2f}x faster!")
    return True

test_cache("https://lites-su1c.onrender.com/v1/chat/completions")

import time
import requests
import os

# CONFIG: Talking to the RELAY you just started
RELAY_URL = "http://localhost:3000/v1/chat/completions" 
WATCH_FILE = "../src/waft/api/main.py"

def get_evolution(code):
    print("🧠 Consulting Gemma-4...")
    payload = {
        "model": "gemma-4",
        "messages": [
            {"role": "system", "content": "You are the Waft Architect. Improve the provided code. Return ONLY the code."},
            {"role": "user", "content": f"Refactor for clarity and add type hints:\n\n{code}"}
        ]
    }
    r = requests.post(RELAY_URL, json=payload)
    return r.json()['choices'][0]['message']['content']

def main():
    print(f"🛰️ Satellite observing: {WATCH_FILE}")
    last_mtime = os.stat(WATCH_FILE).st_mtime
    
    while True:
        mtime = os.stat(WATCH_FILE).st_mtime
        if mtime != last_mtime:
            print("✨ Change detected!")
            with open(WATCH_FILE, "r") as f:
                content = f.read()
            
            new_content = get_evolution(content)
            
            # Simple safety: don't write if the brain returned an error or empty string
            if len(new_content) > 10:
                with open(WATCH_FILE, "w") as f:
                    f.write(new_content)
                print("✅ Evolution applied.")
            
            last_mtime = mtime
        time.sleep(1)

if __name__ == "__main__":
    main()
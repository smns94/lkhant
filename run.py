import core
import os
import sys
import requests
import time
from datetime import datetime

# --- [ CONFIGURATION ] ---
DB_URL = "https://raw.githubusercontent.com/smns94/lkhant/refs/heads/main/database.txt"
KEY_FILE = "key.txt"

# --- [ UI COLORS ] ---
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
    
    # Status မှာ Expire ပါရင် အစိမ်းရောင်ပြမယ်
    status_color = C_GREEN if 'EXP:' in status or 'VERIFIED' in status else C_RED
    
    print(f"{C_YELLOW}╔══════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}DEVICE ID{C_RESET} : {C_GREEN}{did:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}STATUS{C_RESET}    : {status_color}{status:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}╚══════════════════════════════════════════════════════╝{C_RESET}")

def extract_expiry(key):
    try:
        # Key ရဲ့ နောက်ဆုံး ၁၂ လုံးကို ယူပါတယ်
        raw_date = key.strip()[-12:]
        # ပုံစံဖော်ခြင်း: DD/MM/YYYY
        formatted = f"{raw_date[6:8]}/{raw_date[4:6]}/{raw_date[:4]}"
        return formatted
    except:
        return "N/A"

def check_online_key(key):
    try:
        r = requests.get(DB_URL, timeout=10)
        if r.status_code == 200:
            approved_keys = [line.strip() for line in r.text.splitlines() if line.strip()]
            if key.strip() in approved_keys:
                return True, "SUCCESS"
        return False, "INVALID"
    except:
        return False, "OFFLINE"

def main():
    try:
        did = core.get_device_id()
        saved_key = ""

        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                saved_key = f.read().strip()

        # ၁။ Bypass အရင်လုပ်မယ်
        show_smns_banner(did, "INITIALIZING BYPASS...")
        core.start_process()
        time.sleep(2)

        # ၂။ Key Validation Loop
        while True:
            if not saved_key:
                show_smns_banner(did, "PENDING ACTIVATION")
                print(f"\n{C_CYAN}[?] Enter Activation Key to continue{C_RESET}")
                saved_key = input(f"{C_GREEN}root@turbo:~# {C_RESET}").strip().upper()

            is_valid, status = check_online_key(saved_key)

            if is_valid:
                # Expire Date ထုတ်ယူမယ်
                exp = extract_expiry(saved_key)
                
                # Key ကို သိမ်းမယ်
                with open(KEY_FILE, "w") as f:
                    f.write(saved_key)
                
                # *** Banner ကို အသစ်ပြန်ပြမယ် (ဒီနေရာမှာ Expire ပေါ်လာမှာပါ) ***
                show_smns_banner(did, f"VERIFIED (EXP: {exp})")
                print(f"\n{C_GREEN}[✓] Access Granted! Enjoy your service.{C_RESET}")
                
                # တကယ့် process ကို ဒီမှာ ခေါ်ပါ (ဥပမာ Menu)
                # core.main_menu() 
                break
            else:
                if status == "OFFLINE":
                    print(f"\n{C_YELLOW}[!] Offline. Re-Bypassing...{C_RESET}")
                    core.start_process()
                    time.sleep(4)
                else:
                    print(f"\n{C_RED}[X] Invalid Key! Access Denied.{C_RESET}")
                    if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
                    saved_key = ""
                    sys.exit()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Interrupted.{C_RESET}")

if __name__ == "__main__":
    main()

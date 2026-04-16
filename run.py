import core
import os
import sys
import requests
import time

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

def check_online_key(key):
    try:
        # GitHub က database ကို strip() သုံးပြီး သေချာဖတ်ခြင်း
        r = requests.get(DB_URL, timeout=7)
        if r.status_code == 200:
            approved_keys = [line.strip() for line in r.text.splitlines() if line.strip()]
            return key.strip() in approved_keys, "SUCCESS"
        return False, "SERVER_ERROR"
    except:
        return False, "OFFLINE"

def main():
    try:
        did = core.get_device_id()
        saved_key = ""

        # ၁။ သိမ်းထားသော Key ရှိမရှိ စစ်ဆေးခြင်း
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                saved_key = f.read().strip()

        # ၂။ အမြဲတမ်း အရင်ဆုံး Bypass အလုပ်ကို လုပ်ခိုင်းမည်
        show_smns_banner(did, "INITIALIZING BYPASS...")
        print(f"\n{C_CYAN}[*] Running Bypass Tasks... Please wait.{C_RESET}")
        core.start_process() # မူရင်း bypass function
        
        # Bypass လုပ်ပြီး အင်တာနက်တည်ငြိမ်အောင် ခဏစောင့်မည်
        time.sleep(3)

        # ၃။ Key Validation စတင်ခြင်း
        while True:
            if not saved_key:
                show_smns_banner(did, "PENDING ACTIVATION")
                print(f"\n{C_CYAN}[?] Enter Activation Key to continue{C_RESET}")
                saved_key = input(f"{C_GREEN}root@turbo:~# {C_RESET}").strip().upper()

            # Online စစ်ဆေးခြင်း
            print(f"{C_CYAN}[*] Verifying Key Online...{C_RESET}")
            is_valid, status = check_online_key(saved_key)

            if is_valid:
                # Key မှန်ကန်ပါက သိမ်းဆည်းမည်
                with open(KEY_FILE, "w") as f:
                    f.write(saved_key)
                
                show_smns_banner(did, "VERIFIED ONLINE")
                print(f"\n{C_GREEN}[✓] Access Granted! Enjoy your tool.{C_RESET}")
                
                # အကယ်၍ အစ်ကို့ core ထဲမှာ Menu ပြစရာရှိရင် ဒီမှာခေါ်ပါ
                # core.main_menu

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

def check_online(key):
    try:
        # GitHub က database ကို လှမ်းစစ်ခြင်း
        r = requests.get(DB_URL, timeout=5)
        if r.status_code == 200:
            return key in r.text.splitlines(), "VERIFIED"
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

        # --- [ KEY VALIDATION PROCESS ] ---
        while True:
            if not saved_key:
                show_smns_banner(did, "PENDING ACTIVATION")
                print(f"\n{C_CYAN}[?] Enter Activation Key to continue{C_RESET}")
                saved_key = input(f"{C_GREEN}root@turbo:~# {C_RESET}").strip().upper()

            # ၁။ Online ရှိမရှိ အရင်စစ်မယ်
            is_valid, status = check_online(saved_key)

            # ၂။ အကယ်၍ Offline ဖြစ်နေရင် (Portal မိနေရင်) Bypass အရင်လုပ်ခိုင်းမယ်
            if status == "OFFLINE":
                show_smns_banner(did, "PORTAL DETECTED - BYPASSING...")
                print(f"\n{C_YELLOW}[!] No internet. Attempting bypass to verify key...{C_RESET}")
                
                # အစ်ကို့ရဲ့ core ထဲက bypass လုပ်တဲ့ function ကို ဒီမှာခေါ်ပါ
                core.start_process() 
                
                print(f"{C_CYAN}[*] Retrying online verification...{C_RESET}")
                time.sleep(3) # အင်တာနက်ပြန်တက်လာအောင် ခဏစောင့်မယ်
                is_valid, status = check_online(saved_key)

            # ၃။ နောက်ဆုံးရလဒ်ကို စစ်ဆေးခြင်း
            if is_valid:
                with open(KEY_FILE, "w") as f:
                    f.write(saved_key)
                show_smns_banner(did, "VERIFIED ONLINE")
                print(f"\n{C_GREEN}[✓] Access Granted. Tool is ready!{C_RESET}")
                # Tool ရဲ့ Main Logic ကို ဆက်သွားပါ
                # core.run_main_logic()
                break
            else:
                print(f"\n{C_RED}[X] Invalid Key or Server Error!{C_RESET}")
                if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
                saved_key = "" # Key အသစ်ပြန်တောင်းဖို့ clear လုပ်မယ်
                sys.exit()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped by user.{C_RESET}")

if __name__ == "__main__":
    main()

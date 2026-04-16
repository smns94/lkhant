import core
import os
import sys
import requests
import time

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

             {C_YELLOW}>>> VOUCHER BYPASS SYSTEM v2.0 <<<{C_CYAN}
    {C_RESET}"""
    print(banner)
    
    status_color = C_GREEN if 'EXP:' in status or 'VERIFIED' in status else C_RED
    
    print(f"   {C_YELLOW}╔══════════════════════════════════════════════════════╗{C_RESET}")
    print(f"   {C_YELLOW}║{C_RESET} {C_CYAN}DEVICE ID{C_RESET} : {C_GREEN}{did:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"   {C_YELLOW}║{C_RESET} {C_CYAN}STATUS{C_RESET}    : {status_color}{status:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"   {C_YELLOW}╚══════════════════════════════════════════════════════╝{C_RESET}")

def extract_expiry(key):
    try:
        raw = key.strip()[-12:]
        return f"{raw[6:8]}/{raw[4:6]}/{raw[:4]}"
    except:
        return "N/A"

def check_online_key(key):
    try:
        r = requests.get(DB_URL, timeout=8)
        if r.status_code == 200:
            keys = [l.strip() for l in r.text.splitlines() if l.strip()]
            return (key.strip() in keys)
        return False
    except:
        return False

def main():
    try:
        did = core.get_device_id()
        saved_key = ""
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                saved_key = f.read().strip()

        # --- [ STEP 1: KEY CHECK FIRST ] ---
        # သိမ်းထားတဲ့ Key ရှိရင် Online မှာ အရင်စစ်မယ် (Bypass မလုပ်ခင် အရင်လုပ်မယ်)
        if saved_key:
            # အင်တာနက်မရှိရင်တောင် Expire Date ကို Key ထဲကနေ ကြိုထုတ်ထားမယ်
            exp = extract_expiry(saved_key)
            show_smns_banner(did, f"VERIFIED (EXP: {exp})")
        else:
            show_smns_banner(did, "PENDING ACTIVATION")
            print(f"\n   {C_CYAN}[?] Enter Activation Key{C_RESET}")
            saved_key = input(f"   {C_GREEN}root@turbo:~# {C_RESET}").strip().upper()

        # --- [ STEP 2: BYPASS START ] ---
        # Banner မှာ Expire ပေါ်နေချိန်မှာ Bypass ကို စတင်မယ်
        print(f"\n   {C_CYAN}[*] Starting Bypass Process...{C_RESET}")
        core.start_process()

        # --- [ STEP 3: FINAL VERIFICATION ] ---
        # Bypass လုပ်လို့ အင်တာနက်ရလာပြီဆိုမှ Key ကို Online မှာ အတည်ပြုမယ်
        time.sleep(2)
        if check_online_key(saved_key):
            with open(KEY_FILE, "w") as f:
                f.write(saved_key)
            # အောင်မြင်ရင် Banner ကို တစ်ခေါက် ထပ် Update လုပ်မယ်
            exp = extract_expiry(saved_key)
            show_smns_banner(did, f"VERIFIED (EXP: {exp})")
            print(f"\n   {C_GREEN}[✓] SYSTEM READY. LOGIN SUCCESSFUL!{C_RESET}")
        else:
            print(f"\n   {C_RED}[X] Access Denied! Invalid Key.{C_RESET}")
            if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
            sys.exit()

    except Exception as e:
        print(f"\n   {C_RED}[!] Error: {e}{C_RESET}")

if __name__ == "__main__":
    main()

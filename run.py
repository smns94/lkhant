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
    
    # SMNS Logo ကို Center ချိန်ရန် Space ထည့်ထားသည်
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
    
    # Information Box (ပိုကျယ်ပြီး Center ကျအောင် ညှိထားသည်)
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
        # User တွေ အဆင်ပြေအောင် timeout ကို နည်းနည်းတိုးထားပေးတယ်
        r = requests.get(DB_URL, timeout=10)
        if r.status_code == 200:
            keys = [l.strip() for l in r.text.splitlines() if l.strip()]
            return (key.strip() in keys)
        return False
    except:
        return False

def main():
    try:
        # Device ID ရယူခြင်း
        try:
            did = core.get_device_id()
        except:
            did = "TRB-UNKNOWN-ID"
            
        # ၁။ Bypass အရင်လုပ်မည်
        show_smns_banner(did, "INITIALIZING BYPASS...")
        core.start_process()
        time.sleep(2)
        
        # ၂။ Key Validation 
        saved_key = ""
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                saved_key = f.read().strip()

        while True:
            if not saved_key:
                show_smns_banner(did, "PENDING ACTIVATION")
                print(f"\n   {C_CYAN}[?] Enter Activation Key to Unlock System{C_RESET}")
                saved_key = input(f"   {C_GREEN}root@turbo:~# {C_RESET}").strip().upper()

            # Online စစ်ဆေးခြင်း
            if check_online_key(saved_key):
                exp = extract_expiry(saved_key)
                with open(KEY_FILE, "w") as f:
                    f.write(saved_key)
                
                # အောင်မြင်ပါက Banner ကို Update လုပ်မည်
                show_smns_banner(did, f"VERIFIED (EXP: {exp})")
                print(f"\n   {C_GREEN}[✓] LOGIN SUCCESSFUL! SYSTEM READY.{C_RESET}")
                
                # အစ်ကို့ရဲ့ Menu ကို ဒီအောက်မှာ ဆက်သွားပါ
                # core.main_menu()
                break
            else:
                print(f"\n   {C_RED}[X] Invalid or Expired Key! Access Denied.{C_RESET}")
                if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
                saved_key = ""
                sys.exit()

    except Exception as e:
        print(f"\n   {C_RED}[!] Error: {e}{C_RESET}")

if __name__ == "__main__":
    main()

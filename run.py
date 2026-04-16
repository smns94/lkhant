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
      >>> {C_YELLOW}VOUCHER BYPASS SYSTEM v2.0{C_CYAN} <<< {C_RESET}
    """
    print(banner)
    
    status_color = C_GREEN if 'EXP:' in status or 'VERIFIED' in status else C_RED
    
    print(f"{C_YELLOW}╔══════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}DEVICE ID{C_RESET} : {C_GREEN}{did:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}STATUS{C_RESET}    : {status_color}{status:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}╚══════════════════════════════════════════════════════╝{C_RESET}")

def extract_expiry(key):
    try:
        # Key ရဲ့ နောက်ဆုံး ၁၂ လုံးကို ရက်စွဲအဖြစ် ယူခြင်း
        raw = key.strip()[-12:]
        return f"{raw[6:8]}/{raw[4:6]}/{raw[:4]}"
    except:
        return "N/A"

def check_online_key(key):
    try:
        r = requests.get(DB_URL, timeout=10)
        if r.status_code == 200:
            keys = [l.strip() for l in r.text.splitlines() if l.strip()]
            return (key.strip() in keys)
        return False
    except:
        return False

def main():
    try:
        did = core.get_device_id()
        
        # ၁။ Bypass အရင်လုပ်မယ်
        show_smns_banner(did, "INITIALIZING BYPASS...")
        core.start_process()
        
        # Bypass ပြီးတာနဲ့ ခဏစောင့်ပြီး Key ဘက်ကို ဆက်သွားမယ်
        time.sleep(2)
        
        # ၂။ Key စစ်တဲ့ အပိုင်း
        saved_key = ""
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                saved_key = f.read().strip()

        while True:
            if not saved_key:
                show_smns_banner(did, "PENDING ACTIVATION")
                print(f"\n{C_CYAN}[?] Enter Activation Key{C_RESET}")
                saved_key = input(f"{C_GREEN}root@turbo:~# {C_RESET}").strip().upper()

            # Online စစ်မယ်
            if check_online_key(saved_key):
                exp = extract_expiry(saved_key)
                with open(KEY_FILE, "w") as f:
                    f.write(saved_key)
                
                # Banner ကို အသစ်ထပ်ပြမယ် (ဒါမှ Status မှာ ပြောင်းသွားမှာပါ)
                show_smns_banner(did, f"VERIFIED (EXP: {exp})")
                print(f"\n{C_GREEN}[✓] LOGIN SUCCESSFUL!{C_RESET}")
                
                # ပင်မ Menu ကို ဒီမှာခေါ်ပါ
                # core.main_menu()
                break
            else:
                print(f"\n{C_RED}[X] Invalid or Expired Key!{C_RESET}")
                if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
                saved_key = ""
                # Key မှားရင် Tool ထဲ ပေးမဝင်တော့ပါဘူး
                sys.exit()

    except Exception as e:
        print(f"\n{C_RED}[!] Error: {e}{C_RESET}")

if __name__ == "__main__":
    main()

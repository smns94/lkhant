import core
import os
import sys

# --- [ UI COLORS & DESIGN ] ---
C_CYAN = '\033[96m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_BOLD = '\033[1m'
C_RESET = '\033[0m'

KEY_FILE = "key.txt"

def show_smns_banner(did, status):
    os.system('clear')
    # ပိုကြီးပြီး ပိုကျယ်သော SMNS ASCII Art
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
    
    # ပိုကျယ်သော Box Border (Width တိုးထားသည်)
    print(f"{C_YELLOW}╔══════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}DEVICE ID{C_RESET} : {C_GREEN}{did:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}STATUS{C_RESET}    : {status_color}{status:<39}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}╚══════════════════════════════════════════════════════╝{C_RESET}")

def main():
    try:
        did = core.get_device_id()
        saved_key = ""

        # ၁။ သိမ်းထားသော Key ရှိမရှိ စစ်ဆေးခြင်း
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                saved_key = f.read().strip()

        if saved_key:
            # သိမ်းထားသော Key ဖြင့် Auto-login စမ်းသပ်ခြင်း
            is_valid, msg, expiry = core.validate_key(did, saved_key)
            if is_valid:
                show_smns_banner(did, f"VERIFIED (EXP: {expiry})")
                print(f"\n{C_GREEN}[✓] Auto-logged in with saved key.{C_RESET}")
                core.start_process()
                return
            else:
                os.remove(KEY_FILE) # Key သက်တမ်းကုန်နေလျှင် ဖျက်ပစ်မည်

        # ၂။ Key မရှိလျှင် သို့မဟုတ် သက်တမ်းကုန်လျှင် အသစ်တောင်းမည်
        show_smns_banner(did, "PENDING ACTIVATION")
        print(f"\n{C_CYAN}[?] Enter Activation Key to continue{C_RESET}")
        key = input(f"{C_GREEN}root@turbo:~# {C_RESET}").strip().upper()
        
        is_valid, msg, expiry = core.validate_key(did, key)
        
        if is_valid:
            # Key မှန်ကန်ပါက ဖိုင်ထဲတွင် သိမ်းဆည်းမည်
            with open(KEY_FILE, "w") as f:
                f.write(key)
                
            show_smns_banner(did, f"VERIFIED (EXP: {expiry})")
            print(f"\n{C_GREEN}[+] Key Activated & Saved Successfully!{C_RESET}")
            core.start_process() 
        else:
            print(f"\n{C_RED}[X] Invalid Key! Access Denied.{C_RESET}")
            sys.exit()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped by user.{C_RESET}")

if __name__ == "__main__":
    main()

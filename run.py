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

def show_smns_banner(did, status):
    os.system('clear')
    # SMNS ASCII Art
    banner = f"""{C_CYAN}{C_BOLD}
   ███████╗███╗   ███╗███╗   ██╗███████╗
   ██╔════╝████╗ ████║████╗  ██║██╔════╝
   ███████╗██╔████╔██║██╔██╗ ██║███████╗
   ╚════██║██║╚██╔╝██║██║╚██╗██║╚════██║
   ███████║██║ ╚═╝ ██║██║ ╚████║███████║
   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝
    >>> {C_YELLOW}VOUCHER BYPASS SYSTEM{C_CYAN} <<< {C_RESET}
    """
    print(banner)
    
    # Status Color Logic
    status_color = C_RED if 'PENDING' in status else C_GREEN
    
    # Info Box
    print(f"{C_YELLOW}╔══════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}DEVICE ID{C_RESET} : {C_GREEN}{did:<31}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}║{C_RESET} {C_CYAN}STATUS{C_RESET}    : {status_color}{status:<31}{C_RESET} {C_YELLOW}║{C_RESET}")
    print(f"{C_YELLOW}╚══════════════════════════════════════════════╝{C_RESET}")

# --- [ MAIN PROCESS ] ---
def main():
    try:
        did = core.get_device_id() # User ID ရယူခြင်း
        
        # အစမှာ Status ကို Pending အနေနဲ့ ပြသမည်
        show_smns_banner(did, "PENDING ACTIVATION")
        
        # Activation Key တောင်းခံခြင်း
        print(f"\n{C_CYAN}[?] Activation Key Required{C_RESET}")
        key = input(f"{C_GREEN}root@turbo:~# {C_RESET}").strip().upper()
        
        # core.so ထဲက မူရင်း logic နဲ့ စစ်ဆေးခြင်း
        is_valid, msg, expiry = core.validate_key(did, key)
        
        if is_valid:
            # Key မှန်ပါက Banner ကို Status သစ်ဖြင့် တစ်ခါပြန်ပြမည်
            show_smns_banner(did, f"VERIFIED (EXP: {expiry})")
            print(f"\n{C_GREEN}[+] Access Granted! Starting...{C_RESET}")
            core.start_process() 
        else:
            print(f"\n{C_RED}[X] Invalid Key! Access Denied.{C_RESET}")
            sys.exit()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped by user.{C_RESET}")

if __name__ == "__main__":
    main()

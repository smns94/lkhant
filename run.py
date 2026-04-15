import os
import sys
import time
import shutil

# --- အရောင်သတ်မှတ်ချက်များ (RGB Style) ---
C = '\033[38;2;0;255;255m'    # Cyan (Main Title)
M = '\033[38;2;255;0;255m'    # Magenta (Sub Title)
G = '\033[38;2;0;255;0m'      # Green (Success)
Y = '\033[38;2;255;255;0m'    # Yellow (Warning/Process)
R = '\033[38;2;255;0;0m'      # Red (Error)
W = '\033[0m'                 # White / Reset

def clear_screen():
    os.system('clear')

def get_center(text):
    # စာသားကို Screen ရဲ့ အလယ်ဗဟို ပို့ပေးတဲ့ function
    term_width = shutil.get_terminal_size().columns
    lines = text.split('\n')
    centered_lines = [line.center(term_width) for line in lines]
    return '\n'.join(centered_lines)

def display_banner():
    clear_screen()
    
    # ကြီးမားသော SMNS ASCII Title
    smns_art = f"""{C}
 ██████  ███▄ ▄███▒ ███▄    █   ██████ 
▒██    ▒  ▓██▒▀█▀ ██▒ ██ ▀█   █ ▒██    ▒ 
░ ▓██▄    ▓██    ▓██░▓██  ▀█ ██▒░ ▓██▄   
  ▒   ██▒ ▒██    ▒██ ▓██▒  ▐▌██▒  ▒   ██▒
▒██████▒▒ ▒██▒   ░██▒▒██░   ▓██░▒██████▒▒
▒ ▒▓▒ ▒ ░ ░ ▒░   ░  ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░ ░  ░      ░░ ░░   ░ ▒░░ ░▒  ░ ░
{W}"""
    
    sub_title = f"{M}>>> SMNS VOUCHER BYPASS TOOLKIT <<<{W}"
    
    print(get_center(smns_art))
    print(get_center(sub_title))
    print(f"{C}" + "━" * shutil.get_terminal_size().columns + f"{W}")

def main():
    display_banner()
    
    # --- Device Info Section ---
    device_id = "TRB-49417534BE" # ဒီနေရာမှာ အစ်ကို့ logic အတိုင်း ID ဆွဲထုတ်ခိုင်းပါ
    expiry_date = "2027-04-13 12:25:00"
    
    print(f"\n {C}┌──────────────────────────────────────────────┐{W}")
    print(f" {C}│{W}  {G}DEVICE ID{W} : {Y}{device_id}{W}                  {C}│{W}")
    print(f" {C}│{W}  {G}STATUS{W}    : {G}(EXP: {expiry_date}){W}      {C}│{W}")
    print(f" {C}└──────────────────────────────────────────────┘{W}")
    
    time.sleep(1)
    print(f"\n{G}[✓] Auto-logged in with saved key.{W}")
    time.sleep(0.8)
    
    print(f"{Y}[*] STAGE 1: EXECUTING INSTANT BYPASS (VOUCHER INJECTION){W}")
    
    # Loading animation အတိုလေး (ပိုလှအောင်)
    for i in range(3):
        print(f"{Y}.{W}", end="", flush=True)
        time.sleep(0.5)
    
    print(f"\n\n{G}[+] INTERNET ACCESS ACTIVE. AI OPTIMIZER ENABLED!{W}")
    
    # ဒီနေရာမှာ အစ်ကို့ရဲ့ နောက်ထပ် function တွေကို ဆက်ရေးလို့ရပါပြီ
    print(f"\n{C}Press Enter to exit...{W}")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Tool Stopped by User.{W}")
        sys.exit()

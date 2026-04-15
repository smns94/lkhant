import os
import sys
import time
import shutil
import re
import uuid

# --- အရောင်သတ်မှတ်ချက်များ (RGB Style) ---
C = '\033[38;2;0;255;255m'    # Cyan (Main Title)
M = '\033[38;2;255;0;255m'    # Magenta (Sub Title)
G = '\033[38;2;0;255;0m'      # Green (Success)
Y = '\033[38;2;255;255;0m'    # Yellow (Warning/Process)
R = '\033[38;2;255;0;0m'      # Red (Error)
W = '\033[0m'                 # White / Reset

def clear_screen():
    os.system('clear')

def strip_ansi(text):
    # အရောင် code များကိုဖယ်၍ စာသားအရှည်အစစ်ကို တွက်ချက်ခြင်း
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text)

def get_center(text):
    # စာသားများကို Screen ၏ အလယ်ဗဟိုသို့ ပို့ပေးခြင်း
    term_width = shutil.get_terminal_size().columns
    lines = text.split('\n')
    centered_lines = []
    for line in lines:
        visible_length = len(strip_ansi(line))
        padding = (term_width - visible_length) // 2
        centered_lines.append(" " * padding + line)
    return '\n'.join(centered_lines)

def get_device_id():
    # ဖုန်း hardware ပေါ်မူတည်ပြီး Unique ID ထုတ်ပေးခြင်း
    # ရှေ့တွင် SMNS- ဟု အမြဲပေါ်နေပါမည်
    node = uuid.getnode()
    unique_id = uuid.UUID(int=node).hex[-10:].upper()
    return f"SMNS-{unique_id}"

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
░ ░▒  ░ ░ ░  ░      ░░ ░░   ░ ▒░░ ░▒  ░ ░{W}"""
    
    sub_title = f"{M}>>> SMNS VOUCHER BYPASS TOOLKIT <<<{W}"
    
    print(get_center(smns_art))
    print(get_center(sub_title))
    print(f"{C}" + "━" * shutil.get_terminal_size().columns + f"{W}")

def main():
    display_banner()
    
    # --- Device Info Section ---
    device_id = get_device_id()
    expiry_date = "2027-04-13 12:25:00"
    
    # {:<11} ဖြင့် Colon (:) များ အပေါ်အောက် ကွက်တိညှိထားပါသည်
    info_box = f"""{C}┌──────────────────────────────────────────────┐
    {G}{'DEVICE ID':<11}{W} : {Y}{device_id}{W}           {C}
   {G}{'EXPIRY DATE':<11}{W} : {G}{expiry_date}{W}           {C}
└──────────────────────────────────────────────┘{W}"""
    
    print(get_center(info_box))
    
    time.sleep(1)
    print(f"\n{G}[✓] Auto-logged in with saved key.{W}")
    time.sleep(0.8)
    
    print(f"{Y}[*] STAGE 1: EXECUTING INSTANT BYPASS (VOUCHER INJECTION){W}")
    
    # Loading animation
    for i in range(3):
        print(f"{Y}.{W}", end="", flush=True)
        time.sleep(0.5)
    
    print(f"\n\n{G}[+] INTERNET ACCESS ACTIVE. AI OPTIMIZER ENABLED!{W}")
    
    print(f"\n{C}Press Enter to exit...{W}")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Tool Stopped by User.{W}")
        sys.exit()

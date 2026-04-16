import sys
import shutil

# Color Codes (အရောင်ဆန်းလေးများ)
# အစ်ကိုကြိုက်တဲ့အရောင်ကို အောက်က C1, C2 နဲ့ အစားထိုးသုံးနိုင်ပါတယ်
C1 = '\033[38;2;0;255;255m'    # Cyan (အပြာနုရောင်ဆန်း)
C2 = '\033[38;2;255;0;255m'    # Magenta (ပန်းခရမ်းရောင်)
C3 = '\033[38;2;255;255;255m'  # White (အဖြူရောင်)
G = '\033[92m'  # Green (အစိမ်းရောင်)
Y = '\033[93m'  # Yellow (အဝါရောင်)
W = '\033[0m'   # Reset (ပုံမှန်အရောင်ပြန်ဖြစ်စေရန်)

# Termux clear
print("\033[H\033[J", end="")

# Screen width ယူခြင်း (အလယ် center ထားရန်)
size = shutil.get_terminal_size()
width = size.columns

# ကြီးမားတဲ့ SMNS ASCII Art (Title)
# ဒါကို ကြီးကြီးမားမားနဲ့ C1 အရောင် (Cyan) နဲ့ပြပါမယ်
banner = f"""{C1}
  ██████  ███▄ ▄███▒ ███▄    █   ██████ 
▒██    ▒  ▓██▒▀█▀ ██▒ ██ ▀█   █ ▒██    ▒ 
░ ▓██▄    ▓██    ▓██░▓██  ▀█ ██▒░ ▓██▄   
  ▒   ██▒ ▒██    ▒██ ▓██▒  ▐▌██▒  ▒   ██▒
▒██████▒▒ ▒██▒   ░██▒▒██░   ▓██░▒██████▒▒
▒ ▒▓▒ ▒ ░ ░ ▒░   ░  ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░ ░  ░      ░░ ░░   ░ ▒░░ ░▒  ░ ░
░  ░  ░   ░      ░      ░   ▒ ░░  ░  ░   
      ░          ░            ░        ░ 
"""

# SMNS Voucher Bypass Toolkit (C2 Magenta အရောင်နဲ့ ပြပါမယ်)
sub_title = f"{C2}>>> SMNS VOUCHER BYPASS TOOLKIT <<<{W}"

# Function to center text (စာသားကို အလယ်ပို့ပေးမယ့် function)
def center_text(text, w):
    centered = ""
    for line in text.split('\n'):
        # စာသားအရှည်ကိုအရင်တိုင်း၊ padding တွက်ပြီး အလယ် center မှာထားမယ်
        centered += line.center(w) + "\n"
    return centered

# Title နဲ့ Sub-title ကို အလယ်ပို့ပြီး ပြသခြင်း
# width ထက် နည်းနည်းလျော့တွက်ပြီး center ကျအောင် လုပ်ထားပါတယ်
c_banner = center_text(banner, int(width * 0.98))
c_sub_title = sub_title.center(width)

# Print Banner and Sub-title
print(c_banner)
print(c_sub_title)
print(f"{Y}" + "─" * width + f"{W}\n") # Line separator

# အစ်ကို့ရဲ့ ကျန်တဲ့ Tool Info command တွေကို ဒီအောက်မှာ ဆက်ရေးပါ
print(f"{G}[✔] DEVICE ID : {W}TRB-49417534BE")
print(f"{G}[✔] EXPIRED   : {W}ACTIVATED (EXP: 2027-04-13 12:25:00)")
print(f"\n{G}[✓] Auto-logged in with saved key.{W}")
print(f"{Y}[*] STAGE 1: EXECUTING INSTANT BYPASS (VOUCHER INJECTION){W}")
print("...")
print(f"\n{G}[+] INTERNET ACCESS ACTIVE. AI OPTIMIZER ENABLED!{W}")

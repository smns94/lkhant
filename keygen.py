import hashlib
import sys
import os

# --- run.py ထဲက SECRET_SALT အတိုင်း ဖြစ်ရပါမယ် ---
SECRET_SALT = "ohmygod@123"

# အရောင်သတ်မှတ်ချက်
G = '\033[38;2;0;255;0m'      # Green
Y = '\033[38;2;255;255;0m'    # Yellow
C = '\033[38;2;0;255;255m'    # Cyan
W = '\033[0m'                 # White

def make_key():
    print(f"{C}--- SMNS KEY GENERATOR (AUTO-SAVE VERSION) ---{W}")
    
    # User ဆီက Device ID တောင်းခြင်း
    did = input(f"{Y}Enter User Device ID: {W}").strip()
    if not did:
        print(f"{Y}[!] Device ID မထည့်ဘဲ လုပ်လို့မရပါဘူး။{W}")
        return

    # Expiry Date (YYYYMMDDHHMM)
    print(f"{C}Example Format: 202612312359 (YearMonthDayHourMinute){W}")
    expiry = input(f"{Y}Enter Expiry Date: {W}").strip()
    
    if len(expiry) != 12:
        print(f"{Y}[!] Expiry format မှားနေပါတယ်။ (၁၂ လုံး ဖြစ်ရပါမယ်){W}")
        return

    # --- Logic: SHA256(ID + EXPIRY + SALT) ---
    raw = f"{did}{expiry}{SECRET_SALT}"
    auth_hash = hashlib.sha256(raw.encode()).hexdigest()
    
    # Key Format: Hash ရှေ့ ၁၂ လုံး + Expiry Date
    final_key = f"{auth_hash[:12].upper()}{expiry}"
    
    # --- Screen ပေါ်မှာပြသခြင်း ---
    print(f"\n{G}[✓] Generated Key for {did}:{W}")
    print(f"{Y}--> {final_key}{W}")

    # --- key.txt ထဲသို့ အလိုလို သိမ်းဆည်းခြင်း ---
    try:
        with open("key.txt", "w") as f:
            f.write(final_key)
        print(f"\n{G}[+] Key has been saved to 'key.txt' automatically!{W}")
    except Exception as e:
        print(f"\n{Y}[!] Error saving key: {e}{W}")

if __name__ == "__main__":
    try:
        make_key()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted by user.{W}")
        sys.exit()

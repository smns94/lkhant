import hashlib
import sys
import os

# --- run.py ထဲက SECRET_SALT အတိုင်း ဖြစ်ရပါမယ် ---
SECRET_SALT = "ohmygod@123"

# အရောင်သတ်မှတ်ချက်
G = '\033[38;2;0;255;0m'      # Green
Y = '\033[38;2;255;255;0m'    # Yellow
C = '\033[38;2;0;255;255m'    # Cyan
R = '\033[38;2;255;0;0m'      # Red
W = '\033[0m'                 # White

def clear_key():
    if os.path.exists("key.txt"):
        os.remove("key.txt")
        print(f"\n{R}[!] Saved key (key.txt) has been deleted.{W}")
    else:
        print(f"\n{Y}[!] No saved key found to delete.{W}")

def make_key():
    print(f"\n{C}--- SMNS KEY MANAGER ---{W}")
    print(f"1. Generate New Key")
    print(f"2. Delete Current Key (key.txt)")
    
    choice = input(f"\n{Y}Choose (1 or 2): {W}").strip()
    
    if choice == "2":
        clear_key()
        return

    # --- Generate Logic ---
    did = input(f"\n{Y}Enter User Device ID: {W}").strip()
    if not did:
        print(f"{R}[!] Device ID is required!{W}")
        return

    print(f"{C}Example: 202612312359{W}")
    expiry = input(f"{Y}Enter Expiry Date: {W}").strip()
    
    if len(expiry) != 12:
        print(f"{R}[!] Invalid Expiry Format!{W}")
        return

    # SHA256 Logic
    raw = f"{did}{expiry}{SECRET_SALT}"
    auth_hash = hashlib.sha256(raw.encode()).hexdigest()
    final_key = f"{auth_hash[:12].upper()}{expiry}"
    
    print(f"\n{G}[✓] New Key: {final_key}{W}")

    # Auto-save to key.txt
    with open("key.txt", "w") as f:
        f.write(final_key)
    print(f"{G}[+] Key saved to 'key.txt'{W}")

if __name__ == "__main__":
    try:
        make_key()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Stopped.{W}")
        sys.exit()

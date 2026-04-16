import hashlib
import sys
import os
from datetime import datetime

# --- run.py ထဲက SECRET_SALT အတိုင်း ဖြစ်ရပါမယ် ---
SECRET_SALT = "ohmygod@123"

# အရောင်သတ်မှတ်ချက်
G = '\033[38;2;0;255;0m'      # Green
Y = '\033[38;2;255;255;0m'    # Yellow
C = '\033[38;2;0;255;255m'    # Cyan
R = '\033[38;2;255;0;0m'      # Red
W = '\033[0m'                 # White

def save_to_history(did, key):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("key_history.txt", "a") as f:
        f.write(f"{now} | ID: {did} | Key: {key}\n")

def delete_key_menu():
    print(f"\n{C}--- KEY DELETION MENU ---{W}")
    print(f"1. Delete Active Key (key.txt)")
    print(f"2. Delete Key from History (One by one)")
    print(f"3. Clear All History")
    print(f"0. Back")
    
    choice = input(f"\n{Y}Choose: {W}").strip()
    
    if choice == "1":
        if os.path.exists("key.txt"):
            os.remove("key.txt")
            print(f"{R}[!] Active Key Deleted.{W}")
        else:
            print(f"{Y}[!] No active key found.{W}")
            
    elif choice == "2":
        if not os.path.exists("key_history.txt"):
            print(f"{Y}[!] History is empty.{W}")
            return
            
        with open("key_history.txt", "r") as f:
            lines = f.readlines()
            
        if not lines:
            print(f"{Y}[!] History is empty.{W}")
            return

        print(f"\n{C}--- SELECT KEY TO DELETE ---{W}")
        for i, line in enumerate(lines):
            print(f"{i+1}. {line.strip()}")
            
        try:
            target = int(input(f"\n{Y}Enter number to delete: {W}")) - 1
            if 0 <= target < len(lines):
                deleted_line = lines.pop(target)
                with open("key_history.txt", "w") as f:
                    f.writelines(lines)
                print(f"{R}[!] Deleted: {deleted_line.strip()}{W}")
            else:
                print(f"{R}[!] Invalid number.{W}")
        except ValueError:
            print(f"{R}[!] Numbers only!{W}")

    elif choice == "3":
        if os.path.exists("key_history.txt"):
            os.remove("key_history.txt")
            print(f"{R}[!] All History Cleared.{W}")

def make_key():
    while True:
        print(f"\n{C}=== SMNS KEY SYSTEM ==={W}")
        print(f"1. Generate New Key")
        print(f"2. View/Delete Keys")
        print(f"0. Exit")
        
        main_choice = input(f"\n{Y}Select: {W}").strip()
        
        if main_choice == "1":
            did = input(f"\n{Y}Enter Device ID: {W}").strip()
            if not did: continue
            
            expiry = input(f"{Y}Enter Expiry (12 digits): {W}").strip()
            if len(expiry) != 12:
                print(f"{R}[!] Invalid Expiry!{W}")
                continue

            # Logic
            raw = f"{did}{expiry}{SECRET_SALT}"
            auth_hash = hashlib.sha256(raw.encode()).hexdigest()
            final_key = f"{auth_hash[:12].upper()}{expiry}"
            
            # Save Active
            with open("key.txt", "w") as f:
                f.write(final_key)
            
            # Save History
            save_to_history(did, final_key)
            
            print(f"\n{G}[✓] Key Created & Saved: {final_key}{W}")
            
        elif main_choice == "2":
            delete_key_menu()
        elif main_choice == "0":
            break

if __name__ == "__main__":
    try:
        make_key()
    except KeyboardInterrupt:
        sys.exit()

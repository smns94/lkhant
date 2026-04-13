import core
import os
import sys

def main():
    did = core.get_device_id() # User ရဲ့ ID ကို ယူမည်
    os.system('clear')
    print(f"DEVICE ID: {did}")
    
    # Activation Key တောင်းခံခြင်း
    key = input("Enter Activation Key: ").strip().upper()
    
    # core.so ထဲက မူရင်း logic နဲ့ စစ်ဆေးခြင်း
    is_valid, msg, expiry = core.validate_key(did, key)
    
    if is_valid:
        print(f"Status: {msg} (Expires: {expiry})")
        core.start_process() # Key မှန်မှ ပရိုဂရမ် စတင်မည်
    else:
        print("Invalid Key! Access Denied.")
        sys.exit()

if __name__ == "__main__":
    main()

#!/bin/bash

# အရောင်သတ်မှတ်ချက်များ (UI လှပစေရန်)
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}==========================================${NC}"
echo -e "${GREEN}      SMNS TOOL AUTO-INSTALLER          ${NC}"
echo -e "${CYAN}==========================================${NC}"

# ၁။ Package များ Update ပြုလုပ်ခြင်း
echo -e "${GREEN}[+] Updating system packages...${NC}"
pkg update -y && pkg upgrade -y

# ၂။ လိုအပ်သော Tools များ သွင်းခြင်း
echo -e "${GREEN}[+] Installing Python and Git...${NC}"
pkg install python git -y

# ၃။ Python Library (Requests) သွင်းခြင်း
echo -e "${GREEN}[+] Installing required python libraries...${NC}"
pip install requests

# ၄။ Folder ဟောင်းရှိလျှင် ဖျက်ထုတ်ခြင်း
if [ -d "lkhant" ]; then
    echo -e "${CYAN}[!] Removing old version...${NC}"
    rm -rf lkhant
fi

# ၅။ Repository ကို Clone ဆွဲခြင်း
echo -e "${GREEN}[+] Downloading tool files from GitHub...${NC}"
# အကို့ Repo က Public ဖြစ်နေဖို့ လိုပါတယ်
git clone https://github.com/smns94/lkhant.git

# ၆။ Tool ကို စတင် Run ခြင်း
if [ -d "lkhant" ]; then
    cd lkhant
    echo -e "${GREEN}[+] Installation Success! Starting SMNS Tool...${NC}"
    echo -e "${CYAN}------------------------------------------${NC}"
    python3 run.py
else
    echo -e "${RED}[-] Error: Download failed. Please check your internet!${NC}"
fi

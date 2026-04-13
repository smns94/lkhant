import hashlib
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# မူရင်း salt အမှန်
SECRET_SALT = "ohmygod@123"

# Bot Token ကို BotFather ဆီကယူပြီး နေရာမှာ အစားထိုးပါ
TOKEN = "8669797151:AAFwU46t3CHkqfcvLt0iOyfDRErCkXoBRmw"

def generate_key(device_id, expiry):
    raw = f"{device_id}{expiry}{SECRET_SALT}"
    auth_hash = hashlib.sha256(raw.encode()).hexdigest()
    return f"{auth_hash[:12].upper()}{expiry}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to SMNS KeyGen Bot!\n\n"
        "Key ထုတ်ရန်: /gen [Device_ID] [Expiry]\n"
        "ဥပမာ: /gen TRB-12345 202612312359"
    )

async def gen_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Command ရဲ့ argument များကို ယူခြင်း
        did = context.args[0]
        exp = context.args[1]
        
        # Key ထုတ်ခြင်း
        final_key = generate_key(did, exp)
        
        response = (
            f"✅ *Key Generated Successfully!*\n\n"
            f"🆔 *Device ID:* `{did}`\n"
            f"📅 *Expiry:* `{exp}`\n"
            f"🔑 *Activation Key:* `{final_key}`"
        )
        await update.message.reply_text(response, parse_mode="Markdown")
        
    except (IndexError, ValueError):
        await update.message.reply_text("❌ အသုံးပြုပုံမှားနေပါသည်။\nဥပမာ: `/gen TRB-12345 202612312359`", parse_mode="Markdown")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen_key))
    
    print("[+] Bot is running...")
    app.run_polling()

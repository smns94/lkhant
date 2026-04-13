import hashlib
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

SECRET_SALT = "ohmygod@123"
TOKEN = "8105499487:AAHXrV-jMr1S9NPEuj35fbUhtbb6V3k6b54"
ADMIN_ID = 7731566362

def generate_key(device_id, expiry):
    raw = f"{device_id}{expiry}{SECRET_SALT}"
    auth_hash = hashlib.sha256(raw.encode()).hexdigest()
    return f"{auth_hash[:12].upper()}{expiry}"

async def gen_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Admin Only!")
        return
    try:
        did = context.args[0]
        exp = context.args[1]
        final_key = generate_key(did, exp)
        await update.message.reply_text(f"🔑 Key: `{final_key}`", parse_mode="Markdown")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /gen [ID] [EXP]")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("gen", gen_key))
    print("[+] Bot is running...")
    app.run_polling()

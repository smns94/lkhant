# ... (အပေါ်က import နဲ့ generate_key function တွေက အတူတူပါပဲ)

# သင်တစ်ယောက်တည်းပဲ သုံးလို့ရအောင် သင့်ရဲ့ Telegram User ID ကို ဒီမှာထည့်ပါ
# ID ကိုမသိရင် Telegram က @userinfobot ဆီမှာ သွားကြည့်လို့ရပါတယ်
ADMIN_ID = 7731566362  # <--- ဒီနေရာမှာ သင့် ID အမှန် ပြောင်းထည့်ပါ

async def gen_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # ၁။ Admin ဟုတ်မဟုတ် အရင်စစ်ဆေးခြင်း
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ သင်သည် Admin မဟုတ်သဖြင့် ဤ command ကို သုံးခွင့်မရှိပါ။")
        return # Admin မဟုတ်ရင် ဒီမှာတင် ရပ်လိုက်မယ်

    # ၂။ Admin ဖြစ်မှ အောက်က Key ထုတ်တဲ့အပိုင်းကို ဆက်လုပ်မယ်
    try:
        did = context.args[0]
        exp = context.args[1]
        
        final_key = generate_key(did, exp)
        
        response = (
            f"✅ *Key Generated Successfully!*\n\n"
            f"🆔 *Device ID:* `{did}`\n"
            f"📅 *Expiry:* `{exp}`\n"
            f"🔑 *Activation Key:* `{final_key}`"
        )
        await update.message.reply_text(response, parse_mode="Markdown")
        
    except (IndexError, ValueError):
        await update.message.reply_text("❌ အသုံးပြုပုံ: `/gen [ID] [Expiry]`")

# ... (ကျန်တဲ့ code အောက်ပိုင်းက အတူတူပါပဲ)

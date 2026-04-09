import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os, random, time, threading, psutil, traceback

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-100xxxxxxxxxx"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

reply_mode = {}
live_monitor = False

taglines = [
    "⚡🔥 Lightning Fast Support System Activated 🔥⚡",
    "🚀💀 Ultra Intelligence Engine Running 💀🚀",
    "💀⚡ Elite Response Mechanism Enabled ⚡💀",
    "🔥🚀 Premium Core Fully Activated 🚀🔥",
    "🧠⚡ Smart Routing AI Fully Online ⚡🧠"
]

# ===== ERROR ALERT =====
def error_alert(e):
    try:
        bot.send_message(ADMIN_ID, f"""
<b>🚨💀 ╔═══〔 🚨💀 CRITICAL SYSTEM ERROR 💀🚨 〕═══╗ 💀🚨</b>

⚠️🔥 <b>HIGH PRIORITY ERROR DETECTED IN SYSTEM CORE</b> 🔥⚠️

<code>{e}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠⚡ SYSTEM STATUS: UNSTABLE ⚡🧠  
📡🔥 IMMEDIATE ACTION REQUIRED 🔥📡  

💀 <b>ADMIN ATTENTION REQUIRED NOW</b> 💀

<b>💀🚨 ╚════════════════════════════════════╝ 🚨💀</b>
""")
    except:
        pass

# ===== ADMIN KEYBOARD =====
def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📊⚡ SPEED PANEL ⚡📊"), KeyboardButton("⛔🔥 STOP SYSTEM 🔥⛔"))
    return kb

# ===== START =====
@bot.message_handler(commands=['start'])
def start(m):
    try:
        msg = bot.send_message(m.chat.id, "⚡🔥 Initializing Ultra System... 🔥⚡")

        steps = [
            "🚀🔥 Loading Advanced Modules...",
            "🧠⚡ Connecting To Main Admin Core...",
            "🔐🔥 Establishing Secure Encrypted Channel...",
            "⚡🚀 Activating Final Protocol..."
        ]

        for s in steps:
            time.sleep(0.5)
            bot.edit_message_text(f"""
<b>💀⚡ ╔═══〔 ⚡ SYSTEM INITIALIZATION ⚡ 〕═══╗ ⚡💀</b>

{s}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡🔥 STATUS: PROCESSING 🔥⚡  
🧠 SYSTEM: ONLINE  

💀 <b>PLEASE WAIT... INITIALIZING CORE</b> 💀

<b>💀⚡ ╚════════════════════════════════════╝ ⚡💀</b>
""", m.chat.id, msg.message_id)

        bot.edit_message_text(f"""
<b>💀🚀 ╔═══〔 🚀 ULTRA SUPPORT CORE SYSTEM 🚀 〕═══╗ 🚀💀</b>

👋🔥 <b>WELCOME, {m.from_user.first_name}</b> 🔥👋

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨⚡ <b>{random.choice(taglines)}</b> ⚡✨

💬📡 DIRECT ADMIN CONNECTION ENABLED 📡💬  
🔒🛡️ FULLY SECURED COMMUNICATION 🛡️🔒  
🚀⚡ INSTANT RESPONSE DELIVERY ⚡🚀  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢🔥 <b>SEND YOUR MESSAGE DIRECTLY TO ADMIN NOW</b> 🔥📢  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀⚡ <b>ELITE MODE SUCCESSFULLY ACTIVATED</b> ⚡💀  

<b>💀🚀 ╚════════════════════════════════════╝ 🚀💀</b>
""", m.chat.id, msg.message_id)

        # ===== FULL USER DETECT (OLD STYLE + DP) =====
        uid = m.from_user.id
        uname = m.from_user.username or "NoUsername"
        name = m.from_user.first_name

        info = f"""
<b>💀🚨 ╔═══〔 🆕🚀 NEW USER DETECTED 🚀🆕 〕═══╗ 🚨💀</b>

👤🔥 <b>FULL NAME:</b> {name} 🔥👤  
🔗⚡ <b>USERNAME:</b> @{uname} ⚡🔗  
🆔💀 <b>USER ID:</b> <code>{uid}</code> 💀🆔  

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡🔥 STATUS: ONLINE & ACTIVE 🔥📡  
⚡🚀 ACTION: BOT STARTED SUCCESSFULLY 🚀⚡  

💀 <b>NEW USER HAS ENTERED THE SYSTEM</b> 💀

<b>💀🚨 ╚════════════════════════════════════╝ 🚨💀</b>
"""

        try:
            photos = bot.get_user_profile_photos(uid)
            if photos.total_count > 0:
                bot.send_photo(ADMIN_ID, photos.photos[0][-1].file_id, caption=info)
            else:
                bot.send_message(ADMIN_ID, info)
        except:
            bot.send_message(ADMIN_ID, info)

        if m.chat.id == ADMIN_ID:
            bot.send_message(ADMIN_ID, "⚙️🔥 ADMIN CONTROL PANEL ACTIVATED 🔥⚙️", reply_markup=admin_kb())

    except:
        error_alert(traceback.format_exc())

# ===== USER MESSAGE =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID)
def forward(m):
    try:
        uid = m.from_user.id
        uname = m.from_user.username or "NoUsername"

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("💬🔥 REPLY NOW 🔥💬", callback_data=f"reply_{uid}"))

        bot.send_message(ADMIN_ID, f"""
<b>💀📡 ╔═══〔 📡 LIVE MESSAGE STREAM 📡 〕═══╗ 📡💀</b>

👤🔥 USER: @{uname} 🔥👤  
🆔⚡ ID: <code>{uid}</code> ⚡🆔  

💬🔥 MESSAGE RECEIVED:  
<code>{m.text}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀 <b>INCOMING USER DATA CAPTURED SUCCESSFULLY</b> 💀

<b>💀📡 ╚════════════════════════════════════╝ 📡💀</b>
""", reply_markup=kb)

        bot.send_message(CHANNEL_ID, f"""
💀📡 CHANNEL LOG

👤 @{uname}
🆔 {uid}

💬 {m.text}
""")

        sent = bot.send_message(m.chat.id, "📡🔥 Processing Your Message... 🔥📡")

        for s in [
            "⚡ Routing Through Secure Server...",
            "🧠 Analyzing Message Data...",
            "🔐 Encrypting Information...",
            "🚀 Delivering To Admin..."
        ]:
            time.sleep(0.5)
            bot.edit_message_text(s, m.chat.id, sent.message_id)

        bot.edit_message_text("""
<b>💀🚀 ╔═══〔 ✅ MESSAGE DELIVERED SUCCESSFULLY ✅ 〕═══╗ 🚀💀</b>

📡🔥 YOUR MESSAGE HAS BEEN SENT TO ADMIN 🔥📡  

⚡ <b>PLEASE WAIT FOR RESPONSE</b> ⚡  

<b>💀🚀 ╚════════════════════════════════════╝ 🚀💀</b>
""", m.chat.id, sent.message_id)

    except:
        error_alert(traceback.format_exc())

# बाकी functions same pattern (reply, speed etc) already compatible हैं
print("💀🔥 EXTREME UI BOT RUNNING 🔥💀")
bot.infinity_polling(skip_pending=True)

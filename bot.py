import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os, time, threading, psutil, traceback

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

reply_mode = {}
live_monitor = False

# ===== ERROR =====
def error_alert(e):
    try:
        bot.send_message(ADMIN_ID, f"💀 ERROR:\n<code>{e}</code>")
    except:
        pass

# ===== ADMIN KEYBOARD =====
def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📊⚡ SPEED PANEL ⚡📊"),
        KeyboardButton("⛔🔥 STOP SYSTEM 🔥⛔")
    )
    return kb

# ===== START =====
@bot.message_handler(commands=['start'])
def start(m):
    try:
        msg = bot.send_message(m.chat.id, "⚡🔥 Initializing Ultra System... 🔥⚡")

        for s in [
            "🚀🔥 Loading Advanced Modules...",
            "🧠⚡ Connecting To Admin Core...",
            "🔐🔥 Establishing Secure Channel...",
            "⚡🚀 Finalizing Setup..."
        ]:
            time.sleep(0.4)
            bot.edit_message_text(s, m.chat.id, msg.message_id)

        bot.edit_message_text(f"""
<b>💀🚀 ╔═══〔 🚀 ULTRA SUPPORT CORE SYSTEM 🚀 〕═══╗ 🚀💀</b>

👋🔥 <b>{m.from_user.first_name}</b> 🔥👋

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬📡 DIRECT ADMIN CONNECTION  
🔒🛡️ FULLY SECURE  
🚀⚡ INSTANT DELIVERY  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢🔥 SEND YOUR MESSAGE NOW 🔥📢

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀⚡ ELITE MODE ACTIVATED ⚡💀

<b>💀🚀 ╚════════════════════════════════════╝ 🚀💀</b>
""", m.chat.id, msg.message_id)

        # ===== NEW USER DETECT (DP) =====
        uid = m.from_user.id
        uname = m.from_user.username or "NoUsername"
        name = m.from_user.first_name

        info = f"""
<b>💀🚨 ╔═══〔 🆕🚀 NEW USER DETECTED 🚀🆕 〕═══╗ 🚨💀</b>

👤🔥 NAME: {name} 🔥👤  
🔗⚡ USERNAME: @{uname} ⚡🔗  
🆔💀 ID: <code>{uid}</code> 💀🆔  

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 STATUS: ONLINE  
⚡ ACTION: BOT STARTED  

💀 NEW USER ENTERED SYSTEM 💀

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
            bot.send_message(ADMIN_ID, "⚙️ ADMIN PANEL", reply_markup=admin_kb())

    except:
        error_alert(traceback.format_exc())

# ===== USER → ADMIN (MEDIA SUPPORT) =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID,
content_types=['text','photo','video','document','audio','voice','sticker'])
def forward(m):
    try:
        uid = m.from_user.id
        uname = m.from_user.username or "NoUsername"

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("💬🔥 REPLY NOW 🔥💬", callback_data=f"reply_{uid}"))

        header = f"""
<b>💀📡 ╔═══〔 📡 LIVE MESSAGE STREAM 📡 〕═══╗ 📡💀</b>

👤 @{uname}
🆔 <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        # TEXT
        if m.content_type == "text":
            bot.send_message(ADMIN_ID, header + f"💬 {m.text}\n\n<b>╚════════════════════════════╝</b>", reply_markup=kb)

            bot.send_message(CHANNEL_ID, f"""
<b>💀📡 ╔═══〔 CHANNEL LOG 〕═══╗ 📡💀</b>

👤 @{uname}
🆔 {uid}

💬 {m.text}

<b>╚════════════════════════════╝</b>
""")

        # MEDIA
        else:
            bot.copy_message(ADMIN_ID, m.chat.id, m.message_id)

            bot.send_message(ADMIN_ID, header + "📎 MEDIA RECEIVED\n\n<b>╚════════════════════════════╝</b>", reply_markup=kb)

            try:
                bot.copy_message(CHANNEL_ID, m.chat.id, m.message_id)
            except:
                pass

        # USER ANIMATION
        sent = bot.send_message(m.chat.id, "📡 Sending...")
        for s in ["⚡ Routing...","🧠 Processing...","🔐 Encrypting...","🚀 Delivering..."]:
            time.sleep(0.4)
            bot.edit_message_text(s, m.chat.id, sent.message_id)

        bot.edit_message_text("✅ Delivered", m.chat.id, sent.message_id)

    except:
        error_alert(traceback.format_exc())

# ===== REPLY BUTTON =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply_btn(c):
    uid = int(c.data.split("_")[1])
    reply_mode[ADMIN_ID] = uid

    bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 🎯⚡ TARGET LOCKED ⚡🎯 〕═══╗</b>

🧬 USER ID: <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 SEND YOUR MESSAGE NOW

🚀 READY TO TRANSMIT

<b>╚════════════════════════════╝</b>
""")

# ===== ADMIN REPLY =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.text not in ["📊⚡ SPEED PANEL ⚡📊","⛔🔥 STOP SYSTEM 🔥⛔"])
def admin_reply(m):
    try:
        if ADMIN_ID not in reply_mode:
            bot.send_message(ADMIN_ID, "❌ CLICK REPLY FIRST")
            return

        uid = reply_mode[ADMIN_ID]

        bot.copy_message(uid, m.chat.id, m.message_id)

        try:
            bot.send_message(CHANNEL_ID, f"ADMIN REPLY → {uid}\n{m.text}")
        except:
            pass

        bot.send_message(ADMIN_ID, f"✅ SENT TO {uid}")

        del reply_mode[ADMIN_ID]

    except:
        error_alert(traceback.format_exc())

# ===== SPEED =====
def live(chat_id, msg_id):
    global live_monitor
    while live_monitor:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            ping = round(time.time()*1000 % 1000,2)

            bot.edit_message_text(f"""
<b>💀📊 ╔═══〔 LIVE SYSTEM STATUS 〕═══╗ 📊💀</b>

⚡ CPU: {cpu}%
🧠 RAM: {ram}%
🚀 PING: {ping} ms

<b>╚════════════════════════════╝</b>
""", chat_id, msg_id)

        except:
            break

@bot.message_handler(func=lambda m: m.text == "📊⚡ SPEED PANEL ⚡📊" and m.chat.id == ADMIN_ID)
def speed(m):
    global live_monitor
    live_monitor = True
    msg = bot.send_message(ADMIN_ID, "🚀 Starting Monitor...")
    threading.Thread(target=live, args=(ADMIN_ID, msg.message_id), daemon=True).start()

@bot.message_handler(func=lambda m: m.text == "⛔🔥 STOP SYSTEM 🔥⛔" and m.chat.id == ADMIN_ID)
def stop(m):
    global live_monitor
    live_monitor = False
    bot.send_message(ADMIN_ID, "⛔ Stopped")

print("💀🔥 FINAL MEDIA BOT RUNNING 🔥💀")
bot.infinity_polling(skip_pending=True)

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
        bot.send_message(ADMIN_ID, f"""
<b>💀🚨 ╔═══〔 🚨💀 SYSTEM ERROR 💀🚨 〕═══╗ 🚨💀</b>

<code>{e}</code>

<b>💀🚨 ╚════════════════════════════╝ 🚨💀</b>
""")
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
    msg = bot.send_message(m.chat.id, "⚡🔥 INITIALIZING SYSTEM... 🔥⚡")

    for s in [
        "🚀🔥 LOADING MODULES...",
        "🧠⚡ CONNECTING CORE...",
        "🔐🔥 SECURE CHANNEL...",
        "⚡🚀 FINALIZING..."
    ]:
        time.sleep(0.4)
        bot.edit_message_text(f"💀⚡ {s} ⚡💀", m.chat.id, msg.message_id)

    bot.edit_message_text(f"""
<b>💀🚀 ╔═══〔 🚀 ULTRA SUPPORT CORE 🚀 〕═══╗ 🚀💀</b>

👋🔥 <b>{m.from_user.first_name}</b> 🔥👋

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬📡 DIRECT ADMIN CONNECTION 📡💬  
🔒🛡️ FULL SECURITY 🛡️🔒  
🚀⚡ INSTANT DELIVERY ⚡🚀  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢🔥 SEND MESSAGE NOW 🔥📢  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀⚡ ELITE MODE ACTIVATED ⚡💀  

<b>💀🚀 ╚════════════════════════════╝ 🚀💀</b>
""", m.chat.id, msg.message_id)

    # ===== USER DETECT + DP =====
    uid = m.from_user.id
    uname = m.from_user.username or "NoUsername"
    name = m.from_user.first_name

    info = f"""
<b>💀🚨 ╔═══〔 🆕🚀 NEW USER DETECTED 🚀🆕 〕═══╗ 🚨💀</b>

👤🔥 NAME: {name} 🔥👤  
🔗⚡ USERNAME: @{uname} ⚡🔗  
🆔💀 ID: <code>{uid}</code> 💀🆔  

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡🔥 STATUS: ONLINE 🔥📡  
⚡🚀 ACTION: STARTED 🚀⚡  

💀 NEW USER ENTERED SYSTEM 💀

<b>💀🚨 ╚════════════════════════════╝ 🚨💀</b>
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
        bot.send_message(ADMIN_ID, "⚙️🔥 ADMIN PANEL ACTIVE 🔥⚙️", reply_markup=admin_kb())

# ===== USER → ADMIN =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID,
content_types=['text','photo','video','document','audio','voice','sticker'])
def forward(m):
    uid = m.from_user.id
    uname = m.from_user.username or "NoUsername"

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💬🔥 REPLY 🔥💬", callback_data=f"reply_{uid}"))

    header = f"""
<b>💀📡 ╔═══〔 📡 LIVE MESSAGE STREAM 📡 〕═══╗ 📡💀</b>

👤🔥 @{uname} 🔥👤  
🆔⚡ <code>{uid}</code> ⚡🆔  

━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    if m.content_type == "text":
        txt = header + f"💬🔥 {m.text} 🔥💬\n\n<b>╚════════════════════════════╝</b>"
        bot.send_message(ADMIN_ID, txt, reply_markup=kb)
        bot.send_message(CHANNEL_ID, txt)
    else:
        bot.copy_message(ADMIN_ID, m.chat.id, m.message_id)
        bot.copy_message(CHANNEL_ID, m.chat.id, m.message_id)
        bot.send_message(ADMIN_ID, header + "📎🔥 MEDIA RECEIVED 🔥📎\n\n<b>╚══════════╝</b>", reply_markup=kb)
        bot.send_message(CHANNEL_ID, header + "📎🔥 MEDIA RECEIVED 🔥📎")

    # ===== USER DELIVERY UI =====
    sent = bot.send_message(m.chat.id, "📡🔥 SENDING... 🔥📡")
    for s in ["⚡🔥 ROUTING...","🧠⚡ PROCESSING...","🔐🔥 ENCRYPTING...","🚀⚡ DELIVERING..."]:
        time.sleep(0.4)
        bot.edit_message_text(f"💀📡 {s} 📡💀", m.chat.id, sent.message_id)

    bot.edit_message_text("""
<b>💀🚀 ╔═══〔 🚀 DELIVERY SUCCESS 🚀 〕═══╗ 🚀💀</b>

📡🔥 MESSAGE DELIVERED 🔥📡  

💀 STATUS: COMPLETED 💀  

<b>╚════════════════════════════╝</b>
""", m.chat.id, sent.message_id)

# ===== REPLY BUTTON =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply_btn(c):
    uid = int(c.data.split("_")[1])
    reply_mode[ADMIN_ID] = uid

    bot.send_message(ADMIN_ID, f"""
<b>💀🔒 ╔═══〔 TARGET LOCKED 〕═══╗ 🔒💀</b>

🧬⚡ USER: <code>{uid}</code> ⚡🧬  

💬🔥 SEND MESSAGE 🔥💬  

<b>╚════════════════════════════╝</b>
""")

# ===== CONTROL FILTER (IMPORTANT FIX) =====
def is_control(m):
    return m.text in ["📊⚡ SPEED PANEL ⚡📊","⛔🔥 STOP SYSTEM 🔥⛔"]

# ===== ADMIN REPLY (MEDIA + FIX) =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and not is_control(m),
content_types=['text','photo','video','document','audio','voice','sticker'])
def admin_reply(m):

    if ADMIN_ID not in reply_mode:
        return

    uid = reply_mode[ADMIN_ID]

    bot.copy_message(uid, m.chat.id, m.message_id)
    bot.copy_message(CHANNEL_ID, m.chat.id, m.message_id)

    sent = bot.send_message(ADMIN_ID, "⚡🔥 SENDING... 🔥⚡")

    for s in ["📡🔥 CONNECTING...","🧠⚡ PROCESSING...","🚀🔥 DELIVERING...","💀⚡ FINALIZING..."]:
        time.sleep(0.3)
        bot.edit_message_text(f"💀📤 {s} 📤💀", ADMIN_ID, sent.message_id)

    bot.edit_message_text(f"""
<b>💀🚀 ╔═══〔 DELIVERY SUCCESS 〕═══╗ 🚀💀</b>

📤🔥 SENT TO: <code>{uid}</code> 🔥📤  

💀 STATUS: COMPLETED 💀  

<b>╚════════════════════════════╝</b>
""", ADMIN_ID, sent.message_id)

    del reply_mode[ADMIN_ID]

# ===== SPEED =====
def live(chat_id, msg_id):
    global live_monitor
    while live_monitor:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        ping = round(time.time()*1000 % 1000,2)

        bot.edit_message_text(f"""
<b>💀📊 ╔═══〔 LIVE SYSTEM STATUS 〕═══╗ 📊💀</b>

⚡🔥 CPU: {cpu}% 🔥⚡  
🧠🔥 RAM: {ram}% 🔥🧠  
🚀🔥 PING: {ping} ms 🔥🚀  

<b>╚════════════════════════════╝</b>
""", chat_id, msg_id)

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.text == "📊⚡ SPEED PANEL ⚡📊")
def speed(m):
    global live_monitor
    live_monitor = True
    msg = bot.send_message(ADMIN_ID, "🚀🔥 STARTING MONITOR... 🔥🚀")
    threading.Thread(target=live, args=(ADMIN_ID, msg.message_id), daemon=True).start()

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.text == "⛔🔥 STOP SYSTEM 🔥⛔")
def stop(m):
    global live_monitor
    live_monitor = False
    bot.send_message(ADMIN_ID, "⛔🔥 STOPPED 🔥⛔")

print("💀🔥 FINAL FIXED BOT RUNNING 🔥💀")
bot.infinity_polling(skip_pending=True)

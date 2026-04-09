import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os, random, time, threading, psutil, traceback

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-100xxxxxxxxxx"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

reply_mode = {}
live_monitor = False

# ===== ADMIN KEYBOARD =====
def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📊⚡ SPEED PANEL ⚡📊"), KeyboardButton("⛔🔥 STOP SYSTEM 🔥⛔"))
    return kb

# ===== ERROR =====
def error_alert(e):
    try:
        bot.send_message(ADMIN_ID, f"<code>{e}</code>")
    except:
        pass

# ===== START =====
@bot.message_handler(commands=['start'])
def start(m):
    msg = bot.send_message(m.chat.id, "⚡🔥 Initializing Ultra System... 🔥⚡")

    for s in [
        "🚀🔥 Loading Advanced Modules...",
        "🧠⚡ Connecting To Main Admin Core...",
        "🔐🔥 Establishing Secure Channel...",
        "⚡🚀 Finalizing..."
    ]:
        time.sleep(0.4)
        bot.edit_message_text(s, m.chat.id, msg.message_id)

    bot.edit_message_text(f"""
<b>💀🚀 ╔═══〔 🚀 ULTRA SUPPORT CORE SYSTEM 🚀 〕═══╗ 🚀💀</b>

👋🔥 <b>{m.from_user.first_name}</b> 🔥👋

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬📡 DIRECT ADMIN CONNECTION  
🔒🛡️ SECURE  
🚀⚡ FAST DELIVERY  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢🔥 SEND MESSAGE 🔥📢

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀 ELITE MODE ACTIVE 💀

<b>💀🚀 ╚════════════════════════════════════╝ 🚀💀</b>
""", m.chat.id, msg.message_id)

    # ADMIN PANEL
    if m.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "⚙️ ADMIN PANEL", reply_markup=admin_kb())

# ===== USER → ADMIN =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID)
def forward(m):
    uid = m.from_user.id
    uname = m.from_user.username or "NoUsername"

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💬🔥 REPLY NOW 🔥💬", callback_data=f"reply_{uid}"))

    bot.send_message(ADMIN_ID, f"""
<b>💀📡 ╔═══〔 📡 LIVE MESSAGE STREAM 📡 〕═══╗ 📡💀</b>

👤 @{uname}
🆔 <code>{uid}</code>

💬 {m.text}

<b>╚════════════════════════════════════╝</b>
""", reply_markup=kb)

    # ===== USER ANIMATION =====
    sent = bot.send_message(m.chat.id, "📡 Sending...")

    for s in ["⚡ Routing...","🧠 Processing...","🔐 Encrypting...","🚀 Delivering..."]:
        time.sleep(0.4)
        bot.edit_message_text(s, m.chat.id, sent.message_id)

    bot.edit_message_text("✅ Delivered", m.chat.id, sent.message_id)

# ===== REPLY BUTTON FIX =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply_btn(c):
    uid = int(c.data.split("_")[1])

    # 🔥 FIX: store properly
    reply_mode[ADMIN_ID] = uid

    bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 🎯⚡ TARGET LOCKED ⚡🎯 〕═══╗</b>

🧬 USER ID: <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 SEND YOUR MESSAGE NOW

🚀 READY TO TRANSMIT

<b>╚════════════════════════════╝</b>
""")

# ===== ADMIN REPLY FIX =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID)
def admin_reply(m):
    try:
        # ignore control buttons
        if m.text in ["📊⚡ SPEED PANEL ⚡📊","⛔🔥 STOP SYSTEM 🔥⛔"]:
            return

        if ADMIN_ID not in reply_mode:
            bot.send_message(ADMIN_ID, "❌ FIRST CLICK REPLY BUTTON")
            return

        uid = reply_mode[ADMIN_ID]

        # 🔥 FIX: copy message correctly
        bot.copy_message(uid, m.chat.id, m.message_id)

        bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 🚀 DELIVERY SUCCESS 🚀 〕═══╗</b>

📤 SENT TO: <code>{uid}</code>

<b>╚════════════════════════════╝</b>
""")

        del reply_mode[ADMIN_ID]

    except:
        error_alert(traceback.format_exc())

# ===== SPEED FIX =====
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
    msg = bot.send_message(ADMIN_ID, "🚀 Starting Live Monitor...")
    threading.Thread(target=live, args=(ADMIN_ID, msg.message_id), daemon=True).start()

@bot.message_handler(func=lambda m: m.text == "⛔🔥 STOP SYSTEM 🔥⛔" and m.chat.id == ADMIN_ID)
def stop(m):
    global live_monitor
    live_monitor = False
    bot.send_message(ADMIN_ID, "⛔ Stopped")

print("💀🔥 FIXED BOT RUNNING 🔥💀")
bot.infinity_polling(skip_pending=True)

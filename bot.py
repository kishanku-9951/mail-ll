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
    "⚡ Lightning Fast Support",
    "🚀 Powered by Intelligence",
    "💀 Elite Response System",
    "🔥 Premium Support Activated",
    "🧠 Smart AI Routing Enabled"
]

# ===== ERROR ALERT =====
def error_alert(e):
    try:
        bot.send_message(ADMIN_ID, f"""
<b>💀🚨 ╔═══〔 SYSTEM ERROR 〕═══╗ 🚨💀</b>

<code>{e}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ System Issue Detected

<b>╚════════════════════════════╝</b>
""")
    except:
        pass

# ===== ADMIN KEYBOARD =====
def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📊 SPEED"), KeyboardButton("⛔ STOP"))
    return kb

# ===== START =====
@bot.message_handler(commands=['start'])
def start(m):
    try:
        msg = bot.send_message(m.chat.id, "⚡ Initializing system...")

        steps = [
            "🚀 Loading modules...",
            "🧠 Connecting to admin core...",
            "🔐 Establishing secure channel...",
            "⚡ Finalizing setup..."
        ]

        for s in steps:
            time.sleep(0.4)
            bot.edit_message_text(f"""
<b>💀⚡ SYSTEM START ⚡💀</b>

{s}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Processing...

<b>╚══════════════════════╝</b>
""", m.chat.id, msg.message_id)

        bot.edit_message_text(f"""
<b>╔═══〔 🚀 ULTRA SUPPORT CORE 🚀 〕═══╗</b>

👋 <b>{m.from_user.first_name}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ <b>{random.choice(taglines)}</b>

💬 Direct Admin Connection  
🔒 Secure  
🚀 Instant Delivery  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢 SEND MESSAGE TO ADMIN

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀 ELITE MODE ACTIVATED

<b>╚════════════════════════════╝</b>
""", m.chat.id, msg.message_id)

        uid = m.from_user.id
        uname = m.from_user.username or "NoUsername"

        bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 NEW USER 〕═══╗</b>

👤 @{uname}
🆔 <code>{uid}</code>

<b>╚══════════════════╝</b>
""")

        if m.chat.id == ADMIN_ID:
            bot.send_message(ADMIN_ID, "⚙️ ADMIN PANEL", reply_markup=admin_kb())

    except:
        error_alert(traceback.format_exc())

# ===== USER → ADMIN =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID)
def forward(m):
    try:
        uid = m.from_user.id
        uname = m.from_user.username or "NoUsername"

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("💬 REPLY", callback_data=f"reply_{uid}"))

        bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 LIVE MESSAGE 〕═══╗</b>

👤 @{uname}
🆔 <code>{uid}</code>

💬 {m.text}

<b>╚══════════════════════╝</b>
""", reply_markup=kb)

        bot.send_message(CHANNEL_ID, f"""
<b>╔═══〔 CHANNEL LOG 〕═══╗</b>

👤 @{uname}
🆔 <code>{uid}</code>

💬 {m.text}

<b>╚══════════════════════╝</b>
""")

        sent = bot.send_message(m.chat.id, "📡 Sending...")

        for s in ["⚡ Routing...","🧠 Processing...","🔐 Encrypting...","🚀 Delivering..."]:
            time.sleep(0.4)
            bot.edit_message_text(f"""
<b>💀📡 TRANSMISSION STATUS 📡💀</b>

{s}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>╚══════════════════════╝</b>
""", m.chat.id, sent.message_id)

        bot.edit_message_text("""
<b>╔═══〔 SUCCESS 〕═══╗</b>

📡 Delivered

<b>╚══════════════════╝</b>
""", m.chat.id, sent.message_id)

    except:
        error_alert(traceback.format_exc())

# ===== REPLY =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply_btn(c):
    uid = int(c.data.split("_")[1])
    reply_mode[ADMIN_ID] = uid

    bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 TARGET LOCKED 〕═══╗</b>

USER: <code>{uid}</code>

Send reply

<b>╚══════════════════════╝</b>
""")

# ===== ADMIN REPLY =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID)
def admin_reply(m):
    try:
        if m.text in ["📊 SPEED","⛔ STOP"]:
            return

        if ADMIN_ID not in reply_mode:
            bot.send_message(ADMIN_ID, "❌ Use reply button")
            return

        uid = reply_mode[ADMIN_ID]

        bot.send_message(uid, m.text)

        bot.send_message(CHANNEL_ID, f"""
<b>╔═══〔 ADMIN REPLY 〕═══╗</b>

TO: <code>{uid}</code>

💬 {m.text}

<b>╚══════════════════════╝</b>
""")

        sent = bot.send_message(ADMIN_ID, "⚡ Sending...")
        for s in ["📡 Delivering...","🧠 Confirming..."]:
            time.sleep(0.3)
            bot.edit_message_text(s, ADMIN_ID, sent.message_id)

        bot.edit_message_text(f"""
<b>╔═══〔 DELIVERY SUCCESS 〕═══╗</b>

TO: <code>{uid}</code>

<b>╚══════════════════════╝</b>
""", ADMIN_ID, sent.message_id)

        del reply_mode[ADMIN_ID]

    except:
        error_alert(traceback.format_exc())

# ===== LIVE SPEED =====
def live(chat_id, msg_id):
    global live_monitor
    while live_monitor:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            ping = round(time.time()*1000 % 1000,2)

            bot.edit_message_text(f"""
<b>╔═══〔 LIVE SYSTEM 〕═══╗</b>

⚡ CPU: {cpu}%
🧠 RAM: {ram}%
🚀 PING: {ping} ms

<b>╚══════════════════════╝</b>
""", chat_id, msg_id)

            time.sleep(2)
        except:
            error_alert(traceback.format_exc())
            break

@bot.message_handler(func=lambda m: m.text == "📊 SPEED" and m.chat.id == ADMIN_ID)
def speed(m):
    global live_monitor
    live_monitor = True
    msg = bot.send_message(ADMIN_ID, "🚀 Starting Monitor...")
    threading.Thread(target=live, args=(ADMIN_ID, msg.message_id), daemon=True).start()

@bot.message_handler(func=lambda m: m.text == "⛔ STOP" and m.chat.id == ADMIN_ID)
def stop(m):
    global live_monitor
    live_monitor = False
    bot.send_message(ADMIN_ID, "⛔ Monitoring Stopped")

print("💀🔥 CLEAN BOX BOT RUNNING 🔥💀")
bot.infinity_polling(skip_pending=True)

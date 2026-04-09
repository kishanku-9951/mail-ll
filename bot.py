import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os, random, time, threading, psutil

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-100xxxxxxxxxx"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

reply_mode = {}
live_monitor = False

# ===== GLITCH =====
def glitch(text):
    chars = ["▓","▒","░","█","▄","▌","▐"]
    return "".join(random.choice(chars) if random.random()<0.12 else c for c in text)

# ===== MATRIX =====
def matrix():
    return "".join(random.choice("01▓▒░█") for _ in range(25))

# ===== ADMIN KEYBOARD =====
def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📊 SPEED"), KeyboardButton("⛔ STOP"))
    return kb

# ===== START =====
@bot.message_handler(commands=['start'])
def start(m):
    msg = bot.send_message(m.chat.id, glitch("⚡ Initializing system...")+"\n"+matrix())

    for s in ["🚀 Loading modules...","🧠 Connecting core...","💀 Activating system..."]:
        time.sleep(0.4)
        bot.edit_message_text(glitch(s)+"\n"+matrix(), m.chat.id, msg.message_id)

    bot.edit_message_text(f"""
<b>💀🚀 ╔═══〔 🚀 ULTRA SUPPORT CORE 🚀 〕═══╗ 🚀💀</b>

👋 <b>Welcome, {m.from_user.first_name}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ <b>⚡ Lightning Fast Support</b>

💬 📡 Direct Admin Connection  
🔒 🛡️ Secure  
🚀 ⚡ Instant Delivery  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢🔥 <b>SEND MESSAGE</b> 🔥📢

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀 ELITE MODE ACTIVATED ⚡

<b>💀🚀 ╚════════════════════════════╝ 🚀💀</b>
""", m.chat.id, msg.message_id)

    uid = m.from_user.id
    uname = m.from_user.username or "NoUsername"

    bot.send_message(ADMIN_ID, f"""
💀🚀 ╔═══〔 NEW USER DETECTED 〕═══╗ 🚀💀

👤 @{uname}
🆔 {uid}

💀🚀 ╚════════════════════════════╝ 🚀💀
""")

    if m.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "💀 ADMIN PANEL", reply_markup=admin_kb())

# ===== USER → ADMIN =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID,
content_types=['text','photo','video','document','audio','voice','sticker'])
def forward(m):
    uid = m.from_user.id
    uname = m.from_user.username or "NoUsername"

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("💬 REPLY", callback_data=f"reply_{uid}"),
        InlineKeyboardButton("⚡ QUICK REPLY", callback_data=f"reply_{uid}")
    )

    bot.send_message(ADMIN_ID, f"""
💀📡 ╔═══〔 LIVE MESSAGE STREAM 〕═══╗ 📡💀

👤 @{uname}
🆔 {uid}

💬 {m.text}

💀📡 ╚════════════════════════════╝ 📡💀
""", reply_markup=kb)

    # CHANNEL
    bot.send_message(CHANNEL_ID, f"""
💀📡 ╔═══〔 CHANNEL LOG 〕═══╗ 📡💀

👤 @{uname}
🆔 {uid}

💬 {m.text}

💀📡 ╚════════════════════════════╝ 📡💀
""")

    # USER ANIMATION
    sent = bot.send_message(m.chat.id, glitch("📡 Sending...")+"\n"+matrix())

    for s in ["🧠 Connecting...","🔐 Encrypting...","🚀 Delivering..."]:
        time.sleep(0.3)
        bot.edit_message_text(glitch(s)+"\n"+matrix(), m.chat.id, sent.message_id)

    bot.edit_message_text("""
💀🚀 ╔═══〔 TRANSMISSION SUCCESS 〕═══╗ 🚀💀

📡 Delivered  
⚡ Active  

💀🚀 ╚════════════════════════════╝ 🚀💀
""", m.chat.id, sent.message_id)

# ===== REPLY =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply_btn(c):
    uid = int(c.data.split("_")[1])
    reply_mode[ADMIN_ID] = uid

    bot.send_message(ADMIN_ID, f"""
💀🔒 ╔═══〔 TARGET LOCKED 〕═══╗ 🔒💀

USER: {uid}

TYPE NOW...

💀🔒 ╚══════════════════════╝ 🔒💀
""")

# ===== ADMIN REPLY =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID)
def admin_reply(m):
    if m.text in ["📊 SPEED","⛔ STOP"]:
        return

    if ADMIN_ID not in reply_mode:
        bot.send_message(ADMIN_ID, "❌ Reply dabao")
        return

    uid = reply_mode[ADMIN_ID]

    bot.copy_message(uid, m.chat.id, m.message_id)
    bot.send_message(CHANNEL_ID, m.text)

    sent = bot.send_message(ADMIN_ID, glitch("⚡ Sending..."))
    time.sleep(0.3)
    bot.edit_message_text(glitch("📡 Delivering..."), ADMIN_ID, sent.message_id)
    time.sleep(0.3)

    bot.edit_message_text(f"""
💀🚀 ╔═══〔 DELIVERY SUCCESS 〕═══╗ 🚀💀

TO: {uid}

💀🚀 ╚══════════════════════╝ 🚀💀
""", ADMIN_ID, sent.message_id)

    del reply_mode[ADMIN_ID]

# ===== SPEED =====
def live(chat_id, msg_id):
    global live_monitor
    while live_monitor:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        speed = round(time.time()*1000 % 1000,2)

        bot.edit_message_text(f"""
💀📊 ╔═══〔 LIVE SYSTEM 〕═══╗ 📊💀

CPU: {cpu}%
RAM: {ram}%
SPD: {speed}ms

{matrix()}

💀📊 ╚══════════════════════╝ 📊💀
""", chat_id, msg_id)

        time.sleep(2)

@bot.message_handler(func=lambda m: m.text == "📊 SPEED" and m.chat.id == ADMIN_ID)
def speed(m):
    global live_monitor
    live_monitor = True
    msg = bot.send_message(ADMIN_ID, "🚀 Monitor...")
    threading.Thread(target=live, args=(ADMIN_ID, msg.message_id), daemon=True).start()

@bot.message_handler(func=lambda m: m.text == "⛔ STOP" and m.chat.id == ADMIN_ID)
def stop(m):
    global live_monitor
    live_monitor = False
    bot.send_message(ADMIN_ID, "⛔ STOPPED")

print("💀🔥 FINAL BOX CYBER BOT RUNNING 🔥💀")
bot.infinity_polling(skip_pending=True)

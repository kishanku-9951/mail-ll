import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, random, time

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

reply_mode = {}

taglines = [
    "⚡ Lightning Fast Support",
    "🚀 Powered by Intelligence",
    "💀 Elite Response System",
    "🔥 Premium Support Activated",
    "🧠 Smart AI Routing Enabled"
]

# ===== START =====
@bot.message_handler(commands=['start'])
def start(m):
    msg = bot.send_message(m.chat.id, "⚡ Initializing system...")

    time.sleep(0.5)
    bot.edit_message_text("🚀 Loading modules...", m.chat.id, msg.message_id)

    time.sleep(0.5)
    bot.edit_message_text("🧠 Connecting to admin core...", m.chat.id, msg.message_id)

    time.sleep(0.5)
    bot.edit_message_text(f"""
<b>╔═══〔 🚀 ULTRA SUPPORT CORE 🚀 〕═══╗</b>

👋 <b>Welcome, {m.from_user.first_name}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ <b>{random.choice(taglines)}</b>

💬 📡 Direct Admin Connection  
🔒 🛡️ End-to-End Secure  
🚀 ⚡ Instant Delivery  

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢🔥 <b>🚀 SEND YOUR MESSAGE TO ADMIN 🚀</b> 🔥📢

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀 <b>ELITE MODE ACTIVATED</b> ⚡

<b>╚════════════════════════════╝</b>
""", m.chat.id, msg.message_id)

    # ===== ADMIN NOTIFY =====
    uid = m.from_user.id
    uname = m.from_user.username or "NoUsername"
    name = m.from_user.first_name

    info = f"""
<b>╔═══〔 🆕🚀 NEW USER DETECTED 🚀🆕 〕═══╗</b>

👤 <b>Name:</b> {name}  
🔗 <b>Username:</b> @{uname}  
🆔 <b>ID:</b> <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 <b>Status:</b> Online  
⚡ <b>Action:</b> Started Bot  

<b>╚════════════════════════════╝</b>
"""

    try:
        photos = bot.get_user_profile_photos(uid)
        if photos.total_count > 0:
            bot.send_photo(ADMIN_ID, photos.photos[0][-1].file_id, caption=info)
        else:
            bot.send_message(ADMIN_ID, info)
    except:
        pass

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

    header = f"""
<b>╔═══〔 📡💬 LIVE MESSAGE STREAM 💬📡 〕═══╗</b>

👤 <b>User:</b> @{uname}  
🆔 <b>ID:</b> <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    try:
        if m.content_type == "text":
            bot.send_message(
                ADMIN_ID,
                header + f"💬🔥 <b>Message:</b>\n<code>{m.text}</code>\n\n<b>╚════════════════════════════╝</b>",
                reply_markup=kb
            )
        else:
            bot.copy_message(ADMIN_ID, m.chat.id, m.message_id)
            bot.send_message(
                ADMIN_ID,
                header + "📎🔥 <b>Media Received</b>\n\n<b>╚════════════════════════════╝</b>",
                reply_markup=kb
            )

        # fake animation feel
        sent = bot.send_message(m.chat.id, "📡 Sending...")
        time.sleep(0.4)
        bot.edit_message_text("⚡ Delivering...", m.chat.id, sent.message_id)
        time.sleep(0.4)
        bot.edit_message_text("""
<b>╔═══〔 ✅🚀 TRANSMISSION SUCCESS 🚀✅ 〕═══╗</b>

📡 <b>Your message delivered</b>  
⚡ <b>Admin will respond soon</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 <b>Status:</b> Active  
🧠 <b>System:</b> Online  

<b>╚════════════════════════════╝</b>
""", m.chat.id, sent.message_id)

    except Exception as e:
        print(e)

# ===== REPLY BUTTON =====
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply_btn(c):
    uid = int(c.data.split("_")[1])
    reply_mode[c.from_user.id] = uid

    bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 🎯⚡ TARGET LOCKED ⚡🎯 〕═══╗</b>

🧬 <b>User ID:</b> <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 <b>Send your reply now</b>

🚀 <b>Ready to transmit</b>

<b>╚════════════════════════════╝</b>
""")

# ===== ADMIN REPLY =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID,
content_types=['text','photo','video','document','audio','voice','sticker'])
def admin_reply(m):
    if ADMIN_ID not in reply_mode:
        return

    uid = reply_mode[ADMIN_ID]

    try:
        bot.copy_message(uid, m.chat.id, m.message_id)

        bot.send_message(ADMIN_ID, f"""
<b>╔═══〔 🚀✅ DELIVERY SUCCESS ✅🚀 〕═══╗</b>

📤 <b>Sent to:</b> <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ <b>Status:</b> Delivered  
🧠 <b>System:</b> Stable  

<b>╚════════════════════════════╝</b>
""")

        del reply_mode[ADMIN_ID]

    except:
        bot.send_message(ADMIN_ID, "❌ Failed")

print("💀🔥 ULTRA EMOJI BOT RUNNING 🔥💀")
bot.infinity_polling(skip_pending=True)

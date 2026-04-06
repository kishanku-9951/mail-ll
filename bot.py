import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json, os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

USERS = "users.json"
BANNED = "banned.json"

reply_mode = {}
sent_messages = {}

# ===== UTILS =====
def load(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# ===== START (GOD UI) =====
@bot.message_handler(commands=['start'])
def start(m):
    users = load(USERS)
    if m.from_user.id not in users:
        users.append(m.from_user.id)
        save(USERS, users)

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📩 CONTACT ADMIN", callback_data="msg"),
        InlineKeyboardButton("👤 PROFILE", callback_data="me")
    )

    bot.send_message(m.chat.id, f"""
<b>╔═══〔 ⚡ SUPPORT SYSTEM ⚡ 〕═══╗</b>

👋 <b>Hello {m.from_user.first_name}</b>

💬 Direct admin chat  
⚡ Instant reply system  
🔒 Fully private & secure  

━━━━━━━━━━━━━━━━━━━━

🚀 <b>Click below to start</b>

<b>╚══════════════════════╝</b>

🔥 <b>BUILD BY YASH</b>
""", reply_markup=kb)

# ===== BUTTON =====
@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    if c.data == "msg":
        bot.send_message(c.message.chat.id, "✍️ <b>Send your message now...</b>")

    elif c.data == "me":
        bot.send_message(c.message.chat.id,
        f"""
<b>╔═══〔 👤 PROFILE 〕═══╗</b>

👤 Name: <b>{c.from_user.first_name}</b>  
🆔 ID: <code>{c.from_user.id}</code>

<b>╚══════════════════════╝</b>

🔥 BUILD BY YASH
""")

    elif c.data == "help":
        if c.from_user.id != ADMIN_ID:
            bot.answer_callback_query(c.id, "❌ Only Admin Allowed", show_alert=True)
            return
        bot.send_message(c.message.chat.id, HELP_TEXT)

    elif c.data.startswith("reply_"):
        uid = int(c.data.split("_")[1])
        reply_mode[c.from_user.id] = uid
        bot.send_message(ADMIN_ID, f"✍️ Reply to <code>{uid}</code>")

# ===== HELP (ADMIN ONLY) =====
HELP_TEXT = """
<b>╔═══〔 ⚙️ ADMIN PANEL 〕═══╗</b>

🔥 <b>FEATURES:</b>
• Smart Reply Button System  
• Auto Forward Messages  
• Seen Status Tracking  
• Broadcast System  
• Ban / Unban Control  
• Direct Messaging  
• Full Media Support  

━━━━━━━━━━━━━━━━━━━━

⚙️ <b>COMMANDS:</b>

/broadcast → Send to all users  
/users → Total users  
/ban USER_ID → Ban  
/unban USER_ID → Unban  
/msg USER_ID text → Direct msg  

━━━━━━━━━━━━━━━━━━━━

🧠 <b>SYSTEM FLOW:</b>
User → Admin  
Admin taps Reply  
Message → Same user  

━━━━━━━━━━━━━━━━━━━━

🔥 <b>BUILD BY YASH</b>

<b>╚══════════════════════╝</b>
"""

# ===== USER → ADMIN =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID,
content_types=['text','photo','video','document','audio','voice','sticker'])
def forward(m):
    if m.from_user.id in load(BANNED):
        return

    users = load(USERS)
    if m.from_user.id not in users:
        users.append(m.from_user.id)
        save(USERS, users)

    uid = m.from_user.id
    uname = m.from_user.username or "NoUsername"

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💬 REPLY", callback_data=f"reply_{uid}"))

    header = f"""
<b>╔═══〔 📩 NEW MESSAGE 〕═══╗</b>

👤 @{uname}  
🆔 <code>{uid}</code>

━━━━━━━━━━━━━━━━━━━━
"""

    if m.content_type == "text":
        bot.send_message(ADMIN_ID, header + f"💬 {m.text}\n\n<b>╚══════════════════════╝</b>", reply_markup=kb)
    else:
        bot.copy_message(ADMIN_ID, m.chat.id, m.message_id)
        bot.send_message(ADMIN_ID, header + "📎 Media\n\n<b>╚══════════════════════╝</b>", reply_markup=kb)

# ===== ADMIN REPLY =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID,
content_types=['text','photo','video','document','audio','voice','sticker'])
def admin_reply(m):
    if ADMIN_ID not in reply_mode:
        return

    uid = reply_mode[ADMIN_ID]
    try:
        sent = bot.copy_message(uid, m.chat.id, m.message_id)
        sent_messages[sent.message_id] = uid
        bot.send_message(ADMIN_ID, "✅ Sent")
        del reply_mode[ADMIN_ID]
    except:
        bot.send_message(ADMIN_ID, "❌ Failed")

# ===== SEEN =====
@bot.message_handler(func=lambda m: True)
def seen(m):
    uid = m.from_user.id
    for msg_id, user in list(sent_messages.items()):
        if user == uid:
            bot.send_message(ADMIN_ID, f"👁️ Seen by <code>{uid}</code>")
            del sent_messages[msg_id]
            break

# ===== BROADCAST =====
@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if m.chat.id != ADMIN_ID:
        return
    bot.send_message(ADMIN_ID, "📢 Send message")
    bot.register_next_step_handler(m, send_all)

def send_all(m):
    users = load(USERS)
    banned = load(BANNED)

    count = 0
    for u in users:
        if u in banned:
            continue
        try:
            bot.copy_message(u, m.chat.id, m.message_id)
            count += 1
        except:
            pass

    bot.send_message(ADMIN_ID, f"✅ Sent to {count}")

# ===== USERS =====
@bot.message_handler(commands=['users'])
def users(m):
    if m.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, f"👥 {len(load(USERS))} users")

# ===== BAN =====
@bot.message_handler(commands=['ban'])
def ban(m):
    if m.chat.id == ADMIN_ID:
        uid = int(m.text.split()[1])
        b = load(BANNED)
        if uid not in b:
            b.append(uid)
            save(BANNED, b)
        bot.send_message(ADMIN_ID, "🚫 Banned")

# ===== UNBAN =====
@bot.message_handler(commands=['unban'])
def unban(m):
    if m.chat.id == ADMIN_ID:
        uid = int(m.text.split()[1])
        b = load(BANNED)
        if uid in b:
            b.remove(uid)
            save(BANNED, b)
        bot.send_message(ADMIN_ID, "✅ Unbanned")

print("🔥 BOT RUNNING - BUILD BY YASH")
bot.infinity_polling(skip_pending=True)

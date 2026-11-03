import telebot
from telebot import types

TOKEN = "9169341515:AAFCLvhjZ-rRrmtbqcHdDSO2erqa8c79UhY"
bot = telebot.TeleBot(TOKEN)

try:
    bot.delete_webhook()
except:
    pass

الاستضافات = []
users = {}

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("📤 رفع استضافة جديدة")
    markup.add("🏢 المكاتب")
    return markup

def back_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 القائمة الرئيسية")
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    users[m.chat.id] = {"step": None}
    text = "اهلا بك في بوت الاستضافة 🚀\n\n📤 رفع استضافة جديدة : ترفع ملفات بوت جديد\n🏢 المكاتب : تشوف كل الاستضافات اللي رفعتها"
    bot.send_message(m.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "🔙 القائمة الرئيسية")
def back(m):
    users[m.chat.id] = {"step": None}
    bot.send_message(m.chat.id, "رجعت للقائمة الرئيسية ✅", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "🏢 المكاتب")
def offices(m):
    if not الاستضافات:
        bot.send_message(m.chat.id, "مفيش استضافات مرفوعة لسه ⛔\nدوس 📤 رفع استضافة جديدة", reply_markup=back_keyboard())
        return
    text = "📋 كل الاستضافات المرفوعة:\n\n"
    for i, h in enumerate(الاستضافات, 1):
        text += f"{i}. 🏢 {h['name']} - {h['user']}\n"
    bot.send_message(m.chat.id, text, reply_markup=back_keyboard())

@bot.message_handler(func=lambda m: m.text == "📤 رفع استضافة جديدة")
def new_host(m):
    users[m.chat.id] = {"step": "await_host_name"}
    bot.send_message(m.chat.id, "تمام 👇\n\nارسل اسم الاستضافة / اسم البوت اللي عايز ترفعه", reply_markup=back_keyboard())

@bot.message_handler(content_types=['text', 'document'])
def all_msg(m):
    chat_id = m.chat.id
    if chat_id not in users:
        users[chat_id] = {"step": None}
    step = users[chat_id].get("step")

    if step == "await_host_name" and m.content_type == 'text':
        if m.text == "🔙 القائمة الرئيسية": return
        users[chat_id]["temp_name"] = m.text
        users[chat_id]["step"] = "await_host_file"
        bot.send_message(chat_id, f"اسم الاستضافة: {m.text} ✅\n\nالان ابعت ملف البوت ( .py او .zip ) او ابعت كود البوت كرسالة", reply_markup=back_keyboard())
        return

    if step == "await_host_file":
        if m.content_type == 'text' and m.text == "🔙 القائمة الرئيسية": return
        file_name = users[chat_id].get("temp_name")
        الاستضافات.append({
            "name": file_name,
            "user": m.from_user.first_name,
            "id": chat_id
        })
        bot.send_message(chat_id, f"✅ تم رفع الاستضافة بنجاح\n\n🏢 الاسم: {file_name}\n👤 بواسطة: {m.from_user.first_name}\n\nسيتم تشغيلها خلال دقائق 🚀", reply_markup=main_keyboard())
        users[chat_id]["step"] = None
        return

print("بوت الاستضافة شغال ✅")
bot.infinity_polling()
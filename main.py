import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# 🔹 BotFather से लिया गया Token डालो
BOT_TOKEN = "YOUR_BOT_TOKEN"

# 🔹 Channel username (without @)
CHANNEL_USERNAME = "bye_artist"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Example NCERT Links (आप चाहो तो Class 1–12 तक डाल सकते हो)
ncert_books = {
    "Class 6": {
        "Maths": "https://ncert.nic.in/textbook/pdf/femh1dd.zip",
        "Science": "https://ncert.nic.in/textbook/pdf/fesc1dd.zip",
    },
    "Class 10": {
        "Maths": "https://ncert.nic.in/textbook/pdf/femh1dd.zip",
        "Science": "https://ncert.nic.in/textbook/pdf/fesc1dd.zip",
    }
}

# ✅ Channel Check Function
def check_subscription(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_member = context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
    return chat_member.status in ["member", "administrator", "creator"]

# ✅ Start Command
def start(update: Update, context: CallbackContext):
    user = update.effective_user

    if not check_subscription(update, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/bye_artist")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"Hello {user.first_name}!\n\n👉 Please join our channel to use this bot.",
            reply_markup=reply_markup
        )
        return

    # Send Animation (GIF/Sticker/Video Note)
    update.message.reply_animation(
        animation="https://files.catbox.moe/lhbsqt.mp4",  # कोई भी gif link डाल सकते हो
        caption="📚 Welcome to NCERT Books Bot!\nSelect a class to get books."
    )

    keyboard = [[InlineKeyboardButton(cls, callback_data=cls)] for cls in ncert_books.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("📖 Choose Class:", reply_markup=reply_markup)

# ✅ Books Command
def books(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(cls, callback_data=cls)] for cls in ncert_books.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("📖 Choose Class:", reply_markup=reply_markup)

# ✅ Help Command
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "ℹ️ Commands:\n"
        "/start - Start Bot\n"
        "/books - Get NCERT Books\n"
        "/about - About Bot\n"
        "/help - Help Menu"
    )

# ✅ About Command
def about(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 *About This Bot:*\n\n"
        "📚 This bot provides NCERT Books (Class 1–12).\n"
        "💡 Created with ❤️ using Python.\n"
        f"📢 Join our channel: @{CHANNEL_USERNAME}",
        parse_mode="Markdown"
    )

# ✅ Button Handler
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data in ncert_books:
        keyboard = [[InlineKeyboardButton(sub, url=link)] for sub, link in ncert_books[data].items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"📖 {data} Books:", reply_markup=reply_markup)

# ✅ Main Function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("books", books))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "YourChannelUsername"  # without @

# Example NCERT Links (आप चाहो तो पूरी Class 1–12 डाल सकते हो)
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


# ✅ Check Subscription
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ✅ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Channel check
    if not await check_subscription(update, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Hello {user.first_name}!\n\n👉 Please join our channel to use this bot.",
            reply_markup=reply_markup
        )
        return

    # Send Animation (gif/sticker)
    await update.message.reply_animation(
        animation="https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif",
        caption="📚 Welcome to NCERT Books Bot!\nSelect a class to get books."
    )

    # Show class menu
    keyboard = [[InlineKeyboardButton(cls, callback_data=cls)] for cls in ncert_books.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 Choose Class:", reply_markup=reply_markup)


# ✅ Books Command
async def books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cls, callback_data=cls)] for cls in ncert_books.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📖 Choose Class:", reply_markup=reply_markup)


# ✅ Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Commands:\n"
        "/start - Start Bot\n"
        "/books - Get NCERT Books\n"
        "/about - About Bot\n"
        "/help - Help Menu"
    )


# ✅ About Command
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *About This Bot:*\n\n"
        "📚 This bot provides NCERT Books (Class 1–12).\n"
        "💡 Created with ❤️ using Python.\n"
        f"📢 Join our channel: @{CHANNEL_USERNAME}",
        parse_mode="Markdown"
    )


# ✅ Button Handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data in ncert_books:
        keyboard = [[InlineKeyboardButton(sub, url=link)] for sub, link in ncert_books[data].items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"📖 {data} Books:", reply_markup=reply_markup)


# ✅ Main Function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("books", books))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == "__main__":
    main()
    main()
    

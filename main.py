import os
if all(tok in key for tok in query.split()):
results.append((cls, title, url))


if not results:
await update.message.reply_text("No matches in catalog. Try different keywords or update catalog.json.")
return


# Show first 25 as buttons
rows = []
for i, (cls, title, url) in enumerate(results[:25], start=1):
rows.append([InlineKeyboardButton(f"{i}. {cls} – {title}", callback_data=f"book|{url}|{title}")])
rows.append([InlineKeyboardButton("🔙 Back", callback_data="back|root")])
await update.message.reply_text("Search results:", reply_markup=InlineKeyboardMarkup(rows))


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
if not query:
return
try:
await query.answer()
except Exception:
pass


data = query.data or ""
action, *rest = data.split("|", 2)


if action == "refresh":
try:
load_catalog()
await query.edit_message_text("Catalog refreshed. Use /start again or pick an option.")
except Exception as e:
await query.edit_message_text(f"Refresh failed: {e}")
return


if action == "class":
cls = rest[0]
books = CATALOG.get(cls, {})
if not books:
await query.edit_message_text(f"No books found for {cls}. Update catalog.json and press Refresh.")
return
rows = []
for title, url in books.items():
rows.append([InlineKeyboardButton(title, callback_data=f"book|{url}|{title}")])
rows.append([InlineKeyboardButton("🔙 Back", callback_data="back|root")])
await query.edit_message_text(f"{cls}: Select a book to download.", reply_markup=InlineKeyboardMarkup(rows))
return


if action == "book":
url, title = rest
await query.edit_message_text(f"Fetching: {title}\nIf it takes long, use direct link: {url}")
await send_pdf(url, title, update, context)
return


if action == "back":
# Back to root list of classes
classes = sorted(CATALOG.keys())
rows = chunk_buttons([(c, f"class|{c}") for c in classes], row=2)
rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="refresh|root")])
try:
await query.edit_message_text("Choose your class:", reply_markup=InlineKeyboardMarkup(rows))
except Exception:
await

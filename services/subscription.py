from aiogram import Bot
from db.database import DB

async def not_subscribed(bot: Bot, db: DB, user_id: int):
    missing = []
    for ch in await db.list_channels():
        try:
            member = await bot.get_chat_member(ch["chat_id"], user_id)
            if member.status in ("left", "kicked"):
                missing.append(ch)
        except Exception:
            missing.append(ch)
    return missing

def subscribe_kb(missing):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    rows = [[InlineKeyboardButton(text=f"📢 {c['title']}", url=c["link"])] for c in missing]
    rows.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
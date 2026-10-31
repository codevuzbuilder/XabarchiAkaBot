from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

REG = {0: "🔵", 1: "🟢", 2: "🔴"}  # "rang" indikatori

DEFAULTS = {
    "save": "📥 Saqlash",
    "history": "🗂 Tarixim",
    "autopay": "💳 Avto to'lov",
    "subscription": "📢 Obuna",
    "account": "🔗 Botni ulash",
    "design": "🎨 Dizayn",
    "edit": "✏️ Tugmalarni tahrirlash",
    "partner": "🤝 Hamkorlik",
    "back": "⬅️ Orqaga",
}

def main_menu(labels: dict, color: int) -> InlineKeyboardMarkup:
    d = REG[color]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{d} {labels['save']}", callback_data="m:save")],
        [InlineKeyboardButton(text=f"{d} {labels['history']}", callback_data="m:history")],
        [InlineKeyboardButton(text=f"{d} {labels['autopay']}", callback_data="m:autopay")],
        [InlineKeyboardButton(text=f"{d} {labels['account']}", callback_data="m:account")],
        [InlineKeyboardButton(text=f"{d} {labels['subscription']}", callback_data="m:subscription")],
        [InlineKeyboardButton(text=f"{d} {labels['design']}", callback_data="m:design"),
         InlineKeyboardButton(text=f"{d} {labels['edit']}", callback_data="m:edit")],
        [InlineKeyboardButton(text=f"{d} {labels['partner']}", callback_data="m:partner")],
    ])
    return kb

def color_menu(color: int):
    d = REG[color]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{d} Rangni o'zgartirish", callback_data="color:next")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="m:home")],
    ])
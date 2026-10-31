from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.menus import main_menu, DEFAULTS
from services.subscription import not_subscribed, subscribe_kb
from utils.premium_emoji import premium_text

router = Router()

async def load_labels(db, uid):
    out = {}
    for k, v in DEFAULTS.items():
        out[k] = await
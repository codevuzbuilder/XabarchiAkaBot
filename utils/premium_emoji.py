from aiogram.types import MessageEntity
from config import PREMIUM_EMOJI_ENABLED

# Bot egasi o'z premium emoji ID'larini shu yerga yozadi
# (Premium bot orqali olinadi: message.entity.custom_emoji_id)
PREMIUM = {
    "save": "5368324170671202286",
    "history": "5368324170671202286",
    "pay": "5368324170671202286",
}

def premium_text(name: str, fallback: str = "•") -> tuple[str, list | None]:
    """Premium yoqilgan bo'lsa (text, [entitiy]), aks holda (fallback, None)."""
    if not PREMIUM_EMOJI_ENABLED or name not in PREMIUM:
        return fallback, None
    text = fallback
    ent = MessageEntity(
        type="custom_emoji", offset=0, length=len(text),
        custom_emoji_id=PREMIUM[name],
    )
    return text, [ent]
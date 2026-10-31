from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN", "")
ADMIN_ID = int(getenv("ADMIN_ID", "0"))
DB_PATH = getenv("DB_PATH", "bot.db")
PREMIUM_EMOJI_ENABLED = getenv("PREMIUM_EMOJI_ENABLED", "0") == "1"

TEZCHECK_BASE_URL = getenv("TEZCHECK_BASE_URL", "https://api.tezcheck.uz")
TEZCHECK_SECRET = getenv("TEZCHECK_SECRET", "")

CLICK_SERVICE_ID = getenv("CLICK_SERVICE_ID", "")
CLICK_MERCHANT_ID = getenv("CLICK_MERCHANT_ID", "")
CLICK_MERCHANT_USER_ID = getenv("CLICK_MERCHANT_USER_ID", "")
CLICK_SECRET_KEY = getenv("CLICK_SECRET_KEY", "")

WEBHOOK_HOST = getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(getenv("WEBHOOK_PORT", "8080"))
import os
from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))

REAL_DATABASE_URL = os.getenv(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://sergey:11@localhost:5432/bot",
)

main_bot_token = os.getenv("MAIN_TELEGRAM_TOKEN")
payment_telegram_token = os.getenv("PAYMENT_TELEGRAM_TOKEN")
support_telegram_token = os.getenv("SUPPORT_TELEGRAM_TOKEN")
comment_telegram_token = os.getenv("COMMENT_TELEGRAM_TOKEN")
SITE_DOMAIN = os.getenv("SITE_DOMAIN")

# ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=60)
# SECRET_KEY = env.str("SECRET_KEY", default="secret")
# ALGORITHM = env.str("ALGORITHM", default="HS256")

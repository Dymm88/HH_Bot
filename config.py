import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# Константы приложения
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN = os.getenv("TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
EMAIL = os.getenv("EMAIL")
RESUME_ID = os.getenv("RESUME_ID")
APPLICATION = os.getenv("APPLICATION")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": f"{APPLICATION} ({EMAIL})",
    "Content-Type": "application/json",
}

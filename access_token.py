import requests
from dotenv import load_dotenv, set_key

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN, HEADERS, REFRESH_TOKEN, APPLICATION

load_dotenv()


def get_code() -> str:
    """
    Функция для получения кода авторизации.
    """
    auth_code = (
        f"https://hh.ru/oauth/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}"
    )
    print("Перейди по ссылке и скопируй код:", auth_code)
    code = input("Вставь код авторизации: ")
    return code


def get_access_token(auth_code: str) -> None:
    """
    Функция для получения токена доступа.
    """
    url = "https://api.hh.ru/token"
    headers = {
        "User-Agent": APPLICATION,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    r = requests.post(url=url, headers=headers, data=data)
    if "access_token" in r.json() and "refresh_token" in r.json():
        set_key(".env", "TOKEN", r.json()["access_token"])
        set_key(".env", "REFRESH_TOKEN", r.json()["refresh_token"])



def refresh_token() -> None:
    """
    Функция для обновления токена доступа.
    """
    url = "https://hh.ru/oauth/token"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "VacancyBot",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    }
    r = requests.post(url=url, headers=headers, data=data)
    if "access_token" in r.json() and "refresh_token" in r.json():
        set_key(".env", "TOKEN", r.json()["access_token"])
        set_key(".env", "REFRESH_TOKEN", r.json()["refresh_token"])



def check_token_and_application() -> None:
    """
    Функция для проверки валидности токена и приложения.
    """
    url = "https://api.hh.ru/me"
    r = requests.get(url=url, headers=HEADERS)
    if r.status_code == 200:
        print("Токен и приложение валидны")
    else:
        print("Токен или приложение невалидно")


if __name__ == "__main__":
    """
    Необходимо закомментировать ненужное
    """
    # Функции для получения токена доступа.
    access_code = get_code()
    get_access_token(access_code)
    # Функция для обновления токена доступа.
    # refresh_token()
    # Функция для проверки валидности токена доступа.
    # check_token_and_application()

import aiohttp

from config import HEADERS
from params import companies


async def put_in_black_list(vacancy_list: tuple[str]) -> None:
    """
    Асинхронная функция для добавления компаний в черный список.

    :param vacancy_list: Список компаний
    """
    async with aiohttp.ClientSession() as session:
        for name in vacancy_list:
            if name["employer"]["name"] in companies:
                url = f"https://api.hh.ru/vacancies/blacklisted/{name['id']}"
                async with session.put(url=url, headers=HEADERS) as response:
                    if response.status != 200:
                        print(
                            f"Не удалось добавить компанию {name['employer']['name']} в черный список."
                        )


async def get_black_list() -> list:
    """
    Асинхронная функция для получения черного списка компаний.

    :return: Список идентификаторов компаний в черном списке
    """
    url = "https://api.hh.ru/vacancies/blacklisted"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADERS) as response:
            black_list_data = await response.json()
            black_list = [t["id"] for t in black_list_data["items"]]
            return black_list

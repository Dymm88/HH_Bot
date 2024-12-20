import asyncio
import logging

import aiohttp

from black_list import put_in_black_list, get_black_list
from config import HEADERS, RESUME_ID
from message import MESSAGE_TEXT
from params import params_All

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.hh.ru"


async def get_vacancies(params: dict[str | None]) -> list[dict[str | None]]:
    url = f"{API_BASE_URL}/vacancies"
    vacancy_list = []
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url, headers=HEADERS, params=params) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch vacancies: HTTP {response.status}")
                    break
                items = await response.json()
                vacancy_list.extend(items["items"])
                if items["pages"] == params["page"] + 1:
                    break
                params["page"] += 1
    return vacancy_list


async def vacancy_ids(vacancy_list: list[dict[str | None]]) -> list[int]:
    vacancy_list_id = [vacancy["id"] for vacancy in vacancy_list]
    put_in_black_list(vacancy_list)
    ended_vacancy_list = list(set(vacancy_list_id) - set(get_black_list()))
    return ended_vacancy_list


async def send_vacancy(session: aiohttp.ClientSession, item: int) -> bool:
    url = f"{API_BASE_URL}/negotiations"
    params = {"resume_id": RESUME_ID, "vacancy_id": str(item), "message": MESSAGE_TEXT}
    async with session.post(url, headers=HEADERS, params=params) as response:
        if response.status == 201:
            logger.info(f"Резюме успешно отправлено на вакансию {item}")
            return True
        elif response.status == 200:
            logger.info(f"Необходимо выполнение задания для вакансии {item}")
        elif response.status == 400:
            logger.warning("Лимит на количество отправленных резюме")
        else:
            logger.error(
                f"Произошла ошибка при отправке резюме на вакансию {item}: {response.status}"
            )
    return False


async def response_vacancies(list_vacancies: list[int]) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = [send_vacancy(session, item) for item in list_vacancies]
        results = await asyncio.gather(*tasks)
    success = sum(results)
    logger.info(f"Количество отправленных отзывов - {success}")


async def main() -> None:
    params = params_All.copy()
    vacancy_list = await get_vacancies(params)
    list_vacancies = await vacancy_ids(vacancy_list)
    await response_vacancies(list_vacancies)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

import aiohttp

from black_list import put_in_black_list, get_black_list
from config import HEADERS, RESUME_ID
from message import MESSAGE_TEXT
from params import params_All


async def get_vacancies(params):
    url = "https://api.hh.ru/vacancies"
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url, headers=HEADERS, params=params) as r:
                print(r.status)
                vacancy_list = []
                items = await r.json()
                vacancy_list += items["items"]
                if items["pages"] == params["page"] + 1:
                    break
                params["page"] += 1
        print(vacancy_list)


async def vacancy_ids(vacancy_list):
    vacancy_list_id = [vacancy["id"] for vacancy in vacancy_list]
    put_in_black_list(vacancy_list)
    ended_vacancy_list = list(set(vacancy_list_id) - set(get_black_list()))
    return ended_vacancy_list


async def response_vacancies(list_vacancies):
    success = 0
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in list_vacancies:
            task = asyncio.create_task(send_vacancy(session, item, success))
            tasks.append(task)
        await asyncio.gather(*tasks)
    print(f"Количество отправленных отзывов - {success}")


async def send_vacancy(session, item, success):
    async with session.post(
        f"https://api.hh.ru/negotiations?resume_id={RESUME_ID}"
        f"&vacancy_id={str(item)}&message={MESSAGE_TEXT}",
        headers=HEADERS,
    ) as r:
        match r.status:
            case 201:
                success += 1
                print(f"Резюме успешно отправлено на вакансию {item}")
            case 200:
                print(f"Необходимо выполнение задания для вакансии {item}")
            case 400:
                print(f"Лимит на количество отправленных резюме")
            case _:
                print(
                    f"Произошла ошибка при отправке резюме на вакансию {item}: {r.status}"
                )


async def main():
    params = params_All
    vacancy_list = await get_vacancies(params)
    list_vacancies = await vacancy_ids(vacancy_list)
    await response_vacancies(list_vacancies)


asyncio.run(main())

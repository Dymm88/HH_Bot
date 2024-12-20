import requests

from black_list import get_black_list, put_in_black_list
from config import HEADERS, RESUME_ID
from message import MESSAGE_TEXT


def get_vacancies(
    params: dict[str, str | int | bool]
) -> list[dict[str, str | int | bool | None]]:
    """
    Функция для получения вакансий.

    :param params: Параметры запроса
    :return: список вакансий
    """
    vacancy_list = []
    url = "https://api.hh.ru/vacancies"
    while True:
        r = requests.get(url=url, headers=HEADERS, params=params)
        items = r.json()["items"]
        vacancy_list += items
        if r.json()["pages"] == params["page"] + 1:
            break
        params["page"] += 1
    return vacancy_list


def vacancy_ids(vacancy_list: list[dict[str, str | int | bool | None]]) -> list[int]:
    """
    Функция для извлечения идентификаторов вакансий.

    :param vacancy_list: Список вакансий
    :return: список идентификаторов вакансий, исключая компании из черного списка
    """
    vacancy_list_id = [vacancy["id"] for vacancy in vacancy_list]
    put_in_black_list(vacancy_list)
    ended_vacancy_list = list(set(vacancy_list_id) - set(get_black_list()))
    return ended_vacancy_list


def response_vacancies(list_vacancies: list[int]) -> None:
    """
    Функция для отправки резюме с сопроводительным письмом на полученные вакансии.

    :param list_vacancies: Список идентификаторов вакансий
    """
    success = 0
    for item in list_vacancies:
        r = requests.post(
            f"https://api.hh.ru/negotiations?resume_id={RESUME_ID}&vacancy_id={str(item)}&message={MESSAGE_TEXT}",
            headers=HEADERS,
        )
        match r.status_code:
            case 201:
                success += 1
                print(f"Резюме успешно отправлено на вакансию {item}")
            case 200:
                print(f"Необходимо выполнение задания для вакансии {item}")
            case 400:
                print(f"Лимит на количество отправленных резюме")
            case _:
                print(
                    f"Произошла ошибка при отправке резюме на вакансию {item}: {r.status_code}"
                )
    print(f"Количество отправленных отзывов - {success}")

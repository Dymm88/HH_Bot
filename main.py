import asyncio

from access_token import check_token_and_application
from params import params_All
from vacancies import get_vacancies, vacancy_ids, response_vacancies


async def main() -> None:
    """
    Основная функция, которая вызывает функции для получения и обработки вакансий.
    """
    check_token_and_application()
    params = params_All.copy()
    vacancy_list = await get_vacancies(params)
    list_vacancies = await vacancy_ids(vacancy_list)
    await response_vacancies(list_vacancies)


if __name__ == "__main__":
    asyncio.run(main())

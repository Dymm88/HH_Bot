from access_token import check_token_and_application
from params import params_SPb, params_All
from vacancies import get_vacancies, vacancy_ids, response_vacancies


def main() -> None:
    """
    Основная функция, которая вызывает функции для получения и обработки вакансий.
    """
    # Проверяем токен и приложение на валидность
    check_token_and_application()

    # Получаем вакансии в Санкт-Петербурге
    data_spb = get_vacancies(params_SPb)
    # Извлекаем идентификаторы вакансий, исключая вакансии из черного списка
    list_vacancies = vacancy_ids(data_spb)
    # Отправляем резюме на полученные вакансии
    response_vacancies(list_vacancies)

    # Получаем вакансии по всей России
    data_all = get_vacancies(params_All)
    # Извлекаем идентификаторы вакансий, исключая вакансии из черного списка
    list_vacancies = vacancy_ids(data_all)
    # Отправляем резюме на полученные вакансии
    response_vacancies(list_vacancies)


if __name__ == "__main__":
    main()

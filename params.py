params_SPb = {  # параметры для поиска вакансий в SPb
    "page": 0,
    "per_page": 100,
    "text": "python Python NOT преподаватель NOT ментор NOT наставник NOT QA NOT ML",
    "experience": ["between1And3", "between3And6"],
    "area": 2,
    "period": 7,
    "schedule": "remote",
    "salary": 200_000,
    "search_field": "name",
}

params_All = {  # параметры для поиска вакансий по РФ
    "page": 0,
    "per_page": 100,
    "text": "python Python NOT преподаватель NOT ментор NOT наставник NOT QA NOT ML",
    "experience": ["between1And3", "between3And6"],
    "area": 113,
    "period": 7,
    "schedule": "remote",
    "salary": 200_000,
    "search_field": "name",
}

companies = (  # список компаний, id вакансий которых нужно добавить в blacklist
    "Aston",
    "Яндекс Крауд",
    "Яндекс Крауд: Поддержка",
    "Rebotica",
    "ИнфоТеКС",
    "АйТи-Солюшн",
    "EasyCode",
    "Школа математики и программирования Matrix",
    "Ворк5",
    "Журавлева Елена Александровна",
    "Журавлев Александр Сергеевич",
    "LATOKEN",
)

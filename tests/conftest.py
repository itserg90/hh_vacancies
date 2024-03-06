import pytest

from src.class_vacancy import Vacancy


@pytest.fixture()
def api_json_vacancies():
    return {"items": [{"name": "имя_1",
                       "alternate_url": "ссылка",
                       "salary": 100000,
                       "requirement": "описание_1"},
                      {"name": "имя_2",
                       "alternate_url": "ссылка",
                       "salary": None,
                       "requirement": "описание_2"},
                      {"name": "имя_3",
                       "alternate_url": "ссылка",
                       "salary": {"from": 50000, "to": 100000, "currency": "RUR"},
                       "snippet": {"requirement": "описание_3"}}
                      ]}


@pytest.fixture()
def json_vacancies():
    return [{"name": "имя_1",
             "url": "ссылка",
             "salary": 100000,
             "requirement": "описание_1"},
            {"name": "имя_2",
             "url": "ссылка",
             "salary": None,
             "requirement": "описание_2"},
            {"name": "имя_3",
             "url": "ссылка",
             "salary": None,
             "requirement": None}
            ]


@pytest.fixture()
def vacancies_of_objects():
    return [Vacancy("имя_1", "ссылка", {"from": 50000, "to": 100000, "currency": "RUR"}, "описание_1"),
            Vacancy("имя_2", "ссылка", {"from": None, "to": 100000, "currency": "RUR"}, "описание_2"),
            Vacancy("имя_3", "ссылка", {"from": 50000, "to": None, "currency": "RUR"}, "описание_3"),
            Vacancy("имя_4", "ссылка", "Зарплата не указана", "описание_4")]

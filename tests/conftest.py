import pytest

from src.class_vacancy import Vacancy


@pytest.fixture()
def api_json_vacancies():
    return {"items": [{"id": 1,
                       "name": "имя_1",
                       "alternate_url": "ссылка",
                       "salary": {"from": 5000, "to": 10000, "currency": "USD"},
                       "snippet": {"requirement": "описание_1"}},
                      {"id": 2,
                       "name": "имя_2",
                       "alternate_url": "ссылка",
                       "salary": None,
                       "snippet": {"requirement": "описание_2"}},
                      {"id": 3,
                       "name": "имя_3",
                       "alternate_url": "ссылка",
                       "salary": {"from": 50000, "to": 100000, "currency": "RUR"},
                       "snippet": {"requirement": "описание_3"}}
                      ]}


@pytest.fixture()
def json_vacancies():
    return [{"id": 1,
             "name": "имя_1",
             "url": "ссылка",
             "salary": 100000,
             "requirement": "описание_1"},
            {"id": 2,
             "name": "имя_2",
             "url": "ссылка",
             "salary": None,
             "requirement": "описание_2"},
            {"id": 3,
             "name": "имя_3",
             "url": "ссылка",
             "salary": None,
             "requirement": None}
            ]


@pytest.fixture()
def vacancies_of_objects():
    return [Vacancy(1, "имя_1", "ссылка", {"from": 0, "to": 0}, "описание_1"),
            Vacancy(2, "имя_2", "ссылка", {"from": 50000, "to": 100000, "currency": "RUR"}, "описание_2"),
            Vacancy(3, "имя_3", "ссылка", {"from": None, "to": 100000, "currency": "RUR"}, "описание_3"),
            Vacancy(4, "имя_4", "ссылка", {"from": 50000, "to": None, "currency": "RUR"}, "описание_4")]

import io

from src.class_api import ApiVacanciesHh
from src.class_vacancy import Vacancy
from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, user_interaction


def test_filter_vacancies_by_name(api_json_vacancies):
    api_1 = ApiVacanciesHh()
    api_1.filter_vacancies_by_name(api_json_vacancies)
    assert len(api_1.hh_vacancies) == 2


def test_class_vacancy(json_vacancies):
    current_list = Vacancy.cast_to_object_list(json_vacancies)
    assert current_list[0].name == "имя_1"
    assert current_list[1].salary == {"from": 0, "to": 0}
    assert current_list[2].requirements == "Описание не указано"


def test_validate_salary(json_vacancies):
    current_list = Vacancy.cast_to_object_list(json_vacancies)
    assert current_list[1].salary == {"from": 0, "to": 0}


def test_validate_requirements(json_vacancies):
    current_list = Vacancy.cast_to_object_list(json_vacancies)
    assert current_list[-1].requirements == "Описание не указано"


def test_lt_salary(vacancies_of_objects):
    current_list = sorted(vacancies_of_objects, reverse=True)
    assert current_list[-1].salary == {"from": 0, "to": 0}


def test_get_salary(vacancies_of_objects):
    assert vacancies_of_objects[0].get_salary() == 0
    assert vacancies_of_objects[1].get_salary() == 50_000
    assert vacancies_of_objects[2].get_salary() == 100_000
    assert vacancies_of_objects[3].get_salary() == 50_000


def test_filter_vacancies(vacancies_of_objects):
    current_list = filter_vacancies(vacancies_of_objects, ["описание_1"])
    assert len(current_list) == 1

    current_list = filter_vacancies(vacancies_of_objects, [])
    assert len(current_list) == 4


def test_get_vacancies_by_salary(vacancies_of_objects):
    current_list = get_vacancies_by_salary(vacancies_of_objects, "")
    assert len(current_list) == 4

    current_list = get_vacancies_by_salary(vacancies_of_objects, "50000")
    assert len(current_list) == 3

    current_list = get_vacancies_by_salary(vacancies_of_objects, "70000")
    assert len(current_list) == 2

    current_list = get_vacancies_by_salary(vacancies_of_objects, "110000")
    assert len(current_list) == 0


def test_sort_vacancies(vacancies_of_objects):
    current_list = sort_vacancies(vacancies_of_objects)
    assert current_list[-1].salary["from"] == 0
    assert current_list[1].salary["from"] == 50000


def test_get_top_vacancies(vacancies_of_objects):
    current_list = get_top_vacancies(vacancies_of_objects, 2)
    assert len(current_list) == 2


def test_user_interaction(monkeypatch, vacancies_of_objects):
    def mock_get(*args):
        pass

    def mock_hh(*args, **kwargs):
        return vacancies_of_objects

    monkeypatch.setattr("src.class_api.ApiVacanciesHh.get_vacancies", mock_get)
    monkeypatch.setattr("src.class_vacancy.Vacancy.cast_to_object_list", mock_hh)
    monkeypatch.setattr("sys.stdin", io.StringIO("python\nthree\n3\n\n100000\nn\nнет"))

    user_interaction()

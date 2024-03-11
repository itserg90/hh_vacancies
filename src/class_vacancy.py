from abc import ABC, abstractmethod


class AbstractVacancy(ABC):
    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, hh_vacancies):
        pass


class Vacancy(AbstractVacancy):
    """Класс для создания объектов"""

    __slots__ = ("id", "name", "link", "salary", "requirements")

    def __init__(self, id_vacancies, name: str, link: str, salary: (dict, None), requirements: str):
        self.id = id_vacancies
        self.name = name
        self.link = link

        self.salary = salary
        self.__validate_salary(salary)

        self.requirements = requirements
        self.__validate_requirements(requirements)

    def __validate_salary(self, salary) -> None:
        """Валидация зарплаты"""

        if salary:
            self.salary = salary
        else:
            self.salary = {"from": 0, "to": 0}

    def __validate_requirements(self, requirements) -> None:
        """Валидация описания"""

        if requirements:
            self.requirements = requirements
        else:
            self.requirements = "Описание не указано"

    @classmethod
    def cast_to_object_list(cls, hh_vacancies: list) -> list:
        """Преобразуем данные JSON в объекты класса"""

        current_list = []
        for vacancy in hh_vacancies:
            current_list.append(cls(vacancy["id"],
                                    vacancy["name"],
                                    vacancy["url"],
                                    vacancy["salary"],
                                    vacancy["requirement"]))
        return current_list

    def get_salary(self) -> int:
        """Получаем дельту зарплаты для сортировки"""

        if self.salary["from"] == 0 and self.salary["to"] == 0:
            res_self = 0
        elif self.salary["from"] and self.salary["to"]:
            res_self = self.salary["to"] - self.salary["from"]
        elif self.salary["from"] and not self.salary["to"]:
            res_self = self.salary["from"]
        else:
            res_self = self.salary["to"]
        return res_self

    def __lt__(self, other):
        salary_1 = self.get_salary()
        salary_2 = other.get_salary()
        return salary_1 < salary_2

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.name}, {self.link}, {self.salary}, {self.requirements})"

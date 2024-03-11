from abc import ABC, abstractmethod
import json
from pathlib import Path
from config import ROOT_DIR
from src.class_vacancy import Vacancy


class AbstractJSONSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(AbstractJSONSaver):
    """Класс для создания файла и сохранения, добавления и удаления вакансий"""

    COUNT_SAVER = 0

    def __init__(self):
        JSONSaver.COUNT_SAVER += 1
        self.__file_path = Path(ROOT_DIR, "data", "vacancies_")
        self.__filename = f"{self.__file_path}{JSONSaver.COUNT_SAVER}.json"
        if not Path(ROOT_DIR, "data").exists():
            Path(ROOT_DIR, "data").mkdir()
        if not Path(self.__filename).is_file():
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump([], file)

    def get_vacancy(self, job_name) -> list:
        """Получение данных из файла"""

        with open(self.__filename, "r", encoding="utf-8") as file:
            new_vacancies = []
            vacancies = json.load(file)
            for vacancy in vacancies:
                if job_name.lower() in vacancy.name:
                    new_vacancies.append(vacancy)
        return new_vacancies

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """ Дабавление вакансии в файл"""

        with open(self.__filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
            if vacancy.id not in [vac.id for vac in vacancies]:
                vacancies.append({"name": vacancy.name,
                                  "url": vacancy.link,
                                  "salary": vacancy.salary,
                                  "requirements": vacancy.requirements})
            with open(self.__filename, "w", encoding="utf-8") as file_1:
                json.dump(vacancies, file_1)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """ Удаление вакансии из файла"""

        with open(self.__filename, "r", encoding="utf-8") as file:
            new_vacancies = []
            vacancies = json.load(file)
            for current_vacancy in vacancies:
                if not vacancy.id == current_vacancy.id:
                    new_vacancies.append(current_vacancy)
            with open(self.__filename, "w", encoding="utf-8") as file_1:
                json.dump(new_vacancies, file_1)

from abc import ABC, abstractmethod
import json


class Json(ABC):
    def __init__(self, file, vacancies):
        """

        :param file: название файла, по которому совершаются все операции
        :param vacancies: python объект с вакансиями, получили через API
        """
        self.file = file
        self.vacancies = vacancies

    @abstractmethod
    def write_info(self):
        """
        Метод для записи информации в файл
        """
        pass

    @abstractmethod
    def add_info(self):
        """
        Метод для добавления информации в файл
        """
        pass

    @abstractmethod
    def delete_info(self):
        """
        Метод для удаления всей информации из файла
        """
        pass

def _perform_write(data, file_obj):
    if file_obj is None:
        return
    try:
        better_format = json.dumps(data, indent=2, ensure_ascii=False)
        file_obj.write(better_format)
    except Exception as e:
        print(f"Exception occurred while writing to file: {e}")


class JsonFileHandler(Json):

    def _open_file(self, mode):
        try:
            return open(self.file, mode, encoding="utf-8")
        except Exception as e:
            print(f"Exception occurred while opening the file: {e}")
            return None

    def write_info(self):
        with self._open_file("wt") as vacancies_from_hh:
            _perform_write(self.vacancies, vacancies_from_hh)

    def add_info(self):
        with self._open_file("r+t") as vacancies_from_hh:
            if vacancies_from_hh is None:
                return
            try:
                python_obj = json.load(vacancies_from_hh)
                python_obj.extend(self.vacancies)
                _perform_write(python_obj, vacancies_from_hh)
            except Exception as e:
                print(f"Exception occurred while adding information to file: {e}")

    def delete_info(self):
        with self._open_file("wt") as vacancies_from_hh:
            if vacancies_from_hh is not None:
                try:
                    vacancies_from_hh.truncate()
                except Exception as e:
                    print(f"Exception occurred while deleting information from file: {e}")


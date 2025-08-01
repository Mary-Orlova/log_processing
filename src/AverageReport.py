"""
Класс-отчет по статистики эндпойнтов(роутов route):
кол-во запросов и среднее время ответа
"""

from typing import List, Tuple


class AverageReport:
    def __init__(self) -> None:
        self.data = {}

    def add_record(self, record: dict) -> None:
        """
        Добавление записи лога для статистики
        :param record: словарь с route(эндпойнт) и время ответа 'response_time'
        :return: None
        """

        route = record.get("url")
        response_time = record.get("response_time", 0.0)

        if not route:
            return
        if route not in self.data:
            self.data[route] = {"count": 0, "total_time": 0.0}

        self.data[route]["count"] += 1
        self.data[route]["total_time"] += response_time

    def final_report(self) -> Tuple[List[str], List[List]]:
        """
        Итоговые данные отчёта.

        :return:
        headers: список заголовков таблицы
        report_data: список строк с данными handler, total, avg_response_time
        """
        report_data = []
        for route, stats in self.data.items():
            count = stats["count"]
            avg_time = stats["total_time"] / count if count else 0.0
            report_data.append([route, count, round(avg_time, 4)])

        # Сортировка запросов по убыванию
        report_data.sort(key=lambda x: x[1], reverse=True)

        # Нумерация строк для вывода в таблице
        report_data = [[idx] + row for idx, row in enumerate(report_data)]
        headers = [" ", "handler", "total", "avg_response_time"]
        return headers, report_data

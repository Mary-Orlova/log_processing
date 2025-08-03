import pytest
from _pytest.python_api import approx

import src.AverageReport as avg_report


def test_add_record():
    """
    Тест создание записи логов
    :return: None
    """
    report = avg_report.AverageReport()
    record = {"url": "/home", "response_time": 1.23}
    report.add_record(record)
    assert "/home" in report.data
    assert report.data["/home"]["count"] == 1
    assert report.data["/home"]["total_time"] == approx(1.23)


def test_add_record_no_url():
    """
    Тест добавление записи в отчет без url
    :return: None
    """
    report = avg_report.AverageReport()
    report.add_record({"response_time": 2.0})
    assert report.data == {}


def test_final_report_sort_and_avg():
    report = avg_report.AverageReport()
    report.add_record({"url": "/a", "response_time": 1.0})
    report.add_record({"url": "/b", "response_time": 1.0})
    report.add_record({"url": "/a", "response_time": 2.0})
    report.add_record({"url": "/b", "response_time": 2.0})

    # Заголовки, список: индекс, url, количество_запросов, среднее_время
    headers, data = report.final_report()

    assert headers == [" ", "handler", "total", "avg_response_time"]
    assert len(data) == 2

    # _row Результат фильтрации нужных строк в готовом отчёте
    a_row = next(row for row in data if row[1] == "/a")
    assert a_row[2] == 2  # Проверка, что посчитали именно 2 запроса.
    assert a_row[3] == pytest.approx(
        1.5
    )  # Проверка, что avg ~1.5 с учётом неточностей хранения float

    b_row = next(row for row in data if row[1] == "/b")
    assert b_row[2] == 2
    assert b_row[3] == pytest.approx(1.5)

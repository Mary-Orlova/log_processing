import json

import pytest


@pytest.fixture
def test_report() -> object:
    """
    Фикстура тестового отчета
    метод add_record добавляет записи.
    """

    class TestReport:
        def __init__(self):
            self.records = []
            self.final_called = False

        def add_record(self, record):
            self.records.append(record)

        def final_report(self):
            self.final_called = True
            # Возврает для теста отчета логов: заголовки и строку данных
            return (["handler", "count", "avg_time"], [[0, "/test", 1, 0.1]])

    return TestReport()


@pytest.fixture
def example_log() -> json:
    """
    Фикстура тестовых логов
    :return Возвращает список строк лог-файла в формате JSON
    """
    return [
        json.dumps(
            {
                "@timestamp": "2025-07-22T13:57:34+00:00",
                "status": 200,
                "url": "/test",
                "request_method": "GET",
                "response_time": 0.032,
                "http_user_agent": "...",
            }
        ),
        json.dumps(
            {
                "@timestamp": "2025-07-23T13:57:34+00:00",
                "status": 200,
                "url": "/test2",
                "request_method": "GET",
                "response_time": 0.072,
                "http_user_agent": "...",
            }
        ),
        "",  # пустая строка, игнорируется
    ]

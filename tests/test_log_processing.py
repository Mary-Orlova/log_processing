import asyncio

import pytest

from src.main import log_processing


@pytest.mark.asyncio
async def test_log_processing(tmp_path, test_report, example_log):
    """
    Тест log_processing на чтение и запись логов c фильтром по дате
    """

    # Временный файл с тестовыми логами
    file_path = tmp_path / "logfile.log"
    file_path.write_text("\n".join(example_log), encoding="utf-8")

    # Запуск процессинга с фильтром по дате 2025-07-22
    await asyncio.to_thread(log_processing, [str(file_path)], test_report, "2025-07-22")

    # Вывод только первая записи
    assert len(test_report.records) == 1
    assert test_report.records[0]["url"] == "/test"
    assert test_report.records[0]["response_time"] == 0.032

import asyncio
import json

import pytest

from src.main import log_processing


@pytest.mark.asyncio
async def test_log_processing_json_error(tmp_path, test_report, caplog):
    """
    Тест-проверка корректности обоработки ошибки JSON
    """
    bad_log_file = tmp_path / "bad.log"
    bad_log_file.write_text('{"bad_json": true,,}', encoding="utf-8")

    with caplog.at_level("ERROR"):
        await asyncio.to_thread(log_processing, [str(bad_log_file)], test_report)

        # Проверка, что в логах появилась ошибка JSONDecodeError
        assert any("JSONDecodeError" in record.message or "Expecting property name" in record.message
                   for record in caplog.records)
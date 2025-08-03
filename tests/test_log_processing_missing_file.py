import asyncio
from unittest.mock import patch

import pytest

from src.main import log_processing, logger


@pytest.mark.asyncio
async def test_log_processing_missing_file(test_report):
    """
    Тест-проверка при отсутствии файла на вывод сообщения об ошибке
    """

    missing_file = "none_file.log"

    with patch("builtins.print") as mock_print:
        await asyncio.to_thread(log_processing, [missing_file], test_report)
        mock_print.assert_called_with(f"Файл не найден: {missing_file}")

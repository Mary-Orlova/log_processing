"""
Основной файл запуска скрипта для обработки логов, формирования отчета
"""

import argparse
import json
from typing import List, Optional

from tabulate import tabulate

from src.AverageReport import AverageReport
from src.logging_config import setup_custom_logger

logger = setup_custom_logger(__name__)


def log_processing(
    log_files: List[str], report: AverageReport, date_filter: Optional[str] = None
) -> None:
    """
    Чтение логов из файлов, фильтр по дате (если указано),
    добавление данных для отчета по логам.

    :param: log_files список путей файлов с логами
    :param: report - файл для записи отчета
    :param: date_filter строка с датой в формате 'YYYY-MM-DD'
    """

    for log_file in log_files:

        try:
            with open(log_file, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError as e:
                        logger.error(
                            f"Возникло исключение при чтении логов в файле: {str(e)}"
                        )
                        raise

                    # Проверка, есть ли фильтр по дате - если нет, продолжаем
                    timestamp = record.get("@timestamp", "")
                    if date_filter and not timestamp.startswith(date_filter):
                        continue

                    # Добавление в отчёт
                    report.add_record(record)
                logger.info(f"Данные из файла {log_file} добавлены в отчет.")

        except FileNotFoundError:
            print(f"Файл не найден: {log_file}")
        except Exception as e:
            logger.error(f"Ошибка при обработке файла {log_file}: {e}")


def parse_args() -> argparse.Namespace:
    """
    Аргументы для парсинга командной строки

    :return объекты
    """
    parser = argparse.ArgumentParser(description="Обработка лог файлов.")
    parser.add_argument(
        "--file",
        nargs="+",
        required=True,
        help="Путь к лог-файлу/файлам для обработки.",
    )
    parser.add_argument(
        "--report",
        choices=["average"],
        required=True,
        help="Тип отчёта для формирования (например, average).",
    )
    parser.add_argument(
        "--date", help="Фильтрация по дате в формате ГГГГ-ММ-ДД (например, 2025-08-01)."
    )

    return parser.parse_args()


def main() -> None:
    """
    Инициализация скрипта для обработки логов.
    """
    args = parse_args()

    try:
        if args.report == "average":
            report = AverageReport()  # отчет вызов класса
    except BaseException as e:
        logger.error(f"Отчет не реализован {str(e)}")
        raise

    log_processing(args.file, report, args.date)

    headers, data = report.final_report()
    print(tabulate(data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()

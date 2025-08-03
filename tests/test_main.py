import argparse
import builtins

import src.main as main


def test_main(monkeypatch, test_report):
    """
    Тест на основную функцию запуска main Обработки логов
    :param monkeypatch: замена зависимостей на тестовые заглушки
    :param test_report: тестовый отчет
    :return:
    """

    # Патчим аргументы
    monkeypatch.setattr(
        main,
        "parse_args",
        lambda: argparse.Namespace(file=["logfile.log"], report="average", date=None),
    )

    # Патчим AverageReport - возвращает фикстуру отчета test_report
    monkeypatch.setattr(main, "AverageReport", lambda: test_report)

    # Патчим log_processing, проверка вызова
    called = {}

    def fake_log_processing(files, report, date_filter):
        called["files"] = files
        called["report"] = report
        called["date_filter"] = date_filter

    monkeypatch.setattr(main, "log_processing", fake_log_processing)

    # Вывод
    output = []
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: output.append(args))

    main.main()

    assert called["files"] == ["logfile.log"]
    assert called["report"] == test_report
    assert called["date_filter"] is None

    assert test_report.final_called
    assert any("handler" in str(line) for line in output)

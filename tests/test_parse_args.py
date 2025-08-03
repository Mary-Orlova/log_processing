import sys

import pytest

import src.main as main


def test_parse_args(monkeypatch):
    """
    Тест на корректность парсинга аргументов
    """
    args_list = [
        "prog",
        "--file",
        "log1.log",
        "log2.log",
        "--report",
        "average",
        "--date",
        "2025-08-01",
    ]
    monkeypatch.setattr(sys, "argv", args_list)

    args = main.parse_args()
    assert args.file == ["log1.log", "log2.log"]
    assert args.report == "average"
    assert args.date == "2025-08-01"

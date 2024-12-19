#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from example_1 import Staff, Worker, IllegalYearError, UnknownCommandError


def test_add_worker():
    staff = Staff()
    staff.add("Иванов И.Б.", "Студент", 2022)
    assert len(staff.workers) == 1
    assert staff.workers[0] == Worker(name="Иванов И.Б.", post="Студент", year=2022)


def test_add_worker_illegal_year():
    staff = Staff()
    with pytest.raises(IllegalYearError):
        staff.add("Jane Doe", "Преподаватель", 2025)

    with pytest.raises(IllegalYearError):
        staff.add("Jane Doe", "Преподаватель", -1)


def test_select_workers():
    staff = Staff()
    staff.add("Кожуховский В.А.", "Студент", 2022)
    staff.add("Иванов И.И.", "Студент", 2018)
    staff.add("Иванов И.А.", "Преподаватель", 2015)

    selected = staff.select(5)
    assert len(selected) == 2
    assert selected[0].name == "Иванов И.А."
    assert selected[1].name == "Иванов И.И."


def test_select_no_workers():
    staff = Staff()
    staff.add("Кожуховский В.А.", "Студент", 2022)
    selected = staff.select(5)
    assert len(selected) == 0


def test_str_representation():
    staff = Staff()
    staff.add("Кожуховский В.А.", "Студент", 2022)
    staff.add("Иванов И.И.", "Студент", 2022)
    expected_output = (
        "+------+--------------------------------+----------------------+----------+\n"
        "|  №   |             Ф.И.О.             |      Должность       |   Год    |\n"
        "+------+--------------------------------+----------------------+----------+\n"
        "|    1 | Иванов И.И.                    | Студент              |     2022 |\n"
        "|    2 | Кожуховский В.А.               | Студент              |     2022 |\n"
        "+------+--------------------------------+----------------------+----------+"
    )
    assert str(staff) == expected_output


def test_unknown_command_error():
    with pytest.raises(UnknownCommandError):
        raise UnknownCommandError("invalid_command")

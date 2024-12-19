#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import date
from example_1 import Staff, Worker


def test_add_worker():
    staff = Staff()
    staff.add("Иванов И.Б.", "Студент", 2022)
    assert len(staff.workers) == 1
    assert staff.workers[0] == Worker(name="Иванов И.Б.", post="Студент", year=2022)


def test_add_worker_sorted():
    staff = Staff()
    staff.add("Кожуховский В.А.", "Студент", 2022)
    staff.add("Иванов И.Б.", "Преподаватель", 2020)
    assert staff.workers[0].name == "Иванов И.Б."
    assert staff.workers[1].name == "Кожуховский В.А."


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
    staff.add("Кожуховский В.А.", "Студент", date.today().year)
    selected = staff.select(5)
    assert len(selected) == 0


def test_str_representation():
    staff = Staff()
    staff.add("Кожуховский В.А.", "Студент", 2022)
    staff.add("Иванов И.И.", "Студент", 2022)
    str_repr = str(staff)

    assert "Иванов И.И." in str_repr
    assert "Кожуховский В.А." in str_repr
    assert "Студент" in str_repr
    assert "2022" in str_repr


def test_save_and_load(tmp_path):
    # Создаем временный файл
    file_path = tmp_path / "workers.xml"

    # Создаем и сохраняем данные
    staff = Staff()
    staff.add("Иванов И.Б.", "Студент", 2022)
    staff.save(str(file_path))

    # Создаем новый объект и загружаем данные
    new_staff = Staff()
    new_staff.load(str(file_path))

    # Проверяем загруженные данные
    assert len(new_staff.workers) == 1
    assert new_staff.workers[0].name == "Иванов И.Б."
    assert new_staff.workers[0].post == "Студент"
    assert new_staff.workers[0].year == 2022

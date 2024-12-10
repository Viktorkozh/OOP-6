#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Разработайте аналог утилиты tree в Linux. Используйте возможности модуля
# argparse для управления отображением дерева каталогов файловой системы.
# Добавьте дополнительные уникальные возможности в данный программный продукт.

# Выполнить индивидуальное задание 2 лабораторной работы 2.19, добавив
# аннтотации типов. Выполнить проверку программы с помощью утилиты mypy.

# Выполнить индивидуальное задание лабораторной работы 4.5,
# использовав классы данных, а также загрузку и сохранение данных в формат XML.

import os
import argparse
import stat


def is_hidden(filepath: str) -> bool:
    if os.path.basename(filepath).startswith("."):
        return True
    try:
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    except AttributeError:
        return False


def list_files(
    startpath: str, depth: int = -1, level: int = 0, show_hidden: bool = False
) -> None:
    if depth == 0:
        return
    if level == 0:
        print(startpath)

    for element in os.listdir(startpath):
        path = os.path.join(startpath, element)
        indent = " " * 4 * level
        if (element.startswith(".") or is_hidden(path)) and not show_hidden:
            continue
        if os.path.isdir(path):
            print(f"{indent}└── {element}/")
            list_files(path, depth - 1, level + 1, show_hidden)
        else:
            if element.startswith(".") or is_hidden(path):
                # Скрытые файлы будут отображаться на сером фоне
                print(f"{indent}└── \033[100m{element}\033[0m")
            else:
                print(f"{indent}└── {element}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Display directory tree")
    parser.add_argument("path", nargs="?", default=".", help="Directory path")
    parser.add_argument("-d", "--depth", type=int, default=-1, help="Depth of the tree")
    parser.add_argument("--hidden", action="store_true", help="Show hidden files")
    args = parser.parse_args()

    list_files(args.path, args.depth, show_hidden=args.hidden)


if __name__ == "__main__":
    main()

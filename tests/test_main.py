#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import tempfile
import xml.etree.ElementTree as ET
from main import (
    list_files,
    save_to_xml,
    load_from_xml,
    print_directory,
    is_hidden,
    File,
    Directory,
)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_is_hidden():
    assert is_hidden(".hidden_file") == True
    assert is_hidden("visible_file") == False


def test_list_files(temp_dir):
    os.makedirs(os.path.join(temp_dir, "subdir"))
    with open(os.path.join(temp_dir, "file1.txt"), "w") as f:
        f.write("test content")
    with open(os.path.join(temp_dir, ".hidden_file"), "w") as f:
        f.write("hidden content")

    directory = list_files(temp_dir, depth=1)
    assert len(directory.files) == 1
    assert directory.files[0].name == "file1.txt"
    assert len(directory.subdirs) == 1

    directory = list_files(temp_dir, depth=1, show_hidden=True)
    assert len(directory.files) == 2
    assert {f.name for f in directory.files} == {"file1.txt", ".hidden_file"}


def test_save_and_load_xml(temp_dir):
    directory = Directory(path=temp_dir)
    directory.files = [
        File(name="file1.txt", size=100),
        File(name="file2.txt", size=200),
    ]
    subdir = Directory(path=os.path.join(temp_dir, "subdir"))
    subdir.files = [File(name="subfile.txt", size=50)]
    directory.subdirs = [subdir]

    xml_path = os.path.join(temp_dir, "test.xml")
    save_to_xml(directory, xml_path)
    assert os.path.exists(xml_path)

    loaded_directory = load_from_xml(xml_path)
    assert loaded_directory.path == temp_dir
    assert len(loaded_directory.files) == 2
    assert len(loaded_directory.subdirs) == 1
    assert loaded_directory.subdirs[0].path == os.path.join(temp_dir, "subdir")


def test_print_directory(temp_dir, capsys):
    directory = Directory(path=temp_dir)
    directory.files = [
        File(name="file1.txt", size=100),
        File(name="file2.txt", size=200),
    ]
    subdir = Directory(path=os.path.join(temp_dir, "subdir"))
    subdir.files = [File(name="subfile.txt", size=50)]
    directory.subdirs = [subdir]

    print_directory(directory)
    captured = capsys.readouterr()

    assert "file1.txt (100 bytes)" in captured.out
    assert "file2.txt (200 bytes)" in captured.out
    assert "subdir/" in captured.out
    assert "subfile.txt (50 bytes)" in captured.out


def test_xml_element_creation(temp_dir):
    directory = Directory(path=temp_dir)
    directory.files = [File(name="file1.txt", size=100)]

    xml_element = save_to_xml(directory, ET.Element("root"))

    assert xml_element.get("path") == temp_dir
    file_elements = xml_element.findall("file")
    assert len(file_elements) == 1
    assert file_elements[0].get("name") == "file1.txt"
    assert file_elements[0].get("size") == "100"

import streamlit as st
from library.custom_logging import setup_logging
from library.IndentationHelper import IndentationHelper
from config_file import load_config, is_value_changed, save_config
from PIL import Image, ImageDraw, ImageFont
import string
import os
import torchvision.transforms as transforms
import numpy as np
import math
import cv2
from library.components import add_text_to_image
from datetime import datetime
import time
import shutil
from stqdm import stqdm
import library.style_button as sb
import json
import pickle
import torch
import pandas as pd
from joblib import Memory
# хранение в памяти
memory = Memory(location="./cachedir", verbose=0)


class PageTools:

    def __init__(self):

        # Назначение переменной логирования
        self.log = setup_logging()
        # Загрузка конфигурационного файла
        self.config_data = load_config()
        # Класс функций для отступов
        self.helper = IndentationHelper()
        # Обновляем изменяемые переменные после предыдущего запуска
        self._init_params()
        # Выгружаем и инициализируем переменные стандартных путей
        self._init_default_path()
        # Создаем директории, если они не существуют
        self._make_os_dir()
        # Инициализируем листы
        self._init_list()
        # Инициализируем словари
        self._init_dir()

    def _time(self):
        self.timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")

    def _init_default_path(self):
        paths = self.config_data["dir_paths"]
        for key, value in paths.items():
            setattr(self, key, self.config_data[f"{value}"])

    def _init_params(self):
        params = self.config_data["dir_params"]
        for key, value in params.items():
            setattr(self, key, self.config_data[f"{value}"])

    def _init_list(self):
        lists = self.config_data["dir_lists"]
        for key, value in lists.items():
            setattr(self, key, self.config_data[f"{value}"])

    def _init_dir(self):
        # Словарь для хранения информации
        dirs = self.config_data["dir_dirs"]
        for key, value in dirs.items():
            setattr(self, key, self.config_data[f"{value}"])

    def _make_os_dir(self):
        paths = self.config_data["dir_paths"]
        for key, value in paths.items():
            if key is not "script_path":
                print(self.config_data[f"{value}"])
                os.makedirs(self.config_data[f"{value}"], exist_ok=True)

    def _clean_temp(self):
        pass

    def _refresh_inference_params(self):
        pass

    def save_to_json(self, data, file_path):
        """
        Сохраняет данные в формате JSON в указанный файл.

        Параметры:
        - data: словарь или список данных для сохранения в JSON.
        - file_path: строка, путь к файлу JSON.

        Возвращает:
        - None
        """

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def add_key_value(self, dictionary, key, value):
        """
        Добавляет новый ключ и значение в словарь.

        Параметры:
        - dictionary: словарь, в который добавляется новый ключ и значение.
        - key: ключ для добавления.
        - value: значение для добавления.

        Возвращает:
        - dictionary: словарь с добавленным ключом и значением.
        """
        dictionary[key] = value
        return dictionary

    def run(self):
        """
        Запуск приложения.
        """

        # Содержимое страницы
        self.title_page()

        # Контейнер ввода параметров
        self.input_param_container()

    def title_page(self):
        """
        Содержимое страницы ввиде вступительного текста.
        """
        self.helper.create_indentations(1)
        self.progress = st.container()

    def input_param_container(self):

        # Контейнер для ввода параметров
        self.cont_param = st.container()


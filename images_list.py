import os
from tkinter import *
from tkinter.ttk import *
from image_processor import ImageProcessor
from time import sleep

on_click = "<Button-1>"

class ImagesList():
    """
    Класс описывает виджет списка изображений с кнопками для работы с выделением
    """

    def __init__(self, root):
        self.root = root
        self.opened_path = None
        self.opened_files = []

        buttons_frame = Frame(self.root)
        buttons_frame.pack(side = 'top', fill = 'x')

        select_all_button = Button(buttons_frame, text = 'Выбрать все')
        select_all_button.grid(row = 0, column = 0)
        select_all_button.bind(on_click, self.select_all)

        select_new_button = Button(buttons_frame, text = 'Выбрать не уменьшенные')
        select_new_button.grid(row = 0, column = 1)
        select_new_button.bind(on_click, self.select_new)

        select_resized_button = Button(buttons_frame, text = 'Выбрать уменьшенные')
        select_resized_button.grid(row = 0, column = 2)
        select_resized_button.bind(on_click, self.select_resized)

        self.progressbar = Progressbar(self.root, orient=HORIZONTAL, length=200, mode='determinate')
        self.progressbar.pack(side = 'bottom', fill = 'x')

        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side = 'right', fill = 'y')

        self.files_list = Listbox(
            self.root, 
            height = 400, 
            yscrollcommand = scrollbar.set,
            selectmode = EXTENDED
        )
        self.files_list.pack(fill = BOTH)
        scrollbar.config(command = self.files_list.yview)

    def get_files_list(self, path):
        """
        Возвращает список изображений (JPG) в папке path
        """
        def is_jpeg_file(filename):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext and ext in ('.jpg', '.jpeg'):
                    return True
            return False

        dir_items_list = os.listdir(path)
        files_list = []
        for item in dir_items_list:
            if is_jpeg_file(item): files_list.append(item)

        return sorted(files_list)

    def read_files_in(self, path = None):
        """
        Заполняет список изображений в окошко
        """
        if path == None: path = self.opened_path

        self.opened_path = path
        self.files_list.delete(0, END)
        self.opened_files = []
        self.opened_files = self.get_files_list(path)
        for num, filename in enumerate(self.opened_files):
            self.files_list.insert(END, "{0}. {1}".format(num, filename) )

    def get_selected_files(self):
        """
        Возвращает список индексов выбраных файлов
        """
        return self.files_list.curselection()

    def resize_selected(self):
        """
        Уменьшает все выбранные изображения
        """
        selected_items = self.get_selected_files()
        selected_files = []
        for index in selected_items:
            one = os.path.join(self.opened_path, self.opened_files[int(index)])
            selected_files.append(one)

        self.progressbar['maximum'] = len(selected_files)
        for num, one in enumerate(selected_files):
            ImageProcessor.shrink_2x(one)
            self.progressbar['value'] = num + 1
            self.root.update()
        self.read_files_in()

    def select_all(self, event):
        """
        Отмечает выбранными все изображения в списке
        """
        self.files_list.select_set(0, END)

    def select_new(self, event):
        """
        Отмечает выбранными не уменьшенные (без суффикса _resized) изображения
        """
        self.files_list.select_clear(0, END)
        for num, one in enumerate(self.opened_files):
            if not '_resized' in one:
                self.files_list.select_set(num)

    def select_resized(self, event):
        """
        Отмечает выбранными уже уменьшенные (с _resized) изображения
        """
        self.files_list.select_clear(0, END)
        for num, one in enumerate(self.opened_files):
            if '_resized' in one:
                self.files_list.select_set(num)

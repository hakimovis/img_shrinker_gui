#!/usr/bin/env python3.2

import os
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from images_list import ImagesList

on_click = "<Button-1>"

class AppController():
    def __init__(self):
        self.cfg = {'curr_path': os.path.dirname(os.path.abspath(__file__))}
        self.cfg_path = os.path.join(self.cfg['curr_path'], 'resizer.cfg')
        self.read_cfg()
        self.draw_root_window()
        self.images_list = ImagesList(self.root)
        self.read_files_in()

        self.root.mainloop()

    def draw_root_window(self):
        root = Tk()
        root.config(height = 300, width = 600)
        root.geometry('500x400')
        root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root = root

        toolbar = Frame(root)
        toolbar.pack(side = TOP, fill = 'x')

        open_folder_button = Button(toolbar, text = 'Открыть папку')
        open_folder_button.bind(on_click, self.open_dir)
        open_folder_button.grid(sticky = 'w', row = 0, column = 0)

        resize_button = Button(toolbar, text = 'Уменьшить выбранные')
        resize_button.grid(sticky = 'e', row = 0, column = 1)
        resize_button.bind(on_click, self.resize_images)

        self.path_input = Entry(toolbar, text = '', width = 60)
        self.path_input.grid(row = 1, column = 0, columnspan = 2)

        Label(root, text = 'Это уменьшалка для больших фотографий').pack(side = 'bottom')

    def open_dir(self, ev):
        path = tkinter.filedialog.Directory(
            self.root, initialdir = self.cfg['last_opened']
        ).show()
        if not path: return
        self.read_files_in(path)

    def resize_images(self, ev):
        self.images_list.resize_selected()

    def read_files_in(self, path = None):
        if path == None: path = self.cfg.get('last_opened', self.cfg['curr_path'])
        self.cfg['last_opened'] = path
        self.images_list.read_files_in(path)
        print("reading %s"%path)
        self.path_input.delete(0, END)
        self.path_input.insert(0, path)

    def read_cfg(self):
        if os.path.isfile(self.cfg_path):
            lines = open(self.cfg_path, 'r').readlines()
            for one in lines:
                if not ":" in one: continue
                parts = one.split(":")
                self.cfg[parts[0]] = ":".join(parts[1:]).strip() # На случай, если там были двоеточия
            print("Config read: {0}".format(self.cfg))
        else:
            print("No config file...")
    def write_cfg(self):
        print("Saving config: {0}".format(self.cfg))
        f = open(self.cfg_path, 'w')
        for key, value in self.cfg.items():
            if key: f.write("{0}: {1}\n".format(key, value))
        f.close()

    def close_app(self):
        self.write_cfg()
        self.root.destroy()

app = AppController()
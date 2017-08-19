# -*- coding: utf-8 -*-

import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex as C
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp
from kivy.properties import ObjectProperty

# Using Material Design Widgets
from kivymd.theming import ThemeManager
from kivymd.date_picker import MDDatePicker

Window.maximize()

from kivy import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

class Inventory(BoxLayout):
    previous_date = ObjectProperty()

    def products_date_pick(self):
        MDDatePicker(self.set_products_date).open()

    def set_products_date(self, date_obj):
        self.previous_date = date_obj
        self.ids.products_date_label.text = str(date_obj)

    def imports_date_pick(self):
        MDDatePicker(self.set_imports_date).open()

    def set_imports_date(self, date_obj):
        self.previous_date = date_obj
        self.ids.imports_date_label.text = str(date_obj)

    def exports_date_pick(self):
        MDDatePicker(self.set_exports_date).open()

    def set_exports_date(self, date_obj):
        self.previous_date = date_obj
        self.ids.exports_date_label.text = str(date_obj)

class Sales(BoxLayout):
    previous_date = ObjectProperty()

    def sale_date_pick(self):
        MDDatePicker(self.set_previous_date).open()

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj
        self.ids.sale_date_picker_label.text = str(date_obj)

class Manager(ScreenManager):
    pass

class MainPageButton(Button):
    pass

class MainLayout(BoxLayout):
    def return_to_page(self, page):
        self.ids.manager.current = page


class PharmacyApp(App):
    theme_cls = ThemeManager()

    def build(self):
        return MainLayout()

    def on_pause(self):
        return True

    def on_stop(self):
        pass

if __name__ == '__main__':
    LabelBase.register(name='PICTO', fn_regular='includes/modernpics.otf')
    LabelBase.register(name='rap', fn_regular='includes/raphaelicons-webfont.ttf')
    PharmacyApp().run()
# -*- coding: utf-8 -*-

import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex as C
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
import math

# Using Material Design Widgets
from kivymd.theming import ThemeManager
from kivymd.button import MDIconButton
from kivymd.label import MDLabel
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField
from kivymd.date_picker import MDDatePicker
from kivymd.snackbar import Snackbar

# Inventory
from inventory import *
# Search
from search import *

# Fonts
from iconfonts import *
from os.path import join, dirname

# TODO
"""
The Problem Of Import Details And Export Details
"""

Window.maximize()

from kivy import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# SALES PART
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
    layout_content = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)


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
    IconFonts().register('default_font', 'includes/ionicons/ionicons.ttf',
                         join(dirname(__file__), 'includes/ionicons/ionicons.fontd'))
    IconFonts().register('fontawesome', 'includes/fontaweasome/fontawesome-webfont.ttf',
                         join(dirname(__file__), 'includes/fontaweasome/font-awesome.fontd'))
    PharmacyApp().run()
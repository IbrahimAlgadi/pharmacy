from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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

# Exports
from export_details_table import *
from exports_table import *
from import_details_table import *
from imports_table import *
from suppliers_table import *
from categories_table import *
from products_table import *
# INVENTORY PART

class Inventory(BoxLayout):
    previous_date = ObjectProperty()
    layout_content_1 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)
        print self.layout_content_1
        # self.layout_content_1.bind(minimum_height=self.layout_content_1.setter('height'))

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




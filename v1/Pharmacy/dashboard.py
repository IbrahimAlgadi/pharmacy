from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
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


class Dashboard(BoxLayout):
    pass

class DashboardDisplay(GridLayout):
    def __int__(self, **kwargs):
        self.bind(minimum_height=self.setter('height'))
        super(DashboardDisplay, self).__init__(**kwargs)

    def on_children(self, instance, value):
        self.bind(minimum_height=self.setter('height'))

class CustomLayout(GridLayout):
    background_image = ObjectProperty(
        Image(source='img/figure1.zip',anim_delay=.1)
    )
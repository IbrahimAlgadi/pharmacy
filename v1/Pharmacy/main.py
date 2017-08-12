import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from  kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex as C
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

Window.maximize()

from kivy import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')


class Manager(ScreenManager):
    pass

class MainPageButton(Button):
    pass

class MainLayout(BoxLayout):
    def return_to_page(self, page):
        self.ids.manager.current = page


class PharmacyApp(App):
    def build(self):
        return MainLayout()
    def printArko(self, event):
        print 'arkon'

if __name__ == '__main__':
    LabelBase.register(name='PICTO', fn_regular='includes/modernpics.otf')
    LabelBase.register(name='rap', fn_regular='includes/raphaelicons-webfont.ttf')
    PharmacyApp().run()
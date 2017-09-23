from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.utils import get_color_from_hex as C

class DropDownButton(Button):
    father = ObjectProperty(None)
    dist_id = None
    button_number = NumericProperty(0)
    def __init__(self, obj,number,id, **kwargs):
        self.father = obj
        self.dist_id = id
        self.button_number = number
        kwargs['background_normal'] = ''
        kwargs['text_size'] = self.size
        kwargs['halign'] = 'left'
        kwargs['valign'] = 'top'
        if self.button_number % 2 == 1:
            kwargs['background_color'] = C('#1976d2')
        else:
            kwargs['background_color'] = C('#2196f3')
        super(DropDownButton, self).__init__(**kwargs)
    def on_release(self):
        self.father.text = self.dist_id

class TextInputWithDropper(BoxLayout):
    def __init__(self, **kwargs):
        self.padding = '5px'
        self.spacing = '10px'
        super(TextInputWithDropper, self).__init__(**kwargs)

class Droppper(DropDown):
    def __init__(self, **kwargs):
        super(Droppper, self).__init__(**kwargs)

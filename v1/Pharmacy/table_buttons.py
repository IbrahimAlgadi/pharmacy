from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
# Using Material Design Widgets
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex as C
from kivymd.button import MDIconButton
from kivymd.textfields import MDTextField

# USABLE WIDGETS
class DialogTextInput(MDTextField):
    def __init__(self,text,**kwargs):
        # kwargs['hint_text'] = "Destination"
        kwargs['text'] = text
        super(DialogTextInput, self).__init__(**kwargs)

# Boxes I use To Add Labels
class DataWidget(BoxLayout):
    def __init__(self, counter, **kwargs):
        super(DataWidget, self).__init__(**kwargs)

class DataWidget2(BoxLayout):
    def __init__(self, counter, **kwargs):
        super(DataWidget2, self).__init__(**kwargs)

# Data Labels I am Using
class DataLabel(Label):
    pass

# Edit Button I am using
class EditButton(MDIconButton):
    rec_id = 0
    obj = ObjectProperty(None)
    def __init__(self,obj, rec_id, **kwargs):
        self.rec_id = rec_id
        self.obj = obj
        kwargs['icon'] = 'pen'
        kwargs['theme_text_color'] = 'Custom'
        kwargs['text_color'] = C("#76ff03")
        super(EditButton, self).__init__(**kwargs)

    def on_release(self):
        self.obj.edit_data(self.rec_id)


# Delete Button I am Using
class DeleteButton(MDIconButton):
    obj = ObjectProperty(None)
    fat = ObjectProperty(None)
    rec_id = 0
    # getting a ExportTable1 instance fat
    # and DataWidget object to delete it from the database
    def __init__(self,fat , obj, rec_id, **kwargs):
        self.rec_id = rec_id
        # using object property magic
        self.obj = obj
        self.fat = fat
        kwargs['icon'] = 'delete'
        kwargs['theme_text_color'] = 'Custom'
        kwargs['text_color'] = C("#ff1744")
        super(DeleteButton, self).__init__(**kwargs)
        # MDIconButton.text_color

    def on_release(self):
        print "delete record : ",self.rec_id
        self.parent.parent.parent.remove_widget(self.obj)
        self.fat.delete_data(self.rec_id)
        self.fat.call_load()
# USABLE WIDGETS
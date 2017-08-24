from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex as C
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
import math

# Using Material Design Widgets
from kivymd.button import MDIconButton
from kivymd.label import MDLabel
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField
from kivymd.date_picker import MDDatePicker
from kivymd.snackbar import Snackbar

# database
from imports import *
from table_buttons import *
from supplier import *

from dropdown_tools import *

class SupplierButtonDropper(Button):
    _id = None
    number = NumericProperty(0)
    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['background_normal'] = ''
        kwargs['background_color'] = C('#1976d2')
        kwargs['text'] = 'Select'
        super(SupplierButtonDropper, self).__init__(**kwargs)

    def call_the_drop(self, text_input_object):
        self.textinput = text_input_object
        self.dropdown = Droppper(size_hint=(None, None), size=(90, 200))
        data_object = Supplier()
        data = sorted(list(data_object.get_suppliers()))
        # data_object = Supplier()
        data_dict = data_object.get_suppliers()
        for key in data:
            _id = str(data_dict.get(key)['id'])
            destination = data_dict.get(key)['name']
            btn = DropDownButton(self.textinput,self.number, _id, text=destination, size_hint_y=None, height=44)
            self.number += 1
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.number = 0
        self.dropdown.open(self)

class ImportTable1(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    data_object = Import()
    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 0
    offset = 4
    _data = None

    def __init__(self, **kwargs):
        super(ImportTable1, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()
        try:
            self.k_id = sorted([int(x) for x in self._data])[-1] + 1
            print self.parent
        except:
            print "Error"

    def delete_data(self, id):
        try:
            self.data_object.id = id
            self.data_object.delete_import()
            self.pagination_next(self.current)
        except KeyError:
            print "Key Not Found"

    def call_load(self):
        Clock.schedule_once(self.load_data)

    def calc_pages(self, pages, num_pages, num_page):
        pages_dict = dict()
        pages_lens = list()
        num = 0
        while num <= len(self.pages):
            pages_lens.append(num)
            num = num + self.offset
        pages_lens.append(len(self.pages))
        for num in range(0, num_pages):
            pages_dict[num + 1] = pages[pages_lens[num]:pages_lens[num + 1]]
        page_count = len(pages_dict.keys())
        return num_page, page_count, pages_dict[num_page]

    def pagination_next(self, page=1):
        self.current = int(page)
        self.pages = sorted(list(self.data_object.get_imports()))
        no_pages = int(math.ceil(len(self.pages) / float(self.offset)))
        try:
            self.current, page_count, self.page = self.calc_pages(self.pages, no_pages, self.current)
            self._data = self.page
            self.call_load()
            if self.current == page_count:
                deactivate = True
            else:
                deactivate = False
        except:
            deactivate = True
            self.current = 1
        return deactivate, str(self.current)

    def pagination_prev(self, page=1):
        self.current = int(page)
        self.pages = sorted(list(self.data_object.get_imports()))
        no_pages = int(math.ceil(len(self.pages) / float(self.offset)))
        try:
            self.current, page_count, self.page = self.calc_pages(self.pages, no_pages, self.current)
            self._data = self.page
            self.call_load()
            if self.current == 1:
                deactivate = True
            else:
                deactivate = False
        except:
            deactivate = True
            self.current = 1
        return deactivate, str(self.current)

    def load_data(self, dt):
        self.clear_widgets()
        self.count = self.current * self.offset - self.offset + 1
        data_object = Supplier()
        data_dict = data_object.get_suppliers()
        for key in self._data:
            id = str(self.data_object.get_imports().get(key)['id'])
            receipt_number = self.data_object.get_imports().get(key)['receipt_number']
            date = str(self.data_object.get_imports().get(key)['date'])
            supplier_id = str(data_dict.get(str(self.data_object.get_imports().get(key)['supplier_id']))['name'])
            status = str(self.data_object.get_imports().get(key)['status'])

            if self.count % 2 == 1:
                self.d = DataWidget2(self.count,
                                     size_hint_y=None,
                                     height='40px')
            else:
                self.d = DataWidget(self.count,
                                    size_hint_y=None,
                                    height='40px')

            b = EditButton(self, id, text="edit")
            de = DeleteButton(self, self.d, id, text="delete")
            option = BoxLayout()

            option.add_widget(b)
            option.add_widget(de)

            self.d.add_widget(DataLabel(text=str(self.count)))
            self.d.add_widget(DataLabel(text=receipt_number))
            self.d.add_widget(DataLabel(text=date))
            self.d.add_widget(DataLabel(text=supplier_id))
            self.d.add_widget(DataLabel(text=status))
            self.d.add_widget(option)

            super(ImportTable1, self).add_widget(self.d)
            self.count += 1

    def save_edited_data(self, id, receipt_number, date, supplier_id,status):
        self.data_object.id = id
        self.data_object.receipt_number = receipt_number
        self.data_object.date = date
        self.data_object.supplier_id = supplier_id
        self.data_object.status = status
        self.data_object.update_import()
        self.dialog.dismiss()
        self.pagination_next()

    def edit_data(self, id):
        receipt_ = self.data_object.get_imports().get(id)['receipt_number']
        dat = str(self.data_object.get_imports().get(id)['date'])
        supplier_ = str(self.data_object.get_imports().get(id)['supplier_id'])
        stat = str(self.data_object.get_imports().get(id)['status'])
        b = GridLayout(size_hint=(None, None),
                       height='200px',
                       width="400px",
                       cols=2
                       )
        receipt_number = DialogTextInput(receipt_)
        date = DialogTextInput(dat)
        supplier_id = DialogTextInput(supplier_)
        status = DialogTextInput(stat)

        b.add_widget(MDLabel(
                             text="Receipt Number",
                             size_hint_x=None,
                             width="90px"
                             ))
        b.add_widget(receipt_number)
        b.add_widget(MDLabel(
            text="Date",
            size_hint_x=None,
            width="90px"))
        b.add_widget(date)
        b.add_widget(MDLabel(
                             text="Suppler ID",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(supplier_id)
        b.add_widget(MDLabel(id='date',
                             text="Status",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(status)

        self.dialog = MDDialog(title="This is a test dialog",
                               content=b,
                               size_hint=(None, None),
                               height="500px",
                               width="500px",
                               auto_dismiss=False)
        self.dialog.add_action_button("Save",
                                      action=lambda *x: self.save_edited_data(id, receipt_number.text, date.text,
                                                                              supplier_id.text,status.text))
        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def add_data(self, receipt_number, date, supplier_id,status):
        self.data_object.receipt_number = receipt_number
        self.data_object.date = date
        self.data_object.supplier_id = supplier_id
        self.data_object.status = status
        if receipt_number != '' and date!= '' and supplier_id!= '' and status != '':
            self.data_object.insert_import()
        else:
            Snackbar(text=" You Need To Fill All Fields ").show()
        self.call_load()
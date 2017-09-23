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
import _mysql_exceptions

# database
from import_detail import *
from imports import *
from product import *
from table_buttons import *

from dropdown_tools import *

class ImportImportDetailsButtonDropper(Button):
    _id = None
    number = NumericProperty(0)
    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['background_normal'] = ''
        kwargs['background_color'] = C('#1976d2')
        kwargs['text'] = 'Select'
        super(ImportImportDetailsButtonDropper, self).__init__(**kwargs)

    def call_the_drop(self, text_input_object):
        self.textinput = text_input_object
        self.dropdown = Droppper(size_hint=(None, None), size=(90, 200))
        data_object = Import()
        data = sorted(list(data_object.get_imports()))
        data_dict = data_object.get_imports()
        for key in data:
            _id = str(data_dict.get(key)['id'])
            destination = data_dict.get(key)['receipt_number']
            btn = DropDownButton(self.textinput,self.number, _id, text=destination, size_hint_y=None, height=44)
            self.number += 1
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.number = 0
        self.dropdown.open(self)

class ProductImportDetailsButtonDropper(Button):
    _id = None
    number = NumericProperty(0)
    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['background_normal'] = ''
        kwargs['background_color'] = C('#1976d2')
        kwargs['text'] = 'Select'
        super(ProductImportDetailsButtonDropper, self).__init__(**kwargs)

    def call_the_drop(self, text_input_object):
        self.textinput = text_input_object
        self.dropdown = Droppper(size_hint=(None, None), size=(90, 200))
        data_object = Product()
        data = sorted(list(data_object.get_products()))
        data_dict = data_object.get_products()
        for key in data:
            _id = str(data_dict.get(key)['id'])
            destination = data_dict.get(key)['brandname']
            btn = DropDownButton(self.textinput,self.number, _id, text=destination, size_hint_y=None, height=44)
            self.number += 1
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.number = 0
        self.dropdown.open(self)

class ImportTable2(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    data_object = ImportDetail()
    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 0
    offset = 4
    _data = None
    data_in_page = None

    def __init__(self, **kwargs):
        super(ImportTable2, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()

    def delete_data(self, id):
        try:
            self.data_object.import_id = id
            self.data_object.delete_import_detail()
            self.pagination_next(self.current)
        except KeyError:
            Snackbar(text=" Key Not Found ").show()
        except _mysql_exceptions.IntegrityError:
            Snackbar(text="Cannot delete or update a parent row: a foreign key constraint fails").show()

    def call_load(self):
        Clock.schedule_once(self.load_data)

    def pagination_next(self, page=1):
        self.current = int(page)
        no_pages = int(math.ceil(float(self.data_object.count_import_detail()) / float(self.offset)))
        if self.current <= no_pages:
            offset = (self.current - 1) * self.offset
            self.data_in_page = self.data_object.get_import_details_page(offset, self.offset)
            self.pages = list(self.data_in_page)
            self._data = self.pages
            self.call_load()
        else:
            deactivate = False
        if self.current >= no_pages:
            deactivate = True
            self.current = no_pages
        else:
            deactivate = False
        return deactivate, str(self.current)

    def pagination_prev(self, page=1):
        self.current = int(page)
        if self.current > 0:
            offset = (self.current - 1) * self.offset
            self.data_in_page = self.data_object.get_import_details_page(offset, self.offset)
            self.pages = list(self.data_in_page)
            self._data = self.pages
            self.call_load()
        else:
            deactivate = True
            self.current = 1
        if self.current == 1:
            deactivate = True
        else:
            deactivate = False
        return deactivate, str(self.current)

    def load_data(self, dt):
        self.clear_widgets()
        self.count = self.current * self.offset - self.offset + 1
        import_data_object = Import()
        import_data_dict = import_data_object.get_imports()
        product_data_object = Product()
        product_data_dict = product_data_object.get_products()
        # print product_data_dict
        # print self._data
        for key in self._data:

            id = str(self.data_in_page.get(key)['id'])
            import_id = import_data_dict.get(str(self.data_in_page.get(key)['import_id']))['receipt_number']
            product_id = product_data_dict.get(str(self.data_in_page.get(key)['product_id']))['brandname']
            # print str(self.data_in_page.get(key)['product_id']) , "=>" , product_id
            quantity = str(self.data_in_page.get(key)['quantity'])
            unitprice = str(self.data_in_page.get(key)['unitprice'])

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
            self.d.add_widget(DataLabel(text=import_id))
            self.d.add_widget(DataLabel(text=product_id))
            self.d.add_widget(DataLabel(text=quantity))
            self.d.add_widget(DataLabel(text=unitprice))
            self.d.add_widget(option)

            super(ImportTable2, self).add_widget(self.d)
            self.count += 1

    def save_edited_data(self, id, import_id, product_id, quantity, unitprice):
        self.data_object.id = id
        self.data_object.import_id = import_id
        self.data_object.product_id = product_id
        self.data_object.quantity = quantity
        self.data_object.status = unitprice
        self.data_object.update_import_detail()
        self.dialog.dismiss()
        self.pagination_next()

    def edit_data(self, id):
        import_id = str(self.data_in_page.get(id)['import_id'])
        product_id = str(self.data_in_page.get(id)['product_id'])
        quantity = str(self.data_in_page.get(id)['quantity'])
        unitprice = str(self.data_in_page.get(id)['unitprice'])
        b = GridLayout(size_hint=(None, None),
                       height='200px',
                       width="400px",
                       cols=2
                       )
        imp_id = DialogTextInput(import_id)
        prod_id = DialogTextInput(product_id)
        qty = DialogTextInput(quantity)
        uprice = DialogTextInput(unitprice)

        b.add_widget(MDLabel(id='destination',
                             text="Import ID",
                             size_hint_x=None,
                             width="90px"
                             ))
        b.add_widget(imp_id)
        b.add_widget(MDLabel(
            text="Product ID",
            size_hint_x=None,
            width="90px"))
        b.add_widget(prod_id)
        b.add_widget(MDLabel(id='date',
                             text="Quantity",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(qty)
        b.add_widget(MDLabel(id='date',
                             text="Unit Price",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(uprice)

        self.dialog = MDDialog(title="Update Import",
                               content=b,
                               size_hint=(None, None),
                               height="500px",
                               width="500px",
                               auto_dismiss=False)
        self.dialog.add_action_button("Save",
                                      action=lambda *x: self.save_edited_data(id, imp_id.text, prod_id.text,
                                                                              qty.text, uprice.text))
        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def add_data(self, import_import_id, import_product_id, import_quantity, import_unitprice):
        self.data_object.import_id = import_import_id
        self.data_object.product_id = import_product_id
        self.data_object.quantity = import_quantity
        self.data_object.unitprice = import_unitprice

        if import_import_id != '' and import_product_id != '' and import_quantity != '' and import_unitprice != '':
            self.data_object.insert_import_detail()
        else:
            Snackbar(text=" You Need To Fill All Fields ").show()
        self.call_load()

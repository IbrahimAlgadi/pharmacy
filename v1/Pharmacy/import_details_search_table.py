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

class ImportSearchTable2(GridLayout):
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

    search_result = data_object.get_import_details()

    _filter_import_id = False
    _filter_product_id = False
    _product_id_search = " AND product_id = {} "
    _filter_quantity = False
    _quantity_search = " AND quantity LIKE {} "
    _filter_unitprice = False
    _unitprice_search = " AND unitprice LIKE {} "

    def __init__(self, **kwargs):
        super(ImportSearchTable2, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()
        try:
            self.k_id = sorted([int(x) for x in self._data])[-1] + 1
            print self.parent
        except:
            print "Error"

    def activate_import_id(self, state):
        if state == 'down':
            self._filter_import_id = True
        else:
            self._filter_import_id = False
            self.search_result = self.data_object.get_import_details()
            self.pagination_next()
            
    def activate_product_id(self, state):
        if state == 'down':
            self._filter_product_id = True
        else:
            self._filter_product_id = False

    def activate_quantity(self, state):
        if state == 'down':
            self._filter_quantity = True
        else:
            self._filter_quantity = False

    def activate_unitprice(self, state):
        if state == 'down':
            self._filter_unitprice = True
        else:
            self._filter_unitprice = False

    def filter(self,import_import_search_id_text, import_product_search_id, import_search_quantity, import_search_unit_price):
        if self._filter_import_id :
            if import_import_search_id_text != '':
                self.sql = "SELECT * FROM import_details WHERE import_id = {} ".format(import_import_search_id_text)
            else:
                self.sql = "SELECT * FROM import_details WHERE import_id LIKE '%%' "
            if self._filter_product_id and import_product_search_id != '':
                self.sql += self._product_id_search.format(import_product_search_id)
            if self._filter_quantity and import_search_quantity != '':
                self.sql += self._quantity_search.format(import_search_quantity)
            if self._filter_unitprice and import_search_unit_price != '':
                self.sql += self._unitprice_search.format(import_search_unit_price)
            s = self.data_object.execute(self.sql)
            name = dict()
            for val in s:
                name[val['import_id']] = val
            self.search_result = name
        else:
            self.search_result = self.data_object.get_import_details()

        self.pagination_next()

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
        self.pages = sorted(list(self.search_result))
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
        self.pages = sorted(list(self.search_result))
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
        import_data_object = Import()
        import_data_dict = import_data_object.get_imports()
        product_data_object = Product()
        product_data_dict = product_data_object.get_products()
        # print product_data_dict
        # print self._data
        for key in self._data:

            id = str(self.search_result.get(key)['id'])
            import_id = import_data_dict.get(str(self.search_result.get(key)['import_id']))['receipt_number']
            product_id = product_data_dict.get(str(self.search_result.get(key)['product_id']))['brandname']
            # print str(self.data_object.get_import_details().get(key)['product_id']) , "=>" , product_id
            quantity = str(self.search_result.get(key)['quantity'])
            unitprice = str(self.search_result.get(key)['unitprice'])

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

            super(ImportSearchTable2, self).add_widget(self.d)
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
        import_id = str(self.data_object.get_import_details().get(id)['import_id'])
        product_id = str(self.data_object.get_import_details().get(id)['product_id'])
        quantity = str(self.data_object.get_import_details().get(id)['quantity'])
        unitprice = str(self.data_object.get_import_details().get(id)['unitprice'])
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


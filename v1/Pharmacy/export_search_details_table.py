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
from export_detail import *
from export import *
from product import *
from table_buttons import *
from dropdown_tools import *

class ExportExportDetailsButtonDropper(Button):
    _id = None
    number = NumericProperty(0)
    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['background_normal'] = ''
        kwargs['background_color'] = C('#1976d2')
        kwargs['text'] = 'Select'
        super(ExportExportDetailsButtonDropper, self).__init__(**kwargs)

    def call_the_drop(self, text_input_object):
        self.textinput = text_input_object
        self.dropdown = Droppper(size_hint=(None, None), size=(90, 200))
        data_object = Export()
        data = sorted(list(data_object.get_exports()))
        data_dict = data_object.get_exports()
        for key in data:
            _id = str(data_dict.get(key)['id'])
            destination = data_dict.get(key)['destination']
            btn = DropDownButton(self.textinput,self.number, _id, text=destination, size_hint_y=None, height=44)
            self.number += 1
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.number = 0
        self.dropdown.open(self)

class ProductExportDetailsButtonDropper(Button):
    _id = None
    number = NumericProperty(0)
    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['background_normal'] = ''
        kwargs['background_color'] = C('#1976d2')
        kwargs['text'] = 'Select'
        super(ProductExportDetailsButtonDropper, self).__init__(**kwargs)

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

class ExportSearchTable2(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    data_object = ExportDetail()
    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 0
    offset = 4
    _data = None

    search_result = data_object.get_export_details()

    _filter_export_id = False
    _filter_product_id = False
    _product_id_search = " AND product_id = {} "
    _filter_quantity = False
    _quantity_search = " AND quantity LIKE '%{}%' "
    _filter_unitprice = False
    _unitprice_search = " AND unitprice LIKE '%{}%' "

    def __init__(self, **kwargs):
        super(ExportSearchTable2, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()

    def activate_export_id(self, state):
        if state == 'down':
            self._filter_export_id = True
        else:
            self._filter_export_id = False
            self.search_result = self.data_object.get_export_details()
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

    def filter(self,export_search_export_id_text, export_search_product_id, export_search_quantity, export_search_unitprice):
        if self._filter_export_id :
            if export_search_export_id_text != '':
                self.sql = "SELECT * FROM export_details WHERE export_id = {} ".format(export_search_export_id_text)
            else:
                self.sql = "SELECT * FROM export_details WHERE export_id LIKE '%%' "
            if self._filter_product_id and export_search_product_id != '':
                self.sql += self._product_id_search.format(export_search_product_id)
            if self._filter_quantity and export_search_quantity != '':
                self.sql += self._quantity_search.format(export_search_quantity)
            if self._filter_unitprice and export_search_unitprice != '':
                self.sql += self._unitprice_search.format(export_search_unitprice)
            s = self.data_object.execute(self.sql)
            name = dict()
            for val in s:
                name[val['export_id']] = val
            self.search_result = name
        else:
            self.search_result = self.data_object.get_export_details()

        self.pagination_next()

    def delete_data(self, id):
        try:
            self.data_object.export_id = id
            self.data_object.delete_export_detail()
            self.pagination_next(self.current)
        except KeyError:
            print "Key Not Found"

        except _mysql_exceptions.IntegrityError:
            Snackbar(text=str("You Connot Delete This Record")).show()


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
        export_data_object = Export()
        export_data_dict = export_data_object.get_exports()
        product_data_object = Product()
        product_data_dict = product_data_object.get_products()
        for key in self._data:
            id = str(self.search_result.get(key)['id'])
            export_id = export_data_dict.get(str(self.search_result.get(key)['export_id']))[
                'destination']
            product_id = product_data_dict.get(str(self.search_result.get(key)['product_id']))[
                'brandname']
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
            self.d.add_widget(DataLabel(text=export_id))
            self.d.add_widget(DataLabel(text=product_id))
            self.d.add_widget(DataLabel(text=quantity))
            self.d.add_widget(DataLabel(text=unitprice))
            self.d.add_widget(option)

            super(ExportSearchTable2, self).add_widget(self.d)
            self.count += 1

    def save_edited_data(self, id, export_id, product_id, quantity, unitprice):
        self.data_object.id = id
        self.data_object.export_id = export_id
        self.data_object.product_id = product_id
        self.data_object.quantity = quantity
        self.data_object.status = unitprice
        self.data_object.update_export()
        self.dialog.dismiss()
        self.pagination_next()

    def edit_data(self, id):
        export_id = str(self.data_object.get_export_details().get(id)['export_id'])
        product_id = str(self.data_object.get_export_details().get(id)['product_id'])
        quantity = str(self.data_object.get_export_details().get(id)['quantity'])
        unitprice = str(self.data_object.get_export_details().get(id)['unitprice'])
        b = GridLayout(size_hint=(None, None),
                       height='200px',
                       width="400px",
                       cols=2
                       )
        exp_id = DialogTextInput(export_id)
        prod_id = DialogTextInput(product_id)
        qty = DialogTextInput(quantity)
        uprice = DialogTextInput(unitprice)

        b.add_widget(MDLabel(id='destination',
                             text="Export ID",
                             size_hint_x=None,
                             width="90px"
                             ))
        b.add_widget(exp_id)
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

        self.dialog = MDDialog(title="This is a test dialog",
                               content=b,
                               size_hint=(None, None),
                               height="500px",
                               width="500px",
                               auto_dismiss=False)
        self.dialog.add_action_button("Save",
                                      action=lambda *x: self.save_edited_data(id, exp_id.text, prod_id.text,
                                                                              qty.text,uprice.text))
        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def add_data(self, export_export_id, export_product_id, export_quantity, export_unitprice):
        self.data_object.export_id = export_export_id
        self.data_object.product_id = export_product_id
        self.data_object.quantity = export_quantity
        self.data_object.unitprice = export_unitprice

        if export_export_id != '' and export_product_id != '' and export_quantity != '' and export_unitprice != '':
            self.data_object.insert_export_detail()
        else:
            Snackbar(text=" You Need To Fill All Fields ").show()
        self.call_load()

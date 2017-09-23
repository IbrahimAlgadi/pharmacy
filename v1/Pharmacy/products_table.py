from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
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
from product import *
from table_buttons import *
from category import *

from dropdown_tools import *

class ButtonDropper(Button):
    _id = None
    number = NumericProperty(0)
    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['background_normal'] = ''
        kwargs['background_color'] = C('#1976d2')
        kwargs['text'] = 'Select'
        super(ButtonDropper, self).__init__(**kwargs)

    def call_the_drop(self, text_input_object):
        self.textinput = text_input_object
        self.dropdown = Droppper(size_hint=(None, None), size=(90, 200))
        data_object = Category()
        data = sorted(list(data_object.get_categories()))
        data_dict = data_object.get_categories()
        for key in data:
            _id = str(data_dict.get(key)['id'])
            destination = data_dict.get(key)['name']
            btn = DropDownButton(self.textinput,self.number, _id, text=destination, size_hint_y=None,
                                 height=44)
            self.number += 1
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.number = 0
        self.dropdown.open(self)

class ProductsTable(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    data_object = Product()

    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 1
    offset = 10
    _data = None
    data_in_page = None

    def __init__(self, **kwargs):
        self.bind(minimum_height=self.setter('height'))
        super(ProductsTable, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()

    def delete_data(self, id):
        try:
            self.data_object.id = id
            self.data_object.delete_product()
            self.pagination_next(self.current)
        except KeyError:
            print "Key Not Found"

    def call_load(self):
        Clock.schedule_once(self.load_data)

    def pagination_next(self, page=1):
        self.current = int(page)
        no_pages = int(math.ceil(float(self.data_object.count_product()) / float(self.offset)))

        if self.current <= no_pages:
            offset = (self.current - 1) * self.offset
            self.data_in_page = self.data_object.get_products_page(offset, self.offset)
            self.pages = list(self.data_in_page)
            self._data = self.pages
            self.call_load()
        else:
            deactivate = True
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
            self.data_in_page = self.data_object.get_products_page(offset, self.offset)
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
        categories_object = Category()
        self.category_dict = categories_object.get_categories()

        self._data = sorted(list(self.data_in_page))

        for key in self._data:
            id = str(self.data_in_page.get(key)['id'])
            brandname = str(self.data_in_page.get(key)['brandname'])
            genericname = str(self.data_in_page.get(key)['genericname'])
            quantityperunit = str(self.data_in_page.get(key)['quantityperunit'])
            unitprice = str(self.data_in_page.get(key)['unitprice'])
            category_id = str(self.category_dict.get( str(self.data_object.get_products().get(key)['category_id']) )['name'])
            expiry_date = str(self.data_in_page.get(key)['expiry_date'])
            status = str(self.data_in_page.get(key)['status'])

            size = 0

            if len(brandname) > len(category_id) and len(brandname) > len(genericname) :
                size = len(brandname)
            elif len(category_id ) > len(brandname) and len(category_id ) > len(genericname):
                size = len(category_id)
            elif len(genericname) > len(brandname) and len(genericname) > len(brandname):
                size = len(genericname)

            if size <= 15:
                size = 50
            elif size > 15:
                size += 40

            if self.count % 2 == 1:
                self.d = DataWidget2(self.count,
                                     size_hint_y=None,
                                     height='{}px'.format(size))
            else:
                self.d = DataWidget(self.count,
                                    size_hint_y=None,
                                    height='{}px'.format(size))

            b = EditButton(self, id, text="edit")
            de = DeleteButton(self, self.d, id, text="delete")
            option = BoxLayout()

            option.add_widget(b)
            option.add_widget(de)

            self.d.add_widget(DataLabel(text=str(self.count), size_hint_x=None, width='40px'))
            self.d.add_widget(DataLabel(text=brandname))
            self.d.add_widget(DataLabel(text=genericname))
            self.d.add_widget(DataLabel(text=quantityperunit))
            self.d.add_widget(DataLabel(text=unitprice))
            self.d.add_widget(DataLabel(text=category_id))
            self.d.add_widget(DataLabel(text=expiry_date))
            self.d.add_widget(DataLabel(text=status))
            self.d.add_widget(option)

            super(ProductsTable, self).add_widget(self.d)
            self.count += 1

    def save_edited_data(self, id, brandname, genericname, quantityperunit, unitprice, category_id, expiry_date, status):
        self.data_object.id = id
        self.data_object.brandname = brandname
        self.data_object.genericname = genericname
        self.data_object.quantityperunit = quantityperunit
        self.data_object.unitprice = unitprice
        self.data_object.category_id = category_id
        self.data_object.expiry_date = expiry_date
        self.data_object.status = status
        self.data_object.update_product()
        self.dialog.dismiss()
        self.pagination_next()

    def edit_data(self, id):
        brandname = str(self.data_in_page.get(id)['brandname'])
        genericname = str(self.data_in_page.get(id)['genericname'])
        quantityperunit = str(self.data_in_page.get(id)['quantityperunit'])
        unitprice = str(self.data_in_page.get(id)['unitprice'])
        category_id = str(self.data_in_page.get(id)['category_id'])
        expiry_date = str(self.data_in_page.get(id)['expiry_date'])
        status = str(self.data_in_page.get(id)['status'])
        b = GridLayout(size_hint=(None, None),
                       height='200px',
                       width="400px",
                       cols=2
                       )
        brandname_wid = DialogTextInput(brandname)
        genericname_wid = DialogTextInput(genericname)
        quantityperunit_wid = DialogTextInput(quantityperunit)
        unitprice_wid = DialogTextInput(unitprice)
        category_id_wid = DialogTextInput(category_id)
        expiry_date_wid = DialogTextInput(expiry_date)
        status_wid = DialogTextInput(status)

        b.add_widget(MDLabel(
                             text="Brand Name",
                             size_hint_x=None,
                             width="90px"
                             ))
        b.add_widget(brandname_wid)
        b.add_widget(MDLabel(
            text="Generic Name",
            size_hint_x=None,
            width="90px"))
        b.add_widget(genericname_wid)
        b.add_widget(MDLabel(
                             text="Quantity Per Unit",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(quantityperunit_wid)
        b.add_widget(MDLabel(
                             text="Unit Price",
                             size_hint_x=None,
                             width="90px"
                             ))
        b.add_widget(unitprice_wid)
        b.add_widget(MDLabel(
            text="Category ID",
            size_hint_x=None,
            width="90px"))
        b.add_widget(category_id_wid)
        b.add_widget(MDLabel(
                             text="Expiry Date",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(expiry_date_wid)
        b.add_widget(MDLabel(
                             text="Status",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(status_wid)

        self.dialog = MDDialog(title="Update Product",
                               content=b,
                               size_hint=(None, None),
                               height="500px",
                               width="500px",
                               auto_dismiss=False)
        self.dialog.add_action_button("Save",
                                      action=lambda *x: self.save_edited_data(id, brandname_wid.text, genericname_wid.text, quantityperunit_wid.text, unitprice_wid.text,
                                                                              category_id_wid.text, expiry_date_wid.text, status_wid.text))
        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()
        self.pagination_next()
        self.call_load()

    def add_data(self, product_barcode, brandname, genericname, quantityperunit, unitprice, category_id, expiry_date, status):
        self.data_object.barcode = product_barcode
        self.data_object.brandname = brandname
        self.data_object.genericname = genericname
        self.data_object.quantityperunit = quantityperunit
        self.data_object.unitprice = unitprice
        self.data_object.category_id = category_id
        self.data_object.expiry_date = expiry_date
        self.data_object.status = status
        if product_barcode != '':
            if brandname != '' and genericname != '' and quantityperunit != '' and unitprice != '' and category_id != '' and expiry_date != '' and status != '':
                self.data_object.insert_product()
            else:
                Snackbar(text=" You Need To Fill All Fields ").show()
        else:
            Snackbar(text=" You Need To Add Barcode It's Important ").show()
        self.pagination_next()
        self.call_load()
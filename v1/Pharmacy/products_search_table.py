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
from product_report import *
from table_buttons import *
from category import *

from threading import Thread

from dropdown_tools import *

from excel import *
from datetime import datetime

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
            btn = DropDownButton(self.textinput,self.number, _id, text=destination, size_hint_y=None, height=44)
            self.number += 1
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.number = 0
        self.dropdown.open(self)

class ProductsSearchTable(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    data_object = Product()

    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 0
    offset = 11
    _data = None

    _genericname_filter = False
    _genericname = " AND genericname LIKE '%{}%' "
    _quantityperunit_filter = False
    _quantityperunit = " AND quantityperunit LIKE '%{}%' "
    _unitprice_filter = False
    _unitprice = " AND unitprice LIKE '%{}%' "
    _cat_id_filter = False
    _cat_id = " AND category_id = {} "
    _expiry_date_filter = False
    _expiry_date = " AND expiry_date LIKE '%{}%' "
    _status_filter = False
    _status = " AND status LIKE '%{}%' "

    search_result = data_object.get_products()

    def __init__(self, **kwargs):
        self.bind(minimum_height=self.setter('height'))
        super(ProductsSearchTable, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()


    def generate_pdf(self, dt):
        sorted_list = sorted(self.search_result)
        cat = Category()
        th = Thread(target=generate_pdf, args=(sorted_list, self.search_result, cat.get_categories()))
        th.start()

    def generate_excel_sheet(self, dt):
        id = []
        brandname = []
        genericname = []
        quantityperunit = []
        unitprice = []
        category_id = []
        expiry_date = []
        status = []

        # for interpreting the category type
        categories_object = Category()
        self.category_dict = categories_object.get_categories()

        try:
            for v in self.search_result.values():
                id.append(int(v.get('id')))
                brandname.append(v.get('brandname'))
                genericname.append(v.get('genericname'))
                quantityperunit.append(int(v.get('quantityperunit')))
                unitprice.append(float(v.get('unitprice')))
                category_id.append(self.category_dict.get(str(v.get('category_id')))['name'])
                expiry_date.append(v.get('expiry_date'))
                status.append(v.get('status'))

            data_dict = {
                # '1_ID': id,
                '2_Brand_Name': brandname,
                '3_Generic_Name': genericname,
                '4_Quantity_Per_Unit': quantityperunit,
                '5_Unit_Price': unitprice,
                '6_Category': category_id,
                '7_Expiry_Date': expiry_date,
                '8_Status': status
            }
        except:
            # i will use snack bar to tell an exception
            pass
        # generate_excel(data_dict, excel_file_name="supplier_report4")

        th = Thread(target=generate_excel, args=(data_dict, "ExcelReports\\products_report\\products_report_"+
                                                 str(datetime.today()).replace(" ","_").replace(":", "_")))
        th.start()

    def make_excel(self):
        Clock.schedule_once(self.generate_excel_sheet)

    def make_report(self):
        Clock.schedule_once(self.generate_pdf)

    def activate_genericname(self, state):
        if state == 'down':
            self._genericname_filter = True
        else:
            self._genericname_filter = False

    def activate_quantityperunit(self, state):
        if state == 'down':
            self._quantityperunit_filter = True
        else:
            self._quantityperunit_filter = False

    def activate_unitprice(self, state):
        if state == 'down':
            self._unitprice_filter = True
        else:
            self._unitprice_filter = False

    def activate_category_id(self, state):
        if state == 'down':
            self._cat_id_filter = True
        else:
            self._cat_id_filter = False

    def activate_expiry_date(self, state):
        if state == 'down':
            self._expiry_date_filter = True
        else:
            self._expiry_date_filter = False

    def activate_status(self, state):
        if state == 'down':
            self._status_filter = True
        else:
            self._status_filter = False

    def filter(self,product_search_brandname, product_search_genericname, product_search_quantityperunit, product_search_unitprice, product_search_category_id, products_search_date_label, product_search_status):
        self.sql = "SELECT * FROM products WHERE brandname LIKE '%{}%' ".format(product_search_brandname)
        if self._genericname_filter:
            self.sql += self._genericname.format(product_search_genericname)
        if self._quantityperunit_filter:
            self.sql += self._quantityperunit.format(product_search_quantityperunit)
        if self._unitprice_filter:
            self.sql += self._unitprice.format(product_search_unitprice)
        if self._cat_id_filter:
            self.sql += self._cat_id.format(product_search_category_id)
        if self._expiry_date_filter:
            self.sql += self._expiry_date.format(products_search_date_label)
        if self._status_filter:
            self.sql += self._status.format(product_search_status)

        s = self.data_object.execute(self.sql)
        name = dict()
        for val in s:
            name[val['brandname']] = val
        self.search_result = name
        self.pagination_next()

    def delete_data(self, id):
        try:
            self.data_object.id = id
            self.data_object.delete_product()
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
        categories_object = Category()
        self.category_dict = categories_object.get_categories()
        # print self.category_dict
        for key in self._data:
            id = str(self.search_result.get(key)['id'])
            brandname = str(self.search_result.get(key)['brandname'])
            genericname = str(self.search_result.get(key)['genericname'])
            quantityperunit = str(self.search_result.get(key)['quantityperunit'])
            unitprice = str(self.search_result.get(key)['unitprice'])
            category_id = str(self.category_dict.get( str(self.search_result.get(key)['category_id']) )['name'])
            # print self.search_result.get(key)['category_id']
            expiry_date = str(self.search_result.get(key)['expiry_date'])
            status = str(self.search_result.get(key)['status'])

            size = 0

            if len(brandname) > len(category_id) and len(brandname) > len(genericname):
                size = len(brandname)
            elif len(category_id) > len(brandname) and len(category_id) > len(genericname):
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

            super(ProductsSearchTable, self).add_widget(self.d)
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
        brandname = str(self.data_object.get_products().get(id)['brandname'])
        genericname = str(self.data_object.get_products().get(id)['genericname'])
        quantityperunit = str(self.data_object.get_products().get(id)['quantityperunit'])
        unitprice = str(self.data_object.get_products().get(id)['unitprice'])
        category_id = str(self.data_object.get_products().get(id)['category_id'])
        expiry_date = str(self.data_object.get_products().get(id)['expiry_date'])
        status = str(self.data_object.get_products().get(id)['status'])
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

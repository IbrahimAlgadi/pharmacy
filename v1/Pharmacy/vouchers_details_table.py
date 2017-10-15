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
from kivymd.selectioncontrols import MDCheckbox

# database
from product import *
from table_buttons import *
# from category import *
from voucher_detail import *

from dropdown_tools import *


class Voucher_Product_Selector(MDCheckbox):
    voucher_id = None
    delete_tigger = ObjectProperty(None)
    parentObject = ObjectProperty(None)

    def __init__(self, voucher_id, delete_product_button, parentObject, **kwargs):
        self.voucher_id = voucher_id
        self.delete_tigger = delete_product_button
        self.parentObject = parentObject
        #kwargs['opposite_colors'] = True
        #kwargs['theme_text_color'] = C("#fff111")
        #kwargs['text_color'] = (0, 1, 0, .4)
        super(Voucher_Product_Selector, self).__init__(**kwargs)

    def on_active(self, instance, value):
        if value:
            self.delete_tigger.disabled = False
            print self.voucher_id
            print self.delete_tigger.state
            self.parentObject.add_to_delete_list(self.voucher_id)
        else:
            self.parentObject.remove_from_delete_list(self.voucher_id)

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

class VouchersDetailsTable(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    data_object = VoucherDetail()
    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 1
    offset = 4
    _data = None
    data_in_page = None
    total = ObjectProperty(None)
    voucher_id = NumericProperty(1)
    load_voucher_from_id = None
    delete_product_button = ObjectProperty(None)
    product_name = ObjectProperty(None)
    buffered_list = dict()
    item_counter = 1
    product_id = None
    # this variable is used to store the indexes of the values required to be deleted
    selected_for_delete = []

    def __init__(self, **kwargs):
        self.bind(minimum_height=self.setter('height'))
        super(VouchersDetailsTable, self).__init__(**kwargs)
        # self.pagination_next()
        # self.call_load()

    def load_voucher_details(self, id, state):
        if state:
            self.load_voucher_from_id = id
            print self.load_voucher_from_id
            self.pagination_next()
            self.call_load()
        else:
            print "Deactivate"

    def delete_data(self, id):
        try:
            self.data_object.id = id
            self.data_object.delete_voucher_detail()
            self.pagination_next(self.current)
        except KeyError:
            print "Key Not Found"

    # here i will get the value of the index in the current list that is been displayed in the table

    def select_to_delete(self):
        pass

    def pagination_next(self, page=1):
        self.current = int(page)
        no_pages = int(math.ceil(float(self.data_object.count_with_id(self.load_voucher_from_id)) / float(self.offset)))

        if self.current <= no_pages:
            offset = (self.current - 1) * self.offset
            self.data_in_page = self.data_object.get_voucher_from_id(self.load_voucher_from_id,offset, self.offset)
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
            self.data_in_page = self.data_object.get_voucher_from_id(self.load_voucher_from_id,offset, self.offset)
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

    def get_product_from_barcode(self, barcode):
        product_object = Product()
        if barcode != '':
            product_id = product_object.execute("SELECT * FROM products WHERE barcode="+barcode)
            # print product_id
            if product_id == ():
                pass
            else:
                self.product_id = str(product_id[0]["id"])
                brand = str(product_id[0]["brandname"])
                # print
                self.product_name.text = brand
                Snackbar(text="Found "+self.product_id+" "+brand).show()

    def call_load(self):
        Clock.schedule_once(self.load_data)

    def load_data(self, dt):
        self.clear_widgets()
        self.count = self.current * self.offset - self.offset + 1
        product_object = Product()

        self._data = []
        if self.data_in_page != None:
            self._data = sorted(list(self.data_in_page))
        # print self._data
        # print self.data_in_page
        self.sum = 0.0
        self.count = 1
        if self._data != []:
            for key in self._data:
                id = str(self.data_in_page.get(key)['id'])
                voucher_id = str(self.data_in_page.get(key)['voucher_id'])
                product_id = str(self.data_in_page.get(key)['product_id'])
                price = product_object.execute("SELECT unitprice FROM products WHERE id="+product_id)[0]['unitprice']
                quantity = str(self.data_in_page.get(key)['quantity'])

                self.sum = float(self.sum) + float(price) * float(quantity)

                if self.count % 2 == 1:
                    self.d = DataWidget2(self.count,
                                         size_hint_y=None,
                                         height='40px')
                else:
                    self.d = DataWidget(self.count,
                                        size_hint_y=None,
                                        height='40px')

                S = Voucher_Product_Selector(id, self.delete_product_button, self ,disabled=True)
                # de = DeleteButton(self, self.d, id, text="delete")

                self.d.add_widget(DataLabel(text=str(self.count)))
                # self.d.add_widget(DataLabel(text=voucher_id))
                self.d.add_widget(DataLabel(text=product_id))
                self.d.add_widget(DataLabel(text=quantity))
                self.d.add_widget(DataLabel(text=str(price)))
                self.d.add_widget(S)

                super(VouchersDetailsTable, self).add_widget(self.d)
                self.count += 1
            self.total.text = '[color="#000000"][b][size=40]{}SDG[/size][/b][/color]'.format(str(self.sum))

    def add_to_delete_list(self, id):
        print "id to delete: ", id
        self.selected_for_delete.append(id)
        print self.selected_for_delete
        if len(self.selected_for_delete) < 1:
            self.delete_product_button.disabled = True

    def remove_from_delete_list(self, id):
        print "Removed id = ",id
        self.selected_for_delete.remove(id)
        print self.selected_for_delete
        if len(self.selected_for_delete) < 1:
            self.delete_product_button.disabled = True

    def delete_from_the_buffer(self):
        print "delete: ",self.selected_for_delete
        print self.buffered_list
        for a in self.selected_for_delete:
            self.buffered_list.pop(a)
        self.selected_for_delete = []
        print self.buffered_list
        self.call_load_buffered_data()


    def call_load_buffered_data(self):
        Clock.schedule_once(self.load_data_buffered_data)

    def load_data_buffered_data(self, dt):
        self.clear_widgets()
        # do i really need a loop every time i really need to adjust my prospective
        self._data = []
        if self.buffered_list != None:
            self._data = sorted(list(self.buffered_list))
        product_object = Product()
        # print self._data
        # print self.data_in_page
        self.sum = 0.0
        self.count = 1
        if self._data != []:
            for key in self._data:
                # id = str(self.buffered_list.get(key)['id'])
                voucher_id = str(self.buffered_list.get(key)['voucher_id'])
                product_id = str(self.buffered_list.get(key)['product_id'])
                price = str(product_object.execute("SELECT unitprice FROM products WHERE id=" + product_id)[0]['unitprice'])
                quantity = str(self.buffered_list.get(key)['quantity'])

                self.sum = float(self.sum) + float(price) * float(quantity)

                if self.count % 2 == 1:
                    self.d = DataWidget2(self.count,
                                         size_hint_y=None,
                                         height='40px')
                else:
                    self.d = DataWidget(self.count,
                                        size_hint_y=None,
                                        height='40px')

                S = Voucher_Product_Selector(key, self.delete_product_button, self)
                # de = DeleteButton(self, self.d, id, text="delete")

                self.d.add_widget(DataLabel(text=str(self.count)))
                # self.d.add_widget(DataLabel(text=voucher_id))
                self.d.add_widget(DataLabel(text=product_id))
                self.d.add_widget(DataLabel(text=quantity))
                self.d.add_widget(DataLabel(text=price))
                self.d.add_widget(S)

                super(VouchersDetailsTable, self).add_widget(self.d)
                self.count += 1
            self.total.text = '[color="#000000"][b][size=40]{}SDG[/size][/b][/color]'.format(str(self.sum))

    def save_edited_data(self, id, brandname, genericname, quantityperunit, unitprice, category_id, expiry_date, status):
        self.data_object.id = id
        self.data_object.brandname = brandname
        self.data_object.genericname = genericname
        self.data_object.quantityperunit = quantityperunit
        self.data_object.unitprice = unitprice
        self.data_object.category_id = category_id
        self.data_object.expiry_date = expiry_date
        self.data_object.status = status
        self.data_object.update_voucher_detail()
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

        self.dialog = MDDialog(title="Update Vocuher",
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

    def create_new_voucher(self, voucher_id):
        self.voucher_id = voucher_id
        self.reset_item_counter()
        # print self.voucher_id

    def on_voucher_id(self, *args):
        self.clear_widgets()
        Snackbar(text=" Added New Voucher ").show()

    def reset_item_counter(self):
        self.item_counter = 1

    def add_data(self, quantity):
        self.buffered_list[self.item_counter] = {"voucher_id":self.voucher_id,"product_id":self.product_id, "quantity":quantity}
        self.item_counter = len(self.buffered_list) + 1
        self.call_load_buffered_data()

    def add_to_database(self):
        self._data = sorted(list(self.buffered_list))
        if self._data != []:
            for key in self._data:
                self.data_object.voucher_id = str(self.buffered_list.get(key)['voucher_id'])
                self.data_object.product_id = str(self.buffered_list.get(key)['product_id'])
                self.data_object.quantity = str(self.buffered_list.get(key)['quantity'])
                self.data_object.insert_voucher_detail()
            Snackbar(text=" Voucher Has Been Purchased Successfully ").show()

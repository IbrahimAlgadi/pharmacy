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

from threading import Thread

# database
from supplier import *
from table_buttons import *
from supplier_report import *

from excel import *
from datetime import datetime

class SupplierSearchTable(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    data_object = Supplier()
    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 0
    offset = 11
    _data = None
    _filter_add = " AND address LIKE '%{}%' "
    _address = False
    _filter_contact = " AND contact LIKE '%{}%' "
    _contact = False
    sql = ''
    search_result = data_object.get_suppliers()

    def __init__(self, **kwargs):
        super(SupplierSearchTable, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()


    def activate_address(self, state):
        if state == 'down':
            self._address = True
        else:
            self._address = False

    def activate_contact(self, state):
        if state == 'down':
            self._contact = True
        else:
            self._contact = False

    def filter(self,supplier_search_name, supplier_search_address, supplier_search_contact):
        self.sql = "SELECT * FROM suppliers WHERE name LIKE '%{}%' ".format(supplier_search_name)
        if self._address:
            self.sql += self._filter_add.format(supplier_search_address)
        if self._contact:
            self.sql += self._filter_contact.format(supplier_search_contact)
        s = self.data_object.execute(self.sql)
        name = dict()
        for val in s:
            name[val['name']] = val
        self.search_result = name
        self.pagination_next()

    def generate_pdf(self, dt):
        sorted_list = sorted(self.search_result)
        th = Thread(target=generate_pdf, args=(sorted_list, self.search_result))
        th.start()

    def generate_excel_sheet(self, dt):
        address = list()
        contact = list()
        id = list()
        name = list()

        # result = list(sup.execute('SELECT * FROM suppliers'))

        # print self.search_result.values()

        for v in self.search_result.values():
            address.append(v.get('address'))
            contact.append(int(v.get('contact')))
            id.append(int(v.get('id')))
            name.append(v.get('name'))

        data_dict = {
            # '1_ID': id,
            '2_Name': name,
            '3_Address': address,
            '4_Contact': contact
        }

        # generate_excel(data_dict, excel_file_name="supplier_report4")

        th = Thread(target=generate_excel, args=(data_dict, "ExcelReports\\supplier_report\\supplier_report_"+
                                                 str(datetime.today()).replace(" ","_").replace(":", "_")))
        th.start()

    def make_excel(self):
        Clock.schedule_once(self.generate_excel_sheet)

    def make_report(self):
        Clock.schedule_once(self.generate_pdf)

    def delete_data(self, id):
        try:
            self.data_object.id = id
            self.data_object.delete_supplier()
            self.pagination_next(self.current)
        except KeyError:
            print "Key Not Found"
        except e:
            Snackbar(text=str(e)).show()


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
        for key in self._data:
            id = str(self.search_result.get(key)['id'])
            name = str(self.search_result.get(key)['name'])
            address = str(self.search_result.get(key)['address'])
            contact = str(self.search_result.get(key)['contact'])

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
            self.d.add_widget(DataLabel(text=name))
            self.d.add_widget(DataLabel(text=address))
            self.d.add_widget(DataLabel(text=contact))
            self.d.add_widget(option)

            super(SupplierSearchTable, self).add_widget(self.d)
            self.count += 1

    def save_edited_data(self, id, name, address, contact):
        self.data_object.id = id
        self.data_object.name = name
        self.data_object.address = address
        self.data_object.contact = contact
        self.data_object.update_supplier()
        self.dialog.dismiss()
        self.pagination_next()

    def edit_data(self, id):
        name = self.data_object.get_suppliers().get(id)['name']
        address = str(self.data_object.get_suppliers().get(id)['address'])
        contact = self.data_object.get_suppliers().get(id)['contact']
        b = GridLayout(size_hint=(None, None),
                       height='200px',
                       width="400px",
                       cols=2
                       )
        name_wid = DialogTextInput(name)
        address_wid = DialogTextInput(address)
        contact_wid = DialogTextInput(contact)

        b.add_widget(MDLabel(id='Name',
                             text="Destination",
                             size_hint_x=None,
                             width="90px"
                             ))
        b.add_widget(name_wid)
        b.add_widget(MDLabel(
            text="Address",
            size_hint_x=None,
            width="90px"))
        b.add_widget(address_wid)
        b.add_widget(MDLabel(id='Contact',
                             text="Status",
                             size_hint_x=None,
                             width="90px"))
        b.add_widget(contact_wid)

        self.dialog = MDDialog(title="This is a test dialog",
                               content=b,
                               size_hint=(None, None),
                               height="500px",
                               width="500px",
                               auto_dismiss=False)
        self.dialog.add_action_button("Save",
                                      action=lambda *x: self.save_edited_data(id, name_wid.text, address_wid.text,
                                                                              contact_wid.text))
        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()
        self.pagination_next()
        self.call_load()

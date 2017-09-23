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

import _mysql_exceptions
# Using Material Design Widgets
from kivymd.button import MDIconButton
from kivymd.label import MDLabel
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField
from kivymd.date_picker import MDDatePicker
from kivymd.snackbar import Snackbar

# database
from export import *
from table_buttons import *

class ExportSearchTable1(GridLayout):
    count = NumericProperty(0)
    d = ObjectProperty(None)
    export_object = Export()
    # pagination
    pages = list()
    page = list()
    page_no = 0
    current = 0
    offset = 4
    _data = None

    search_result = dict()

    _filter_status = False
    _status_search = " AND status LIKE '%{}%' "
    _filter_date = False
    _date_search = " AND date LIKE '{}' "

    def __init__(self, **kwargs):
        super(ExportSearchTable1, self).__init__(**kwargs)
        self.pagination_next()
        self.call_load()

    def activate_export_date(self, state):
        if state == 'down':
            self._filter_date = True
        else:
            self._filter_date = False

    def activate_status(self, state):
        if state == 'down':
            self._filter_status = True
        else:
            self._filter_status = False

    def filter(self,export_search_destination, exports_search_date_label, export_search_status):

        self.sql = "SELECT * FROM exports WHERE destination LIKE '%{}%' ".format(export_search_destination)

        if self._filter_date:
            self.sql += self._date_search.format(exports_search_date_label)
            # print self.sql
        if self._filter_status:
            self.sql += self._status_search.format(export_search_status)

        if self._filter_date and self._filter_status and export_search_destination == '':
            self.search_result = self.export_object.get_exports()

        s = self.export_object.execute(self.sql)
        name = dict()
        for val in s:
            name[val['destination']] = val
        self.search_result = name
        self.pagination_next()

    def delete_data(self, id):
        try:
            self.export_object.id = id
            self.export_object.delete_export()
            self.pagination_next(self.current)
        except KeyError:
            print "Key Not Found"
        except _mysql_exceptions.IntegrityError:
            Snackbar(text=str("You Cannot Delete This Record")).show()

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
            date = str(self.search_result.get(key)['date'])
            status = self.search_result.get(key)['status']
            destination = self.search_result.get(key)['destination']

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
            self.d.add_widget(DataLabel(text=destination))
            self.d.add_widget(DataLabel(text=date))
            self.d.add_widget(DataLabel(text=status))
            self.d.add_widget(option)

            super(ExportSearchTable1, self).add_widget(self.d)
            self.count += 1

    def save_edited_data(self, id, destination, date, status):
        self.export_object.id = id
        self.export_object.destination = destination
        self.export_object.date = date
        self.export_object.status = status
        self.export_object.update_export()
        self.dialog.dismiss()
        self.pagination_next()

    def edit_data(self, id):
        dest = self.export_object.get_exports().get(id)['destination']
        dat = str(self.export_object.get_exports().get(id)['date'])
        stat = self.export_object.get_exports().get(id)['status']
        b = GridLayout(size_hint=(None, None),
                       height='200px',
                       width="400px",
                       cols=2
                       )
        destination = DialogTextInput(dest)
        date = DialogTextInput(dat)
        status = DialogTextInput(stat)

        b.add_widget(MDLabel(id='destination',
                             text="Destination",
                             size_hint_x=None,
                             width="90px"
                             ))
        b.add_widget(destination)
        b.add_widget(MDLabel(
            text="Date",
            size_hint_x=None,
            width="90px"))
        b.add_widget(date)
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
                                      action=lambda *x: self.save_edited_data(id, destination.text, date.text,
                                                                              status.text))
        self.dialog.add_action_button("Cancel",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

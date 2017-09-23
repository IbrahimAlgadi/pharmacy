from database import Database
from datetime import date

class Import():
    id = None
    receipt_number = None
    date = None
    status = None
    supplier_id = None

    def __init__(self):
        self._db = Database("imports")

    def get_imports(self):
        self._import = self._db.getrecords()
        json = dict()
        for data in self._import:
            id = data.get('id')
            json["%s"%id] = data
        return json

    def get_imports_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM imports "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def get_import(self):
        self._import = self._db.getrecord()
        return self._import

    def insert_import(self):
        data = dict()
        data['date'] = self.date
        data['receipt_number'] = self.receipt_number
        data['status'] = self.status
        data['supplier_id'] = self.supplier_id
        self._db.insert(data)

    def update_import(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['date'] = self.date
            data['receipt_number'] = self.receipt_number
            data['status'] = self.status
            data['supplier_id'] = self.supplier_id
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_import(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    def count_import(self):
        self._import = self._db.counterecords()
        return self._import

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export


if __name__ == '__main__':
    exp = Import()
    # print exp.get_imports()
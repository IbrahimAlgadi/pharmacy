from database import Database
from datetime import date

class Supplier():
    id = None
    name = None
    address = None
    contact = None

    def __init__(self):
        self._db = Database("suppliers")

    def get_suppliers(self):
        self.export = self._db.getrecords()
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s"%id] = data
        # print json
        return json

    def get_suppliers_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM suppliers "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def get_supplier(self):
        self.export = self._db.getrecord()
        return self.export

    def insert_supplier(self):
        data = dict()
        data['name'] = self.name
        data['address'] = self.address
        data['contact'] = self.contact
        self._db.insert(data)

    def update_supplier(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['name'] = self.name
            data['address'] = self.address
            data['contact'] = self.contact
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_supplier(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    def count_supplier(self):
        self.export = self._db.counterecords()
        return self.export

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = Supplier()
    print exp.get_suppliers()




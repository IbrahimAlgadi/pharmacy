from database import Database
from datetime import date

class ImportDetail():
    id = None
    import_id = None
    product_id = None
    quantity = None
    unitprice = None

    def __init__(self):
        self._db = Database("import_details")

    def get_import_details(self):
        self.import_detail = self._db.getrecords()
        json = dict()
        for data in self.import_detail:
            id = data.get('id')
            json["%s"%id] = data
        # print json
        return json

    def get_import_details_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM import_details "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def get_import_detail(self):
        self.import_detail = self._db.getrecord()
        return self.import_detail

    def insert_import_detail(self):
        data = dict()
        data['import_id'] = self.import_id
        data['product_id'] = self.product_id
        data['quantity'] = self.quantity
        data['unitprice'] = self.unitprice
        self._db.insert(data)

    def update_import_detail(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['import_id'] = self.import_id
            data['product_id'] = self.product_id
            data['quantity'] = self.quantity
            data['unitprice'] = self.unitprice
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_import_detail(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    def count_import_detail(self):
        self.import_detail = self._db.counterecords()
        return self.import_detail

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = ImportDetail()
    print exp.get_import_details()

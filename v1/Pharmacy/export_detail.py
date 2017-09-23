from database import Database
from datetime import date

class ExportDetail():
    id = None
    export_id = None
    product_id = None
    quantity = None
    unitprice = None

    def __init__(self):
        self._db = Database("export_details")

    def get_export_details(self):
        self.export_detail = self._db.getrecords()
        json = dict()
        for data in self.export_detail:
            id = data.get('id')
            json["%s"%id] = data
        # print json
        return json

    def get_export_details_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM export_details "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def get_export_detail(self):
        self.export_detail = self._db.getrecord()
        return self.export_detail

    def insert_export_detail(self):
        data = dict()
        data['export_id'] = self.export_id
        data['product_id'] = self.product_id
        data['quantity'] = self.quantity
        data['unitprice'] = self.unitprice
        self._db.insert(data)

    def update_export_detail(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['export_id'] = self.export_id
            data['product_id'] = self.product_id
            data['quantity'] = self.quantity
            data['unitprice'] = self.unitprice
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_export_detail(self):
        bool = self._db.delete(self.id)
        print bool
        if bool:
            print "ID = ", self.id, " is not deleted"
        else:
            print "ID = ", self.id, " is deleted"
        return bool


    def count_export_detail(self):
        self.export_detail = self._db.counterecords()
        return self.export_detail

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = ExportDetail()
    print exp.get_export_details()

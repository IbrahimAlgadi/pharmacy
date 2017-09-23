from database import Database
from datetime import date

class Product():
    id = None
    barcode = None
    brandname = None
    genericname = None
    quantityperunit = None
    unitprice = None
    category_id = None
    expiry_date = None
    status = None

    def __init__(self):
        self._db = Database("products")

    def get_products(self):
        self.export = self._db.getrecords()
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s"%id] = data
        return json

    def get_products_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = "SELECT * FROM products "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def get_product(self):
        self.export = self._db.getrecord()
        return self.export

    def insert_product(self):
        data = dict()
        data['barcode'] = self.barcode
        data['brandname'] = self.brandname
        data['genericname'] = self.genericname
        data['quantityperunit'] = self.quantityperunit
        data['unitprice'] = self.unitprice
        data['category_id'] = self.category_id
        data['expiry_date'] = self.expiry_date
        data['status'] = self.status
        self._db.insert(data)

    def update_product(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['brandname'] = self.brandname
            data['genericname'] = self.genericname
            data['quantityperunit'] = self.quantityperunit
            data['unitprice'] = self.unitprice
            data['category_id'] = self.category_id
            data['expiry_date'] = self.expiry_date
            data['status'] = self.status
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_product(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    def count_product(self):
        self.export = self._db.counterecords()
        return self.export

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = Product()
    print exp.get_products_page(1,5)





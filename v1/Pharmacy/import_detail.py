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

if __name__ == '__main__':
    exp = ImportDetail()
    print exp.get_import_details()

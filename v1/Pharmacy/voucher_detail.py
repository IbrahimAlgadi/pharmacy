from database import Database
from datetime import date

class VoucherDetail():
    id = None
    voucher_id = None
    product_id = None
    quantity = None


    def __init__(self):
        self._db = Database("voucher_details")

    def get_voucher_details(self):
        self.export = self._db.getrecords()
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s"%id] = data
        return json

    def get_voucher_from_id(self, id, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM voucher_details WHERE voucher_id="+str(id)
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def count_with_id(self, id):
        sql = "SELECT COUNT(*) FROM voucher_details WHERE voucher_id="+str(id)
        self.export = self.execute(sql)
        return self.export[0]['COUNT(*)']

    def get_voucher_details_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM voucher_details "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def get_voucher_detail(self):
        self.export = self._db.getrecord()
        return self.export

    def insert_voucher_detail(self):
        data = dict()
        data['voucher_id'] = self.voucher_id
        data['product_id'] = self.product_id
        data['quantity'] = self.quantity
        self._db.insert(data)

    def update_voucher_detail(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['voucher_id'] = self.voucher_id
            data['product_id'] = self.product_id
            data['quantity'] = self.quantity
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_voucher_detail(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    def count_voucher_detail(self):
        self.export = self._db.counterecords()
        return self.export

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = VoucherDetail()
    print exp.get_voucher_details()
    print exp.get_voucher_from_id(1,4,4)
    print exp.count_with_id(1)




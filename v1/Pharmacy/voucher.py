from database import Database
from datetime import date

class Voucher():
    id = None
    date = None
    submitted_by = None
    status = None


    def __init__(self):
        self._db = Database("vouchers")

    def get_vouchers(self):
        self.export = self._db.getrecords()
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s"%id] = data
        return json

    def get_vouchers_page(self, offset, per_page):
        if offset < 0:
            offset = offset-1
        sql = ""
        sql = "SELECT * FROM `vouchers` "
        sql += " WHERE `date` LIKE '{}-{}-{}' ".format(str(date.today().year),str(date.today().month),str(date.today().day))
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        # print sql
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def count_voucher(self):
        sql = "SELECT COUNT(*) FROM `vouchers` WHERE `date` LIKE '{}-{}-{}' ".format(str(date.today().year),str(date.today().month),str(date.today().day))
        # print sql
        self.export = self.execute(sql)
        return self.export[0]['COUNT(*)']

    def get_voucher(self):
        self.export = self._db.getrecord()
        return self.export

    def insert_voucher(self):
        data = dict()
        data['date'] = self.date
        data['submitted_by'] = self.submitted_by
        data['status'] = self.status
        self._db.insert(data)

    def update_voucher(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['date'] = self.date
            data['submitted_by'] = self.submitted_by
            data['status'] = self.status
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_voucher(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    #def count_voucher(self):
    #    self.export = self._db.counterecords()
    #    return self.export

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = Voucher()
    print exp.count_voucher()
    print exp.get_vouchers_page(0,4)




from database import Database
from datetime import date

class Export():
    id = None
    date = None
    status = None
    destination = None

    def __init__(self):
        self._db = Database("exports")

    def get_exports(self):
        self.export = self._db.getrecords()
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s"%id] = data
        # print json
        return json

    def get_exports_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM exports "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
        return json

    def get_export(self):
        self.export = self._db.getrecord()
        return self.export

    def insert_export(self):
        data = dict()
        data['date'] = self.date
        data['status'] = self.status
        data['destination'] = self.destination
        self._db.insert(data)

    def update_export(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['date'] = self.date
            data['status'] = self.status
            data['destination'] = self.destination
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_export(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    def count_export(self):
        self.export = self._db.counterecords()
        return self.export

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = Export()

    # exp.id = 2
    # exp.date = date.today()
    # exp.status = "OK"
    # exp.destination = "Malysia"
    # exp.update_exports()
    # exp.delete_export()
    # exp.count_export()
    #for key in exp.get_exports():
    #    print "id +> ",exp.get_exports().get(key)['status']
    # print exp.count_export()
    #exp.status = "on"
    #exp.date = date.today()
    #exp.destination = "Safari"
    #exp.insert_export()


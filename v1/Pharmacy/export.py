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
        print self.export

    def get_export(self):
        self.export = self._db.getrecord()
        print self.export

    def insert_exports(self):
        data = dict()
        data['date'] = self.date
        data['status'] = self.status
        data['destination'] = self.destination
        self._db.insert(data)

    def update_exports(self):
        data = dict()
        print self.id
        if self.id != None:
            data['date'] = self.date
            data['status'] = self.status
            data['destination'] = self.destination
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_export(self):
        self._db.delete(self.id)

    def count_export(self):
        self.export = self._db.counterecords()
        print self.export

if __name__ == '__main__':
    exp = Export()

    # exp.id = 2
    # exp.date = date.today()
    # exp.status = "OK"
    # exp.destination = "Malysia"
    # exp.update_exports()
    # exp.delete_export()
    # exp.count_export()
    # exp.get_exports()


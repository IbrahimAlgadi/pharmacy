from database import Database
from datetime import date

class Category():
    id = None
    name = None


    def __init__(self):
        self._db = Database("categories")

    def get_categories(self):
        self.export = self._db.getrecords()
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s"%id] = data
        # print json
        return json

    def get_category(self):
        self.export = self._db.getrecord()
        return self.export

    def insert_category(self):
        data = dict()
        data['name'] = self.name
        self._db.insert(data)

    def update_category(self):
        data = dict()
        print "updated",self.id
        if self.id != None:
            data['name'] = self.name
            self._db.update(self.id, data)
        else:
            print "You Need To Set the id"

    def delete_category(self):
        print "ID = ",self.id, " is deleted"
        self._db.delete(self.id)

    def count_category(self):
        self.export = self._db.counterecords()
        return self.export

if __name__ == '__main__':
    exp = Category()
    print exp.get_categories()




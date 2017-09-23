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
        return json

    def get_categories_page(self, offset, per_page):
        if offset < 0:
            offset = offset*-1
        sql = ""
        sql = "SELECT * FROM categories "
        sql += " LIMIT {} ".format(per_page)
        sql += " OFFSET {} ".format(offset)
        self.export = self.execute(sql)
        json = dict()
        for data in self.export:
            id = data.get('id')
            json["%s" % id] = data
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

    def execute(self, command):
        self.export = self._db.execute(command)
        return self.export

if __name__ == '__main__':
    exp = Category()
    # print exp.get_categories()
    #name = dict()
    #for s in exp.execute("SELECT * FROM categories WHERE name LIKE '%h%' ORDER BY name"):
    #    name[s['name']] = s
    #print sorted(name)
    print exp.get_categories_page(4,5)



import MySQLdb
import _mysql_exceptions

class Database():
    user = "root"
    passwd = ""
    db = "i3m_pharmacy"
    host = "localhost"
    port = 3306
    def __init__(self, table):
        self.table = table
        self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
        self.cur = self.db.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, command):
        self.cur.execute(command)
        return self.cur.fetchall()

    def getrecords(self):
        self.cur.execute("SELECT * FROM "+self.table)
        return self.cur.fetchall()

    def getrecord(self, id):
        q = "SELECT * FROM {} WHERE id=%s".format(self.table)
        self.cur.execute(q,(id,))
        return self.cur.fetchone()

    def insert(self, data):
        keys = sorted(data.keys())
        values = [ data[v] for v in keys ]

        q = 'INSERT INTO {} ({}) VALUES ({}) '.format(
            self.table,
            ', '.join(keys),
            ', '.join('%s' for i in range(len(values)))
        )
        print q , tuple(values)
        self.cur.execute(q, values)
        self.db.commit()
        return self.db.affected_rows()

    def update(self, id, data):
        keys = sorted(data.keys())
        values = [data[v] for v in keys]

        for i,k in enumerate(keys):
            if k == 'id':
                del keys[i]
                del values[i]

        q = 'UPDATE {} SET {} WHERE id=%s'.format(
            self.table,
            ', '.join(map(lambda str: '{}=%s'.format(str), keys))
        )
        print q
        print tuple(values+[id])
        self.cur.execute(q, values+[id])
        self.db.commit()
        return self.db.affected_rows()

    def delete(self, id):
        self.cur.execute("DELETE FROM {} WHERE id=%s".format(self.table), [id])
        self.db.commit()



    def counterecords(self):
        q = "SELECT COUNT(*) FROM {}".format(self.table)
        self.cur.execute(q)
        return self.cur.fetchone()['COUNT(*)']

if __name__ == '__main__':
    db = Database("exports")
    print db.counterecords()
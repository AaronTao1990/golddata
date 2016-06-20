from pymongo import Connection

class WemediaDao(object):

    def __init__(self, MONGO_CONFIG):
        self.conn = Connection(MONGO_CONFIG['host'])
        self.db = self.conn[MONGO_CONFIG['db']]
        self.coll = self.db[MONGO_CONFIG['coll']]

    def get_tasks(self):
        for item in self.coll.find():
            yield item

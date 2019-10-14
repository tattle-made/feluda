import unittest
from db import sqlDatabase, mongoDB
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from os import environ


class sqlDBTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'sql_test.db'
        self.db = sqlDatabase(self.filename)

    def testInsertValues(self):
        pass

    def testDeleteValues(self):
        pass

    def testInsertArray(self):
        pass

    def testReadArray(self):
        pass

    def tearDown(self):
        # drop all tables created
        # self.db.query('drop table')
        pass


class mongoDBTests(unittest.TestCase):
    def setUp(self):
        self.mongo_url = environ['MONGO_URL']

    def testConnection(self):
        # https://stackoverflow.com/questions/30539183/how-do-you-check-if-the-client-for-a-mongodb-instance-is-valid
        timeout = 5
        self.cli = MongoClient(
            self.mongo_url, serverSelectionTimeoutMS=timeout)
        try:
            temp = self.cli.server_info()
        except ServerSelectionTimeoutError as e:
            self.fail('No mongo servers found in ' + str(timeout) + 'ms')

    def testInsertValues(self):
        pass

    def testDeleteValues(self):
        pass

    def testInsertMultipleUniqueValuesDocID(self):
        pass

    def tearDown(self):
        pass


class wordvecDBTests(unittest.TestCase):
    # test wordvec DB is setup
    def setUp(self):
        self.filename = 'docs_sqlite_db.db'
        self.db = sqlDatabase(self.filename)

    def tearDown(self):
        return super().tearDown()


class cloudAccessTests(unittest.TestCase):
    def testS3Access(self):
        pass

    def testFirebaseAccess(self):
        pass

from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
import database.db_kyoto as dbk
import logging
from database.api import NonExistentUID

import unittest

class Test(unittest.TestCase):

    def test_wrong_post(self):
        self.assertRaises(dbk.DataBaseError, dbk.post("test"))

    def test_wrong_retrieve(self):
        self.assertRaises(NonExistentUID, dbk.retrieve("ee229238"))

    def test_wrong_close(self):
        self.assertRaises(dbk.DataBaseError, dbk.bye())

    def test_wrong_policy(self):
        dbk.init()
        self.assertRaises(ValueError, dbk.post("test", expiry_policy='NO_SUCH_POLICY'))
        dbk.bye()

    def test_gen_behavious(self):
        dbk.init()
        uid = dbk.post("test")
        logging.debug(dbk.retrieve(uid))
        logging.debug(dbk.get_creation_timestamp(uid))
        uid_clash = dbk.post("a", preferred_uid="1")
        uid_clahs1 = dbk.post("b", preferred_uid="1")
        logging.debug(dbk.retrieve(uid_clash))
        logging.debug(dbk.retrieve(uid_clahs1))

if __name__ == '__main__':
    unittest.main()


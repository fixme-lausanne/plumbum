#!/usr/bin/env python3
from os.path import dirname, abspath, join
import sys
sys.path.append(join(dirname(dirname(abspath(__file__))), "database"))
from db_memory import MemoryDB as dbk
import logging
from db import NonExistentUID

import unittest

class Test(unittest.TestCase):
    SHORT_WRITE = "amenophis3"
        
    def test_wrong_retrieve(self):
        self.assertRaises(NonExistentUID, dbk.read, "ee229238")

    def test_write_n_retrieve(self):
        dbk.init()
        uid = dbk.write(Test.SHORT_WRITE)
        ret = dbk.read(uid)
        assert ret == Test.SHORT_WRITE
        
    def test_prefered_uid(self):
        uid = "1"
        real_uid = dbk.write(Test.SHORT_WRITE, preferred_uid=uid)
        assert uid == real_uid
        ret = dbk.read(uid)
        assert ret == Test.SHORT_WRITE
        
    def test_uid_clash(self):
        uid = "1"
        real_uid1 = dbk.write(Test.SHORT_WRITE, preferred_uid=uid)
        real_uid2 = dbk.write(Test.SHORT_WRITE, preferred_uid=uid)
        assert real_uid1 != real_uid2

if __name__ == '__main__':
    unittest.main()


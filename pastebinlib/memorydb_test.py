from pastebinlib.memorydb import post, retrieve, get_creation_timestamp, _db
from pastebinlib.api import NonExistentUID

import unittest
import time


class TestMemoryDB(unittest.TestCase):

    def setUp(self):
        _db.clear()
        
    def testSimple(self):
        hai_uid = post('hai')
        print(hai_uid)
        self.assertEquals('hai', retrieve(hai_uid))
        self.assertTrue(time.time() - get_creation_timestamp(hai_uid) < 1)
    
    def testNonExistent(self):
        with self.assertRaises(NonExistentUID):
            retrieve('not here')

    def testCollisions(self):
        a_uid = post('a')
        another_uid = post('a')
        
    
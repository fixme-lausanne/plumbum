from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
from pastebinlib.db_memory import post, retrieve, get_creation_timestamp, _db
from pastebinlib.api import NonExistentUID

import unittest
import time


class TestMemoryDB(unittest.TestCase):

    def setUp(self):
        _db.clear()
        
    def testSimple(self):
        hai_uid = post('hai')
        print(hai_uid)
        self.assertEqual('hai', retrieve(hai_uid))
        self.assertTrue(time.time() - get_creation_timestamp(hai_uid) < 1)
    
    def testNonExistent(self):
        with self.assertRaises(NonExistentUID):
            retrieve('not here')

    def testCollisions(self):
        ''' This is design choice: when the same content is posted again
        it gets a new uid (and new metadata, etc...) '''
        a_uid = post('a')
        another_uid = post('a')
        self.assertNotEqual(a_uid, another_uid)
        

if __name__ == '__main__':
    unittest.main()
    

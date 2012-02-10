from pastebin.memory_db import post, retrieve, NonExistentUID

import unittest


class TestMemoryDB(unittest.TestCase):

    def test_simple(self):
        hai_uid = post('hai')
        print(hai_uid)
        set.assertEquals('hai', retrieve(hai_uid))
        self.assertRaises(NonExistentUID, retrieve['not here'])

    
if __name__ == '__main__':
    unittest.main()
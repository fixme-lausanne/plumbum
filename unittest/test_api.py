#!/usr/bin/env python3

import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import unittest
import api

class ApiTest(unittest.TestCase):
    CONTENT = "dfsdafsadfasdfas"
    #def post(utf8_text, expiry_policy=EXPIRY_NEVER, prefered_uid=None,linked_uid_list=None):
    def test_empty_post(self):
        post_content = ""
        uid = api.post(post_content)
        self.assertIsNone(uid)

    def test_wrong_expiry_policy(self):
        with self.assertRaises(ValueError):
            api.post(ApiTest.CONTENT, expiry_policy=99)
        
    def test_preferred_uid(self):
        pref_uid = "burger"
        uid = api.post(ApiTest.CONTENT, preferred_uid=pref_uid)
        self.assertEqual(uid, pref_uid)
        ret_content = api.retrieve(pref_uid)
        self.assertEqual(ret_content, ApiTest.CONTENT)
        
    def test_preferred_uid_clash(self):
        pref_uid = "rtt"
        uid = api.post(ApiTest.CONTENT, preferred_uid=pref_uid)
        self.assertEqual(uid, pref_uid)
        ret_content = api.retrieve(pref_uid)
        self.assertEqual(ret_content, ApiTest.CONTENT)
        uid2 = api.post(ApiTest.CONTENT, preferred_uid=pref_uid)
        self.assertNotEqual(uid2, uid)
    
    def test_normal_retrieve(self):
        uid = api.post(ApiTest.CONTENT)
        ret = api.retrieve(uid)
        self.assertEqual(ApiTest.CONTENT, ret)
        
if __name__ == "__main__":
    unittest.main()

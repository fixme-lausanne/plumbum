#!/usr/bin/env python3
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import rawserver.rawserver as raw
from subprocess import Popen
import subprocess
import unittest
from telnetlib import Telnet
from threading import Thread

class TestRawServer(unittest.TestCase):
    PPORT = 1338
    GPORT = 1339
    IP = "127.0.0.1"
    
    def setUp(self):
        self.server = Thread(target=raw.start, args=(,))

    def tearDown(self):
        pass

    @unittest.skipIf(0 == subprocess.check_output(["netcat", "-h"]),  "Requiers netcat to test")
    def testNetcatPost(self):
        p1 = Popen(["echo", "hello"], stdout=subprocess.PIPE)
        p2 = Popen(["netcat", str(TestRawServer.IP), str(TestRawServer.PPORT)], stdin=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        sys.stderr.write(output)
        
    def testTelnetPost(self):
        conn = Telnet(TestRawServer.IP, TestRawServer.PPORT) 
        conn.write("Hello")
        conn.read_until("No match", 5)
        conn.close()
        
    def testWrongRetrieve(self):
        pass

    def test_gen_behavious(self):
        pass
        
if __name__ == '__main__':
    unittest.main()

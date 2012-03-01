#!/usr/bin/env python3
import rawserver.rawserver as raw
import sys
from os.path import join, dirname, abspath
sys.path.append(join(dirname(abspath(__file__)), "httpserver"))
import bottleserver as http

if __name__ == "__main__":
    raw.start()
    http.start()

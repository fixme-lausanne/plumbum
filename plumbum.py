#!/usr/bin/env python3
import rawserver.rawserver as raw
import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), "httpserver"))
import bottleserver as http

if __name__ == "__main__":
    raw.start()
    http.start()

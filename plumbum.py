#!/usr/bin/env python3
import rawserver.rawserver as raw
import sys
from os.path import join, dirname, abspath
sys.path.append(join(dirname(abspath(__file__)), "httpserver"))
import bottleserver as http
import logging

if __name__ == "__main__":
    logging.info("Starting raw server")
    raw.start()
    logging.info("Starting http server")
    http.start()

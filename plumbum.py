#!/usr/bin/env python
import httpserver.bottleserver as http
import rawserver.rawserver as raw

if __name__ == "__main__":
    raw.start()
    http.start()

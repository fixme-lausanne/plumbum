#!/usr/bin/env python3
import httpserver.bottleserver as http
import rawserver.socketserver as raw

if __name__ == "__main__":
    raw.start()
    http.start()

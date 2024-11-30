# -*- coding:utf-8 -*-

import time
from bottle import response


def generate_events():
    count = 0
    while True:
        yield f"data: Event {count} at {time.ctime()}\n\n"
        count += 1
        time.sleep(1)


# try except KeyboardInterrupt
def events():
    response.content_type = 'text/event-stream'
    return generate_events()

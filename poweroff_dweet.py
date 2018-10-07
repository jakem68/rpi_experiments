#!/usr/bin/env python

__author__ = 'Jan Kempeneers'

import dweepy, time, threading, Queue, os
from subprocess import call


def dweet_listener(thing_name, q):
    while True:
        try:
            for dweet in dweepy.listen_for_dweets_from(thing_name):
                q.put(dweet)
                # print(dweet)
        except:
            print("no incoming messages for {}, reconnecting the listener".format(thing_name))
            pass
        # print(dweet)
        # for dweet in dweepy.listen_for_dweets_from('cirris_dweet135c1'):
        #     print(dweet)


def main():
    test_device = "thisksjtest1"
    q = Queue.Queue()
    thread1 = threading.Thread(target=dweet_listener, args=(test_device, q))
    thread1.start()
    while True:
        print("waiting for incoming message from test_device")
        message = q.get()
        content = message["content"]
        print(content["msg"])
        if content["msg"] == 1:
            os.system('sudo shutdown -h now')

        time.sleep(0.1)


if __name__ == "__main__":
    main()

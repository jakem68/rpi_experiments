#!/usr/bin/env python

__author__ = 'Jan Kempeneers'

import dweepy, time, threading, Queue, sine_variable_to_dweet, webbrowser
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
    test_device = "cirris_dweet135c1"
    q = Queue.Queue()
    thread1 = threading.Thread(target=dweet_listener, args=(test_device, q))
    thread1.start()
    thread2 = threading.Thread(target=sine_variable_to_dweet.run, args=([test_device]))
    thread2.start()
    while True:
        print("waiting for incoming message from test_device")
        message = q.get()
        content = message["content"]
        try:
            switch1 = content["switch1"]
            switch1_switched = True
            print("switch1 is {}".format(switch1))
        except:
            switch1_switched = False
            pass
        try:
            slider1 = content["slider1"]
            print("slider1 is {}".format(slider1))
        except:
            print("error occured")
            pass
        # print(content)
        # print(key1)

        try:
            chrome_path = '/usr/bin/chromium-browser %s'
            url = 'https://youtu.be/weRHyjj34ZE?t=47s'
            if switch1 and switch1_switched:
                call(["amixer", "-D", "pulse", "sset", "Master", "100%"])
                webbrowser.get(chrome_path).open(url)
            if not switch1:
                call(["amixer", "-D", "pulse", "sset", "Master", "0%"])
        except:
            pass

        time.sleep(0.1)


if __name__ == "__main__":
    main()

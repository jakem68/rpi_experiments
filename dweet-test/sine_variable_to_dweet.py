#!/usr/bin/env python

__author__ = 'Jan Kempeneers'

import dweepy, math, time

def run(thing="cirris_dweet135c1"):
    switch1 = False
    slider1=0
    while True:
        # values = {'switch1': switch1}
        slider1 += 10
        sin_slider1 = int(round(math.sin(math.radians(slider1))*100))+100
        values = {'slider1': sin_slider1}
        # print values
        try:
            dweepy.dweet_for(thing, values)
        except:
            print("COULD NOT SEND THIS TIME, WILL TRY AGAIN NEXT TIME ........................................")
            pass
        switch1 = not switch1

        # for dweet in dweepy.listen_for_dweets_from('unipi_haas'):
        #     print(dweet)

        time.sleep(5)

def main():
    run()

if __name__ == "__main__":
    main()

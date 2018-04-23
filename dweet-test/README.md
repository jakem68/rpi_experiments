# dweet-test
A test program to test interactive widgets on Freeboard.io (https://freeboard.io/board/_aZ6J_) running three parallel threads
* sine_variable_to_dweet.py sends a variable to dweet.io to move a slider
* dweet_listener_and_main listens to a dweet variable and passes events to a queue
* and acts upon receiving events in the queue

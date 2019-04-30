import sys
import time

from rtmidi.midiutil import open_midiport

class MidiInputHandler(object):    
    def __call__(self, event, data=None):
        message, _ = event
        print(message)

def create_port(type_, client_name):
    return open_midiport(type_=type_, use_virtual=True, client_name=client_name)

def create_ports(client_name):
    midiin, _ = create_port('input', client_name)
    midiout, _ = create_port('output', client_name)
    return midiin, midiout

client_name = 'Launchpad MK2'

midiin, midiout = create_ports(client_name)

midiin.set_callback(MidiInputHandler())
midiin.ignore_types(sysex=False)

print("Entering main loop. Press Control-C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
    del midiout

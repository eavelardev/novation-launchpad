import novation_launchpad as launchpad
import time

class MidiInputHandler(object):    
    def __call__(self, event, data=None):
        message, _ = event

        if len(message) is 17 and message[:2] == [240, 126] and \
            message[3:8] == [6, 2, 0, 32, 41] and \
            message[9:12] == [0, 0, 0] and message[-1] is 247:

            revision = message[15]
            revision += message[14] * 10
            revision += message[13] * 100
            revision += message[12] * 1000

            device = 'unknown'
            if message[8] is 105:
                device = 'Mk2'
            elif message[8] is 81:
                device = 'Pro'

            print(f'Launchpad {device} [{message[2]}] with firmware revision {revision}.')


def main():

	lp = launchpad.LaunchpadMk2()

	if lp.Open( 0, "mk2" ):
		print( " - Launchpad Mk2: OK" )
	else:
		print( " - Launchpad Mk2: ERROR" )
		return

	lp.midi.devIn.set_callback(MidiInputHandler())
	lp.midi.devIn.ignore_types(sysex=False)

	lp.midi.RawWriteSysEx( [  126, 127, 6, 1 ] )
	time.sleep(0.005)

	lp.Close()
	
if __name__ == '__main__':
	main()

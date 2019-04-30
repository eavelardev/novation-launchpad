import novation_launchpad as launchpad
import time

# -----------------------------
# |   [0,0] ... [7,0]         |
# | -------------------       |
# | | [0,1] ... [7,1] | [8,1] |
# | |  ...       ...  |  ...  |
# | | [0,8] ... [7,8] | [8,8] |
# | -------------------       |
# -----------------------------

def main():
    lp = launchpad.LaunchpadMk2()

    if lp.Open( 0, "mk2" ):
        print( " - Launchpad Mk2: OK" )
    else:
        print( " - Launchpad Mk2: ERROR" )
        return

    lp.ButtonFlush()

    lp.LedCtrlXYByRGB( 0, 1, [63, 0, 0])   # Red
    lp.LedCtrlXYByRGB( 7, 1, [0, 63, 0])   # Green
    lp.LedCtrlXYByRGB( 0, 8, [0, 0, 63])   # Blue
    lp.LedCtrlXYByRGB( 7, 8, [63, 63, 63]) # White

    print("Entering main loop. Press Control-C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        lp.Reset()
        lp.Close()

if __name__ == '__main__':
	main()

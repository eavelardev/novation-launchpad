import novation_launchpad as launchpad
import numpy as np
import time

img_mask = [[0,1,1,0,0,0,0,1],
            [0,0,2,3,0,0,0,3],
            [0,0,0,2,2,2,2,3],
            [3,3,0,2,0,2,2,0],
            [3,3,0,4,2,2,2,3],
            [0,3,0,2,3,3,3,0],
            [0,3,2,3,2,3,2,0],
            [0,0,2,3,5,5,3,0]]

img_colors = [[0,0,0],[29,43,83],[255,255,39],[255,163,0],[255,0,77],[171,82,54]]

img = np.array([[img_colors[img_mask[x][y]] for y in range(8)] for x in range(8)]) // 4

def main():
    lp = launchpad.LaunchpadMk2()

    if lp.Open( 0, "mk2" ):
        print( " - Launchpad Mk2: OK" )
    else:
        print( " - Launchpad Mk2: ERROR" )
        return

    lp.ButtonFlush()

    for x in range(8):
        for y in range(1,9):
            lp.LedCtrlXYByRGB(x, y, list(img[y-1,x]))

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

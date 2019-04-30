import novation_launchpad as launchpad
import cv2 as cv
import time

def main():
    lp = launchpad.LaunchpadMk2()

    if lp.Open( 0, "mk2" ):
        print( " - Launchpad Mk2: OK" )
    else:
        print( " - Launchpad Mk2: ERROR" )
        return

    lp.ButtonFlush()

    img = cv.imread('img/8x8_characters.png')
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) // 4

    img_patch = img[:8, 6:14]

    for x in range(8):
        for y in range(1,9):
            lp.LedCtrlXYByRGB(x, y, list(img_patch[y-1,x]))

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

import cv2 as cv
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

    img = cv.imread('img/8x8_rgb.png', cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    lp.ButtonFlush()

    for x in range(8):
        for y in range(1,9):
            lp.LedCtrlXYByRGB(x, y, list(img[y-1,x] // 4))

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

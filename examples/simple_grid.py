import novation_launchpad as launchpad
import rtmidi
import time

# -----------------------------
# |   [0,0] ... [7,0]         |
# | -------------------       |
# | | [0,1] ... [7,1] | [8,1] |
# | |  ...       ...  |  ...  |
# | | [0,8] ... [7,8] | [8,8] |
# | -------------------       |
# -----------------------------

grid_octave = 2

# You can define your own grid ;)

layout_mask1 = [[28,29,30,31,32,33,34,35],
                [24,25,26,27,36,37,38,39],
                [20,21,22,23,40,41,42,43],
                [16,17,18,19,44,45,46,47],
                [12,13,14,15,48,49,50,51],
                [ 8, 9,10,11,52,53,54,55],
                [ 4, 5, 6, 7,56,57,58,59],
                [ 0, 1, 2, 3,60,61,62,63]]

layout_mask2 = [[28,29,30,31,60,61,62,63],
                [24,25,26,27,56,57,58,59],
                [20,21,22,23,52,53,54,55],
                [16,17,18,19,48,49,50,51],
                [12,13,14,15,44,45,46,47],
                [ 8, 9,10,11,40,41,42,43],
                [ 4, 5, 6, 7,36,37,38,39],
                [ 0, 1, 2, 3,32,33,34,35]]

layout_mask3 = [[28,29,30,31,32,33,34,35],
                [27,26,25,24,39,38,37,36],
                [20,21,22,23,40,41,42,43],
                [19,18,17,16,47,46,45,44],
                [12,13,14,15,48,49,50,51],
                [11,10, 9, 8,55,54,53,52],
                [ 4, 5, 6, 7,56,57,58,59],
                [ 3, 2, 1, 0,63,62,61,60]]

layout_mask4 = [[56,57,58,59,60,61,62,63],
                [48,49,50,51,52,53,54,55],
                [40,41,42,43,44,45,46,47],
                [32,33,34,35,36,37,38,39],
                [24,25,26,27,28,29,30,31],
                [16,17,18,19,20,21,22,23],
                [ 8, 9,10,11,12,13,14,15],
                [ 0, 1, 2, 3, 4, 5, 6, 7]]

# I like this layout
layout_mask5 = [[63,62,61,60,59,58,57,56],
                [48,49,50,51,52,53,54,55],
                [47,46,45,44,43,42,41,40],
                [32,33,34,35,36,37,38,39],
                [31,30,29,28,27,26,25,24],
                [16,17,18,19,20,21,22,23],
                [15,14,13,12,11,10, 9, 8],
                [ 0, 1, 2, 3, 4, 5, 6, 7]]

colors =   [[30, 0, 0],     # 0. middle_c/error
            [0, 10, 30],    # 1. root
            [10, 10, 15],   # 2. white_key/ok
            [0, 0, 0],      # 3. black_key
            [0, 50, 0]]     # 4. pressed


class MidiInputHandler(object):
    def __init__(self, lp):
        self.lp = lp
        self.init_note = grid_octave * 12
        self.velocity = 100
        self.pads_type = None
        self.notes_out = None
        self.my_layout = layout_mask5
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_virtual_port("Grid Instrument")

        self.lp.LedCtrlXYByRGB(0, 0, colors[4])
        self.lp.LedCtrlXYByRGB(1, 0, colors[4])

        # I use this for layout_mask5 to indicate the keys direction
        self.lp.LedCtrlXYByRGB(8, 2, colors[4])
        self.lp.LedCtrlXYByRGB(8, 4, colors[4])
        self.lp.LedCtrlXYByRGB(8, 6, colors[4])
        self.lp.LedCtrlXYByRGB(8, 8, colors[4])

        self.update_layout()

    def __call__(self, event, data=None):
        msg, _ = event
        self.lp.msg = msg

        but = self.lp.ButtonStateXY()
        self.lp.msg = None

        x = but[0]
        y = but[1]
        pressed = but[2] is 127

        if x < 8 and y > 0:
            if pressed:
                self.midiout.send_message([144, self.notes_out[y-1][x], self.velocity])
                self.lp.LedCtrlXYByRGB(x, y, colors[4])
            else:
                self.midiout.send_message([128, self.notes_out[y-1][x], 0])
                self.lp.LedCtrlXYByRGB(x, y, colors[self.pads_type[y-1][x]])
        if x is 0 and y is 0:
            if pressed:
                if self.init_note + 1 <= 48:    # increase one note
                    self.init_note += 1
                    self.lp.LedCtrlXYByRGB(x, y, colors[2])
                    self.update_layout()
                else:
                    self.lp.LedCtrlXYByRGB(x, y, colors[0])
            else:
                    self.lp.LedCtrlXYByRGB(x, y, colors[4])
        if x is 1 and y is 0:
            if pressed:
                if self.init_note - 1 >= 20:    # decrease one note
                    self.init_note -= 1
                    self.lp.LedCtrlXYByRGB(x, y, colors[2])
                    self.update_layout()
                else:
                    self.lp.LedCtrlXYByRGB(x, y, colors[0])
            else:
                    self.lp.LedCtrlXYByRGB(x, y, colors[4])

    def update_layout(self):
        self.notes_out = [[val + self.init_note for val in row] for row in self.my_layout]

        self.pads_type = []

        for row in self.notes_out:
            new_row = []
            for val in row:
                if val is 60:
                    new_row.append(0)
                elif val % 12 is 0:
                    new_row.append(1)
                elif val % 12 in [2,4,5,7,9,11]:
                    new_row.append(2)
                else:
                    new_row.append(3)
            self.pads_type.append(new_row)

        for x in range(8):
            for y in range(1,9):
                self.lp.LedCtrlXYByRGB(x, y, colors[self.pads_type[y-1][x]])
        

def main():
    lp = launchpad.LaunchpadMk2()

    if lp.Open( 0, "mk2" ):
        print( " - Launchpad Mk2: OK" )
    else:
        print( " - Launchpad Mk2: ERROR" )
        return

    lp.midi.devIn.set_callback(MidiInputHandler(lp))

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

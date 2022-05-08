# An imperfect adaptation of 
# https://community.element14.com/challenges-projects/project14/acoustics/b/blog/posts/neotrellis-synth
# for the Adafruit 8x8 NeoTrellis Feather M4 Kit Pack : ID 1929

from time import sleep
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

import board
import busio

from digitalio import DigitalInOut, Direction, Pull
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

i2c_bus = busio.I2C(board.SCL, board.SDA)

int_pin = DigitalInOut(board.D5)
int_pin.direction = Direction.INPUT
int_pin.pull = Pull.DOWN

trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x30), NeoTrellis(i2c_bus, False, addr=0x2E)],
    [NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x31)],
]

trellis = MultiTrellis(trelli)
tempo = 240  # Starting BPM - higher than 400 is iffy
clocksrc = 0  # 0 for internal clock, 1 for any incoming NoteOn over Midi Ch2 as clock

# colors for the 8 triggers
TRIGGER_COLOR = (
    (0, 0, 255),
    (0, 124, 255),
    (0, 255, 124),
    (0, 255, 30),
    (30, 255, 0),
    (124, 255, 0),
    (255, 124, 0),
    (255, 0, 0),
)

TICKER_COLOR = (255, 255, 255)


def wheel(pos):  # Input a value 0 to 255 to get a color value.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    elif pos < 85:
        return (int(pos * 3), int(255 - pos * 3), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - pos * 3), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))


# light up all keys at start
for y in range(8):
    for x in range(8):
        trellis.color(x, y, 0x303030)
        sleep(0.01)

midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=1, midi_out=usb_midi.ports[1], out_channel=0
)

# Our global state
current_step = 7  # we start on the last step since we increment first
# the state of the sequencer
beatstate = [
    [False] * 8,
    [False] * 8,
    [False] * 8,
    [False] * 8,
    [False] * 8,
    [False] * 8,
    [False] * 8,
    [False] * 8,
]
# our notes per y-axis row
notestate = [24, 25, 26, 27, 28, 29, 30, 31]  # C0  # D0  # E0  # F0  # G0


def pulse(x, y, edge):  # Check for pressed buttons
    if edge == NeoTrellis.EDGE_RISING:
        beatstate[y][x] = not beatstate[y][x]  # enable the trigger
        if beatstate[y][x]:
            color = TRIGGER_COLOR[y]
        else:
            color = 0
        trellis.color(x, y, color)


def tick():
    global current_step
    # redraw the last step to remove the ticker bar (e.g. 'normal' view)
    for y in range(8):
        color = 0
        if beatstate[y][current_step]:
            color = TRIGGER_COLOR[y]
        trellis.color(current_step, y, color)

    # next beat!
    current_step = (current_step + 1) % 8

    # draw the vertical ticker bar, with selected voices highlighted
    for y in range(8):
        if beatstate[y][current_step]:
            r, g, b = TRIGGER_COLOR[y]
            color = (r // 2, g // 2, b // 2)
            midi.send(NoteOn(notestate[y]))
            midi.send(NoteOff(notestate[y]))
        else:
            color = TICKER_COLOR
            midi.send(NoteOff(notestate[y]))
        trellis.color(current_step, y, color)

for y in range(8):
    for x in range(8):
        trellis.color(x, y, 0x0)
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, pulse)
        sleep(0.01)

while True:
    if (clocksrc=1):
        msg = midi.receive()
        if isinstance(msg, NoteOn):
            tick()

        trellis.sync()
    else:
        stamp = time.monotonic()
        tick()
        while time.monotonic() - stamp < 60/tempo:
            trellis.sync()
            time.sleep(0.01)  # a little delay here helps avoid debounce annoyances


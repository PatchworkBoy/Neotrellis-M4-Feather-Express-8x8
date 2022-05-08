# Write your code here :-)
from time import sleep

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.midi_message import note_parser
from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend

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
    [NeoTrellis(i2c_bus, False, addr=0x30),
     NeoTrellis(i2c_bus, False, addr=0x2E)],
    [NeoTrellis(i2c_bus, False, addr=0x2F),
     NeoTrellis(i2c_bus, False, addr=0x31)]
]
trellis = MultiTrellis(trelli)

# light up all keys at start
for y in range(8):
    for x in range(8):
        trellis.color(y, x, 0x909090)
        sleep(0.01)

midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0],
     in_channel=1, midi_out=usb_midi.ports[1], out_channel=0)

def XY(x, y, offset=-1):
    return (y + offset) * 8 + (x + offset)

OFF = (0, 0, 0)
RED = (200, 0, 0)
ORANGE = (150, 50, 0)
YELLOW = (100, 100, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
PURPLE = (100, 0, 200)
PINK = (130, 0, 70)
W25 = (25, 25, 25)
W50 = (50, 50, 50)
W75 = (75, 75, 75)
W100 = (100, 100, 100)
color = OFF

def momentary(color=OFF, off=-1, on=-1, x=-1, y=-1):  # use to make key momentary
    if on == -1:
        on = color
    if off == -1:
        off = (round(on[0] / 5), round(on[1] / 5), round(on[2] / 5))
    return {"off": off, "on": on, "type": "momentary", "x": x, "y": y}

def latching(color=OFF, off=-1, on=-1, x=-1, y=-1):  # use to make key latching
    if on == -1:
        on = color
    if off == -1:
        off = (round(on[0] / 5), round(on[1] / 5), round(on[2] / 5))
    return {"off": off, "on": on, "state": False, "type": "latching", "x": x, "y": y}

# --------------------------------------------------------------------------------------

# BUTTONS  0 = button, 1 = pad data, 2 = midi data (need to change some code around to get this to work)

x = 0

BUTTONS = [
    [XY(1, 1), momentary(YELLOW, x = 1, y = 1)],
    [XY(2, 1), momentary(YELLOW, x = 2, y = 1)],
    [XY(3, 1), momentary(YELLOW, x = 3, y = 1)],
    [XY(4, 1), momentary(YELLOW, x = 4, y = 1)],
    [XY(5, 1), momentary(BLUE, x = 5, y = 1)],
    [XY(6, 1), momentary(BLUE, x = 6, y = 1)],
    [XY(7, 1), momentary(BLUE, x = 7, y = 1)],
    [XY(8, 1), momentary(BLUE, x = 8, y = 1)],
    [XY(1, 2), momentary(YELLOW, x = 1, y = 2)],
    [XY(2, 2), momentary(YELLOW, x = 2, y = 2)],
    [XY(3, 2), momentary(W50, x = 3, y = 2)],
    [XY(4, 2), momentary(W50, x = 4, y = 2)],
    [XY(5, 2), momentary(BLUE, x = 5, y = 2)],
    [XY(6, 2), momentary(BLUE, x = 6, y = 2)],
    [XY(7, 2), momentary(BLUE, x = 7, y = 2)],
    [XY(8, 2), momentary(BLUE, x = 8, y = 2)],
    [XY(1, 3), momentary(W75, x = 1, y = 3)],
    [XY(2, 3), momentary(RED, x = 2, y = 3)],
    [XY(3, 3), momentary(RED, x = 3, y = 3)],
    [XY(4, 3), momentary(RED, x = 4, y = 3)],
    [XY(5, 3), momentary(BLUE, x = 5, y = 3)],
    [XY(6, 3), momentary(BLUE, x = 6, y = 3)],
    [XY(7, 3), momentary(BLUE, x = 7, y = 3)],
    [XY(8, 3), momentary(BLUE, x = 8, y = 3)],
    [XY(1, 4), momentary(RED, x = 1, y = 4)],
    [XY(2, 4), momentary(RED, x = 2, y = 4)],
    [XY(3, 4), momentary(RED, x = 3, y = 4)],
    [XY(4, 4), momentary(RED, x = 4, y = 4)],
    [XY(5, 4), momentary(BLUE, x = 5, y = 4)],
    [XY(6, 4), momentary(BLUE, x = 6, y = 4)],
    [XY(7, 4), momentary(BLUE, x = 7, y = 4)],
    [XY(8, 4), momentary(BLUE, x = 8, y = 4)],
    [XY(1, 5), latching(PINK, x = 1, y = 5)],
    [XY(2, 5), latching(PINK, x = 2, y = 5)],
    [XY(3, 5), latching(PINK, x = 3, y = 5)],
    [XY(4, 5), latching(PINK, x = 4, y = 5)],
    [XY(5, 5), latching(PINK, x = 5, y = 5)],
    [XY(6, 5), latching(PINK, x = 6, y = 5)],
    [XY(7, 5), latching(PINK, x = 7, y = 5)],
    [XY(8, 5), latching(PINK, x = 8, y = 5)],
    [XY(1, 6), latching(GREEN, x = 1, y = 6)],
    [XY(2, 6), latching(GREEN, x = 2, y = 6)],
    [XY(3, 6), latching(GREEN, x = 3, y = 6)],
    [XY(4, 6), latching(GREEN, x = 4, y = 6)],
    [XY(5, 6), latching(GREEN, x = 5, y = 6)],
    [XY(6, 6), latching(GREEN, x = 6, y = 6)],
    [XY(7, 6), latching(GREEN, x = 7, y = 6)],
    [XY(8, 6), latching(GREEN, x = 8, y = 6)],
    [XY(1, 7), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 1, y = 7)],
    [XY(2, 7), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 2, y = 7)],
    [XY(3, 7), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 3, y = 7)],
    [XY(4, 7), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 4, y = 7)],
    [XY(5, 7), momentary(ORANGE, x = 5, y = 7)],
    [XY(6, 7), momentary(ORANGE, x = 6, y = 7)],
    [XY(7, 7), momentary(ORANGE, x = 7, y = 7)],
    [XY(8, 7), momentary(ORANGE, x = 7, y = 7)],
    [XY(1, 8), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 1, y = 8)],
    [XY(2, 8), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 2, y = 8)],
    [XY(3, 8), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 3, y = 8)],
    [XY(4, 8), momentary(off=(50, 50, 50), on=(50, 20, 20), x = 4, y = 8)],
    [XY(5, 8), momentary(ORANGE, x = 5, y = 8)],
    [XY(6, 8), momentary(ORANGE, x = 6, y = 8)],
    [XY(7, 8), momentary(off=(100, 100, 100), on=W75, x = 7, y = 8)],
    [XY(8, 8), momentary(off=(100, 100, 100), on=W75, x = 8, y = 8)],
]

# --------------------------------------------------------------------------------------

buttonData = [{}, {}]  # [{key nums: data}, {key nums: midi data}]
keys = (
    []
)  # [keynum] -> [1 = key data [momentary, latching]], [2 = midi data (int or tuple)]

for button in BUTTONS:
    buttonData[0].update({button[0]: button[1]})  # add key data

for keynum in range(0, 64):
    stuff = [
        keynum,
        buttonData[0].get(keynum, {"off": OFF, "on": OFF, "type": "empty"}),
        buttonData[1].get(keynum, 0),
    ]

    keys.append(stuff)

# --------------------------------------------------------------------------------------

def blink(xcoord, ycoord, edge):
    padNum = XY(xcoord, ycoord, 0)

    if edge == NeoTrellis.EDGE_RISING:
        # print('key press! ', padNum)

        if keys[padNum][1]["type"] is "momentary":
            #print("momentary ", padNum, " on")
            midi.send(NoteOn(padNum))

            color = keys[padNum][1]["on"]
            trellis.color(xcoord, ycoord, color)

        elif keys[padNum][1]["type"] is "latching":
            midi.send(NoteOn(padNum))
            if not keys[padNum][1]["state"]:
                color = keys[padNum][1]["on"]
                #print("latching ", padNum, " on ", keys[padNum])

            elif keys[padNum][1]["state"]:
                color = keys[padNum][1]["off"]
                #print("latching ", padNum, " off ", keys[padNum])

            trellis.color(xcoord, ycoord, color)
            keys[padNum][1]["state"] = not keys[padNum][1]["state"]

        elif keys[padNum][1]["type"] is "empty":
            print("Empty")

    elif edge == NeoTrellis.EDGE_FALLING:
        midi.send(NoteOff(padNum))
        # print('key release! ', padNum)
        if keys[padNum][1]["type"] is "momentary":
            #print("momentary ", padNum, " off")
            color = keys[padNum][1]["off"]
            trellis.color(xcoord, ycoord, color)

# turn off all keys now. this way you can tell if anything errored between line 32 and here
for y in range(8):
    for x in range(8):
        trellis.color(x, y, keys[XY(x, y, 0)][1]["off"])
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, blink)
        sleep(0.01)

def noteLED(note):
    pad = keys[note][1]
    if pad["type"] is "latching" and pad["state"] is True:
        color = pad["on"]
    else:
        color = pad["off"]
    cx = pad["x"]-1
    cy = pad["y"]-1
    trellis.color(cx, cy, PURPLE)

def LEDoff(note):
    pad = keys[note][1]
    if pad["type"] is "latching" and pad["state"] is True:
        color = pad["on"]
    else:
        color = pad["off"]
    cx = pad["x"]-1
    cy = pad["y"]-1
    trellis.color(cx, cy, color)

while True:
    trellis.sync()
    msg = midi.receive()
    if isinstance(msg, NoteOn) and msg.velocity != 0:
        noteLED(msg.note)
    elif isinstance(msg, NoteOff):
        LEDoff(msg.note)

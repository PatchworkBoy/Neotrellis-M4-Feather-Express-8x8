# Adafruit's 8x8 NeoTrellis Feather M4 Kit
https://github.com/adafruit | https://www.adafruit.com/product/1929

Seems very few sketches &amp; examples have been updated for the Adafruit Neotrellis M4 Feather Express 8x8 Kit, so here are ones I've cobbled together thus far, mainly ripped from code for the earlier NeotrellisM4 4x8 (https://www.adafruit.com/product/4020 - can still get from Digi-Key)... 

None of these are perfect, all need improvement, but give a vague starting point.

Don't hammer any of these with too much MIDI In data... the Feather will lag and buffer. Can tell this is happening by ceasing MIDI input and watching things continue to react. Typically sending much beyond 480bpm NoteOn pulse to MIDI In on Ch16 is enough to cause things to lag (eg: sixteenths at 120bpm). 

The whole timing side of things needs work - these are all very hacky basic sketches.

- https://github.com/PatchworkBoy/Neotrellis-M4-Feather-Express-8x8/tree/main/cp_sequencer : CircuitPython USB-MIDI sequencer, 8 steps x 8 channels. Uses internal clock by default. Fire any NoteOn in on Channel2 to provide an external clock. Recommend fiddling around in VCVRack2Free to convert it into a 4x16 / 2x32 / 2x24 & 1x8 sequencer etc using 8-in-1-out sequential switch, triggered by a single step on Ch8 (for example). Adapted from https://community.element14.com/challenges-projects/project14/acoustics/b/blog/posts/neotrellis-synth. WARNING: Has timing issues. Will wander in and out of sync with an identical BPM clock, regardless of internal or external sync. 
- https://github.com/PatchworkBoy/Neotrellis-M4-Feather-Express-8x8/tree/main/cp_basiccontroller : CircuitPython USB-MIDI controller. Supports momentary and latching buttons. Provides MIDI Feedback via MIDI NoteOn sent to MIDI In on channel 2 lighting the matching key on the keypad. Adapted from https://github.com/theisaaclloyd/neotrellism4-midi-controller.
- https://github.com/PatchworkBoy/Neotrellis-M4-Feather-Express-8x8/tree/main/ino_basiccontroller : Arduino C++ implementation of the CircuitPython USB-MIDI controller above - needs setting to TinyUSB stack. Outputs NoteOn/Off C0 thru D#5 on all channels. Send any NoteOn to MIDI In on channel 16 to trigger a column ticker. Same to channel 15 for a row ticker. Sending any MIDI note to Channel14 triggers a reset of both column and row tickers to position 0. Sending NoteOn to any other channel will flash respective mapped key for that note. Perfect for use with Trowasoft triggerSeq / Stoermelder MIDI-CAT in VCVRack, sending x2 clock to ch16, x4 clock to trowasoft, /4 clock to ch15.

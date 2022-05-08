# Adafruit's Neotrellis-M4-Feather-Express-8x8
https://www.adafruit.com/product/1929

Seems very few sketches &amp; examples exist for the updated Adafruit Neotrellis M4 Feather Express 8x8 UNTZstrument refresh, so here are ones I've cobbled together thus far... none of these are perfect, all need improvement, but give a semi-decent starting point.

- https://github.com/PatchworkBoy/Neotrellis-M4-Feather-Express-8x8/tree/main/cp_sequencer : CircuitPython USB-MIDI sequencer, 8 steps x 8 channels. Uses internal clock by default. Fire any NoteOn in on Channel2 to provide an external clock. Recommend fiddling around in VCVRack2Free to convert it into a 4x16 / 2x32 / 2x24 & 1x8 sequencer etc using 8-in-1-out sequential switch, triggered by a single step on Ch8 (for example). Adapted from https://community.element14.com/challenges-projects/project14/acoustics/b/blog/posts/neotrellis-synth. WARNING: Has timing issues. Will wander in and out of sync with an identical BPM clock, regardless of internal or external sync.

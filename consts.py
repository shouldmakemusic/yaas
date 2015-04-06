import Live 

IS_LIVE_9 = Live.Application.get_application().get_major_version() == 9

LOOPER = "Looper"
CHANNEL = 0 # Channels are numbered 0 through 15, this script only makes use of one MIDI Channel (Channel 1)
CHANNEL_LIGHTHOUSE = 1 # Midi channel 2

DEFAULT_PORT_LIGHTHOUSE = 9050
DEFAULT_OSC_RECEIVE = False
DEFAULT_SHOW_RED_FRAME = True

MIDI_NOTE_TYPE = 0

MAX_LOOPER = 1.0
MIN_LOOPER = 0.0

MESSAGE_TYPE_MIDI_NOTE_PRESSED = 144
MESSAGE_TYPE_MIDI_NOTE_RELEASED = 128
MESSAGE_TYPE_MIDI_CC = 176
MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_PRESSED = 145
MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_RELEASED = 129

#track
num_tracks = 7 

NEXT = True
PREV = False
CURRENT = -1

MIDI_CC = 'MIDI CC'

PLAY = 'PLAY'
STOP = 'STOP'
RECORD = 'RECORD'

CHAIN_MODE_SHORTENED = True

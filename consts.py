import Live 

IS_LIVE_9 = Live.Application.get_application().get_major_version() == 9

# for multiple instances these constants have to be adopted
YAAS_DIR = "YAAS"

PORT_LIGHTHOUSE = 9050

CURRENT = -1
LOOPER = "Looper"
CHANNEL = 0 # Channels are numbered 0 through 15, this script only makes use of one MIDI Channel (Channel 1)
CHANNEL_LIGHTHOUSE = 1 # Midi channel 2


MIDI_NOTE_TYPE = 0
MAX = 1000
MIN = -1000
MAX_LOOPER = 1.0
MIN_LOOPER = 0.0

MESSAGE_TYPE_MIDI_NOTE_PRESSED = 144
MESSAGE_TYPE_MIDI_NOTE_RELEASED = 128
MESSAGE_TYPE_MIDI_CC = 176
MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_PRESSED = 145
MESSAGE_TYPE_LIGHTHOUSE_MIDI_NOTE_RELEASED = 129

#track
num_tracks = 7 



# method, track_id, chain_nr
DEVICE_HELPER = 'device_helper'
TRACK_HELPER  = 'track_helper'
LOOPER_HELPER = 'looper_helper'
PEDAL_HELPER = 'pedal_helper'

NEXT = True
PREV = False



CHAIN_MODE_SHORTENED = True

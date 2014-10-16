import Live 

IS_LIVE_9 = Live.Application.get_application().get_major_version() == 9
IS_LIVE_9_1 = IS_LIVE_9 and Live.Application.get_application().get_minor_version() >= 1
IS_LIVE_9_2 = IS_LIVE_9 and Live.Application.get_application().get_minor_version() >= 2

CURRENT = -1
LOOPER = "Looper"

MIDI_NOTE_TYPE = 0
MAX = 1000
MIN = -1000
MAX_LOOPER = 1.0
MIN_LOOPER = 0.0

#track
num_tracks = 7 

#track_volume = 14 #this is cc
#arm_current_track = 1

clip_launch_notes = [92, 93, 94, 95, 97, 98, 99] #this is a set of seven "white" notes, starting at C3

# track
select_track_notes = [11, 21, 31, 41, 51, 61]
looper_notes = [15, 25, 35, 45, 55, 65]
stop_clips_notes = [20, 30, 40, 50, 60, 70]
# 101 und 111 sind die beiden pedale bei bank 0 ...
track_stop_notes = [100] #momentan ist nur ein track selectiert - das stopt ihn

# device
rec_all_notes = [17, 27, 37, 47, 57, 67]
click_notes = [18, 28, 38, 48, 58, 68]
tap_tempo_notes = [19, 29, 39, 49, 59, 69]

# scene
scene_down = [82]
scene_up = [87]
#scene_launch_notes = [60, 62, 64, 65, 67, 69, 71] das koennte die szene wie die tracks abspielen lassen
stop_all_clips = 88
play_current_scene = 83

# navigation / red box movement
select_box_right = [86, 96, 76]
select_box_left = [81, 91, 71]
select_box_down = [85]
select_box_up = [90]

# method, track_id, chain_nr
DEVICE_HELPER = 'device_helper'
TRACK_HELPER  = 'track_helper'
LOOPER_HELPER = 'looper_helper'
PEDAL_HELPER = 'pedal_helper'

NEXT = True
PREV = False
midi_note_definitions = {
#    1  : [[TRACK_HELPER, CURRENT], 'arm', []],
    6  : [[TRACK_HELPER, 0], 'get_focus', []],
    16 : [[TRACK_HELPER, 0      ], 'arm', []],
    26 : [[TRACK_HELPER, 1      ], 'arm', []],
    36 : [[TRACK_HELPER, 2      ], 'arm', []],
    46 : [[TRACK_HELPER, 3      ], 'arm', []],
    56 : [[TRACK_HELPER, 4      ], 'arm', []],
    66 : [[TRACK_HELPER, 5      ], 'arm', []],
    2  : [DEVICE_HELPER, 'set_chain_selector', [0, 0]],
    3  : [DEVICE_HELPER, 'set_chain_selector', [0, 1]],
    4  : [DEVICE_HELPER, 'set_chain_selector', [0, 2]],
    5  : [DEVICE_HELPER, 'set_chain_selector', [0, 3]],
    7  : [DEVICE_HELPER, 'set_chain_selector', [0, 4]],
    8  : [DEVICE_HELPER, 'set_chain_selector', [0, 5]],
    9  : [DEVICE_HELPER, 'set_chain_selector', [0, 6]],
    10 : [DEVICE_HELPER, 'set_chain_selector', [0, 7]],
#    2  : [DEVICE_HELPER, 'trigger_device_chain', [0, 0]],
#    3  : [DEVICE_HELPER, 'trigger_device_chain', [0, 1]],
#    4  : [DEVICE_HELPER, 'trigger_device_chain', [0, 2]],
#    5  : [DEVICE_HELPER, 'trigger_device_chain', [0, 3]],
#    7  : [DEVICE_HELPER, 'trigger_device_chain', [0, 4]],
#    8  : [DEVICE_HELPER, 'trigger_device_chain', [0, 5]],
#    9  : [DEVICE_HELPER, 'trigger_device_chain', [0, 6]],
#    10 : [DEVICE_HELPER, 'trigger_device_chain', [0, 7]],
    72 : [LOOPER_HELPER, 'activate_looper', [1]],     
    74 : [LOOPER_HELPER, 'activate_looper', [2]], 
    77 : [LOOPER_HELPER, 'switch_view', [1]],
    79 : [LOOPER_HELPER, 'switch_view', [2]],
    12 : [DEVICE_HELPER, 'navigate_device_focus', [0, PREV]],
    22 : [DEVICE_HELPER, 'navigate_device_focus', [1, PREV]],
    32 : [DEVICE_HELPER, 'navigate_device_focus', [2, PREV]],
    42 : [DEVICE_HELPER, 'navigate_device_focus', [3, PREV]],
    52 : [DEVICE_HELPER, 'navigate_device_focus', [4, PREV]],
    62 : [DEVICE_HELPER, 'navigate_device_focus', [5, PREV]],
    13 : [DEVICE_HELPER, 'navigate_device_focus', [0, NEXT]],
    23 : [DEVICE_HELPER, 'navigate_device_focus', [1, NEXT]],
    33 : [DEVICE_HELPER, 'navigate_device_focus', [2, NEXT]],
    43 : [DEVICE_HELPER, 'navigate_device_focus', [3, NEXT]],
    53 : [DEVICE_HELPER, 'navigate_device_focus', [4, NEXT]],
    63 : [DEVICE_HELPER, 'navigate_device_focus', [5, NEXT]],
    14 : [DEVICE_HELPER, 'toggle_device', [0, CURRENT]],
    24 : [DEVICE_HELPER, 'toggle_device', [0, CURRENT]],
    34 : [DEVICE_HELPER, 'toggle_device', [0, CURRENT]],
    44 : [DEVICE_HELPER, 'toggle_device', [0, CURRENT]],
    54 : [DEVICE_HELPER, 'toggle_device', [0, CURRENT]],
    64 : [DEVICE_HELPER, 'toggle_device', [0, CURRENT]],
    1  : [DEVICE_HELPER, 'use_trigger_device_chain_for_pedals', [0]],
}
midi_cc_definitions = {
    101: [PEDAL_HELPER,  'handle_effect_slider', [0, 1]],
    111: [PEDAL_HELPER,  'handle_effect_slider', [0, 2]],
    102: [PEDAL_HELPER,  'handle_send', [0, 0]],
    112: [PEDAL_HELPER,  'handle_send', [0, 1]],
    103: [PEDAL_HELPER,  'handle_send', [1, 0]],
    113: [PEDAL_HELPER,  'handle_send', [1, 1]],
    104: [PEDAL_HELPER,  'handle_send', [2, 0]],
    114: [PEDAL_HELPER,  'handle_send', [2, 1]],
    105: [PEDAL_HELPER,  'handle_send', [3, 0]],
    115: [PEDAL_HELPER,  'handle_send', [3, 1]],
    106: [PEDAL_HELPER,  'handle_send', [4, 0]],
    116: [PEDAL_HELPER,  'handle_send', [4, 1]],
    107: [PEDAL_HELPER,  'handle_send', [5, 0]],
    117: [PEDAL_HELPER,  'handle_send', [5, 1]],
    108: [PEDAL_HELPER,  'handle_volume', [CURRENT, 0]],
    118: [PEDAL_HELPER,  'handle_volume', [CURRENT, 1]],
    109: [PEDAL_HELPER,  'handle_volume', [CURRENT, 0]],
    119: [PEDAL_HELPER,  'handle_volume', [CURRENT, 1]],
    110: [PEDAL_HELPER,  'handle_volume', [CURRENT, 0]],
    120: [PEDAL_HELPER,  'handle_volume', [CURRENT, 1]],
}

TRIGGER_DEVICE_CHAIN_NAME_INC = "Effekte Inc"
TRIGGER_DEVICE_CHAIN_NAME_EXC = "Effekte Exc"
TRIGGER_DEVICE_CHAIN_NAME = ["Effekte", "Didge Effekt Rack"]
CHAIN_MODE_SHORTENED = True

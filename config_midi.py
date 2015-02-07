from consts import *

RED_FRAME_CONTROLLER = "RedFrameController"
TRACK_CONTROLLER = "TrackController"
SONG_CONTROLLER = "SongController"

# scene
scene_down = [82]
scene_up = [87]
stop_all_clips = 88
play_current_scene = 83

# navigation / red box movement
select_box_right = [86, 96, 76]
select_box_left = [81, 91, 71]
select_box_down = [85]
select_box_up = [90]

midi_note_definitions = {
    
    # Bank 00
    1  : [DEVICE_HELPER, 'select_current_then_select_next_hash_device', [0]],
    2  : [DEVICE_HELPER, 'set_chain_selector', [0]],
    3  : [DEVICE_HELPER, 'set_chain_selector', [1]],
    4  : [DEVICE_HELPER, 'set_chain_selector', [2]],
    5  : [DEVICE_HELPER, 'set_chain_selector', [3]],

    6  : [[TRACK_HELPER, 0], 'get_focus', []],
    7  : [DEVICE_HELPER, 'set_chain_selector', [4]],
    8  : [DEVICE_HELPER, 'set_chain_selector', [5]],
    9  : [DEVICE_HELPER, 'set_chain_selector', [6]],
    10 : [DEVICE_HELPER, 'set_chain_selector', [7]],

    # Bank 01    
    12 : [DEVICE_HELPER, 'navigate_device_focus', [0, PREV]],
    13 : [DEVICE_HELPER, 'navigate_device_focus', [0, NEXT]],
    14 : [DEVICE_HELPER, 'toggle_device', [CURRENT, CURRENT]],
    15 : [LOOPER_HELPER, 'clipLooper', [0]],
    16 : [[TRACK_HELPER, 0], 'arm', []],
    
#    2  : [DEVICE_HELPER, 'trigger_device_chain', [0, 0]],
#    3  : [DEVICE_HELPER, 'trigger_device_chain', [0, 1]],
#    4  : [DEVICE_HELPER, 'trigger_device_chain', [0, 2]],
#    5  : [DEVICE_HELPER, 'trigger_device_chain', [0, 3]],
#    7  : [DEVICE_HELPER, 'trigger_device_chain', [0, 4]],
#    8  : [DEVICE_HELPER, 'trigger_device_chain', [0, 5]],
#    9  : [DEVICE_HELPER, 'trigger_device_chain', [0, 6]],
#    10 : [DEVICE_HELPER, 'trigger_device_chain', [0, 7]],
    26 : [[TRACK_HELPER, 1      ], 'arm', []],
    36 : [[TRACK_HELPER, 2      ], 'arm', []],
    46 : [[TRACK_HELPER, 3      ], 'arm', []],
    56 : [[TRACK_HELPER, 4      ], 'arm', []],
    66 : [[TRACK_HELPER, 5      ], 'arm', []],

    72 : [LOOPER_HELPER, 'activate_looper', [1]],     
    74 : [LOOPER_HELPER, 'activate_looper', [2]], 
    77 : [LOOPER_HELPER, 'switch_view', [1]],
    79 : [LOOPER_HELPER, 'switch_view', [2]],
    22 : [DEVICE_HELPER, 'navigate_device_focus', [1, PREV]],
    32 : [DEVICE_HELPER, 'navigate_device_focus', [2, PREV]],
    42 : [DEVICE_HELPER, 'navigate_device_focus', [3, PREV]],
    52 : [DEVICE_HELPER, 'navigate_device_focus', [4, PREV]],
    62 : [DEVICE_HELPER, 'navigate_device_focus', [5, PREV]],
    23 : [DEVICE_HELPER, 'navigate_device_focus', [1, NEXT]],
    33 : [DEVICE_HELPER, 'navigate_device_focus', [2, NEXT]],
    43 : [DEVICE_HELPER, 'navigate_device_focus', [3, NEXT]],
    53 : [DEVICE_HELPER, 'navigate_device_focus', [4, NEXT]],
    63 : [DEVICE_HELPER, 'navigate_device_focus', [5, NEXT]],
    24 : [DEVICE_HELPER, 'toggle_device', [CURRENT, CURRENT]],
    34 : [DEVICE_HELPER, 'toggle_device', [CURRENT, CURRENT]],
    44 : [DEVICE_HELPER, 'toggle_device', [CURRENT, CURRENT]],
    54 : [DEVICE_HELPER, 'toggle_device', [CURRENT, CURRENT]],
    64 : [DEVICE_HELPER, 'toggle_device', [CURRENT, CURRENT]],
    25 : [LOOPER_HELPER, 'clipLooper', [1]],
    35 : [LOOPER_HELPER, 'clipLooper', [2]],
    45 : [LOOPER_HELPER, 'clipLooper', [3]],
    55 : [LOOPER_HELPER, 'clipLooper', [4]],
    65 : [LOOPER_HELPER, 'clipLooper', [5]],
    

    92 : [RED_FRAME_CONTROLLER, 'play_clip', [1]],
    93 : [RED_FRAME_CONTROLLER, 'play_clip', [2]],
    94 : [RED_FRAME_CONTROLLER, 'play_clip', [3]],
    95 : [RED_FRAME_CONTROLLER, 'play_clip', [4]],
    97 : [RED_FRAME_CONTROLLER, 'play_clip', [5]],
    98 : [RED_FRAME_CONTROLLER, 'play_clip', [6]],
    99 : [RED_FRAME_CONTROLLER, 'play_clip', [7]],
    
    20 : [TRACK_CONTROLLER, 'stop_or_restart_clip', [1]],
    30 : [TRACK_CONTROLLER, 'stop_or_restart_clip', [2]],
    40 : [TRACK_CONTROLLER, 'stop_or_restart_clip', [3]],
    50 : [TRACK_CONTROLLER, 'stop_or_restart_clip', [4]],
    60 : [TRACK_CONTROLLER, 'stop_or_restart_clip', [5]],
    70 : [TRACK_CONTROLLER, 'stop_or_restart_clip', [6]],
    100: [TRACK_CONTROLLER, 'stop', [CURRENT]],
    
    17 : [SONG_CONTROLLER, 'record', []],
    27 : [SONG_CONTROLLER, 'record', []],
    37 : [SONG_CONTROLLER, 'record', []],
    47 : [SONG_CONTROLLER, 'record', []],
    57 : [SONG_CONTROLLER, 'record', []],
    67 : [SONG_CONTROLLER, 'record', []],
    18 : [SONG_CONTROLLER, 'metronom', []],
    28 : [SONG_CONTROLLER, 'metronom', []],
    38 : [SONG_CONTROLLER, 'metronom', []],
    48 : [SONG_CONTROLLER, 'metronom', []],
    58 : [SONG_CONTROLLER, 'metronom', []],
    68 : [SONG_CONTROLLER, 'metronom', []],
    19 : [SONG_CONTROLLER, 'tap_tempo', []],
    29 : [SONG_CONTROLLER, 'tap_tempo', []],
    39 : [SONG_CONTROLLER, 'tap_tempo', []],
    49 : [SONG_CONTROLLER, 'tap_tempo', []],
    59 : [SONG_CONTROLLER, 'tap_tempo', []],
    69 : [SONG_CONTROLLER, 'tap_tempo', []],
    11 : [SONG_CONTROLLER, 'select_track', [1]],
    21 : [SONG_CONTROLLER, 'select_track', [2]],
    31 : [SONG_CONTROLLER, 'select_track', [3]],
    41 : [SONG_CONTROLLER, 'select_track', [4]],
    51 : [SONG_CONTROLLER, 'select_track', [5]],
    61 : [SONG_CONTROLLER, 'select_track', [6]],
    
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
from consts import *

RED_FRAME_CONTROLLER = "RedFrameController"
TRACK_CONTROLLER = "TrackController"
SONG_CONTROLLER = "SongController"
SCENE_CONTROLLER = "SceneController"
DEVICE_CONTROLLER = "DeviceController"
PEDAL_CONTROLLER = "PedalController"
LOOPER_CONTROLLER = "LooperController"

# navigation / red box movement
select_box_right = [86, 96, 76]
select_box_left = [81, 91, 71]
select_box_down = [85]
select_box_up = [90]

midi_note_definitions = {
    
    # Bank 00
    1  : [DEVICE_CONTROLLER, 'select_current_then_select_next_hash_device', [0]],
    2  : [DEVICE_CONTROLLER, 'set_chain_selector', [0]],
    3  : [DEVICE_CONTROLLER, 'set_chain_selector', [1]],
    4  : [DEVICE_CONTROLLER, 'set_chain_selector', [2]],
    5  : [DEVICE_CONTROLLER, 'set_chain_selector', [3]],

    6  : [TRACK_CONTROLLER, 'get_focus', [1]],
    
    7  : [DEVICE_CONTROLLER, 'set_chain_selector', [4]],
    8  : [DEVICE_CONTROLLER, 'set_chain_selector', [5]],
    9  : [DEVICE_CONTROLLER, 'set_chain_selector', [6]],
    10 : [DEVICE_CONTROLLER, 'set_chain_selector', [7]],

    # Bank 01    
    12 : [DEVICE_CONTROLLER, 'navigate_device_focus', [0, PREV]],
    13 : [DEVICE_CONTROLLER, 'navigate_device_focus', [0, NEXT]],
    
    14 : [DEVICE_CONTROLLER, 'toggle_device', [CURRENT, CURRENT]],
    15 : [LOOPER_CONTROLLER, 'clipLooper', [0]],    
    16 : [TRACK_CONTROLLER, 'arm', [1]],
    
#    2  : [DEVICE_CONTROLLER, 'trigger_device_chain', [0, True]],
#    3  : [DEVICE_CONTROLLER, 'trigger_device_chain', [1, True]],
#    4  : [DEVICE_CONTROLLER, 'trigger_device_chain', [2, True]],
#    5  : [DEVICE_CONTROLLER, 'trigger_device_chain', [3, True]],
#    7  : [DEVICE_CONTROLLER, 'trigger_device_chain', [4, True]],
#    8  : [DEVICE_CONTROLLER, 'trigger_device_chain', [5, True]],
#    9  : [DEVICE_CONTROLLER, 'trigger_device_chain', [6, True]],
#    10 : [DEVICE_CONTROLLER, 'trigger_device_chain', [7, True]],
    26 : [TRACK_CONTROLLER, 'arm', [2]],
    36 : [TRACK_CONTROLLER, 'arm', [3]],
    46 : [TRACK_CONTROLLER, 'arm', [4]],
    56 : [TRACK_CONTROLLER, 'arm', [5]],
    66 : [TRACK_CONTROLLER, 'arm', [6]],

    72 : [LOOPER_CONTROLLER, 'activate_looper', [1]],     
    74 : [LOOPER_CONTROLLER, 'activate_looper', [2]], 
    77 : [LOOPER_CONTROLLER, 'switch_view', [1]],
    79 : [LOOPER_CONTROLLER, 'switch_view', [2]],
    22 : [DEVICE_CONTROLLER, 'navigate_device_focus', [1, PREV]],
    32 : [DEVICE_CONTROLLER, 'navigate_device_focus', [2, PREV]],
    42 : [DEVICE_CONTROLLER, 'navigate_device_focus', [3, PREV]],
    52 : [DEVICE_CONTROLLER, 'navigate_device_focus', [4, PREV]],
    62 : [DEVICE_CONTROLLER, 'navigate_device_focus', [5, PREV]],
    23 : [DEVICE_CONTROLLER, 'navigate_device_focus', [1, NEXT]],
    33 : [DEVICE_CONTROLLER, 'navigate_device_focus', [2, NEXT]],
    43 : [DEVICE_CONTROLLER, 'navigate_device_focus', [3, NEXT]],
    53 : [DEVICE_CONTROLLER, 'navigate_device_focus', [4, NEXT]],
    63 : [DEVICE_CONTROLLER, 'navigate_device_focus', [5, NEXT]],
    24 : [DEVICE_CONTROLLER, 'toggle_device', [CURRENT, CURRENT]],
    34 : [DEVICE_CONTROLLER, 'toggle_device', [CURRENT, CURRENT]],
    44 : [DEVICE_CONTROLLER, 'toggle_device', [CURRENT, CURRENT]],
    54 : [DEVICE_CONTROLLER, 'toggle_device', [CURRENT, CURRENT]],
    64 : [DEVICE_CONTROLLER, 'toggle_device', [CURRENT, CURRENT]],
    25 : [LOOPER_CONTROLLER, 'clipLooper', [1]],
    35 : [LOOPER_CONTROLLER, 'clipLooper', [2]],
    45 : [LOOPER_CONTROLLER, 'clipLooper', [3]],
    55 : [LOOPER_CONTROLLER, 'clipLooper', [4]],
    65 : [LOOPER_CONTROLLER, 'clipLooper', [5]],
    

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
    11 : [TRACK_CONTROLLER, 'get_focus', [1]],
    21 : [TRACK_CONTROLLER, 'get_focus', [2]],
    31 : [TRACK_CONTROLLER, 'get_focus', [3]],
    41 : [TRACK_CONTROLLER, 'get_focus', [4]],
    51 : [TRACK_CONTROLLER, 'get_focus', [5]],
    61 : [TRACK_CONTROLLER, 'get_focus', [6]],
    # scene
#scene_down = [82]
#scene_up = [87]
#stop_all_clips = 88
#play_current_scene = 83
    82 : [SCENE_CONTROLLER, 'scene_down', []],
    83 : [SCENE_CONTROLLER, 'play_scene_select_next', [CURRENT]],
    #84 : [SCENE_CONTROLLER, 'play_scene', [CURRENT]],
    #84 : [SCENE_CONTROLLER, 'play_scene', [3]],
    87 : [SCENE_CONTROLLER, 'scene_up', []],
    88 : [SCENE_CONTROLLER, 'stop', [CURRENT]],
    84 : [SCENE_CONTROLLER, 'send_available_methods_to_lighthouse', []],

}

midi_cc_definitions = {
    101: [PEDAL_CONTROLLER,  'handle_effect_slider', [0, 1]],
    111: [PEDAL_CONTROLLER,  'handle_effect_slider', [0, 2]],
    102: [PEDAL_CONTROLLER,  'handle_send', [0, 0]],
    112: [PEDAL_CONTROLLER,  'handle_send', [0, 1]],
    103: [PEDAL_CONTROLLER,  'handle_send', [1, 0]],
    113: [PEDAL_CONTROLLER,  'handle_send', [1, 1]],
    104: [PEDAL_CONTROLLER,  'handle_send', [2, 0]],
    114: [PEDAL_CONTROLLER,  'handle_send', [2, 1]],
    105: [PEDAL_CONTROLLER,  'handle_send', [3, 0]],
    115: [PEDAL_CONTROLLER,  'handle_send', [3, 1]],
    106: [PEDAL_CONTROLLER,  'handle_send', [4, 0]],
    116: [PEDAL_CONTROLLER,  'handle_send', [4, 1]],
    107: [PEDAL_CONTROLLER,  'handle_send', [5, 0]],
    117: [PEDAL_CONTROLLER,  'handle_send', [5, 1]],
    108: [PEDAL_CONTROLLER,  'handle_volume', [CURRENT, 0]],
    118: [PEDAL_CONTROLLER,  'handle_volume', [CURRENT, 1]],
    109: [PEDAL_CONTROLLER,  'handle_volume', [CURRENT, 0]],
    119: [PEDAL_CONTROLLER,  'handle_volume', [CURRENT, 1]],
    110: [PEDAL_CONTROLLER,  'handle_volume', [CURRENT, 0]],
    120: [PEDAL_CONTROLLER,  'handle_volume', [CURRENT, 1]],
}
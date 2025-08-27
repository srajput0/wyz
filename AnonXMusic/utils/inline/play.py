import math
import time
from datetime import datetime
from random import choice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic.utils.formatters import time_to_seconds


# def get_dynamic_beat_pattern(base_patterns, offset=0):
#     """Generate dynamic beat patterns based on current time"""
#     milliseconds = int((time.time() * 1000) % 1000)
#     pattern_index = ((milliseconds // 62) + offset) % len(base_patterns)
#     return base_patterns[pattern_index]




def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]
    return buttons


def speed_markup(_, chat_id):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🕒 0.5x",
                    callback_data=f"SpeedUP {chat_id}|0.5",
                ),
                InlineKeyboardButton(
                    text="🕓 0.75x",
                    callback_data=f"SpeedUP {chat_id}|0.75",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["P_B_4"],
                    callback_data=f"SpeedUP {chat_id}|1.0",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🕤 1.5x",
                    callback_data=f"SpeedUP {chat_id}|1.5",
                ),
                InlineKeyboardButton(
                    text="🕛 2.0x",
                    callback_data=f"SpeedUP {chat_id}|2.0",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


def get_time_stamp():
    """Get current timestamp for unique callbacks"""
    return int(datetime.utcnow().timestamp() * 1000)

def create_bar(played_sec, duration_sec):
    """Create progress bar"""
    position = math.floor((played_sec / duration_sec) * 10) if duration_sec > 0 else 0
    return "".join(["━" * position] + ["⚪"] + ["─" * (8 - position)] if position <= 8 else "━━━━━━━━━⚪")



# Beat Frames
frames = ["ılıılıılıılı", "liiliiliilii", "ılıılıılıılıI"]

def get_beat_frame():
    """Get current beat frame - exactly 3 changes per second"""
    # Get milliseconds since epoch
    ms = int((time.time() * 1000))
    # Each frame shows for 333ms (1000ms/3 ≈ 333ms for 3 changes per second)
    frame_index = (ms // 333) % len(frames)
    return frames[frame_index]

def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    
    # Create progress bar
    bar = create_bar(played_sec, duration_sec)
    
    # Get timestamp for unique callback
    timestamp = get_time_stamp()
    
    # Get current beat frame
    current_frame = get_beat_frame()

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text=current_frame,
                callback_data=f"BeatFrame_{timestamp}",
            )
        ],
        [
            InlineKeyboardButton(
                text="❚❚ ", 
                callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="✯", 
                callback_data="close"
            ),
            InlineKeyboardButton(
                text="►► ", 
                callback_data=f"ADMIN Skip|{chat_id}"
            ),
        ],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"AviaxPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"AviaxPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons

import math
import time
from datetime import datetime
from random import choice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic.utils.formatters import time_to_seconds


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
    """Speed control markup - this function should be called by callback handlers"""
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🐌 0.5x",
                    callback_data=f"SpeedUP {chat_id}|0.5",
                ),
                InlineKeyboardButton(
                    text="🚶 0.75x",
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
                    text="🏃 1.5x",
                    callback_data=f"SpeedUP {chat_id}|1.5",
                ),
                InlineKeyboardButton(
                    text="🚀 2.0x",
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
    """Create enhanced progress bar with dynamic elements"""
    if duration_sec <= 0:
        return "━━━━━━━━━⚪"
    
    position = math.floor((played_sec / duration_sec) * 10)
    position = min(position, 9)
    
    # Dynamic progress bar with pulsing effect
    filled = "━" * position
    current = "⚪"
    remaining = "─" * (9 - position)
    
    return f"{filled}{current}{remaining}"


# Ultra-dynamic beat frames with faster animation
# frames = [
#     "♪ ılıılıılıılı ♪",
#     "♫ liiliiliilii ♫", 
#     "♪ ılıılıılıılıI ♪",
#     "♫ İlİİlİİlİİl ♫",
#     "♪ ıLıLıLıLıLı ♪",
#     "♫ ılıLıLıLılı ♫",
#     "♪ LıLıLıLıLıL ♪",
#     "♫ ılıİlıİlıİ ♫"
# ]

def get_beat_frame():
    """Get current beat frame - FAST 3 changes per second"""
    # Use microseconds for ultra-precise timing
    microseconds = int(time.time() * 1000000)
    # Each frame shows for exactly 333,333 microseconds (333.333ms)
    frame_duration = 333333
    frame_index = (microseconds // frame_duration) % len(frames)
    return frames[frame_index]


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    
    # Create progress bar
    bar = create_bar(played_sec, duration_sec)
    
    # Get timestamp for unique callback
    timestamp = get_time_stamp()
    
    # Get current beat frame with ultra-fast animation
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
                text="❚❚", 
                callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="✯", 
                callback_data="close"
            ),
            InlineKeyboardButton(
                text="►►", 
                callback_data=f"ADMIN Skip|{chat_id}"
            ),
        ],
    ]
    return buttons


# def speed_control_markup(_, chat_id):
#     """Enhanced speed control markup with better callback handling"""
#     buttons = [
#         [
#             InlineKeyboardButton(
#                 text="🐌 0.25x (Turtle)",
#                 callback_data=f"SpeedUP {chat_id}|0.25",
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 text="🚶‍♂️ 0.5x (Slow)",
#                 callback_data=f"SpeedUP {chat_id}|0.5",
#             ),
#             InlineKeyboardButton(
#                 text="🚶‍♀️ 0.75x (Slower)",
#                 callback_data=f"SpeedUP {chat_id}|0.75",
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 text="▶️ 1.0x (Normal) ▶️",
#                 callback_data=f"SpeedUP {chat_id}|1.0",
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 text="🏃‍♂️ 1.25x (Fast)",
#                 callback_data=f"SpeedUP {chat_id}|1.25",
#             ),
#             InlineKeyboardButton(
#                 text="🏃‍♀️ 1.5x (Faster)",
#                 callback_data=f"SpeedUP {chat_id}|1.5",
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 text="🚀 2.0x (Lightning)",
#                 callback_data=f"SpeedUP {chat_id}|2.0",
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 text="🔙 Back to Player",
#                 callback_data=f"back_to_player_{chat_id}",
#             ),
#             InlineKeyboardButton(
#                 text="❌ Close",
#                 callback_data="close",
#             ),
#         ],
#     ]
#     return InlineKeyboardMarkup(buttons)


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


# Additional utility function for ultra-dynamic frames
def get_super_fast_beat():
    """Alternative ultra-fast beat animation - 5 changes per second"""
    microseconds = int(time.time() * 1000000)
    # 200ms per frame = 5 changes per second
    frame_duration = 200000
    
    super_frames = [
        "💫 ●○●○●○● 💫",
        "✨ ○●○●○●○ ✨",
        "🌟 ●○●○●○● 🌟",
        "⭐ ○●○●○●○ ⭐",
        "💥 ●●○○●●○ 💥",
        "🔥 ○○●●○○● 🔥",
        "⚡ ●○○●●○○ ⚡",
        "🎵 ○●●○○●● 🎵"
    ]
    
    frame_index = (microseconds // frame_duration) % len(super_frames)
    return super_frames[frame_index]


def enhanced_player_markup(_, chat_id, played, dur, use_super_fast=False):
    """Enhanced player with optional super-fast animation"""
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    
    # Create progress bar
    bar = create_bar(played_sec, duration_sec)
    
    # Get timestamp for unique callback
    timestamp = get_time_stamp()
    
    # Choose animation speed
    current_frame = get_super_fast_beat() if use_super_fast else get_beat_frame()

    buttons = [
        [
            InlineKeyboardButton(
                text=f"🎵 {played} {bar} {dur} 🎵",
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
                text="⚡ Speed Control ⚡",
                callback_data=f"speed_control_{chat_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="⏮️", 
                callback_data=f"ADMIN Previous|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⏸️", 
                callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⏭️", 
                callback_data=f"ADMIN Skip|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀 Shuffle", 
                callback_data=f"ADMIN Shuffle|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔁 Repeat", 
                callback_data=f"ADMIN Repeat|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="📋 Queue", 
                callback_data=f"PlayList|{chat_id}"
            ),
            InlineKeyboardButton(
                text="❌ Close", 
                callback_data="close"
            ),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

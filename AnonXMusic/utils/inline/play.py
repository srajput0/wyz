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
    position = min(position, 9)  # Ensure position doesn't exceed bar length
    
    # Dynamic progress bar with different styles
    filled = "━" * position
    current = "⚪"
    remaining = "─" * (9 - position)
    
    return f"{filled}{current}{remaining}"


# Enhanced Beat Frames with more dynamic patterns
frames = [
    "♪ ılıılıılıılı ♪",
    "♫ liiliiliilii ♫", 
    "♪ ılıılıılıılıI ♪",
    "♫ İlİİlİİlİİl ♫",
    "♪ ıLıLıLıLıLı ♪"
]

def get_beat_frame():
    """Get current beat frame - exactly 3 changes per second"""
    ms = int((time.time() * 1000))
    # Each frame shows for 333ms (1000ms/3 ≈ 333ms for exactly 3 changes per second)
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
                text="⚡ Speed Control",
                callback_data=f"SpeedMarkup|{chat_id}"
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


# Enhanced speed markup with better visual indicators
def enhanced_speed_markup(_, chat_id):
    """Enhanced speed control markup with better UX"""
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🐌 0.25x (Ultra Slow)",
                    callback_data=f"SpeedUP {chat_id}|0.25",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🚶‍♂️ 0.5x (Slow)",
                    callback_data=f"SpeedUP {chat_id}|0.5",
                ),
                InlineKeyboardButton(
                    text="🚶‍♀️ 0.75x (Slower)",
                    callback_data=f"SpeedUP {chat_id}|0.75",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="▶️ 1.0x (Normal)",
                    callback_data=f"SpeedUP {chat_id}|1.0",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏃‍♂️ 1.25x (Fast)",
                    callback_data=f"SpeedUP {chat_id}|1.25",
                ),
                InlineKeyboardButton(
                    text="🏃‍♀️ 1.5x (Faster)",
                    callback_data=f"SpeedUP {chat_id}|1.5",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🚀 2.0x (Ultra Fast)",
                    callback_data=f"SpeedUP {chat_id}|2.0",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Back to Player",
                    callback_data=f"BackToPlayer|{chat_id}",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


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


# Additional utility functions for enhanced player experience
def get_dynamic_player_markup(_, chat_id, is_paused=False, shuffle=False, repeat_mode="off"):
    """Dynamic player markup that changes based on player state"""
    
    # Play/Pause button changes based on state
    play_pause_text = "▶️" if is_paused else "⏸️"
    play_pause_action = "Resume" if is_paused else "Pause"
    
    # Shuffle button changes color when active
    shuffle_text = "🔀 ON" if shuffle else "🔀"
    
    # Repeat mode indicator
    repeat_icons = {
        "off": "🔁",
        "track": "🔂",
        "playlist": "🔁 ALL"
    }
    repeat_text = repeat_icons.get(repeat_mode, "🔁")
    
    buttons = [
        [
            InlineKeyboardButton(
                text="⏮️", 
                callback_data=f"ADMIN Previous|{chat_id}"
            ),
            InlineKeyboardButton(
                text=play_pause_text, 
                callback_data=f"ADMIN {play_pause_action}|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⏭️", 
                callback_data=f"ADMIN Skip|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=shuffle_text, 
                callback_data=f"ADMIN Shuffle|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⚡ Speed", 
                callback_data=f"SpeedMarkup|{chat_id}"
            ),
            InlineKeyboardButton(
                text=repeat_text, 
                callback_data=f"ADMIN Repeat|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="📋 Queue", 
                callback_data=f"PlayList|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🎵 Lyrics", 
                callback_data=f"GetLyrics|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Close", 
                callback_data="close"
            )
        ],
    ]
    return buttons

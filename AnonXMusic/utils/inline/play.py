import math

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pyrogram.types import InlineKeyboardButton

from AnonXMusic.utils.formatters import time_to_seconds

import time


def get_dynamic_beat_pattern(base_patterns, offset=0):
    """Generate dynamic beat patterns based on current time"""
    milliseconds = int((time.time() * 1000) % 1000)
    pattern_index = ((milliseconds // 62) + offset) % len(base_patterns)
    return base_patterns[pattern_index]




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



def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    anon = math.floor(percentage)

    # More varied beat patterns for rapid animation
    beat_patterns = [
        "ılıılıılıılıılıılı",        # Pattern 1
        "ılııııılııııılııı",         # Pattern 2
        "łııłııłııłııłııł",         # Pattern 3
        "ııııłııııłııııłı",         # Pattern 4
        "ıłıłıłıłıłıłıłıł",         # Pattern 5
        "ııııııłłłłłııııı",         # Pattern 6
        "łłłıııłłłıııłłłı",         # Pattern 7
        "ıłııłıııłııłıııł",         # Pattern 8
        "ılılılılılılılılı",         # Pattern 9
        "lılılılılılılılıl",         # Pattern 10
        "ııłłııłłııłłııłł",         # Pattern 11
        "łııłııłııłııłııł",         # Pattern 12
        "ıııłłłıııłłłıııł",         # Pattern 13
        "łłııııłłııııłłıı",         # Pattern 14
        "ılılılııııılılılı",         # Pattern 15
        "lılılııııııılılıl",         # Pattern 16
    ]
    
    # Use milliseconds for faster animation
    import time
    milliseconds = int((time.time() * 1000) % 1000)  # Get current milliseconds
    pattern_index = (milliseconds // 62) % len(beat_patterns)  # Changes roughly every ~62ms
    beat_animation = beat_patterns[pattern_index]
    
    # Calculate position for progress bar
    position = math.floor((played_sec / duration_sec) * 10)
    ba = "".join(["━" * position] + ["⚪"] + ["─" * (8 - position)] if position <= 8 else "━━━━━━━━━⚪")

    # Create two beat pattern rows for more dynamic visualization
    beat_pattern_1 = beat_patterns[(pattern_index + 1) % len(beat_patterns)]
    beat_pattern_2 = beat_patterns[(pattern_index + 2) % len(beat_patterns)]

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {ba} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text=beat_animation,
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text=beat_pattern_1,
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text=beat_pattern_2,
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text="i speed name",
                callback_data=f"show_speed_markup|{user_id}|{channel}"
            )
        ],
        [
            InlineKeyboardButton(text="❚❚ ", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"), 
            InlineKeyboardButton(
                text="|►►", callback_data=f"ADMIN Skip|{chat_id}"
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

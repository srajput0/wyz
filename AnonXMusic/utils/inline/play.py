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



def generate_beat_pattern():
    """Generate dynamic beat patterns with micro-variations"""
    chars = ["ı", "ł", "ı", "l"]
    base_patterns = [
        "".join(choice(chars) for _ in range(randint(15, 20))),  # Random length pattern
        "ııłłııłłııłłııłł",
        "łıłıłıłıłıłıłıłı",
        "ılılılılılılılılı",
        "łııłııłııłııłııł",
        "ıłıłıłıłıłıłıłıł",
    ]
    
    # Add dynamic variations
    pattern = choice(base_patterns)
    current_ms = datetime.now().microsecond % 1000
    
    # Create variations based on microseconds
    if current_ms < 200:
        return pattern[::-1]  # Reverse
    elif current_ms < 400:
        return pattern[len(pattern)//2:] + pattern[:len(pattern)//2]  # Rotate
    elif current_ms < 600:
        return "ı" + pattern[1:] + "ł"  # Change edges
    elif current_ms < 800:
        return "".join([c.upper() if i % 2 == 0 else c for i, c in enumerate(pattern)])
    else:
        return pattern

def get_dynamic_patterns():
    """Get multiple dynamic patterns for multi-line display"""
    patterns = []
    for _ in range(3):
        current_micro = datetime.now().microsecond
        pattern = generate_beat_pattern()
        # Add micro-variations based on current microsecond
        if current_micro % 2 == 0:
            pattern = "❮" + pattern + "❯"
        else:
            pattern = "⟨" + pattern + "⟩"
        patterns.append(pattern)
    return patterns

def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    anon = math.floor(percentage)

    # Calculate position for progress bar with smoother animation
    position = math.floor((played_sec / duration_sec) * 10)
    micro_position = (played_sec / duration_sec) * 1000 % 1  # For micro-movements
    
    # Enhanced progress bar with micro-movements
    if micro_position < 0.5:
        cursor = "⚪"
    else:
        cursor = "⭕"
        
    ba = "".join(["━" * position] + [cursor] + ["─" * (8 - position)] if position <= 8 else "━━━━━━━━━⚪")

    # Get dynamic beat patterns
    beat_patterns = get_dynamic_patterns()
    
    # Add timestamp to callback data for unique updates
    current_time = f"{datetime.now().timestamp()}"

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {ba} {dur}",
                callback_data=f"GetTimer",
            )
        ]
    ]
    
    # Add beat pattern rows with unique callbacks
    for i, pattern in enumerate(beat_patterns):
        buttons.append([
            InlineKeyboardButton(
                text=pattern,
                callback_data=f"GetTimer{i}_{current_time}"
            )
        ])

    # Control buttons
    buttons.append([
        InlineKeyboardButton(text="❚❚ ", callback_data=f"ADMIN Pause|{chat_id}"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        InlineKeyboardButton(text="|►►", callback_data=f"ADMIN Skip|{chat_id}")
    ])

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

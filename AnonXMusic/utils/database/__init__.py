# This file makes the directory a Python package

from typing import List, Dict, Union
from AnonXMusic.core.mongo import mongodb

# MongoDB collections
channeldb = mongodb.cplaymode
playcounts = mongodb.playcounts

async def get_cmode(chat_id: int) -> Union[str, None]:
    """Get channel play mode for a chat
    
    Parameters:
        chat_id (int): ID of the chat
        
    Returns:
        str or None: Channel mode if found, None otherwise
    """
    mode = await channeldb.find_one({"chat_id": chat_id})
    if not mode:
        return None
    return mode.get("mode")

# Re-export functions from other modules
from .play_counts import (
    increment_group_played,
    get_group_played,
    get_top_groups
)

# List all functions that should be available when importing from this package
__all__ = [
    "get_cmode",
    "increment_group_played", 
    "get_group_played",
    "get_top_groups"
]

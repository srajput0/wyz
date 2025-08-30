
from typing import Dict, List
from AnonXMusic.core.mongo import mongodb

playcounts = mongodb.playcounts

async def increment_group_played(chat_id: int) -> bool:
    """Increment the play count for a group"""
    try:
        await playcounts.update_one(
            {"chat_id": chat_id},
            {"$inc": {"play_count": 1}},
            upsert=True
        )
        return True
    except:
        return False

async def get_group_played(chat_id: int) -> int:
    """Get the play count for a specific group"""
    count = await playcounts.find_one({"chat_id": chat_id})
    if count:
        return count.get("play_count", 0)
    return 0

async def get_top_groups(limit: int = 10) -> List[Dict]:
    """Get the top groups by play count"""
    cursor = playcounts.find().sort("play_count", -1).limit(limit)
    top_groups = await cursor.to_list(length=limit)
    return top_groups

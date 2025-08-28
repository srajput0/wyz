
import os
import re
import aiofiles
import aiohttp

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    """Resize image keeping ratio"""
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def create_modern_thumbnail_card(videoid, output_path):
    """
    Generate a modern glassmorphism thumbnail card
    """

    # ✅ Step 1: Fetch video info
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = re.sub("\W+", " ", result.get("title", "Unknown")).title()
        duration = result.get("duration", "0:00")
        views = result.get("viewCount", {}).get("short", "0 views")
        thumbnail = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0]

        # ✅ Step 2: Download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube_thumb = Image.open(f"cache/thumb{videoid}.png").convert("RGB")

        # ✅ Step 3: Background (blurred)
        canvas = youtube_thumb.resize((1280, 720)).filter(ImageFilter.GaussianBlur(25))
        overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 180))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)

        draw = ImageDraw.Draw(canvas)

        # ✅ Step 4: Fonts
        try:
            title_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 42)
            info_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 28)
            control_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 52)
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            control_font = ImageFont.load_default()

        # ✅ Step 5: Glassmorphism Card
        card_w, card_h = 1000, 550
        card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 40))
        mask = Image.new("L", (card_w, card_h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w, card_h], 40, fill=255)
        canvas.paste(card, (140, 90), mask)

        # ✅ Step 6: Video Thumbnail inside card
        thumb_resized = youtube_thumb.resize((960, 300))
        thumb_mask = Image.new("L", (960, 300), 0)
        ImageDraw.Draw(thumb_mask).rounded_rectangle([0, 0, 960, 300], 30, fill=255)
        canvas.paste(thumb_resized, (160, 110), thumb_mask)

        # ✅ Step 7: Title & subtitle
        short_title = title[:45] + "..." if len(title) > 45 else title
        draw.text((180, 430), short_title, fill="black", font=title_font)
        draw.text((180, 480), f"YouTube | {views}", fill=(50, 50, 50), font=info_font)

        # ✅ Step 8: Progress bar
        bar_x, bar_y, bar_w, bar_h = 180, 520, 920, 8
        draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], 4, fill=(160, 160, 160))
        progress = int(bar_w * 0.25)  # Fake 25% progress
        draw.rounded_rectangle([bar_x, bar_y, bar_x+progress, bar_y+bar_h], 4, fill=(255, 0, 0))

        # Time
        draw.text((180, 540), "0:00", fill="black", font=info_font)
        draw.text((bar_x+bar_w-70, 540), duration, fill="black", font=info_font)

        # ✅ Step 9: Control buttons
        icons = ["🔀", "⏮", "▶", "⏭", "🔁"]
        x_pos = [300, 450, 640, 830, 1000]
        for icon, x in zip(icons, x_pos):
            draw.text((x, 580), icon, fill="black", font=control_font)

        # ✅ Step 10: Save & cleanup
        canvas.save(output_path, quality=95)
        os.remove(f"cache/thumb{videoid}.png")

        return output_path

    except Exception as e:
        print(f"Thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL

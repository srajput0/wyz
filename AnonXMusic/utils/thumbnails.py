import os
import re
import random
import math
import time
from datetime import datetime

import aiofiles
import aiohttp

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps

from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from AnonXMusic import app
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 65:
            title += " " + i
    return title.strip()


def create_gradient_background(width, height, colors):
    """Create smooth gradient background"""
    gradient = Image.new('RGBA', (width, height), colors[0])
    draw = ImageDraw.Draw(gradient)
    
    for i in range(height):
        ratio = i / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    return gradient


def create_clean_panel(draw, x, y, width, height, bg_color=(255, 255, 255, 30), border_color=(255, 255, 255, 60)):
    """Create clean modern panel with subtle border"""
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius=12,
        fill=bg_color,
        outline=border_color,
        width=1
    )


def create_simple_visualizer(draw, x, y, width, height, bars=24):
    """Clean minimal audio visualizer"""
    t = time.time()
    bar_width = (width - (bars * 2)) // bars
    
    for i in range(bars):
        # Simple sine wave for bars
        bar_height = int(height * 0.3 + math.sin(t * 4 + i * 0.5) * height * 0.4)
        bar_height = max(8, min(height - 4, bar_height))
        
        bar_x = x + i * (bar_width + 2)
        bar_y = y + height - bar_height
        
        # Clean gradient colors
        if i < bars // 3:
            color = (64, 224, 255)  # Light blue
        elif i < 2 * bars // 3:
            color = (128, 255, 128)  # Light green
        else:
            color = (255, 128, 255)  # Light pink
        
        # Draw clean rounded bars
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + bar_width, y + height],
            radius=bar_width // 2,
            fill=color
        )


def create_modern_progress_bar(draw, x, y, width, height, progress=0.0):
    """Modern clean progress bar"""
    # Background track
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius=height // 2,
        fill=(255, 255, 255, 40)
    )
    
    # Progress fill
    fill_width = int(width * progress)
    if fill_width > 0:
        draw.rounded_rectangle(
            [x, y, x + fill_width, y + height],
            radius=height // 2,
            fill=(64, 224, 255)
        )
    
    # Progress indicator
    indicator_x = x + fill_width - 6
    draw.ellipse(
        [indicator_x, y - 2, indicator_x + 12, y + height + 2],
        fill=(255, 255, 255)
    )


def create_clean_button(draw, x, y, size, icon, color=(255, 255, 255)):
    """Clean modern circular button"""
    # Button background
    draw.ellipse(
        [x - size//2, y - size//2, x + size//2, y + size//2],
        fill=(255, 255, 255, 40),
        outline=(255, 255, 255, 80),
        width=1
    )
    
    # Icon will be drawn separately with text


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        # Create clean HD canvas
        canvas = Image.new('RGBA', (1280, 720), (20, 25, 35, 255))
        
        # Load and process original thumbnail
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        
        # Clean enhancement - not overdone
        enhancer = ImageEnhance.Brightness(image1)
        image1 = enhancer.enhance(0.8)
        
        enhancer = ImageEnhance.Contrast(image1)
        image1 = enhancer.enhance(1.2)
        
        # Subtle blur for background
        blurred = image1.filter(ImageFilter.GaussianBlur(radius=1.5))
        
        # Apply dark overlay for text readability
        overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 80))
        blurred = Image.alpha_composite(blurred.convert('RGBA'), overlay)
        
        canvas.paste(blurred, (0, 0))
        draw = ImageDraw.Draw(canvas)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 36)
            brand_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 48)
            info_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 24)
            control_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 28)
        except:
            title_font = ImageFont.load_default()
            brand_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            control_font = ImageFont.load_default()
        
        # Clean brand section
        create_clean_panel(draw, 30, 30, 400, 100, (0, 0, 0, 120), (64, 224, 255, 100))
        
        # Simple logo placeholder
        draw.ellipse([50, 50, 90, 90], fill=(64, 224, 255), outline=(255, 255, 255, 150), width=2)
        draw.text((65, 62), "♪", fill=(255, 255, 255), font=control_font)
        
        # Brand text - clean and simple
        draw.text((110, 45), "WYNK", fill=(255, 255, 255), font=brand_font, 
                 stroke_width=1, stroke_fill=(0, 0, 0))
        draw.text((110, 85), "MUSIC", fill=(64, 224, 255), font=info_font)
        
        # Clean visualizer
        create_simple_visualizer(draw, 500, 40, 750, 80, 30)
        
        # Info section - clean layout
        info_y = 160
        info_items = [
            (f"Channel: {channel}", 50),
            (f"Views: {views}", 50),
            (f"Duration: {duration}", 50)
        ]
        
        for i, (text, x) in enumerate(info_items):
            y = info_y + i * 35
            create_clean_panel(draw, x - 10, y - 8, 350, 30, (255, 255, 255, 20))
            draw.text((x, y), text, fill=(255, 255, 255), font=info_font)
        
        # Clean title section
        title_y = 580
        create_clean_panel(draw, 30, title_y - 10, 1220, 60, (0, 0, 0, 150))
        
        draw.text((50, title_y), clear(title), fill=(255, 255, 255), font=title_font,
                 stroke_width=1, stroke_fill=(0, 0, 0))
        
        # Modern progress bar
        progress_y = 660
        progress_value = (time.time() * 0.1) % 1.0  # Animated progress
        create_modern_progress_bar(draw, 50, progress_y, 1180, 12, progress_value)
        
        # Time stamps
        draw.text((50, progress_y + 20), "1:23", fill=(200, 200, 200), font=info_font)
        draw.text((1200, progress_y + 20), duration, fill=(200, 200, 200), font=info_font)
        
        # Clean control buttons
        controls_y = 680
        buttons = [
            ("⏮", 200), ("⏸", 300), ("⏭", 400), ("🔀", 500), ("🔁", 600), ("⚡", 700)
        ]
        
        for icon, x in buttons:
            create_clean_button(draw, x, controls_y, 40, icon)
            
            # Icon color based on type
            if icon == "⏸":
                color = (255, 100, 100)  # Red for pause
            elif icon == "⚡":
                color = (255, 255, 100)  # Yellow for boost
            else:
                color = (255, 255, 255)  # White for others
            
            draw.text((x - 8, controls_y - 12), icon, fill=color, font=control_font)
        
        # Clean timestamp overlay
        draw.text((1150, 50), duration, fill=(255, 255, 255), font=info_font,
                 stroke_width=1, stroke_fill=(0, 0, 0))
        
        # Quality indicator
        draw.text((1150, 80), "HD", fill=(64, 224, 255), font=info_font,
                 stroke_width=1, stroke_fill=(0, 0, 0))
        
        # Clean up
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        canvas.save(f"cache/{videoid}.png", quality=90, optimize=True)
        return f"cache/{videoid}.png"
        
    except Exception as e:
        print(f"Clean thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL

import os
import re
import random
import math
import time

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
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


def create_dynamic_gradient(width, height):
    """Create a dynamic gradient background based on current time"""
    gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)
    
    # Time-based color variations
    t = time.time()
    
    # Primary Wynk colors with time-based variations
    primary_colors = [
        (255, 176, 49),   # Wynk Orange
        (255, 49, 49),    # Wynk Red
        (138, 43, 226),   # Purple
        (0, 191, 255),    # Blue
    ]
    
    # Select colors based on time
    color_index = int(t) % len(primary_colors)
    color1 = primary_colors[color_index]
    color2 = primary_colors[(color_index + 1) % len(primary_colors)]
    
    # Create gradient
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 180))
    
    return gradient


def add_music_visualizer_effect(draw, width, height):
    """Add dynamic music visualizer bars"""
    t = time.time()
    bar_width = 8
    bar_count = 20
    spacing = width // bar_count
    
    for i in range(bar_count):
        # Create dynamic bar heights
        freq = 2 + i * 0.3
        bar_height = int(30 + 25 * math.sin(t * freq + i))
        
        x = i * spacing + 50
        y_bottom = height - 100
        y_top = y_bottom - bar_height
        
        # Gradient colors for bars
        color_intensity = int(255 * (bar_height / 55))
        color = (color_intensity, 176, 49, 200)  # Wynk orange with transparency
        
        draw.rectangle([x, y_top, x + bar_width, y_bottom], fill=color)


def create_wynk_logo(size=60):
    """Create a simple Wynk Music logo"""
    logo = Image.new('RGBA', (size * 3, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    
    # Wynk "W" style logo
    points = [
        (10, 10), (20, 50), (30, 20), (40, 50), (50, 10)
    ]
    draw.line(points, fill=(255, 176, 49), width=4)
    
    return logo


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

        # Dynamic color scheme based on time
        t = time.time()
        colors = [
            "#FFB031",  # Wynk Orange
            "#FF3131",  # Wynk Red
            "#8A2BE2",  # Purple
            "#00BFFF"   # Blue
        ]
        border_color = colors[int(t) % len(colors)]
        
        # Load and process main thumbnail
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        
        # Apply dynamic filters
        bg_bright = ImageEnhance.Brightness(image1)
        bg_logo = bg_bright.enhance(0.8)  # Slightly darker for overlay
        bg_contra = ImageEnhance.Contrast(bg_logo)
        bg_logo = bg_contra.enhance(1.3)  # Higher contrast
        
        # Apply blur effect
        bg_logo = bg_logo.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Add border with dynamic color
        logox = ImageOps.expand(bg_logo, border=15, fill=border_color)
        background = changeImageSize(1280, 720, logox)
        
        # Create dynamic gradient overlay
        gradient = create_dynamic_gradient(1280, 720)
        background = Image.alpha_composite(background.convert('RGBA'), gradient).convert('RGB')
        
        draw = ImageDraw.Draw(background)
        
        # Add music visualizer effect
        add_music_visualizer_effect(draw, 1280, 720)
        
        # Load fonts
        try:
            arial = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 32)
            font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 36)
            font4 = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 40)
            logo_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 50)
        except:
            arial = ImageFont.load_default()
            font = ImageFont.load_default()
            font4 = ImageFont.load_default()
            logo_font = ImageFont.load_default()
        
        # Create Wynk Music branding area with glassmorphism effect
        overlay = Image.new('RGBA', (400, 120), (0, 0, 0, 120))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle([0, 0, 400, 120], radius=20, fill=(255, 255, 255, 30))
        background.paste(overlay, (50, 20), overlay)
        
        # Add Wynk Music logo and text
        draw.text((70, 40), "♪", fill="#FFB031", font=logo_font)
        draw.text((120, 50), "WYNK MUSIC", fill="#FFFFFF", font=font4, stroke_width=2, stroke_fill="#000000")
        draw.text((120, 90), "Stream • Discover • Enjoy", fill="#FFB031", font=arial)
        
        # Channel and views info with modern styling
        info_overlay = Image.new('RGBA', (500, 80), (0, 0, 0, 100))
        info_draw = ImageDraw.Draw(info_overlay)
        info_draw.rounded_rectangle([0, 0, 500, 80], radius=15, fill=(0, 0, 0, 150))
        background.paste(info_overlay, (55, 520), info_overlay)
        
        draw.text(
            (75, 540),
            f"📺 {channel}",
            (255, 255, 255),
            font=arial,
            stroke_width=1,
            stroke_fill="#000000"
        )
        draw.text(
            (75, 570),
            f"👁 {views}",
            (255, 176, 49),
            font=arial,
            stroke_width=1,
            stroke_fill="#000000"
        )
        
        # Title with enhanced styling
        title_overlay = Image.new('RGBA', (1170, 60), (0, 0, 0, 120))
        title_draw = ImageDraw.Draw(title_overlay)
        title_draw.rounded_rectangle([0, 0, 1170, 60], radius=10, fill=(0, 0, 0, 180))
        background.paste(title_overlay, (55, 610), title_overlay)
        
        draw.text(
            (75, 630),
            clear(title),
            fill="#FFFFFF",
            font=font,
            stroke_width=2,
            stroke_fill="#000000"
        )
        
        # Modern progress bar
        progress_y = 680
        draw.rounded_rectangle(
            [(55, progress_y), (1220, progress_y + 12)],
            radius=6,
            fill="#333333"
        )
        
        # Animated progress indicator
        progress_pos = 55 + int((time.time() * 50) % 1165)
        draw.rounded_rectangle(
            [(55, progress_y), (progress_pos, progress_y + 12)],
            radius=6,
            fill=border_color
        )
        
        # Progress dot with glow effect
        dot_x = progress_pos
        for i in range(3):
            draw.ellipse(
                [(dot_x - 8 + i, progress_y + 2 - i), (dot_x + 8 - i, progress_y + 10 + i)],
                fill=(255, 255, 255, 100 - i * 30)
            )
        
        # Control buttons with modern design
        controls_y = 695
        button_spacing = 80
        start_x = 480
        
        control_icons = ["↻", "⏮", "⏸", "⏭", "🔀"]
        for i, icon in enumerate(control_icons):
            x = start_x + i * button_spacing
            
            # Button background
            draw.ellipse(
                [(x - 20, controls_y), (x + 20, controls_y + 40)],
                fill=(255, 176, 49, 200),
                outline="#FFFFFF",
                width=2
            )
            
            # Icon
            draw.text(
                (x - 8, controls_y + 8),
                icon,
                fill="#FFFFFF",
                font=font4
            )
        
        # Duration badge
        duration_overlay = Image.new('RGBA', (120, 40), (0, 0, 0, 150))
        duration_draw = ImageDraw.Draw(duration_overlay)
        duration_draw.rounded_rectangle([0, 0, 120, 40], radius=20, fill=(0, 0, 0, 200))
        background.paste(duration_overlay, (1100, 50), duration_overlay)
        
        draw.text(
            (1130, 62),
            duration,
            fill="#FFB031",
            font=arial,
            anchor="mm"
        )
        
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
        
    except Exception as e:
        print(f"Thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL

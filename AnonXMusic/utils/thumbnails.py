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
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


def create_neon_glow_effect(draw, x, y, width, height, color, intensity=3):
    """Create a neon glow effect"""
    for i in range(intensity):
        alpha = 255 - (i * 60)
        glow_color = (*color, alpha)
        offset = i * 2
        draw.rounded_rectangle(
            [x - offset, y - offset, x + width + offset, y + height + offset],
            radius=10 + offset,
            outline=glow_color,
            width=2
        )


def create_particle_effect(draw, width, height, time_offset=0):
    """Create floating particles effect"""
    t = time.time() + time_offset
    particles = []
    
    for i in range(50):
        # Create floating particles
        x = (50 + i * 25 + math.sin(t + i) * 30) % width
        y = (100 + i * 15 + math.cos(t + i * 0.7) * 40) % height
        size = 2 + math.sin(t * 2 + i) * 2
        
        # Particle color with transparency
        alpha = int(100 + math.sin(t * 3 + i) * 100)
        colors = [(255, 176, 49, alpha), (255, 49, 49, alpha), (138, 43, 226, alpha), (0, 191, 255, alpha)]
        color = colors[i % len(colors)]
        
        # Draw particle
        draw.ellipse([x - size, y - size, x + size, y + size], fill=color)


def create_wave_animation(draw, width, height):
    """Create animated wave background"""
    t = time.time()
    wave_height = 100
    
    for y in range(0, height, 3):
        wave1 = math.sin((y / 50) + (t * 4)) * 20
        wave2 = math.cos((y / 80) + (t * 2)) * 15
        wave3 = math.sin((y / 30) + (t * 6)) * 10
        
        total_wave = wave1 + wave2 + wave3
        
        # Create wave colors
        color_intensity = int(128 + total_wave * 2)
        color_intensity = max(0, min(255, color_intensity))
        
        # Multi-colored waves
        r = int(255 * (0.5 + math.sin(t + y / 100) * 0.3))
        g = int(176 * (0.5 + math.cos(t + y / 80) * 0.3))
        b = int(49 * (0.5 + math.sin(t * 2 + y / 60) * 0.3))
        
        alpha = int(50 + math.sin(t + y / 40) * 30)
        
        # Draw wave lines
        for x in range(0, width, 5):
            wave_x = x + total_wave
            if 0 <= wave_x <= width:
                draw.point((int(wave_x), y), fill=(r, g, b, alpha))


def create_sound_visualizer(draw, x, y, width, height, bars=30):
    """Create advanced sound visualizer"""
    t = time.time()
    bar_width = width // bars
    
    for i in range(bars):
        # Multiple frequency simulation
        freq1 = math.sin(t * 8 + i * 0.5) * 0.3
        freq2 = math.cos(t * 12 + i * 0.3) * 0.2
        freq3 = math.sin(t * 16 + i * 0.8) * 0.15
        freq4 = math.cos(t * 20 + i * 0.1) * 0.1
        
        combined = freq1 + freq2 + freq3 + freq4
        bar_height = int(height * 0.3 + (combined * height * 0.6))
        bar_height = max(5, min(height - 10, bar_height))
        
        bar_x = x + i * bar_width
        bar_y = y + height - bar_height
        
        # Gradient colors for bars
        hue = (i / bars + t * 0.5) % 1.0
        if hue < 0.33:
            color = (255, int(176 + hue * 79), 49)
        elif hue < 0.66:
            color = (255, 49, int(49 + (hue - 0.33) * 157))
        else:
            color = (int(138 + (hue - 0.66) * 117), 43, 226)
        
        # Draw bar with glow
        draw.rectangle([bar_x, bar_y, bar_x + bar_width - 2, y + height], fill=color)
        
        # Add glow effect
        glow_alpha = int(100 + math.sin(t * 4 + i) * 50)
        glow_color = (*color, glow_alpha)
        draw.rectangle([bar_x - 1, bar_y - 2, bar_x + bar_width + 1, y + height + 2], 
                      outline=glow_color, width=1)


def create_holographic_text(draw, text, x, y, font, base_color=(255, 255, 255)):
    """Create holographic text effect"""
    t = time.time()
    
    # Multiple layers for holographic effect
    offsets = [(-2, -1), (-1, 0), (0, 1), (1, 2), (2, 1)]
    colors = [
        (255, 0, 255, 80),   # Magenta
        (0, 255, 255, 100),  # Cyan
        (255, 255, 0, 120),  # Yellow
        (255, 176, 49, 150), # Orange
        base_color           # Main color
    ]
    
    for i, (offset_x, offset_y) in enumerate(offsets):
        # Add time-based shimmer
        shimmer = math.sin(t * 3 + i) * 2
        final_x = x + offset_x + shimmer
        final_y = y + offset_y
        
        draw.text((final_x, final_y), text, fill=colors[i], font=font,
                 stroke_width=1, stroke_fill=(0, 0, 0, 100))


def create_energy_rings(draw, center_x, center_y, max_radius=100):
    """Create expanding energy rings"""
    t = time.time()
    
    for i in range(5):
        radius = (30 + i * 15 + t * 50) % max_radius
        alpha = int(255 - (radius / max_radius) * 255)
        
        colors = [(255, 176, 49, alpha), (255, 49, 49, alpha), (138, 43, 226, alpha)]
        color = colors[i % len(colors)]
        
        draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], outline=color, width=2)


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

        # Create base canvas
        canvas = Image.new('RGBA', (1280, 720), (0, 0, 0, 255))
        
        # Load original thumbnail
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        
        # Apply dramatic effects
        enhancer = ImageEnhance.Brightness(image1)
        image1 = enhancer.enhance(0.7)  # Darker base
        
        enhancer = ImageEnhance.Contrast(image1)
        image1 = enhancer.enhance(1.5)  # Higher contrast
        
        enhancer = ImageEnhance.Color(image1)
        image1 = enhancer.enhance(1.3)  # More saturated
        
        # Apply blur for depth
        blurred = image1.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Create the base image
        canvas.paste(blurred, (0, 0))
        
        # Convert to RGBA for overlay effects
        canvas = canvas.convert('RGBA')
        
        # Create overlay for effects
        overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Add wave animation background
        create_wave_animation(draw, 1280, 720)
        
        # Add particle effects
        create_particle_effect(draw, 1280, 720)
        create_particle_effect(draw, 1280, 720, 1.5)  # Different timing
        
        # Composite overlay
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 42)
            brand_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 56)
            info_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 28)
            control_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 32)
        except:
            title_font = ImageFont.load_default()
            brand_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            control_font = ImageFont.load_default()
        
        # Create dynamic brand area with advanced effects
        brand_overlay = Image.new('RGBA', (500, 140), (0, 0, 0, 0))
        brand_draw = ImageDraw.Draw(brand_overlay)
        
        # Animated background for brand
        t = time.time()
        for i in range(10):
            alpha = int(30 + math.sin(t + i) * 20)
            color = (255, 176, 49, alpha) if i % 2 else (138, 43, 226, alpha)
            brand_draw.rounded_rectangle([i*5, i*3, 500-i*5, 140-i*3], 
                                       radius=15+i, fill=color)
        
        canvas.paste(brand_overlay, (40, 30), brand_overlay)
        
        # Add energy rings around logo
        create_energy_rings(draw, 120, 100, 80)
        
        # Holographic Wynk Music text
        create_holographic_text(draw, "♪ WYNK", 150, 50, brand_font)
        create_holographic_text(draw, "MUSIC", 150, 100, brand_font)
        draw.text((150, 140), "PREMIUM EXPERIENCE", fill=(255, 176, 49), 
                 font=info_font, stroke_width=1, stroke_fill=(0, 0, 0))
        
        # Advanced sound visualizer
        create_sound_visualizer(draw, 600, 50, 600, 120, 40)
        
        # Dynamic info panels
        info_panels = [
            (f"📺 {channel}", 60, 500),
            (f"👁 {views} views", 60, 540),
            (f"⏱ {duration}", 60, 580)
        ]
        
        for text, x, y in info_panels:
            # Animated info backgrounds
            panel_alpha = int(120 + math.sin(time.time() * 2 + y/100) * 40)
            panel_overlay = Image.new('RGBA', (350, 35), (0, 0, 0, panel_alpha))
            panel_draw = ImageDraw.Draw(panel_overlay)
            panel_draw.rounded_rectangle([0, 0, 350, 35], radius=17, 
                                       fill=(255, 176, 49, 60),
                                       outline=(255, 255, 255, 100), width=1)
            canvas.paste(panel_overlay, (x-10, y-5), panel_overlay)
            
            create_holographic_text(draw, text, x, y, info_font, (255, 255, 255))
        
        # Ultra-dynamic title
        title_y = 630
        title_bg = Image.new('RGBA', (1200, 70), (0, 0, 0, 0))
        title_draw = ImageDraw.Draw(title_bg)
        
        # Animated title background
        for i in range(5):
            alpha = int(80 - i * 15)
            title_draw.rounded_rectangle([i*2, i*2, 1200-i*2, 70-i*2], 
                                       radius=15-i, fill=(0, 0, 0, alpha))
        
        # Add neon border
        create_neon_glow_effect(title_draw, 0, 0, 1200, 70, (255, 176, 49), 4)
        
        canvas.paste(title_bg, (40, title_y-10), title_bg)
        create_holographic_text(draw, clear(title), 60, title_y, title_font)
        
        # Ultra-advanced progress bar
        progress_y = 680
        bar_width = 1180
        bar_height = 16
        
        # Animated progress background
        progress_bg = Image.new('RGBA', (bar_width, bar_height), (0, 0, 0, 0))
        progress_draw = ImageDraw.Draw(progress_bg)
        
        # Multi-layer progress bar
        for layer in range(3):
            alpha = 100 - layer * 25
            progress_draw.rounded_rectangle([layer, layer, bar_width-layer, bar_height-layer],
                                          radius=8-layer, fill=(50, 50, 50, alpha))
        
        canvas.paste(progress_bg, (50, progress_y), progress_bg)
        
        # Animated progress fill
        progress_percent = (time.time() * 10) % 100 / 100
        fill_width = int(bar_width * progress_percent)
        
        progress_fill = Image.new('RGBA', (fill_width, bar_height), (0, 0, 0, 0))
        fill_draw = ImageDraw.Draw(progress_fill)
        
        # Gradient fill
        for x in range(fill_width):
            hue = (x / fill_width + time.time() * 0.5) % 1.0
            if hue < 0.5:
                color = (255, int(176 + hue * 79), 49, 200)
            else:
                color = (255, 49, int(49 + (hue - 0.5) * 157), 200)
            fill_draw.line([(x, 0), (x, bar_height)], fill=color)
        
        canvas.paste(progress_fill, (50, progress_y), progress_fill)
        
        # Glowing progress indicator
        indicator_x = 50 + fill_width
        for size in range(5):
            alpha = 200 - size * 30
            draw.ellipse([indicator_x - 8 + size, progress_y + 3 - size,
                         indicator_x + 8 - size, progress_y + 13 + size],
                        fill=(255, 255, 255, alpha))
        
        # Advanced control buttons
        controls_y = 700
        button_data = [
            ("⏮", 400), ("⏸", 500), ("⏭", 600),
            ("🔀", 300), ("🔁", 700), ("⚡", 800)
        ]
        
        for icon, x in button_data:
            # Animated button backgrounds
            btn_alpha = int(150 + math.sin(time.time() * 4 + x/100) * 50)
            
            # Create button with multiple layers
            for layer in range(4):
                size = 35 - layer * 2
                alpha = btn_alpha - layer * 30
                color = (255, 176, 49, alpha) if icon == "⚡" else (100, 100, 100, alpha)
                
                draw.ellipse([x - size//2, controls_y - size//2,
                             x + size//2, controls_y + size//2],
                            fill=color, outline=(255, 255, 255, alpha//2), width=1)
            
            # Icon with glow
            create_holographic_text(draw, icon, x - 10, controls_y - 12, control_font)
        
        # Clean up
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        canvas.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
        
    except Exception as e:
        print(f"Advanced thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL

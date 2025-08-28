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


def create_premium_gradient(width, height, colors, direction="diagonal"):
    """Create luxury gradient backgrounds"""
    gradient = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    if direction == "diagonal":
        for i in range(width + height):
            ratio = i / (width + height)
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            a = int(colors[0][3] * (1 - ratio) + colors[1][3] * ratio) if len(colors[0]) > 3 else 255
            
            # Draw diagonal lines
            draw.line([(max(0, i-height), min(height, i)), (min(width, i), max(0, i-width))], 
                     fill=(r, g, b, a), width=2)
    
    return gradient


def create_glassmorphism_card(width, height, blur_strength=15):
    """Create premium glassmorphism effect"""
    card = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    
    # Multiple blur layers for depth
    blur_layers = []
    for i in range(5):
        layer = Image.new('RGBA', (width, height), (255, 255, 255, 25 - i * 3))
        blurred = layer.filter(ImageFilter.GaussianBlur(radius=blur_strength - i * 2))
        blur_layers.append(blurred)
    
    # Composite layers
    result = card
    for layer in blur_layers:
        result = Image.alpha_composite(result, layer)
    
    return result


def create_luxury_border(draw, x, y, width, height, thickness=2):
    """Create premium gradient border"""
    # Top gradient border
    for i in range(thickness):
        alpha = int(255 * (1 - i/thickness) * 0.4)
        draw.line([(x, y + i), (x + width, y + i)], fill=(255, 215, 0, alpha), width=1)
    
    # Right gradient border  
    for i in range(thickness):
        alpha = int(255 * (1 - i/thickness) * 0.3)
        draw.line([(x + width - i, y), (x + width - i, y + height)], fill=(255, 182, 193, alpha), width=1)
    
    # Bottom gradient border
    for i in range(thickness):
        alpha = int(255 * (1 - i/thickness) * 0.3)
        draw.line([(x, y + height - i), (x + width, y + height - i)], fill=(138, 43, 226, alpha), width=1)
    
    # Left gradient border
    for i in range(thickness):
        alpha = int(255 * (1 - i/thickness) * 0.4)
        draw.line([(x + i, y), (x + i, y + height)], fill=(0, 191, 255, alpha), width=1)


def create_premium_text_effect(draw, text, x, y, font, primary_color=(255, 255, 255)):
    """Create expensive text effect with multiple shadows"""
    # Deep shadow layers
    shadow_layers = [
        (-6, -4, (0, 0, 0, 80)),
        (-4, -3, (primary_color[0]//4, primary_color[1]//4, primary_color[2]//4, 60)),
        (-3, -2, (primary_color[0]//3, primary_color[1]//3, primary_color[2]//3, 40)),
        (-2, -1, (primary_color[0]//2, primary_color[1]//2, primary_color[2]//2, 60)),
        (-1, 0, primary_color),
    ]
    
    # Add shimmer effect
    t = time.time()
    shimmer = math.sin(t * 2) * 1
    
    for offset_x, offset_y, color in shadow_layers:
        final_x = x + offset_x + shimmer * 0.5
        final_y = y + offset_y
        draw.text((final_x, final_y), text, fill=color, font=font)
    
    # Add highlight
    highlight_color = (min(255, primary_color[0] + 50), min(255, primary_color[1] + 50), min(255, primary_color[2] + 50), 180)
    draw.text((x + 1, y - 1), text, fill=highlight_color, font=font)


def create_premium_visualizer(draw, x, y, width, height, bars=28):
    """Luxury audio visualizer with premium effects"""
    t = time.time()
    bar_width = (width - (bars * 3)) // bars
    
    for i in range(bars):
        # Complex wave simulation
        wave1 = math.sin(t * 6 + i * 0.4) * 0.3
        wave2 = math.cos(t * 8 + i * 0.6) * 0.25
        wave3 = math.sin(t * 12 + i * 0.2) * 0.2
        combined = wave1 + wave2 + wave3
        
        bar_height = int(height * 0.4 + abs(combined) * height * 0.55)
        bar_height = max(12, min(height - 8, bar_height))
        
        bar_x = x + i * (bar_width + 3)
        bar_y = y + height - bar_height
        
        # Premium gradient colors
        progress = i / bars
        if progress < 0.33:
            color1, color2 = (255, 215, 0), (255, 140, 0)  # Gold to orange
        elif progress < 0.66:
            color1, color2 = (255, 140, 0), (255, 20, 147)  # Orange to pink
        else:
            color1, color2 = (255, 20, 147), (138, 43, 226)  # Pink to purple
        
        # Draw gradient bar
        for h in range(bar_height):
            ratio = h / bar_height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            draw.line([(bar_x, bar_y + h), (bar_x + bar_width, bar_y + h)], fill=(r, g, b))
        
        # Add glow effect
        for glow in range(3):
            glow_alpha = 40 - glow * 10
            glow_color = (*color2, glow_alpha)
            draw.rectangle([bar_x - glow, bar_y - glow, bar_x + bar_width + glow, bar_y + 2], 
                         fill=glow_color)


def create_luxury_progress_bar(draw, x, y, width, height, progress=0.0):
    """Premium progress bar with gradient and glow"""
    # Background with subtle gradient
    bg_gradient = create_premium_gradient(width, height, 
                                        [(40, 40, 40, 100), (20, 20, 20, 120)])
    
    # Draw background
    draw.rounded_rectangle([x, y, x + width, y + height], radius=height//2, fill=(0, 0, 0, 60))
    
    # Premium border
    draw.rounded_rectangle([x, y, x + width, y + height], radius=height//2, 
                         outline=(255, 215, 0, 80), width=1)
    
    # Progress fill with luxury gradient
    fill_width = int(width * progress)
    if fill_width > 0:
        # Create gradient fill
        for i in range(fill_width):
            ratio = i / width
            if ratio < 0.5:
                r, g, b = 255, int(215 + ratio * 40), int(ratio * 100)  # Gold to yellow
            else:
                r, g, b = int(255 - (ratio-0.5) * 100), 255, int(100 + (ratio-0.5) * 155)  # Yellow to cyan
            
            draw.line([(x + i, y + 2), (x + i, y + height - 2)], fill=(r, g, b))
    
    # Luxury progress indicator
    if fill_width > height//2:
        indicator_x = x + fill_width - height//2
        
        # Multiple glow layers
        for glow in range(4):
            glow_size = height//2 + glow * 2
            glow_alpha = 60 - glow * 15
            draw.ellipse([indicator_x - glow, y - glow, indicator_x + glow_size + glow, y + height + glow],
                        fill=(255, 255, 255, glow_alpha))
        
        # Core indicator
        draw.ellipse([indicator_x, y, indicator_x + height, y + height], fill=(255, 255, 255))


def create_luxury_button(draw, x, y, size, bg_color=(50, 50, 50, 120), border_color=(255, 215, 0)):
    """Premium button with multiple effects"""
    # Shadow layer
    draw.ellipse([x - size//2 + 2, y - size//2 + 2, x + size//2 + 2, y + size//2 + 2], 
                fill=(0, 0, 0, 60))
    
    # Main button background
    draw.ellipse([x - size//2, y - size//2, x + size//2, y + size//2], fill=bg_color)
    
    # Premium gradient border
    border_thickness = 2
    for i in range(border_thickness):
        alpha = int(255 * (1 - i/border_thickness) * 0.6)
        border_size = size//2 - i
        draw.ellipse([x - border_size, y - border_size, x + border_size, y + border_size], 
                    outline=(*border_color, alpha), width=1)
    
    # Inner highlight
    highlight_size = size//3
    draw.ellipse([x - highlight_size, y - highlight_size - size//6, 
                 x + highlight_size, y + highlight_size - size//6], 
                fill=(255, 255, 255, 40))


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

        # Create premium 4K canvas
        canvas = Image.new('RGBA', (1280, 720), (15, 15, 25, 255))
        
        # Load and enhance thumbnail
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        
        # Premium image processing
        enhancer = ImageEnhance.Brightness(image1)
        image1 = enhancer.enhance(0.75)
        
        enhancer = ImageEnhance.Contrast(image1)
        image1 = enhancer.enhance(1.4)
        
        enhancer = ImageEnhance.Color(image1)
        image1 = enhancer.enhance(1.25)
        
        # Create luxury blur effect
        blur_base = image1.filter(ImageFilter.GaussianBlur(radius=2))
        blur_overlay = Image.new('RGBA', (1280, 720), (10, 10, 20, 140))
        blurred = Image.alpha_composite(blur_base.convert('RGBA'), blur_overlay)
        
        canvas.paste(blurred, (0, 0))
        
        # Add premium gradient overlay
        gradient_overlay = create_premium_gradient(1280, 720, 
                                                 [(0, 0, 0, 0), (0, 0, 0, 100)], "diagonal")
        canvas = Image.alpha_composite(canvas, gradient_overlay)
        
        draw = ImageDraw.Draw(canvas)
        
        # Load premium fonts
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
        
        # Premium glassmorphism main card
        glass_card = create_glassmorphism_card(1200, 660, 20)
        canvas.paste(glass_card, (40, 30), glass_card)
        
        # Luxury border around main card
        create_luxury_border(draw, 40, 30, 1200, 660, 3)
        
        # Premium brand section
        brand_glass = create_glassmorphism_card(480, 120, 15)
        canvas.paste(brand_glass, (60, 50), brand_glass)
        create_luxury_border(draw, 60, 50, 480, 120, 2)
        
        # Luxury logo design
        logo_center_x, logo_center_y = 130, 110
        
        # Multi-layer logo effect
        for layer in range(5):
            size = 35 - layer * 3
            alpha = 150 - layer * 25
            colors = [(255, 215, 0, alpha), (255, 140, 0, alpha), (255, 20, 147, alpha), 
                     (138, 43, 226, alpha), (0, 191, 255, alpha)]
            
            draw.ellipse([logo_center_x - size, logo_center_y - size, 
                         logo_center_x + size, logo_center_y + size], 
                        fill=colors[layer % len(colors)])
        
        # Logo icon
        create_premium_text_effect(draw, "♪", logo_center_x - 12, logo_center_y - 16, 
                                 control_font, (255, 255, 255))
        
        # Premium brand text
        create_premium_text_effect(draw, "WYNK MUSIC", 180, 70, brand_font, (255, 215, 0))
        create_premium_text_effect(draw, "PREMIUM EXPERIENCE", 180, 125, info_font, (255, 182, 193))
        
        # Luxury visualizer
        vis_glass = create_glassmorphism_card(680, 100, 12)
        canvas.paste(vis_glass, (570, 60), vis_glass)
        create_premium_visualizer(draw, 590, 75, 640, 70, 32)
        
        # Premium info panels
        info_items = [
            (f"📺 {channel}", 80, 220),
            (f"👁 {views}", 80, 280), 
            (f"⏱ {duration}", 80, 340)
        ]
        
        for text, x, y in info_items:
            # Glassmorphism info panel
            panel_glass = create_glassmorphism_card(400, 45, 8)
            canvas.paste(panel_glass, (x - 15, y - 10), panel_glass)
            create_luxury_border(draw, x - 15, y - 10, 400, 45, 1)
            
            create_premium_text_effect(draw, text, x, y, info_font, (255, 255, 255))
        
        # Ultra-premium title section
        title_glass = create_glassmorphism_card(1160, 80, 18)
        canvas.paste(title_glass, (60, 520), title_glass)
        create_luxury_border(draw, 60, 520, 1160, 80, 3)
        
        create_premium_text_effect(draw, clear(title), 80, 545, title_font, (255, 255, 255))
        
        # Luxury progress bar
        progress_value = (time.time() * 0.05) % 1.0
        create_luxury_progress_bar(draw, 80, 620, 1120, 16, progress_value)
        
        # Premium time display
        create_premium_text_effect(draw, "0:00", 80, 645, info_font, (200, 200, 200))
        create_premium_text_effect(draw, duration, 1150, 645, info_font, (200, 200, 200))
        
        # Luxury control buttons
        controls = [
            ("⏮", 200, (255, 182, 193)), ("⏸", 300, (255, 100, 100)), ("⏭", 400, (255, 182, 193)),
            ("🔀", 520, (138, 43, 226)), ("🔁", 620, (0, 191, 255)), ("⚡", 720, (255, 215, 0))
        ]
        
        for icon, x, color in controls:
            # Premium button background
            if icon == "⏸":
                create_luxury_button(draw, x, 670, 50, (80, 20, 20, 150), color)
            else:
                create_luxury_button(draw, x, 670, 45, (40, 40, 40, 120), color)
            
            # Premium icon
            create_premium_text_effect(draw, icon, x - 12, 670 - 16, control_font, color)
        
        # Premium quality badges
        create_premium_text_effect(draw, "4K", 1180, 60, info_font, (255, 215, 0))
        create_premium_text_effect(draw, "HDR", 1180, 90, info_font, (255, 20, 147))
        create_premium_text_effect(draw, "DOLBY", 1180, 120, info_font, (138, 43, 226))
        
        # Final premium touches - corner accents
        corner_size = 20
        corner_positions = [(60, 50), (1220, 50), (60, 670), (1220, 670)]
        corner_colors = [(255, 215, 0, 120), (255, 20, 147, 120), (138, 43, 226, 120), (0, 191, 255, 120)]
        
        for (x, y), color in zip(corner_positions, corner_colors):
            draw.polygon([(x, y), (x + corner_size, y), (x, y + corner_size)], fill=color)
        
        # Clean up
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        canvas.save(f"cache/{videoid}.png", quality=95, optimize=True)
        return f"cache/{videoid}.png"
        
    except Exception as e:
        print(f"Premium thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL

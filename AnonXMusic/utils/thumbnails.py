import os
import re
import random
import math
import time
from datetime import datetime
import colorsys

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


def create_cyberpunk_grid(draw, width, height, time_offset=0):
    """Create dynamic cyberpunk grid background"""
    t = time.time() + time_offset
    grid_size = 30
    
    # Main grid lines
    for x in range(0, width, grid_size):
        alpha = int(20 + math.sin(t * 2 + x/50) * 15)
        intensity = math.sin(t + x/100) * 0.5 + 0.5
        color = (0, 255, 255, alpha) if intensity > 0.3 else (255, 0, 255, alpha//2)
        
        # Animated vertical lines
        draw.line([(x, 0), (x, height)], fill=color, width=1)
        
        # Add glitch effect randomly
        if random.random() < 0.1:
            glitch_y = random.randint(0, height-100)
            draw.line([(x-2, glitch_y), (x+2, glitch_y+100)], 
                     fill=(255, 255, 0, 100), width=3)
    
    for y in range(0, height, grid_size):
        alpha = int(15 + math.cos(t * 1.5 + y/60) * 10)
        intensity = math.cos(t * 0.7 + y/80) * 0.5 + 0.5
        color = (0, 255, 255, alpha) if intensity > 0.4 else (255, 0, 255, alpha//2)
        
        draw.line([(0, y), (width, y)], fill=color, width=1)


def create_neural_network_bg(draw, width, height):
    """Create animated neural network background"""
    t = time.time()
    nodes = []
    
    # Generate nodes
    for i in range(25):
        x = (i * 180 + math.sin(t * 2 + i) * 50) % width
        y = (i * 95 + math.cos(t * 1.5 + i) * 80) % height
        size = 3 + math.sin(t * 3 + i) * 2
        
        # Node colors cycle through neon spectrum
        hue = (t * 0.3 + i * 0.1) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), 150)
        
        nodes.append((x, y, size, color))
        
        # Draw pulsing node
        for ring in range(3):
            ring_size = size + ring * 3
            alpha = max(0, 150 - ring * 50)
            ring_color = (*color[:3], alpha)
            draw.ellipse([x - ring_size, y - ring_size, 
                         x + ring_size, y + ring_size], fill=ring_color)
    
    # Connect nearby nodes with animated lines
    for i, (x1, y1, _, color1) in enumerate(nodes):
        for j, (x2, y2, _, color2) in enumerate(nodes[i+1:], i+1):
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            if distance < 200:
                alpha = max(0, int(100 - distance/2))
                connection_color = (
                    (color1[0] + color2[0])//2,
                    (color1[1] + color2[1])//2,
                    (color1[2] + color2[2])//2,
                    alpha
                )
                
                # Animated connection line
                wave = math.sin(t * 4 + distance/20) * 3
                mid_x, mid_y = (x1 + x2)//2 + wave, (y1 + y2)//2 + wave
                
                draw.line([(x1, y1), (mid_x, mid_y)], fill=connection_color, width=2)
                draw.line([(mid_x, mid_y), (x2, y2)], fill=connection_color, width=2)


def create_plasma_effect(draw, width, height, time_offset=0):
    """Create dynamic plasma effect"""
    t = time.time() + time_offset
    
    for y in range(0, height, 4):
        for x in range(0, width, 4):
            # Multi-layered plasma calculation
            plasma1 = math.sin(x/80 + t * 2) * math.cos(y/60 + t * 1.5)
            plasma2 = math.sin((x + y)/100 + t * 3) * 0.7
            plasma3 = math.cos(math.sqrt((x-width/2)**2 + (y-height/2)**2)/120 + t * 2.5) * 0.5
            
            combined = (plasma1 + plasma2 + plasma3) / 3
            
            # Convert to hue
            hue = (combined + 1) / 2
            saturation = 0.8 + math.sin(t + x/100) * 0.2
            brightness = 0.3 + abs(combined) * 0.4
            
            rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
            color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), 60)
            
            draw.rectangle([x, y, x+4, y+4], fill=color)


def create_holographic_neon_text(draw, text, x, y, font, primary_color=(0, 255, 255)):
    """Ultra-modern holographic text with multiple neon layers"""
    t = time.time()
    
    # Create multiple offset layers for depth
    layers = [
        (-4, -2, (255, 0, 255, 40)),    # Magenta shadow
        (-3, -1, (255, 100, 0, 60)),    # Orange glow
        (-2, 0, (0, 255, 255, 80)),     # Cyan base
        (-1, 1, (255, 255, 0, 100)),    # Yellow highlight
        (0, 2, (255, 255, 255, 120)),   # White core
        (1, 1, primary_color + (150,)), # Primary color
        (2, 0, (100, 255, 255, 80)),    # Light cyan
        (3, -1, (255, 200, 255, 60))    # Pink edge
    ]
    
    for offset_x, offset_y, color in layers:
        # Add time-based shimmer and distortion
        shimmer_x = math.sin(t * 4 + offset_x) * 1.5
        shimmer_y = math.cos(t * 3 + offset_y) * 1
        
        final_x = x + offset_x + shimmer_x
        final_y = y + offset_y + shimmer_y
        
        # Draw text with stroke for better neon effect
        draw.text((final_x, final_y), text, fill=color, font=font,
                 stroke_width=2, stroke_fill=(0, 0, 0, 80))
    
    # Add outer glow effect
    for glow in range(5):
        glow_offset = glow * 2
        glow_alpha = max(0, 30 - glow * 6)
        glow_color = (*primary_color[:3], glow_alpha)
        
        glow_x = x - glow_offset + math.sin(t * 2) * 2
        glow_y = y - glow_offset + math.cos(t * 1.5) * 1.5
        
        draw.text((glow_x, glow_y), text, fill=glow_color, font=font)


def create_morphing_visualizer(draw, x, y, width, height, bars=50):
    """Advanced morphing audio visualizer with particle trails"""
    t = time.time()
    bar_width = width // bars
    
    for i in range(bars):
        # Multiple frequency layers for realistic audio simulation
        bass = math.sin(t * 6 + i * 0.3) * 0.4
        mid = math.cos(t * 12 + i * 0.5) * 0.3
        treble = math.sin(t * 24 + i * 0.8) * 0.2
        sub_bass = math.cos(t * 3 + i * 0.1) * 0.15
        
        # Add morphing effect
        morph = math.sin(t * 2 + i * 0.2) * 0.1
        
        combined = bass + mid + treble + sub_bass + morph
        bar_height = int(height * 0.2 + abs(combined) * height * 0.7)
        bar_height = max(8, min(height - 5, bar_height))
        
        bar_x = x + i * bar_width
        bar_y = y + height - bar_height
        
        # Dynamic color cycling
        hue = (i / bars * 2 + t * 0.8) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
        base_color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        
        # Create gradient bar
        for h in range(bar_height):
            gradient_factor = h / bar_height
            intensity = 1.0 - gradient_factor * 0.5
            
            color = (
                int(base_color[0] * intensity),
                int(base_color[1] * intensity),
                int(base_color[2] * intensity)
            )
            
            draw.line([(bar_x + 1, bar_y + h), (bar_x + bar_width - 2, bar_y + h)], 
                     fill=color, width=1)
        
        # Add glow and reflection effects
        for glow in range(3):
            glow_alpha = 60 - glow * 20
            glow_color = (*base_color, glow_alpha)
            
            # Top glow
            draw.rectangle([bar_x - glow, bar_y - glow, 
                          bar_x + bar_width + glow, bar_y + 3], 
                         fill=glow_color)
            
            # Reflection at bottom
            reflection_height = min(15, bar_height // 3)
            reflection_alpha = max(0, glow_alpha // 2)
            reflection_color = (*base_color, reflection_alpha)
            
            draw.rectangle([bar_x, y + height + 5, 
                          bar_x + bar_width - 2, y + height + 5 + reflection_height], 
                         fill=reflection_color)
        
        # Add particle trails for high bars
        if bar_height > height * 0.6:
            particle_count = random.randint(2, 5)
            for p in range(particle_count):
                px = bar_x + random.randint(0, bar_width)
                py = bar_y + random.randint(-20, 0)
                particle_size = random.randint(1, 3)
                
                particle_color = (*base_color, random.randint(100, 200))
                draw.ellipse([px - particle_size, py - particle_size,
                            px + particle_size, py + particle_size], 
                           fill=particle_color)


def create_energy_orb(draw, center_x, center_y, max_radius=150, energy_level=1.0):
    """Create pulsating energy orb with electric arcs"""
    t = time.time()
    
    # Main orb with multiple layers
    for layer in range(8):
        radius = (max_radius * 0.3 + layer * 8 + math.sin(t * 4 + layer) * 5) * energy_level
        alpha = max(0, int(150 - layer * 18))
        
        # Color shifts based on time and layer
        hue = (t * 0.5 + layer * 0.1) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), alpha)
        
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius], 
                    fill=color)
    
    # Electric arcs
    arc_count = int(6 * energy_level)
    for i in range(arc_count):
        angle_start = (t * 3 + i * 60) % 360
        angle_end = angle_start + random.randint(30, 90)
        
        # Arc parameters
        inner_radius = max_radius * 0.4
        outer_radius = max_radius * (0.8 + random.random() * 0.4)
        
        # Calculate arc points
        start_x = center_x + math.cos(math.radians(angle_start)) * inner_radius
        start_y = center_y + math.sin(math.radians(angle_start)) * inner_radius
        end_x = center_x + math.cos(math.radians(angle_end)) * outer_radius
        end_y = center_y + math.sin(math.radians(angle_end)) * outer_radius
        
        # Draw jagged lightning arc
        segments = 8
        points = [(start_x, start_y)]
        
        for seg in range(1, segments):
            progress = seg / segments
            base_x = start_x + (end_x - start_x) * progress
            base_y = start_y + (end_y - start_y) * progress
            
            # Add random jaggedness
            offset_x = random.randint(-15, 15)
            offset_y = random.randint(-15, 15)
            
            points.append((base_x + offset_x, base_y + offset_y))
        
        points.append((end_x, end_y))
        
        # Draw the arc with varying thickness
        for i in range(len(points) - 1):
            thickness = random.randint(2, 4)
            arc_alpha = random.randint(150, 255)
            arc_color = (255, 255, 255, arc_alpha)
            
            draw.line([points[i], points[i + 1]], fill=arc_color, width=thickness)


def create_glitch_effect(image, intensity=0.3):
    """Apply realistic glitch effects to image"""
    t = time.time()
    width, height = image.size
    pixels = list(image.getdata())
    
    if random.random() < intensity:
        # Horizontal line glitch
        glitch_y = random.randint(0, height - 20)
        glitch_height = random.randint(5, 20)
        offset = random.randint(-50, 50)
        
        glitched_pixels = []
        for y in range(height):
            for x in range(width):
                pixel_index = y * width + x
                
                if glitch_y <= y <= glitch_y + glitch_height:
                    # Shift pixels horizontally
                    new_x = (x + offset) % width
                    new_index = y * width + new_x
                    
                    if 0 <= new_index < len(pixels):
                        pixel = pixels[new_index]
                        # Add color distortion
                        r, g, b, a = pixel
                        r = min(255, max(0, r + random.randint(-30, 30)))
                        b = min(255, max(0, b + random.randint(-20, 20)))
                        glitched_pixels.append((r, g, b, a))
                    else:
                        glitched_pixels.append(pixels[pixel_index])
                else:
                    glitched_pixels.append(pixels[pixel_index])
        
        glitched_image = Image.new('RGBA', image.size)
        glitched_image.putdata(glitched_pixels)
        return glitched_image
    
    return image


def create_glass_morphism_panel(draw, x, y, width, height, blur_alpha=80):
    """Create modern glassmorphism effect"""
    # Multiple layers for depth
    layers = [
        (3, (255, 255, 255, 15)),  # Outer glow
        (2, (255, 255, 255, 25)),  # Middle layer
        (1, (255, 255, 255, blur_alpha)),  # Main glass
        (0, (255, 255, 255, 5))   # Inner highlight
    ]
    
    for offset, color in layers:
        draw.rounded_rectangle(
            [x - offset, y - offset, x + width + offset, y + height + offset],
            radius=20 + offset * 2,
            fill=color,
            outline=(255, 255, 255, 40) if offset == 1 else None,
            width=1 if offset == 1 else 0
        )


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

        # Create 4K canvas for ultra-high quality
        canvas = Image.new('RGBA', (1920, 1080), (8, 8, 20, 255))
        
        # Load and enhance original thumbnail
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1920, 1080, youtube)
        
        # Advanced image processing
        enhancer = ImageEnhance.Brightness(image1)
        image1 = enhancer.enhance(0.6)
        
        enhancer = ImageEnhance.Contrast(image1)
        image1 = enhancer.enhance(1.8)
        
        enhancer = ImageEnhance.Color(image1)
        image1 = enhancer.enhance(1.4)
        
        # Apply multiple blur layers for depth
        blur_layers = [
            image1.filter(ImageFilter.GaussianBlur(radius=3)),
            image1.filter(ImageFilter.GaussianBlur(radius=1))
        ]
        
        # Composite blurred layers
        base_image = Image.blend(blur_layers[0], blur_layers[1], 0.6)
        canvas.paste(base_image, (0, 0))
        
        # Apply glitch effect occasionally
        if random.random() < 0.3:
            canvas = create_glitch_effect(canvas, 0.2)
        
        # Create dynamic background overlay
        bg_overlay = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(bg_overlay)
        
        # Layer multiple background effects
        create_neural_network_bg(bg_draw, 1920, 1080)
        create_plasma_effect(bg_draw, 1920, 1080)
        create_cyberpunk_grid(bg_draw, 1920, 1080, 0.5)
        
        # Composite background
        canvas = Image.alpha_composite(canvas, bg_overlay)
        draw = ImageDraw.Draw(canvas)
        
        # Load premium fonts
        try:
            title_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 54)
            brand_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 72)
            info_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 36)
            control_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 42)
        except:
            title_font = ImageFont.load_default()
            brand_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            control_font = ImageFont.load_default()
        
        # Ultra-modern brand section with glassmorphism
        create_glass_morphism_panel(draw, 40, 40, 600, 180, 60)
        
        # Add multiple energy orbs
        create_energy_orb(draw, 140, 130, 90, 1.2)
        create_energy_orb(draw, 550, 110, 60, 0.8)
        
        # Holographic brand text
        create_holographic_neon_text(draw, "♪ WYNK", 200, 70, brand_font, (0, 255, 255))
        create_holographic_neon_text(draw, "MUSIC", 200, 140, brand_font, (255, 0, 255))
        
        # Subtitle with animated glow
        t = time.time()
        subtitle_alpha = int(150 + math.sin(t * 3) * 50)
        draw.text((200, 190), "ULTRA EXPERIENCE", 
                 fill=(255, 176, 49, subtitle_alpha), font=info_font,
                 stroke_width=1, stroke_fill=(0, 0, 0, 100))
        
        # Advanced morphing visualizer
        create_morphing_visualizer(draw, 700, 60, 1100, 160, 60)
        
        # Futuristic info panels with glassmorphism
        info_items = [
            (f"📺 {channel}", 80, 750),
            (f"👁 {views} views", 80, 810),
            (f"⏱ {duration}", 80, 870)
        ]
        
        for text, x, y in info_items:
            # Animated glassmorphism panels
            panel_time = time.time() + y/200
            panel_alpha = int(80 + math.sin(panel_time * 2) * 30)
            
            create_glass_morphism_panel(draw, x-20, y-15, 500, 50, panel_alpha)
            create_holographic_neon_text(draw, text, x, y, info_font, (0, 255, 255))
        
        # Ultra-dynamic title with multiple effects
        title_y = 950
        create_glass_morphism_panel(draw, 40, title_y-20, 1840, 90, 100)
        
        # Add energy effects around title
        create_energy_orb(draw, 100, title_y + 25, 40, 0.6)
        create_energy_orb(draw, 1820, title_y + 25, 35, 0.7)
        
        create_holographic_neon_text(draw, clear(title), 80, title_y, title_font, (255, 255, 0))
        
        # Next-gen progress bar with particles
        progress_y = 1020
        bar_width = 1800
        bar_height = 20
        
        create_glass_morphism_panel(draw, 60, progress_y-5, bar_width, bar_height+10, 120)
        
        # Animated progress with multiple layers
        progress_percent = (time.time() * 8) % 100 / 100
        fill_width = int(bar_width * progress_percent)
        
        # Multi-layer progress fill
        for layer in range(4):
            layer_width = fill_width - layer * 2
            if layer_width > 0:
                layer_alpha = 200 - layer * 40
                
                # Gradient colors
                hue = (time.time() * 0.3 + layer * 0.2) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), layer_alpha)
                
                draw.rounded_rectangle([60 + layer, progress_y + layer, 
                                      60 + layer_width - layer, progress_y + bar_height - layer],
                                     radius=10 - layer, fill=color)
        
        # Animated progress indicator with trails
        indicator_x = 60 + fill_width
        for trail in range(8):
            trail_x = indicator_x - trail * 5
            trail_alpha = max(0, 200 - trail * 25)
            trail_size = 8 - trail
            
            draw.ellipse([trail_x - trail_size, progress_y + 5,
                         trail_x + trail_size, progress_y + 15],
                        fill=(255, 255, 255, trail_alpha))
        
        # Ultra-modern control buttons with advanced effects
        controls_y = 1050
        buttons = [
            ("⏮", 300, (255, 100, 100)), ("⏯", 450, (100, 255, 100)), ("⏭", 600, (100, 100, 255)),
            ("🔀", 150, (255, 255, 100)), ("🔁", 750, (255, 100, 255)), ("⚡", 900, (100, 255, 255))
        ]
        
        for icon, x, color in buttons:
            # Multi-layer button with energy effects
            create_energy_orb(draw, x, controls_y, 50, 0.5)
            
            # Glassmorphism button base
            create_glass_morphism_panel(draw, x-35, controls_y-35, 70, 70, 100)
            
            # Icon with special effects
            create_holographic_neon_text(draw, icon, x-15, controls_y-18, control_font, color)
        
        # Add final atmospheric effects
        atmosphere_overlay = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        atmo_draw = ImageDraw.Draw(atmosphere_overlay)
        
        # Floating particles with trails
        for i in range(30):
            particle_t = time.time() + i * 0.5
            px = (100 + i * 60 + math.sin(particle_t) * 100) % 1920
            py = (80 + i * 30 + math.cos(particle_t * 0.8) * 150) % 1080
            
            # Particle with trail
            for trail in range(5):
                trail_px = px - math.sin(particle_t) * trail * 10
                trail_py = py - math.cos(particle_t * 0.8) * trail * 5
                trail_alpha = max(0, 150 - trail * 30)
                trail_size = max(1, 4 - trail)
                
                hue = (particle_t * 0.2 + i * 0.1) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), trail_alpha)
                
                atmo_draw.ellipse([trail_px - trail_size, trail_py - trail_size,
                                 trail_px + trail_size, trail_py + trail_size], 
                                fill=color)
        
        # Final composite
        canvas = Image.alpha_composite(canvas, atmosphere_overlay)
        
        # Clean up temporary files
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        canvas.save(f"cache/{videoid}.png", quality=95, optimize=True)
        return f"cache/{videoid}.png"
        
    except Exception as e:
        print(f"Ultra-modern thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL

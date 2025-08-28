import os
import re
import random
import math
from typing import Tuple, List

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from AnonXMusic import app
from config import YOUTUBE_IMG_URL


class AdvancedThumbnailGenerator:
    """Advanced thumbnail generator with modern design elements"""
    
    def __init__(self):
        self.gradient_colors = [
            ["#FF6B6B", "#4ECDC4"],  # Coral to Teal
            ["#667eea", "#764ba2"],  # Purple Blue
            ["#f093fb", "#f5576c"],  # Pink Gradient
            ["#4facfe", "#00f2fe"],  # Blue Cyan
            ["#43e97b", "#38f9d7"],  # Green Cyan
            ["#fa709a", "#fee140"],  # Pink Yellow
            ["#a8edea", "#fed6e3"],  # Mint Pink
            ["#ff9a9e", "#fecfef"],  # Rose
        ]
        
        self.accent_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", 
            "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"
        ]
    
    def create_gradient_background(self, width: int, height: int, colors: List[str]) -> Image.Image:
        """Create a smooth gradient background"""
        base = Image.new('RGB', (width, height), colors[0])
        top = Image.new('RGB', (width, height), colors[1])
        
        mask = Image.new('L', (width, height))
        mask_data = []
        for y in range(height):
            for x in range(width):
                # Create diagonal gradient
                distance = math.sqrt((x/width)**2 + (y/height)**2)
                mask_data.append(int(255 * min(distance, 1)))
        
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base
    
    def add_glassmorphism_effect(self, image: Image.Image, x: int, y: int, 
                               width: int, height: int, blur_radius: int = 10) -> Image.Image:
        """Add glassmorphism effect to a rectangular area"""
        # Create a semi-transparent overlay
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Draw rounded rectangle with transparency
        draw.rounded_rectangle(
            [(x, y), (x + width, y + height)], 
            radius=20, 
            fill=(255, 255, 255, 40),
            outline=(255, 255, 255, 80),
            width=2
        )
        
        # Apply blur for glass effect
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        return Image.alpha_composite(image.convert('RGBA'), overlay)
    
    def add_neon_glow(self, draw: ImageDraw.Draw, text: str, pos: Tuple[int, int], 
                     font: ImageFont.FreeTypeFont, color: str, glow_radius: int = 3):
        """Add enhanced neon glow effect to text"""
        x, y = pos
        rgb_color = self.hex_to_rgb(color)
        
        # Outer glow - largest and most transparent
        for i in range(glow_radius * 2, glow_radius, -1):
            glow_alpha = int(100 * (1 - (i - glow_radius) / glow_radius))
            glow_color = (*rgb_color, glow_alpha)
            for dx in range(-i, i + 1):
                for dy in range(-i, i + 1):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= i:
                        intensity = 1 - (distance / i)
                        final_alpha = int(glow_alpha * intensity)
                        if final_alpha > 0:
                            draw.text((x + dx, y + dy), text, font=font, 
                                    fill=(*rgb_color, final_alpha))
        
        # Inner bright glow
        for i in range(glow_radius, 0, -1):
            glow_alpha = int(200 * (i / glow_radius))
            for dx in range(-i, i + 1):
                for dy in range(-i, i + 1):
                    if dx*dx + dy*dy <= i*i:
                        draw.text((x + dx, y + dy), text, font=font, 
                                fill=(*rgb_color, glow_alpha))
        
        # Core text - brightest
        draw.text(pos, text, font=font, fill=color)
        
        # Add extra brightness to core
        draw.text(pos, text, font=font, fill=(*rgb_color, 100))
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def add_wave_pattern(self, image: Image.Image, color: str, amplitude: int = 20, 
                        frequency: float = 0.02) -> Image.Image:
        """Add decorative wave pattern"""
        width, height = image.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        rgb_color = self.hex_to_rgb(color)
        wave_color = (*rgb_color, 100)
        
        # Create wave points
        points = []
        for x in range(0, width + 10, 5):
            y = height - 100 + amplitude * math.sin(frequency * x)
            points.append((x, y))
        
        # Add bottom points to close the shape
        points.extend([(width, height), (0, height)])
        
        if len(points) > 2:
            draw.polygon(points, fill=wave_color)
        
        return Image.alpha_composite(image.convert('RGBA'), overlay)
    
    def add_music_visualizer(self, draw: ImageDraw.Draw, x: int, y: int, 
                           width: int, color: str, bars: int = 20):
        """Add impressive animated-style music visualizer bars with neon effect"""
        bar_width = max(width // bars - 2, 8)
        rgb_color = self.hex_to_rgb(color)
        
        for i in range(bars):
            # Create varied heights for dynamic look
            base_height = 15
            wave_effect = 25 * math.sin((i / bars) * math.pi * 2)
            random_variation = random.randint(-10, 15)
            bar_height = int(base_height + wave_effect + random_variation)
            bar_height = max(bar_height, 5)  # Minimum height
            
            bar_x = x + i * (bar_width + 2)
            bar_y = y - bar_height
            
            # Create neon glow effect for each bar
            for glow in range(3, 0, -1):
                glow_alpha = int(80 * (glow / 3))
                glow_width = bar_width + glow * 2
                glow_height = bar_height + glow * 2
                
                draw.rectangle(
                    [(bar_x - glow, bar_y - glow), 
                     (bar_x + glow_width, y + glow)],
                    fill=(*rgb_color, glow_alpha)
                )
            
            # Main bar with gradient effect
            gradient_steps = max(bar_height // 3, 3)
            for step in range(gradient_steps):
                step_height = bar_height // gradient_steps
                step_y = bar_y + step * step_height
                
                # Gradient from bright at top to dimmer at bottom
                brightness = 1.0 - (step / gradient_steps) * 0.4
                step_color = tuple(int(c * brightness) for c in rgb_color)
                
                draw.rectangle(
                    [(bar_x, step_y), (bar_x + bar_width, step_y + step_height)],
                    fill=(*step_color, 255)
                )
            
            # Add bright highlight on top of each bar
            draw.rectangle(
                [(bar_x, bar_y), (bar_x + bar_width, bar_y + 2)],
                fill="white"
            )

def changeImageSize(maxWidth: int, maxHeight: int, image: Image.Image) -> Image.Image:
    """Resize image while maintaining aspect ratio"""
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    ratio = min(widthRatio, heightRatio)
    
    newWidth = int(ratio * image.size[0])
    newHeight = int(ratio * image.size[1])
    
    return image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)

def clear(text: str, max_length: int = 50) -> str:
    """Clean and truncate text for display"""
    words = text.split(" ")
    title = ""
    for word in words:
        if len(title) + len(word) + 1 <= max_length:
            title += " " + word
        else:
            break
    return title.strip()

def format_duration(duration_str: str) -> str:
    """Format duration string for better display"""
    if ":" in duration_str:
        return duration_str
    return duration_str.replace(":", ":")

def format_views(views_str: str) -> str:
    """Format view count for better display"""
    if "views" not in views_str.lower():
        return f"{views_str} views"
    return views_str

async def get_thumb(videoid: str) -> str:
    """Generate advanced thumbnail for video"""
    cache_path = f"cache/{videoid}.png"
    
    if os.path.isfile(cache_path):
        return cache_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    generator = AdvancedThumbnailGenerator()
    
    try:
        # Search for video information
        results = VideosSearch(url, limit=1)
        video_data = (await results.next())["result"][0]
        
        # Extract video information with fallbacks
        title = video_data.get("title", "Unknown Title")
        title = re.sub(r'\W+', ' ', title).title()
        
        duration = video_data.get("duration", "Unknown")
        thumbnail_url = video_data.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
        
        views = video_data.get("viewCount", {}).get("short", "Unknown Views")
        channel = video_data.get("channel", {}).get("name", "Unknown Channel")
        
        # Download thumbnail
        temp_thumb_path = f"cache/temp_thumb_{videoid}.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(temp_thumb_path, mode="wb") as f:
                        await f.write(await resp.read())
        
        # Load and process thumbnail
        youtube_thumb = Image.open(temp_thumb_path)
        processed_thumb = changeImageSize(1280, 720, youtube_thumb)
        
        # Create gradient background
        gradient_colors = random.choice(generator.gradient_colors)
        background = generator.create_gradient_background(1280, 720, gradient_colors)
        
        # Apply thumbnail with blend mode
        thumb_enhanced = ImageEnhance.Brightness(processed_thumb).enhance(0.8)
        thumb_enhanced = ImageEnhance.Contrast(thumb_enhanced).enhance(1.2)
        
        # Create mask for rounded corners
        mask = Image.new('L', processed_thumb.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            [(0, 0), processed_thumb.size], 
            radius=25, 
            fill=255
        )
        
        # Paste thumbnail onto background
        background.paste(processed_thumb, (0, 0), mask)
        
        # Add glassmorphism overlay for text area
        background = generator.add_glassmorphism_effect(
            background, 40, 500, 1200, 180
        )
        
        # Add wave pattern decoration
        accent_color = random.choice(generator.accent_colors)
        background = generator.add_wave_pattern(background, accent_color)
        
        # Convert to RGBA for drawing
        background = background.convert('RGBA')
        draw = ImageDraw.Draw(background)
        
        # Load fonts with fallbacks
        try:
            title_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 36)
            info_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 28)
            app_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 32)
            control_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            app_font = ImageFont.load_default()
            control_font = ImageFont.load_default()
        
        # Add app name with neon effect
        app_name = unidecode(app.name)
        generator.add_neon_glow(
            draw, app_name, (60, 20), app_font, accent_color, glow_radius=4
        )
        
        # Add channel and views info
        channel_info = f"🎵 {channel} • {format_views(views)}"
        draw.text((60, 520), channel_info, fill="white", font=info_font)
        
        # Add title with shadow effect
        clean_title = clear(title, 60)
        # Shadow
        draw.text((62, 562), clean_title, fill=(0, 0, 0, 120), font=title_font)
        # Main text
        draw.text((60, 560), clean_title, fill="white", font=title_font)
        
        # Add duration badge
        if duration != "Unknown":
            duration_formatted = format_duration(duration)
            # Create rounded rectangle for duration
            duration_bbox = draw.textbbox((0, 0), duration_formatted, font=info_font)
            badge_width = duration_bbox[2] - duration_bbox[0] + 20
            badge_height = duration_bbox[3] - duration_bbox[1] + 10
            
            badge_x = 1280 - badge_width - 20
            badge_y = 20
            
            draw.rounded_rectangle(
                [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
                radius=15,
                fill=(0, 0, 0, 180),
                outline=accent_color,
                width=2
            )
            
            text_x = badge_x + 10
            text_y = badge_y + 5
            draw.text((text_x, text_y), duration_formatted, fill="white", font=info_font)
        
        # Add decorative neon line with pulsing effect
        line_y = 620
        gradient_line_colors = generator.hex_to_rgb(accent_color)
        
        # Create pulsing neon line effect
        for pulse_layer in range(3):
            pulse_width = 6 - pulse_layer * 2
            pulse_alpha = int(255 * (0.8 - pulse_layer * 0.2))
            pulse_color = (*gradient_line_colors, pulse_alpha)
            
            # Main horizontal line
            draw.line([(60, line_y), (1220, line_y)], fill=pulse_color, width=pulse_width)
            
            # Add decorative dots along the line
            for dot_x in range(80, 1200, 40):
                dot_size = pulse_width // 2
                draw.ellipse(
                    [(dot_x - dot_size, line_y - dot_size), 
                     (dot_x + dot_size, line_y + dot_size)],
                    fill=pulse_color
                )
        
        # Add electric spark effects at line ends
        spark_points_left = [
            (55, line_y), (45, line_y - 5), (50, line_y), (40, line_y + 5), (55, line_y)
        ]
        spark_points_right = [
            (1225, line_y), (1235, line_y - 5), (1230, line_y), (1240, line_y + 5), (1225, line_y)
        ]
        
        draw.polygon(spark_points_left, fill=accent_color)
        draw.polygon(spark_points_right, fill=accent_color)
        
        # Add music visualizer
        generator.add_music_visualizer(draw, 60, 650, 200, accent_color)
        
        # Add impressive control buttons with neon effects
        controls_y = 650
        control_spacing = 120
        start_x = 350
        
        # Create custom control symbols with paths
        control_designs = [
            {"name": "prev", "color": accent_color},
            {"name": "play", "color": "#FF3366"},  # Bright red for play
            {"name": "next", "color": accent_color},
            {"name": "shuffle", "color": "#00FF88"},  # Bright green
            {"name": "repeat", "color": "#FFD700"}   # Gold
        ]
        
        for i, control in enumerate(control_designs):
            x = start_x + i * control_spacing
            button_color = control["color"]
            button_rgb = generator.hex_to_rgb(button_color)
            
            # Create multiple glow layers for neon effect
            for glow_size in range(8, 0, -1):
                glow_alpha = int(30 * (glow_size / 8))
                glow_color = (*button_rgb, glow_alpha)
                
                draw.ellipse(
                    [(x - 30 - glow_size, controls_y - 30 - glow_size), 
                     (x + 30 + glow_size, controls_y + 30 + glow_size)],
                    fill=glow_color
                )
            
            # Main button with gradient effect
            draw.ellipse(
                [(x - 30, controls_y - 30), (x + 30, controls_y + 30)],
                fill=(*button_rgb, 200),
                outline=button_color,
                width=3
            )
            
            # Inner highlight circle for 3D effect
            draw.ellipse(
                [(x - 25, controls_y - 25), (x + 25, controls_y + 25)],
                outline=(*button_rgb, 100),
                width=1
            )
            
            # Draw custom symbols with thick lines and glow
            symbol_color = "white"
            line_width = 4
            
            if control["name"] == "prev":
                # Previous symbol: |◄
                draw.line([(x - 12, controls_y - 15), (x - 12, controls_y + 15)], 
                         fill=symbol_color, width=line_width)
                points = [(x - 8, controls_y), (x + 8, controls_y - 12), (x + 8, controls_y + 12)]
                draw.polygon(points, fill=symbol_color)
                
            elif control["name"] == "play":
                # Play/Pause symbol: ▶ or ⏸
                if random.choice([True, False]):  # Randomize play/pause
                    # Play triangle
                    points = [(x - 10, controls_y - 15), (x - 10, controls_y + 15), (x + 15, controls_y)]
                    draw.polygon(points, fill=symbol_color)
                else:
                    # Pause bars
                    draw.rectangle([(x - 8, controls_y - 15), (x - 2, controls_y + 15)], fill=symbol_color)
                    draw.rectangle([(x + 2, controls_y - 15), (x + 8, controls_y + 15)], fill=symbol_color)
                
            elif control["name"] == "next":
                # Next symbol: ►|
                points = [(x - 8, controls_y), (x + 8, controls_y - 12), (x + 8, controls_y + 12)]
                draw.polygon(points, fill=symbol_color)
                draw.line([(x + 12, controls_y - 15), (x + 12, controls_y + 15)], 
                         fill=symbol_color, width=line_width)
                
            elif control["name"] == "shuffle":
                # Shuffle symbol: crossing arrows
                draw.line([(x - 15, controls_y - 8), (x + 15, controls_y + 8)], 
                         fill=symbol_color, width=line_width)
                draw.line([(x - 15, controls_y + 8), (x + 15, controls_y - 8)], 
                         fill=symbol_color, width=line_width)
                # Arrow heads
                draw.polygon([(x + 15, controls_y + 8), (x + 10, controls_y + 3), (x + 10, controls_y + 13)], 
                           fill=symbol_color)
                draw.polygon([(x - 15, controls_y - 8), (x - 10, controls_y - 3), (x - 10, controls_y - 13)], 
                           fill=symbol_color)
                
            elif control["name"] == "repeat":
                # Repeat symbol: circular arrow
                # Draw arc-like repeat symbol
                draw.arc([(x - 12, controls_y - 12), (x + 12, controls_y + 12)], 
                        start=30, end=330, fill=symbol_color, width=line_width)
                # Arrow head
                draw.polygon([(x + 8, controls_y - 10), (x + 12, controls_y - 6), (x + 4, controls_y - 6)], 
                           fill=symbol_color)
        
        # Add subtle vignette effect
        vignette = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
        vignette_draw = ImageDraw.Draw(vignette)
        
        # Create radial gradient for vignette
        center_x, center_y = 640, 360
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(720):
            for x in range(1280):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                alpha = int(60 * (distance / max_distance))
                if alpha > 0:
                    vignette_draw.point((x, y), fill=(0, 0, 0, min(alpha, 100)))
        
        background = Image.alpha_composite(background, vignette)
        
        # Clean up temporary files
        try:
            os.remove(temp_thumb_path)
        except:
            pass
        
        # Convert back to RGB and save
        final_image = background.convert('RGB')
        final_image.save(cache_path, optimize=True, quality=95)
        
        return cache_path
        
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return YOUTUBE_IMG_URL

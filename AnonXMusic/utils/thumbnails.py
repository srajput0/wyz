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


class PremiumThumbnailGenerator:
    """Premium thumbnail generator inspired by professional music video thumbnails"""
    
    def __init__(self):
        # Bright, vibrant gradient combinations
        self.gradient_colors = [
            ["#FF416C", "#FF4B2B"],  # Pink to Red
            ["#667eea", "#764ba2"],  # Blue to Purple  
            ["#f093fb", "#f5576c"],  # Magenta to Pink
            ["#4facfe", "#00f2fe"],  # Blue to Cyan
            ["#43e97b", "#38f9d7"],  # Green to Cyan
            ["#fa709a", "#fee140"],  # Pink to Yellow
            ["#ff9a9e", "#fad0c4"],  # Rose gradient
            ["#a8edea", "#fed6e3"],  # Mint to Pink
            ["#ffecd2", "#fcb69f"],  # Peach gradient
            ["#ff8a80", "#ff5722"],  # Coral gradient
        ]
        
        # Bright accent colors for controls
        self.control_colors = [
            "#FFD700",  # Gold
            "#FF1744",  # Bright Red
            "#00E676",  # Bright Green
            "#00B0FF",  # Bright Blue
            "#FF6D00",  # Bright Orange
            "#E91E63",  # Pink
            "#9C27B0",  # Purple
            "#00BCD4",  # Cyan
        ]
    
    def create_advanced_gradient(self, width: int, height: int, colors: List[str], 
                               direction: str = "diagonal") -> Image.Image:
        """Create advanced gradient backgrounds with multiple directions"""
        base = Image.new('RGBA', (width, height))
        
        for y in range(height):
            for x in range(width):
                if direction == "diagonal":
                    # Diagonal gradient from top-left to bottom-right
                    ratio = (x + y) / (width + height)
                elif direction == "horizontal":
                    ratio = x / width
                elif direction == "vertical":
                    ratio = y / height
                elif direction == "radial":
                    center_x, center_y = width // 2, height // 2
                    max_distance = math.sqrt(center_x**2 + center_y**2)
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = min(distance / max_distance, 1.0)
                else:
                    ratio = (x + y) / (width + height)
                
                # Smooth color interpolation
                ratio = min(max(ratio, 0), 1)
                color1 = self.hex_to_rgb(colors[0])
                color2 = self.hex_to_rgb(colors[1])
                
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                base.putpixel((x, y), (r, g, b, 255))
        
        return base
    
    def add_premium_glow(self, image: Image.Image, x: int, y: int, width: int, height: int,
                        glow_color: str, intensity: float = 1.0) -> Image.Image:
        """Add premium glow effect to specific areas"""
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        rgb_color = self.hex_to_rgb(glow_color)
        
        # Multiple glow layers for realistic effect
        for i in range(15, 0, -1):
            alpha = int(intensity * 20 * (i / 15))
            glow_size = i * 2
            
            draw.rounded_rectangle(
                [(x - glow_size, y - glow_size), 
                 (x + width + glow_size, y + height + glow_size)],
                radius=25,
                fill=(*rgb_color, alpha)
            )
        
        return Image.alpha_composite(image.convert('RGBA'), overlay)
    
    def create_glass_overlay(self, width: int, height: int, x: int, y: int,
                           overlay_width: int, overlay_height: int) -> Image.Image:
        """Create modern glass overlay effect"""
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Main glass rectangle with rounded corners
        draw.rounded_rectangle(
            [(x, y), (x + overlay_width, y + overlay_height)],
            radius=20,
            fill=(0, 0, 0, 120),  # Semi-transparent black
            outline=(255, 255, 255, 60),
            width=2
        )
        
        # Inner highlight for glass effect
        draw.rounded_rectangle(
            [(x + 5, y + 5), (x + overlay_width - 5, y + overlay_height - 5)],
            radius=15,
            outline=(255, 255, 255, 30),
            width=1
        )
        
        return overlay
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def draw_control_button(self, draw: ImageDraw.Draw, x: int, y: int, 
                          button_type: str, color: str, size: int = 25):
        """Draw professional control buttons with bright colors"""
        rgb_color = self.hex_to_rgb(color)
        
        # Multi-layer glow effect
        for glow_layer in range(8, 0, -1):
            glow_alpha = int(150 * (glow_layer / 8) * 0.3)
            glow_size = size + glow_layer * 3
            
            draw.ellipse(
                [(x - glow_size, y - glow_size), (x + glow_size, y + glow_size)],
                fill=(*rgb_color, glow_alpha)
            )
        
        # Main button circle
        draw.ellipse(
            [(x - size, y - size), (x + size, y + size)],
            fill=color,
            outline="white",
            width=3
        )
        
        # Inner circle for depth
        draw.ellipse(
            [(x - size + 5, y - size + 5), (x + size - 5, y + size - 5)],
            outline=(255, 255, 255, 100),
            width=1
        )
        
        # Draw button symbols with white color for visibility
        symbol_color = "white"
        line_width = 4
        
        if button_type == "previous":
            # Previous: |◄
            draw.line([(x - 10, y - 12), (x - 10, y + 12)], fill=symbol_color, width=line_width)
            points = [(x - 5, y), (x + 8, y - 10), (x + 8, y + 10)]
            draw.polygon(points, fill=symbol_color)
            
        elif button_type == "play":
            # Play: ►
            points = [(x - 8, y - 12), (x - 8, y + 12), (x + 12, y)]
            draw.polygon(points, fill=symbol_color)
            
        elif button_type == "pause":
            # Pause: ❚❚
            draw.rectangle([(x - 8, y - 12), (x - 2, y + 12)], fill=symbol_color)
            draw.rectangle([(x + 2, y - 12), (x + 8, y + 12)], fill=symbol_color)
            
        elif button_type == "next":
            # Next: ►|
            points = [(x - 8, y), (x + 5, y - 10), (x + 5, y + 10)]
            draw.polygon(points, fill=symbol_color)
            draw.line([(x + 10, y - 12), (x + 10, y + 12)], fill=symbol_color, width=line_width)
            
        elif button_type == "shuffle":
            # Shuffle: ⧢
            draw.line([(x - 12, y - 6), (x + 12, y + 6)], fill=symbol_color, width=line_width)
            draw.line([(x - 12, y + 6), (x + 12, y - 6)], fill=symbol_color, width=line_width)
            # Arrow heads
            draw.polygon([(x + 12, y + 6), (x + 6, y + 2), (x + 6, y + 10)], fill=symbol_color)
            draw.polygon([(x - 12, y - 6), (x - 6, y - 2), (x - 6, y - 10)], fill=symbol_color)
            
        elif button_type == "repeat":
            # Repeat: ↻
            draw.arc([(x - 10, y - 10), (x + 10, y + 10)], start=45, end=315, 
                    fill=symbol_color, width=line_width)
            # Arrow head
            draw.polygon([(x + 7, y - 7), (x + 12, y - 2), (x + 2, y - 2)], fill=symbol_color)


def changeImageSize(maxWidth: int, maxHeight: int, image: Image.Image) -> Image.Image:
    """Resize image maintaining aspect ratio with high quality"""
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newWidth = int(ratio * image.size[0])
    newHeight = int(ratio * image.size[1])
    return image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)


def clear(text: str, max_length: int = 45) -> str:
    """Clean and truncate text"""
    words = text.split()
    result = ""
    for word in words:
        if len(result + " " + word) <= max_length:
            result += " " + word if result else word
        else:
            break
    return result.strip()


async def get_thumb(videoid: str) -> str:
    """Generate premium advanced thumbnail"""
    cache_path = f"cache/{videoid}.png"
    
    if os.path.isfile(cache_path):
        return cache_path

    generator = PremiumThumbnailGenerator()
    url = f"https://www.youtube.com/watch?v={videoid}"
    
    try:
        # Get video information
        results = VideosSearch(url, limit=1)
        video_data = (await results.next())["result"][0]
        
        title = video_data.get("title", "Unknown Title")
        title = re.sub(r'\W+', ' ', title).title()
        
        duration = video_data.get("duration", "Unknown")
        thumbnail_url = video_data.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
        views = video_data.get("viewCount", {}).get("short", "Unknown Views")
        channel = video_data.get("channel", {}).get("name", "Unknown Channel")
        
        # Download thumbnail
        temp_thumb = f"cache/temp_{videoid}.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(temp_thumb, mode="wb") as f:
                        await f.write(await resp.read())
        
        # Create base canvas
        canvas = Image.new('RGBA', (1280, 720), (0, 0, 0, 255))
        
        # Load and process thumbnail
        youtube_thumb = Image.open(temp_thumb)
        
        # Create advanced gradient background
        gradient_colors = random.choice(generator.gradient_colors)
        gradient_bg = generator.create_advanced_gradient(
            1280, 720, gradient_colors, "diagonal"
        )
        
        # Blend thumbnail with background
        thumb_resized = changeImageSize(1280, 720, youtube_thumb)
        
        # Create a mask for the thumbnail blend
        thumb_enhanced = ImageEnhance.Brightness(thumb_resized).enhance(0.7)
        thumb_enhanced = ImageEnhance.Contrast(thumb_enhanced).enhance(1.3)
        
        # Blend thumbnail with gradient
        blended = Image.blend(gradient_bg.convert('RGB'), thumb_enhanced, 0.6)
        canvas = blended.convert('RGBA')
        
        # Add premium glow to title area
        canvas = generator.add_premium_glow(
            canvas, 600, 100, 600, 200, gradient_colors[1], 0.8
        )
        
        # Create glass overlay for bottom info section
        glass_overlay = generator.create_glass_overlay(1280, 720, 40, 500, 1200, 180)
        canvas = Image.alpha_composite(canvas, glass_overlay)
        
        draw = ImageDraw.Draw(canvas)
        
        # Load fonts with fallbacks
        try:
            app_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 40)
            title_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 72)
            channel_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 32)
            duration_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 28)
        except:
            # Fallback fonts
            app_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            channel_font = ImageFont.load_default()
            duration_font = ImageFont.load_default()
        
        # Draw app name (top left) with glow
        app_name = unidecode(app.name)
        for glow in range(5, 0, -1):
            glow_color = (*generator.hex_to_rgb("#FFD700"), int(100 * glow / 5))
            draw.text((60 + glow, 25 + glow), app_name, fill=glow_color, font=app_font)
        draw.text((60, 25), app_name, fill="#FFD700", font=app_font)
        
        # Duration badge (top right)
        if duration and duration != "Unknown":
            duration_text = duration
            duration_bbox = draw.textbbox((0, 0), duration_text, font=duration_font)
            badge_width = duration_bbox[2] - duration_bbox[0] + 20
            badge_height = duration_bbox[3] - duration_bbox[1] + 12
            
            badge_x = 1280 - badge_width - 20
            badge_y = 20
            
            # Badge background with glow
            for glow in range(4, 0, -1):
                glow_alpha = int(80 * glow / 4)
                draw.rounded_rectangle(
                    [(badge_x - glow, badge_y - glow), 
                     (badge_x + badge_width + glow, badge_y + badge_height + glow)],
                    radius=20,
                    fill=(0, 0, 0, glow_alpha)
                )
            
            draw.rounded_rectangle(
                [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
                radius=15,
                fill=(0, 0, 0, 180),
                outline="#FFD700",
                width=2
            )
            
            draw.text(
                (badge_x + 10, badge_y + 6), 
                duration_text, 
                fill="white", 
                font=duration_font
            )
        
        # Large title (right side) - main focal point
        clean_title = clear(title, 25)
        title_lines = []
        words = clean_title.split()
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 15:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    title_lines.append(current_line)
                current_line = word
        
        if current_line:
            title_lines.append(current_line)
        
        # Draw title with bright colors and glow
        title_start_y = 150
        title_color = "#FFFFFF"
        
        for i, line in enumerate(title_lines[:3]):  # Max 3 lines
            line_y = title_start_y + i * 80
            
            # Multi-layer glow for title
            for glow in range(8, 0, -1):
                glow_alpha = int(150 * glow / 8 * 0.4)
                glow_color = (*generator.hex_to_rgb(gradient_colors[0]), glow_alpha)
                draw.text((650 + glow, line_y + glow), line, fill=glow_color, font=title_font)
            
            # Main title text
            draw.text((650, line_y), line, fill=title_color, font=title_font)
        
        # Channel info (bottom left)
        channel_text = f"{channel} • {views}"
        draw.text((60, 530), channel_text, fill="#CCCCCC", font=channel_font)
        
        # Song title (bottom - larger)
        song_title = clear(title, 50)
        # Shadow for song title
        draw.text((62, 572), song_title, fill=(0, 0, 0, 150), font=channel_font)
        # Main song title
        draw.text((60, 570), song_title, fill="white", font=channel_font)
        
        # Premium control buttons (bottom center) - highly visible
        controls_y = 630
        button_configs = [
            {"type": "previous", "color": generator.control_colors[0], "x_offset": -200},
            {"type": "pause", "color": generator.control_colors[1], "x_offset": -100},
            {"type": "play", "color": generator.control_colors[1], "x_offset": -100},
            {"type": "next", "color": generator.control_colors[2], "x_offset": 0},
            {"type": "shuffle", "color": generator.control_colors[3], "x_offset": 100},
            {"type": "repeat", "color": generator.control_colors[4], "x_offset": 200},
        ]
        
        # Randomize play/pause
        play_or_pause = random.choice(["play", "pause"])
        center_x = 640
        
        active_buttons = [
            {"type": "previous", "color": generator.control_colors[0]},
            {"type": play_or_pause, "color": generator.control_colors[1]},
            {"type": "next", "color": generator.control_colors[2]},
            {"type": "shuffle", "color": generator.control_colors[3]},
            {"type": "repeat", "color": generator.control_colors[4]},
        ]
        
        for i, button in enumerate(active_buttons):
            x_pos = center_x + (i - 2) * 120  # Center the buttons
            generator.draw_control_button(
                draw, x_pos, controls_y, 
                button["type"], button["color"], 30
            )
        
        # Add progress bar simulation
        progress_y = 600
        progress_width = 800
        progress_x = (1280 - progress_width) // 2
        
        # Progress bar background
        draw.rounded_rectangle(
            [(progress_x, progress_y), (progress_x + progress_width, progress_y + 8)],
            radius=4,
            fill=(255, 255, 255, 60)
        )
        
        # Progress bar fill (random progress)
        progress_fill = random.randint(20, 80)
        fill_width = int(progress_width * progress_fill / 100)
        
        draw.rounded_rectangle(
            [(progress_x, progress_y), (progress_x + fill_width, progress_y + 8)],
            radius=4,
            fill=gradient_colors[0]
        )
        
        # Progress dot
        dot_x = progress_x + fill_width
        draw.ellipse(
            [(dot_x - 8, progress_y - 4), (dot_x + 8, progress_y + 12)],
            fill="white",
            outline=gradient_colors[0],
            width=2
        )
        
        # Clean up
        try:
            os.remove(temp_thumb)
        except:
            pass
        
        # Convert to RGB and save with high quality
        final_image = canvas.convert('RGB')
        final_image.save(cache_path, optimize=True, quality=98)
        
        return cache_path
        
    except Exception as e:
        print(f"Thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL

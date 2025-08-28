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
        """Add neon glow effect to text"""
        x, y = pos
        
        # Draw multiple layers for glow effect
        for i in range(glow_radius, 0, -1):
            glow_color = (*self.hex_to_rgb(color), int(255 * (i / glow_radius) * 0.3))
            for dx in range(-i, i + 1):
                for dy in range(-i, i + 1):
                    if dx*dx + dy*dy <= i*i:
                        draw.text((x + dx, y + dy), text, font=font, fill=glow_color)
        
        # Draw main text
        draw.text(pos, text, font=font, fill=color)
    
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
                           width: int, color: str, bars: int = 15):
        """Add animated-style music visualizer bars"""
        bar_width = width // bars
        rgb_color = self.hex_to_rgb(color)
        
        for i in range(bars):
            # Random heights for visualizer effect
            bar_height = random.randint(10, 40)
            bar_x = x + i * bar_width
            bar_y = y - bar_height
            
            # Gradient effect on bars
            alpha = int(255 * (1 - i / bars * 0.5))
            bar_color = (*rgb_color, alpha)
            
            draw.rectangle(
                [(bar_x, bar_y), (bar_x + bar_width - 2, y)],
                fill=bar_color
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
        
        # Add decorative line with gradient effect
        line_y = 620
        gradient_line_colors = generator.hex_to_rgb(accent_color)
        for i in range(5):
            alpha = int(255 * (1 - i / 5))
            line_color = (*gradient_line_colors, alpha)
            draw.line(
                [(60, line_y + i), (1220, line_y + i)],
                fill=line_color,
                width=2
            )
        
        # Add music visualizer
        generator.add_music_visualizer(draw, 60, 650, 200, accent_color)
        
        # Add modern control buttons
        controls_y = 650
        control_symbols = ["⏮", "⏯", "⏭", "🔀", "🔁"]
        control_spacing = 150
        start_x = 400
        
        for i, symbol in enumerate(control_symbols):
            x = start_x + i * control_spacing
            
            # Button background
            draw.ellipse(
                [(x - 25, controls_y - 25), (x + 25, controls_y + 25)],
                fill=(*generator.hex_to_rgb(accent_color), 40),
                outline=accent_color,
                width=2
            )
            
            # Center the symbol
            symbol_bbox = draw.textbbox((0, 0), symbol, font=control_font)
            symbol_width = symbol_bbox[2] - symbol_bbox[0]
            symbol_height = symbol_bbox[3] - symbol_bbox[1]
            symbol_x = x - symbol_width // 2
            symbol_y = controls_y - symbol_height // 2
            
            draw.text((symbol_x, symbol_y), symbol, fill="white", font=control_font)
        
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

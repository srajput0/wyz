

import os
import re
import random
import math
import numpy as np
from typing import Tuple, List

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from AnonXMusic import app
from config import YOUTUBE_IMG_URL


class UltraPremiumThumbnailGenerator:
    """Ultra-advanced thumbnail generator with premium visual effects"""
    
    def __init__(self):
        # Ultra-vibrant gradient combinations
        self.gradient_colors = [
            ["#FF006E", "#8338EC"],  # Magenta to Purple
            ["#00F5FF", "#FF1744"],  # Cyan to Red
            ["#FFDE59", "#FF6B35"],  # Yellow to Orange
            ["#00E676", "#00ACC1"],  # Green to Teal
            ["#E91E63", "#9C27B0"],  # Pink to Purple
            ["#FF5722", "#FF9800"],  # Red-Orange to Orange
            ["#3F51B5", "#E91E63"],  # Indigo to Pink
            ["#00BCD4", "#4CAF50"],  # Cyan to Green
            ["#FF4081", "#536DFE"],  # Pink to Blue
            ["#FFD600", "#FF5722"],  # Gold to Red-Orange
        ]
        
        # Neon control colors
        self.control_colors = [
            "#00FFFF",  # Cyan
            "#FF0080",  # Hot Pink
            "#00FF00",  # Lime
            "#FF8000",  # Orange
            "#8000FF",  # Violet
            "#FF004D",  # Red
            "#00FF80",  # Spring Green
            "#FF0040",  # Rose
        ]
        
        # Modern patterns for overlays
        self.pattern_styles = [
            "hexagonal", "dots", "waves", "geometric", "neural"
        ]
    
    def create_neural_pattern(self, width: int, height: int, intensity: float = 0.3) -> Image.Image:
        """Create modern neural network pattern overlay"""
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Create nodes
        nodes = [(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(25)]
        
        # Draw connections
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                distance = math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)
                if distance < 200:  # Only connect nearby nodes
                    alpha = int(100 * intensity * (1 - distance/200))
                    draw.line([node1, node2], fill=(255, 255, 255, alpha), width=2)
        
        # Draw nodes
        for node in nodes:
            draw.ellipse(
                [(node[0]-5, node[1]-5), (node[0]+5, node[1]+5)],
                fill=(255, 255, 255, int(200 * intensity))
            )
        
        return overlay
    
    def create_wave_pattern(self, width: int, height: int, color: str, intensity: float = 0.4) -> Image.Image:
        """Create flowing wave pattern"""
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        rgb_color = self.hex_to_rgb(color)
        
        # Multiple wave layers
        for wave in range(3):
            points = []
            amplitude = 50 + wave * 20
            frequency = 0.01 + wave * 0.005
            phase = wave * math.pi / 3
            
            for x in range(0, width + 10, 10):
                y = height // 2 + amplitude * math.sin(frequency * x + phase)
                points.append((x, y))
            
            # Close the wave shape
            points.extend([(width, height), (0, height)])
            
            alpha = int(intensity * 100 * (1 - wave * 0.3))
            draw.polygon(points, fill=(*rgb_color, alpha))
        
        return overlay
    
    def create_holographic_gradient(self, width: int, height: int, colors: List[str]) -> Image.Image:
        """Create holographic rainbow gradient effect"""
        base = Image.new('RGBA', (width, height))
        
        for y in range(height):
            for x in range(width):
                # Create holographic effect using multiple sine waves
                holo_factor = (
                    math.sin(x * 0.01) * 
                    math.cos(y * 0.008) * 
                    math.sin((x + y) * 0.005)
                )
                
                ratio = (x + y + holo_factor * 100) / (width + height)
                ratio = abs(ratio % 1.0)  # Keep in range and create repetition
                
                # Multi-color interpolation for holographic effect
                if ratio < 0.33:
                    # First third: color1 to color2
                    local_ratio = ratio * 3
                    color1 = self.hex_to_rgb(colors[0])
                    color2 = self.hex_to_rgb(colors[1])
                elif ratio < 0.66:
                    # Second third: color2 to rainbow
                    local_ratio = (ratio - 0.33) * 3
                    color1 = self.hex_to_rgb(colors[1])
                    color2 = self.hex_to_rgb("#00FFFF")  # Cyan accent
                else:
                    # Third: rainbow back to color1
                    local_ratio = (ratio - 0.66) * 3
                    color1 = self.hex_to_rgb("#00FFFF")
                    color2 = self.hex_to_rgb(colors[0])
                
                r = int(color1[0] * (1 - local_ratio) + color2[0] * local_ratio)
                g = int(color1[1] * (1 - local_ratio) + color2[1] * local_ratio)
                b = int(color1[2] * (1 - local_ratio) + color2[2] * local_ratio)
                
                base.putpixel((x, y), (r, g, b, 255))
        
        return base
    
    def create_3d_text_effect(self, draw: ImageDraw.Draw, text: str, x: int, y: int, 
                             font: ImageFont.ImageFont, main_color: str, depth: int = 6) -> None:
        """Create 3D text effect with depth and shadow"""
        rgb_color = self.hex_to_rgb(main_color)
        
        # Create depth layers (back to front)
        for d in range(depth, 0, -1):
            shadow_alpha = int(200 * (depth - d) / depth)
            shadow_color = (0, 0, 0, shadow_alpha)
            draw.text((x + d, y + d), text, fill=shadow_color, font=font)
        
        # Highlight layer (slightly offset up-left)
        highlight_color = (min(255, rgb_color[0] + 50), 
                          min(255, rgb_color[1] + 50), 
                          min(255, rgb_color[2] + 50))
        draw.text((x - 1, y - 1), text, fill=highlight_color, font=font)
        
        # Main text
        draw.text((x, y), text, fill=main_color, font=font)
    
    def create_neon_glow(self, image: Image.Image, x: int, y: int, width: int, height: int,
                        neon_color: str, intensity: float = 1.5) -> Image.Image:
        """Create intense neon glow effect"""
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        rgb_color = self.hex_to_rgb(neon_color)
        
        # Multiple neon layers with varying intensities
        for i in range(25, 0, -1):
            alpha = int(intensity * 40 * math.exp(-i/8))  # Exponential falloff
            glow_size = i * 3
            
            # Outer glow
            draw.rounded_rectangle(
                [(x - glow_size, y - glow_size), 
                 (x + width + glow_size, y + height + glow_size)],
                radius=35,
                fill=(*rgb_color, alpha)
            )
        
        # Inner bright core
        draw.rounded_rectangle(
            [(x - 5, y - 5), (x + width + 5, y + height + 5)],
            radius=15,
            fill=(*rgb_color, int(intensity * 100))
        )
        
        return Image.alpha_composite(image.convert('RGBA'), overlay)
    
    def create_advanced_control_ui(self, draw: ImageDraw.Draw, center_x: int, bottom_y: int,
                                 gradient_colors: List[str]) -> None:
        """Create ultra-modern control interface"""
        # Control panel background with glassmorphism
        panel_width = 500
        panel_height = 120
        panel_x = center_x - panel_width // 2
        panel_y = bottom_y - 150
        
        # Multi-layer glass effect
        for layer in range(8, 0, -1):
            alpha = int(30 * layer / 8)
            blur_size = layer * 2
            draw.rounded_rectangle(
                [(panel_x - blur_size, panel_y - blur_size), 
                 (panel_x + panel_width + blur_size, panel_y + panel_height + blur_size)],
                radius=25 + blur_size,
                fill=(255, 255, 255, alpha)
            )
        
        # Main glass panel
        draw.rounded_rectangle(
            [(panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height)],
            radius=25,
            fill=(0, 0, 0, 100),
            outline=gradient_colors[0],
            width=3
        )
        
        # Control buttons with advanced styling
        button_y = panel_y + 60
        buttons = [
            {"type": "previous", "x": panel_x + 80, "color": self.control_colors[0]},
            {"type": random.choice(["play", "pause"]), "x": panel_x + 180, "color": self.control_colors[1]},
            {"type": "next", "x": panel_x + 280, "color": self.control_colors[2]},
            {"type": "shuffle", "x": panel_x + 380, "color": self.control_colors[3]},
        ]
        
        for button in buttons:
            self.draw_ultra_control_button(
                draw, button["x"], button_y, 
                button["type"], button["color"], 35
            )
        
        # Ultra-modern progress bar
        progress_y = panel_y + 20
        progress_width = 400
        progress_x = center_x - progress_width // 2
        
        # Progress bar with neon effect
        draw.rounded_rectangle(
            [(progress_x, progress_y), (progress_x + progress_width, progress_y + 6)],
            radius=3,
            fill=(255, 255, 255, 40)
        )
        
        # Animated progress fill
        progress_percent = random.randint(25, 75)
        fill_width = int(progress_width * progress_percent / 100)
        
        # Neon progress fill
        for glow in range(6, 0, -1):
            glow_alpha = int(150 * glow / 6)
            glow_color = (*self.hex_to_rgb(gradient_colors[0]), glow_alpha)
            draw.rounded_rectangle(
                [(progress_x - glow, progress_y - glow), 
                 (progress_x + fill_width + glow, progress_y + 6 + glow)],
                radius=6,
                fill=glow_color
            )
        
        draw.rounded_rectangle(
            [(progress_x, progress_y), (progress_x + fill_width, progress_y + 6)],
            radius=3,
            fill=gradient_colors[0]
        )
        
        # Glowing progress handle
        handle_x = progress_x + fill_width
        for glow in range(8, 0, -1):
            alpha = int(200 * glow / 8)
            size = 12 + glow * 2
            draw.ellipse(
                [(handle_x - size, progress_y - size + 3), 
                 (handle_x + size, progress_y + size + 3)],
                fill=(255, 255, 255, alpha)
            )
        
        draw.ellipse(
            [(handle_x - 8, progress_y - 5), (handle_x + 8, progress_y + 11)],
            fill="white"
        )
    
    def draw_ultra_control_button(self, draw: ImageDraw.Draw, x: int, y: int, 
                                 button_type: str, color: str, size: int = 35):
        """Draw ultra-modern control buttons with advanced effects"""
        rgb_color = self.hex_to_rgb(color)
        
        # Ultra-bright neon glow
        for glow_layer in range(15, 0, -1):
            glow_alpha = int(200 * math.exp(-glow_layer/5))
            glow_size = size + glow_layer * 4
            
            draw.ellipse(
                [(x - glow_size, y - glow_size), (x + glow_size, y + glow_size)],
                fill=(*rgb_color, glow_alpha)
            )
        
        # Button base with gradient effect
        draw.ellipse(
            [(x - size, y - size), (x + size, y + size)],
            fill=color
        )
        
        # Inner glow ring
        draw.ellipse(
            [(x - size + 3, y - size + 3), (x + size - 3, y + size - 3)],
            outline=(255, 255, 255, 180),
            width=3
        )
        
        # Ultra-bright center highlight
        draw.ellipse(
            [(x - size + 8, y - size + 8), (x + size - 8, y + size - 8)],
            outline=(255, 255, 255, 100),
            width=2
        )
        
        # Enhanced button symbols
        symbol_color = "white"
        line_width = 5
        
        if button_type == "previous":
            # Enhanced previous symbol
            draw.rectangle([(x - 15, y - 18), (x - 8, y + 18)], fill=symbol_color)
            points = [(x - 5, y), (x + 15, y - 15), (x + 15, y + 15)]
            draw.polygon(points, fill=symbol_color)
            
        elif button_type == "play":
            # Enhanced play symbol
            points = [(x - 12, y - 18), (x - 12, y + 18), (x + 18, y)]
            draw.polygon(points, fill=symbol_color)
            
        elif button_type == "pause":
            # Enhanced pause symbol
            draw.rounded_rectangle([(x - 12, y - 18), (x - 2, y + 18)], radius=2, fill=symbol_color)
            draw.rounded_rectangle([(x + 2, y - 18), (x + 12, y + 18)], radius=2, fill=symbol_color)
            
        elif button_type == "next":
            # Enhanced next symbol
            points = [(x - 15, y), (x + 5, y - 15), (x + 5, y + 15)]
            draw.polygon(points, fill=symbol_color)
            draw.rectangle([(x + 8, y - 18), (x + 15, y + 18)], fill=symbol_color)
            
        elif button_type == "shuffle":
            # Enhanced shuffle with modern arrows
            draw.line([(x - 15, y - 8), (x + 15, y + 8)], fill=symbol_color, width=line_width)
            draw.line([(x - 15, y + 8), (x + 15, y - 8)], fill=symbol_color, width=line_width)
            # Modern arrow heads
            draw.polygon([(x + 15, y + 8), (x + 8, y + 3), (x + 8, y + 13)], fill=symbol_color)
            draw.polygon([(x - 15, y - 8), (x - 8, y - 3), (x - 8, y - 13)], fill=symbol_color)
            
        elif button_type == "repeat":
            # Enhanced repeat with glow
            draw.arc([(x - 15, y - 15), (x + 15, y + 15)], start=30, end=330, 
                    fill=symbol_color, width=line_width)
            draw.polygon([(x + 10, y - 12), (x + 18, y - 4), (x + 2, y - 4)], fill=symbol_color)
    
    def create_advanced_gradient(self, width: int, height: int, colors: List[str], 
                               direction: str = "holographic") -> Image.Image:
        """Create ultra-advanced gradient with multiple effects"""
        if direction == "holographic":
            return self.create_holographic_gradient(width, height, colors)
        
        base = Image.new('RGBA', (width, height))
        
        for y in range(height):
            for x in range(width):
                if direction == "spiral":
                    center_x, center_y = width // 2, height // 2
                    angle = math.atan2(y - center_y, x - center_x)
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = (angle + distance * 0.01) % (2 * math.pi) / (2 * math.pi)
                elif direction == "diamond":
                    ratio = (abs(x - width//2) + abs(y - height//2)) / (width//2 + height//2)
                elif direction == "wave":
                    wave_factor = math.sin(x * 0.01) * math.cos(y * 0.008)
                    ratio = (x + y + wave_factor * 100) / (width + height)
                else:
                    ratio = (x + y) / (width + height)
                
                ratio = min(max(ratio, 0), 1)
                color1 = self.hex_to_rgb(colors[0])
                color2 = self.hex_to_rgb(colors[1])
                
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                base.putpixel((x, y), (r, g, b, 255))
        
        return base
    
    def add_particle_effects(self, image: Image.Image, count: int = 50) -> Image.Image:
        """Add floating particle effects"""
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        for _ in range(count):
            x = random.randint(0, image.size[0])
            y = random.randint(0, image.size[1])
            size = random.randint(2, 8)
            alpha = random.randint(100, 255)
            color_choice = random.choice(self.control_colors)
            rgb = self.hex_to_rgb(color_choice)
            
            # Particle glow
            for glow in range(size * 2, 0, -1):
                glow_alpha = int(alpha * glow / (size * 2) * 0.3)
                draw.ellipse(
                    [(x - glow, y - glow), (x + glow, y + glow)],
                    fill=(*rgb, glow_alpha)
                )
            
            # Particle core
            draw.ellipse(
                [(x - size, y - size), (x + size, y + size)],
                fill=(*rgb, alpha)
            )
        
        return Image.alpha_composite(image.convert('RGBA'), overlay)
    
    def create_modern_title_card(self, draw: ImageDraw.Draw, title: str, x: int, y: int,
                                width: int, height: int, gradient_colors: List[str]) -> None:
        """Create modern title card with advanced effects"""
        # Glass morphism background
        for blur in range(12, 0, -1):
            alpha = int(40 * blur / 12)
            draw.rounded_rectangle(
                [(x - blur, y - blur), (x + width + blur, y + height + blur)],
                radius=25 + blur,
                fill=(0, 0, 0, alpha)
            )
        
        # Main title card
        draw.rounded_rectangle(
            [(x, y), (x + width, y + height)],
            radius=25,
            fill=(0, 0, 0, 150),
            outline=gradient_colors[0],
            width=4
        )
        
        # Inner border glow
        draw.rounded_rectangle(
            [(x + 5, y + 5), (x + width - 5, y + height - 5)],
            radius=20,
            outline=gradient_colors[1],
            width=2
        )
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def changeImageSize(maxWidth: int, maxHeight: int, image: Image.Image) -> Image.Image:
    """Resize image maintaining aspect ratio with ultra-high quality"""
    ratio = min(maxWidth / image.size[0], maxHeight / image.size[1])
    newWidth = int(ratio * image.size[0])
    newHeight = int(ratio * image.size[1])
    # Use best resampling for highest quality
    return image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)


def clear(text: str, max_length: int = 45) -> str:
    """Clean and truncate text with smart word breaking"""
    # Remove special characters but keep essential ones
    text = re.sub(r'[^\w\s\-\&\.]', ' ', text)
    words = text.split()
    result = ""
    for word in words:
        if len(result + " " + word) <= max_length:
            result += " " + word if result else word
        else:
            break
    return result.strip()


async def get_thumb(videoid: str) -> str:
    """Generate ultra-premium advanced thumbnail"""
    cache_path = f"cache/{videoid}.png"
    
    if os.path.isfile(cache_path):
        return cache_path

    generator = UltraPremiumThumbnailGenerator()
    url = f"https://www.youtube.com/watch?v={videoid}"
    
    try:
        # Get video information
        results = VideosSearch(url, limit=1)
        video_data = (await results.next())["result"][0]
        
        title = video_data.get("title", "Unknown Title")
        title = re.sub(r'[^\w\s\-]', ' ', title).title()
        
        duration = video_data.get("duration", "Unknown")
        thumbnail_url = video_data.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
        views = video_data.get("viewCount", {}).get("short", "Unknown Views")
        channel = video_data.get("channel", {}).get("name", "Unknown Channel")
        
        # Download original thumbnail
        temp_thumb = f"cache/temp_{videoid}.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(temp_thumb, mode="wb") as f:
                        await f.write(await resp.read())
        
        # Create ultra-high quality canvas
        canvas = Image.new('RGBA', (1280, 720), (0, 0, 0, 255))
        
        # Load and process original thumbnail
        youtube_thumb = Image.open(temp_thumb)
        
        # Select random gradient style
        gradient_colors = random.choice(generator.gradient_colors)
        gradient_type = random.choice(["holographic", "spiral", "wave", "diamond"])
        
        # Create premium background
        gradient_bg = generator.create_advanced_gradient(
            1280, 720, gradient_colors, gradient_type
        )
        
        # Advanced thumbnail processing
        thumb_resized = changeImageSize(1280, 720, youtube_thumb)
        
        # Apply premium image effects
        thumb_enhanced = ImageEnhance.Brightness(thumb_resized).enhance(0.6)
        thumb_enhanced = ImageEnhance.Contrast(thumb_enhanced).enhance(1.4)
        thumb_enhanced = ImageEnhance.Color(thumb_enhanced).enhance(1.3)
        
        # Create artistic blend
        blended = Image.blend(gradient_bg.convert('RGB'), thumb_enhanced, 0.7)
        canvas = blended.convert('RGBA')
        
        # Add pattern overlay
        pattern_type = random.choice(generator.pattern_styles)
        if pattern_type == "neural":
            neural_overlay = generator.create_neural_pattern(1280, 720, 0.4)
            canvas = Image.alpha_composite(canvas, neural_overlay)
        elif pattern_type == "waves":
            wave_overlay = generator.create_wave_pattern(1280, 720, gradient_colors[0], 0.3)
            canvas = Image.alpha_composite(canvas, wave_overlay)
        
        # Add floating particles
        canvas = generator.add_particle_effects(canvas, 60)
        
        # Ultra-neon glow for title area
        canvas = generator.create_neon_glow(
            canvas, 50, 80, 1180, 250, gradient_colors[1], 2.0
        )
        
        draw = ImageDraw.Draw(canvas)
        
        # Load premium fonts with better fallbacks
        try:
            app_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 45)
            title_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 85)
            subtitle_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 48)
            info_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 35)
            small_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 28)
        except:
            # High-quality fallbacks
            from PIL import ImageFont
            try:
                app_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 45)
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 85)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 48)
                info_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 35)
                small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 28)
            except:
                app_font = ImageFont.load_default()
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                info_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
        
        # Ultra-modern title card
        title_card_width = 1200
        title_card_height = 300
        title_card_x = 40
        title_card_y = 50
        
        generator.create_modern_title_card(
            draw, title, title_card_x, title_card_y, 
            title_card_width, title_card_height, gradient_colors
        )
        
        # App branding with 3D effect
        app_name = unidecode(app.name).upper()
        generator.create_3d_text_effect(
            draw, app_name, 80, 80, app_font, "#FFD700", 8
        )
        
        # HD/Full Video badge (top right)
        badge_texts = ["HD FULL VIDEO", "PREMIUM QUALITY", "4K VIDEO"]
        badge_text = random.choice(badge_texts)
        
        bbox = draw.textbbox((0, 0), badge_text, font=small_font)
        badge_width = bbox[2] - bbox[0] + 30
        badge_height = bbox[3] - bbox[1] + 20
        badge_x = 1280 - badge_width - 30
        badge_y = 30
        
        # Ultra-bright badge with neon effect
        for glow in range(10, 0, -1):
            glow_alpha = int(150 * glow / 10)
            glow_color = (*generator.hex_to_rgb("#00FFFF"), glow_alpha)
            draw.rounded_rectangle(
                [(badge_x - glow, badge_y - glow), 
                 (badge_x + badge_width + glow, badge_y + badge_height + glow)],
                radius=15,
                fill=glow_color
            )
        
        draw.rounded_rectangle(
            [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
            radius=12,
            fill=(0, 0, 0, 200),
            outline="#00FFFF",
            width=3
        )
        
        draw.text(
            (badge_x + 15, badge_y + 10), 
            badge_text, 
            fill="#00FFFF", 
            font=small_font
        )
        
        # Main title with ultra-premium 3D effect
        clean_title = clear(title, 30)
        title_lines = []
        words = clean_title.split()
        current_line = ""
        
        # Smart line breaking for title
        for word in words:
            if len(current_line + " " + word) <= 12:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    title_lines.append(current_line)
                current_line = word
        
        if current_line:
            title_lines.append(current_line)
        
        # Draw title with ultra-premium 3D effect
        title_start_y = 150
        
        for i, line in enumerate(title_lines[:2]):  # Max 2 lines for readability
            line_y = title_start_y + i * 95
            
            # Ultra-3D effect with multiple shadows and highlights
            generator.create_3d_text_effect(
                draw, line, 80, line_y, title_font, "#FFFFFF", 12
            )
        
        # Duration badge (bottom right corner)
        if duration and duration != "Unknown":
            duration_text = f"⏱ {duration}"
            duration_bbox = draw.textbbox((0, 0), duration_text, font=info_font)
            duration_width = duration_bbox[2] - duration_bbox[0] + 25
            duration_height = duration_bbox[3] - duration_bbox[1] + 15
            
            duration_x = 1280 - duration_width - 25
            duration_y = 720 - duration_height - 25
            
            # Neon duration badge
            neon_color = random.choice(generator.control_colors)
            for glow in range(8, 0, -1):
                glow_alpha = int(120 * glow / 8)
                glow_rgb = generator.hex_to_rgb(neon_color)
                draw.rounded_rectangle(
                    [(duration_x - glow, duration_y - glow), 
                     (duration_x + duration_width + glow, duration_y + duration_height + glow)],
                    radius=18,
                    fill=(*glow_rgb, glow_alpha)
                )
            
            draw.rounded_rectangle(
                [(duration_x, duration_y), (duration_x + duration_width, duration_y + duration_height)],
                radius=15,
                fill=(0, 0, 0, 180),
                outline=neon_color,
                width=3
            )
            
            draw.text(
                (duration_x + 12, duration_y + 7), 
                duration_text, 
                fill=neon_color, 
                font=info_font
            )
        
        # Channel info with modern styling (bottom left)
        channel_y = 720 - 180
        channel_card_width = 600
        channel_card_height = 80
        
        # Channel card background
        generator.create_modern_title_card(
            draw, "", 40, channel_y, channel_card_width, channel_card_height, gradient_colors
        )
        
        # Channel text with glow
        channel_info = f"🎵 {channel}"
        views_info = f"👁 {views}"
        
        for glow in range(3, 0, -1):
            glow_alpha = int(100 * glow / 3)
            draw.text((60 + glow, channel_y + 15 + glow), channel_info, 
                     fill=(255, 255, 255, glow_alpha), font=info_font)
        
        draw.text((60, channel_y + 15), channel_info, fill="#FFFFFF", font=info_font)
        draw.text((60, channel_y + 50), views_info, fill="#CCCCCC", font=small_font)
        
        # Ultra-modern control interface
        generator.create_advanced_control_ui(draw, 640, 720, gradient_colors)
        
        # Add "NOW PLAYING" indicator
        now_playing_y = 400
        now_playing_text = "♪ NOW PLAYING ♪"
        
        # Animated-style glow for "NOW PLAYING"
        for glow in range(15, 0, -1):
            glow_alpha = int(200 * math.sin(glow * 0.2) * 0.3)
            glow_color = (*generator.hex_to_rgb(gradient_colors[0]), glow_alpha)
            draw.text((640 - 150 + glow, now_playing_y + glow), now_playing_text, 
                     fill=glow_color, font=subtitle_font)
        
        draw.text((640 - 150, now_playing_y), now_playing_text, fill="#FFFFFF", font=subtitle_font)
        
        # Add subtle scan lines for retro-futuristic effect
        for y in range(0, 720, 4):
            alpha = 15
            draw.line([(0, y), (1280, y)], fill=(255, 255, 255, alpha), width=1)
        
        # Add corner accents
        accent_color = random.choice(generator.control_colors)
        accent_rgb = generator.hex_to_rgb(accent_color)
        
        # Top-left accent
        for glow in range(20, 0, -1):
            alpha = int(100 * glow / 20)
            draw.polygon([(0, 0), (100, 0), (0, 100)], fill=(*accent_rgb, alpha))
        
        # Bottom-right accent  
        for glow in range(20, 0, -1):
            alpha = int(100 * glow / 20)
            draw.polygon([(1280, 720), (1180, 720), (1280, 620)], fill=(*accent_rgb, alpha))
        
        # Equalizer visualization (left side)
        eq_x = 50
        eq_y = 300
        bar_width = 8
        bar_spacing = 12
        max_height = 100
        
        for i in range(15):  # 15 equalizer bars
            bar_x = eq_x + i * (bar_width + bar_spacing)
            bar_height = random.randint(20, max_height)
            
            # Neon equalizer bars
            bar_color = random.choice(generator.control_colors)
            bar_rgb = generator.hex_to_rgb(bar_color)
            
            # Bar glow
            for glow in range(6, 0, -1):
                glow_alpha = int(150 * glow / 6)
                draw.rectangle(
                    [(bar_x - glow, eq_y + max_height - bar_height - glow), 
                     (bar_x + bar_width + glow, eq_y + max_height + glow)],
                    fill=(*bar_rgb, glow_alpha)
                )
            
            # Main bar
            draw.rounded_rectangle(
                [(bar_x, eq_y + max_height - bar_height), 
                 (bar_x + bar_width, eq_y + max_height)],
                radius=4,
                fill=bar_color
            )
            
            # Bar highlight
            draw.rounded_rectangle(
                [(bar_x + 1, eq_y + max_height - bar_height + 1), 
                 (bar_x + bar_width - 1, eq_y + max_height - 1)],
                radius=3,
                outline=(255, 255, 255, 100),
                width=1
            )
        
        # Add music note particles
        music_notes = ["♪", "♫", "♬", "♩"]
        for _ in range(20):
            note_x = random.randint(100, 1180)
            note_y = random.randint(100, 600)
            note = random.choice(music_notes)
            note_color = random.choice(generator.control_colors)
            note_size = random.randint(20, 40)
            
            try:
                note_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", note_size)
            except:
                note_font = ImageFont.load_default()
            
            # Note glow
            note_rgb = generator.hex_to_rgb(note_color)
            for glow in range(8, 0, -1):
                glow_alpha = int(120 * glow / 8 * 0.4)
                draw.text((note_x + glow, note_y + glow), note, 
                         fill=(*note_rgb, glow_alpha), font=note_font)
            
            draw.text((note_x, note_y), note, fill=note_color, font=note_font)
        
        # Premium waveform visualization (top)
        wave_y = 20
        wave_points = []
        for x in range(0, 1280, 10):
            amplitude = 30 + 20 * math.sin(x * 0.02)
            y = wave_y + amplitude * math.sin(x * 0.01)
            wave_points.append((x, y))
        
        # Draw waveform with glow
        for i in range(len(wave_points) - 1):
            glow_color = (*generator.hex_to_rgb(gradient_colors[0]), 100)
            for thickness in range(8, 0, -1):
                alpha = int(150 * thickness / 8 * 0.3)
                draw.line([wave_points[i], wave_points[i+1]], 
                         fill=(*generator.hex_to_rgb(gradient_colors[0]), alpha), 
                         width=thickness)
            
            draw.line([wave_points[i], wave_points[i+1]], 
                     fill=gradient_colors[0], width=3)
        
        # Artist/Song info panel (center-right)
        info_panel_x = 700
        info_panel_y = 400
        info_panel_width = 500
        info_panel_height = 120
        
        generator.create_modern_title_card(
            draw, "", info_panel_x, info_panel_y, 
            info_panel_width, info_panel_height, gradient_colors
        )
        
        # Song title in info panel
        song_title = clear(title, 35)
        generator.create_3d_text_effect(
            draw, song_title, info_panel_x + 25, info_panel_y + 25, 
            subtitle_font, "#FFFFFF", 6
        )
        
        # Channel name in info panel
        artist_text = f"by {channel}"
        draw.text((info_panel_x + 25, info_panel_y + 80), artist_text, 
                 fill="#CCCCCC", font=info_font)
        
        # Ultra-bright status indicators
        status_indicators = [
            {"text": "🔥 TRENDING", "color": "#FF4500", "x": 80},
            {"text": "⚡ LIVE", "color": "#FF0080", "x": 250}, 
            {"text": "🎧 HD AUDIO", "color": "#00FF80", "x": 380},
        ]
        
        indicator_y = 500
        for indicator in status_indicators:
            indicator_rgb = generator.hex_to_rgb(indicator["color"])
            
            # Status indicator glow
            for glow in range(6, 0, -1):
                glow_alpha = int(150 * glow / 6)
                draw.text((indicator["x"] + glow, indicator_y + glow), indicator["text"], 
                         fill=(*indicator_rgb, glow_alpha), font=small_font)
            
            draw.text((indicator["x"], indicator_y), indicator["text"], 
                     fill=indicator["color"], font=small_font)
        
        # Clean up temporary files
        try:
            os.remove(temp_thumb)
        except:
            pass
        
        # Apply final image enhancements
        final_image = canvas.convert('RGB')
        
        # Slight sharpening for crisp details
        final_image = final_image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        # Enhance overall vibrancy
        final_image = ImageEnhance.Color(final_image).enhance(1.2)
        final_image = ImageEnhance.Contrast(final_image).enhance(1.1)
        
        # Save with maximum quality
        final_image.save(cache_path, optimize=True, quality=100, dpi=(300, 300))
        
        return cache_path
        
    except Exception as e:
        print(f"Ultra thumbnail generation error: {e}")
        # Fallback: create a basic premium thumbnail
        try:
            return await create_fallback_premium_thumb(videoid, generator)
        except:
            return YOUTUBE_IMG_URL


async def create_fallback_premium_thumb(videoid: str, generator) -> str:
    """Create fallback premium thumbnail when main generation fails"""
    cache_path = f"cache/fallback_{videoid}.png"
    
    # Create basic premium canvas
    canvas = Image.new('RGB', (1280, 720))
    gradient_colors = random.choice(generator.gradient_colors)
    
    # Simple gradient background
    gradient_bg = generator.create_advanced_gradient(1280, 720, gradient_colors, "diagonal")
    canvas = gradient_bg.convert('RGB')
    
    draw = ImageDraw.Draw(canvas)
    
    # Basic premium styling
    try:
        title_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 80)
        app_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 50)
    except:
        title_font = ImageFont.load_default()
        app_font = ImageFont.load_default()
    
    # Draw fallback content
    app_name = unidecode(app.name)
    draw.text((60, 60), app_name, fill="#FFD700", font=app_font)
    draw.text((60, 300), "PREMIUM MUSIC", fill="white", font=title_font)
    draw.text((60, 400), "HIGH QUALITY AUDIO", fill="#CCCCCC", font=app_font)
    
    # Basic control buttons
    center_x = 640
    controls_y = 600
    colors = generator.control_colors[:5]
    
    for i, color in enumerate(colors):
        x_pos = center_x + (i - 2) * 100
        generator.draw_ultra_control_button(draw, x_pos, controls_y, "play", color, 25)
    
    canvas.save(cache_path, optimize=True, quality=95)
    return cache_path


# Additional utility functions for premium effects
def create_sparkle_overlay(image: Image.Image, count: int = 30) -> Image.Image:
    """Add sparkle effects to the image"""
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    sparkle_colors = ["#FFFFFF", "#FFD700", "#00FFFF", "#FF0080", "#00FF00"]
    
    for _ in range(count):
        x = random.randint(50, image.size[0] - 50)
        y = random.randint(50, image.size[1] - 50)
        size = random.randint(3, 12)
        color = random.choice(sparkle_colors)
        alpha = random.randint(150, 255)
        
        # Four-pointed star sparkle
        points = [
            (x, y - size),      # Top
            (x + size//2, y - size//2),  # Top-right
            (x + size, y),      # Right
            (x + size//2, y + size//2),  # Bottom-right
            (x, y + size),      # Bottom
            (x - size//2, y + size//2),  # Bottom-left
            (x - size, y),      # Left
            (x - size//2, y - size//2),  # Top-left
        ]
        
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        draw.polygon(points, fill=(*rgb, alpha))
    
    return Image.alpha_composite(image.convert('RGBA'), overlay)


def add_premium_watermark(image: Image.Image, app_name: str, position: str = "bottom_right") -> Image.Image:
    """Add subtle premium watermark"""
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        watermark_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 24)
    except:
        watermark_font = ImageFont.load_default()
    
    watermark_text = f"© {app_name} Premium"
    bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if position == "bottom_right":
        x = image.size[0] - text_width - 30
        y = image.size[1] - text_height - 20
    else:  # bottom_left
        x = 30
        y = image.size[1] - text_height - 20
    
    # Subtle glow
    for glow in range(3, 0, -1):
        draw.text((x + glow, y + glow), watermark_text, 
                 fill=(0, 0, 0, 100), font=watermark_font)
    
    draw.text((x, y), watermark_text, fill=(255, 255, 255, 120), font=watermark_font)
    
    return Image.alpha_composite(image.convert('RGBA'), overlay)


# Export the main function
__all__ = ['get_thumb', 'changeImageSize', 'clear']

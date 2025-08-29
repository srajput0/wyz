

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
        
        # New: Player control icon paths (replace with actual paths or generate them)
        self.icon_paths = {
            "play": "AnonXMusic/assets/play_icon.png", # Placeholder
            "pause": "AnonXMusic/assets/pause_icon.png", # Placeholder
            "next": "AnonXMusic/assets/next_icon.png", # Placeholder
            "previous": "AnonXMusic/assets/prev_icon.png", # Placeholder
            "shuffle": "AnonXMusic/assets/shuffle_icon.png", # Placeholder
            "repeat": "AnonXMusic/assets/repeat_icon.png", # Placeholder
            "volume_up": "AnonXMusic/assets/volume_up_icon.png", # Placeholder
            "volume_down": "AnonXMusic/assets/volume_down_icon.png", # Placeholder
            "volume_mute": "AnonXMusic/assets/volume_mute_icon.png", # Placeholder
            "youtube": "AnonXMusic/assets/youtube_logo.png" # Placeholder
        }
    
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
                    math.sin(x * 0.01) * math.cos(y * 0.008) * math.sin((x + y) * 0.005)
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
        """Create ultra-modern control interface (This will be replaced by the new player card)"""
        pass # This function will be mostly replaced by the new player card design
    
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

    # --- NEW FUNCTIONS FOR PLAYER CARD ---

    def create_glassmorphism_card(self, canvas: Image.Image, x: int, y: int, width: int, height: int, radius: int = 40, blur_radius: int = 30, bg_alpha: int = 150, border_color: str = "#FFFFFF", border_width: int = 3) -> Image.Image:
        """Creates a glassmorphism effect card on the canvas."""
        
        # 1. Create a blurred version of the background section
        bg_section = canvas.crop((x - blur_radius, y - blur_radius, x + width + blur_radius, y + height + blur_radius))
        bg_section = bg_section.filter(ImageFilter.GaussianBlur(blur_radius))
        
        # 2. Create a transparent overlay for the card shape
        card_overlay = Image.new('RGBA', (width + 2 * blur_radius, height + 2 * blur_radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card_overlay)
        draw.rounded_rectangle([(blur_radius, blur_radius), (width + blur_radius, height + blur_radius)], 
                               radius=radius, fill=(255, 255, 255, bg_alpha)) # White with alpha
        
        # 3. Composite the blurred background with the card overlay
        final_card_region = Image.alpha_composite(bg_section, card_overlay)
        
        # 4. Create the border and inner shadow/highlight effect on a new transparent layer
        border_layer = Image.new('RGBA', (width + 2 * blur_radius, height + 2 * blur_radius), (0, 0, 0, 0))
        draw_border = ImageDraw.Draw(border_layer)
        
        # Outer border
        draw_border.rounded_rectangle([(blur_radius, blur_radius), (width + blur_radius, height + blur_radius)], 
                                      radius=radius, outline=border_color, width=border_width)
        
        # Inner highlight for glass effect
        draw_border.rounded_rectangle([(blur_radius + border_width, blur_radius + border_width), 
                                       (width + blur_radius - border_width, height + blur_radius - border_width)], 
                                      radius=radius - border_width, outline=(255, 255, 255, 80), width=1)

        # Drop shadow (optional, can be done with a separate blurred dark shape)
        shadow_offset = 10
        shadow_alpha = 70
        shadow_blur = 15
        shadow_layer = Image.new('RGBA', canvas.size, (0,0,0,0))
        draw_shadow = ImageDraw.Draw(shadow_layer)
        draw_shadow.rounded_rectangle(
            [(x + shadow_offset, y + shadow_offset), 
             (x + width + shadow_offset, y + height + shadow_offset)],
            radius=radius, fill=(0,0,0,shadow_alpha)
        )
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))
        
        # Composite shadow first onto canvas
        canvas = Image.alpha_composite(canvas, shadow_layer)

        # Paste the final card region back onto the canvas
        canvas.paste(final_card_region, (x - blur_radius, y - blur_radius), final_card_region)
        canvas.paste(border_layer, (x - blur_radius, y - blur_radius), border_layer) # Paste border last
        
        return canvas

    def draw_player_icon(self, draw: ImageDraw.Draw, icon_type: str, x: int, y: int, size: int, color: str = "#FFFFFF", glow_color: str = None) -> None:
        """Draws player control icons with an optional subtle glow."""
        
        # Fallback to default if glow_color is not provided
        if glow_color is None:
            glow_color = color 
        
        rgb_color = self.hex_to_rgb(color)
        rgb_glow = self.hex_to_rgb(glow_color)

        # Load icon image
        icon_path = self.icon_paths.get(icon_type)
        if icon_path and os.path.exists(icon_path):
            try:
                icon_img = Image.open(icon_path).convert("RGBA")
                icon_img = icon_img.resize((size, size), Image.Resampling.LANCZOS)
                
                # Apply color tint if the icon is grayscale/white
                # Create a solid color image and use it as a mask
                color_layer = Image.new("RGBA", icon_img.size, (*rgb_color, 255))
                icon_img = Image.alpha_composite(Image.new("RGBA", icon_img.size, (0,0,0,0)), Image.composite(color_layer, icon_img, icon_img))
                
                # Create a separate glow layer for the icon
                icon_glow_layer = Image.new("RGBA", icon_img.size, (0,0,0,0))
                draw_icon_glow = ImageDraw.Draw(icon_glow_layer)
                
                # Draw a slightly larger, blurred version of the icon in glow color
                # This is a simplified way; more accurate would be to use the icon's alpha channel
                draw_icon_glow.ellipse([(0,0), (size,size)], fill=(*rgb_glow, 100)) # Placeholder glow shape
                
                # Paste the glow onto the icon_img (or draw directly on main canvas for more control)
                # For simplicity here, we'll draw directly on the main canvas
                
                return icon_img # Return the image to be composited
            except Exception as e:
                print(f"Could not load/process icon {icon_type}: {e}")
                # Fallback to drawing basic shapes if image fails
        
        # Fallback shapes if icon image is not found or fails to load
        # Draw a circle as the button background
        draw.ellipse([(x - size // 2, y - size // 2), (x + size // 2, y + size // 2)], fill=(*rgb_color, 150))
        
        # Draw the symbol directly
        if icon_type == "play":
            points = [(x - size // 4, y - size // 3), (x - size // 4, y + size // 3), (x + size // 3, y)]
            draw.polygon(points, fill=color)
        elif icon_type == "pause":
            draw.rectangle([(x - size // 4, y - size // 3), (x - size // 10, y + size // 3)], fill=color)
            draw.rectangle([(x + size // 10, y - size // 3), (x + size // 4, y + size // 3)], fill=color)
        elif icon_type == "next":
            draw.polygon([(x + size // 10, y - size // 3), (x + size // 10, y + size // 3), (x + size // 3, y)], fill=color)
            draw.rectangle([(x + size // 4, y - size // 3), (x + size // 2, y + size // 3)], fill=color)
        elif icon_type == "previous":
            draw.polygon([(x - size // 10, y - size // 3), (x - size // 10, y + size // 3), (x - size // 3, y)], fill=color)
            draw.rectangle([(x - size // 4, y - size // 3), (x - size // 2, y + size // 3)], fill=color)
        elif icon_type == "shuffle":
            # Simplified shuffle icon
            draw.line([(x - size // 3, y - size // 6), (x + size // 3, y + size // 6)], fill=color, width=2)
            draw.line([(x - size // 3, y + size // 6), (x + size // 3, y - size // 6)], fill=color, width=2)
        elif icon_type == "repeat":
             draw.arc([(x - size // 3, y - size // 3), (x + size // 3, y + size // 3)], 0, 270, fill=color, width=2)
        elif icon_type == "youtube":
            # Simple YouTube play button style
            draw.rounded_rectangle([(x - size//2 + 5, y - size//4), (x + size//2 - 5, y + size//4)], radius=5, fill="red")
            draw.polygon([(x - size//4, y - size//6), (x - size//4, y + size//6), (x + size//6, y)], fill="white")


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
    """Generate ultra-premium advanced thumbnail with Now Playing card"""
    cache_path = f"cache/{videoid}.png"
    
    if os.path.isfile(cache_path):
        return cache_path

    generator = UltraPremiumThumbnailGenerator()
    
    # Use a dummy video data for testing if no actual video is found
    # In a real scenario, you'd want to handle the case where video_data is None
    video_data = {
        "title": "Guzarish Ghajini Aamir Khan Asin",
        "duration": "5:07",
        "thumbnails": [{"url": "https://i.ytimg.com/vi/lG5y7rG9L3Y/hqdefault.jpg"}],
        "viewCount": {"short": "113M views"},
        "channel": {"name": "T-Series"},
    }

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(videoid, limit=1) # Use videoid directly for search
        search_result = (await results.next())["result"]
        if search_result:
            video_data = search_result[0] # Overwrite with actual data if found
        else:
            print(f"Warning: No video data found for videoid {videoid}, using dummy data.")

        title = video_data.get("title", "Unknown Title")
        title = re.sub(r'[^\w\s\-]', ' ', title).title()
        
        duration = video_data.get("duration", "0:00")
        thumbnail_url = video_data.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
        views = video_data.get("viewCount", {}).get("short", "0 views")
        channel = video_data.get("channel", {}).get("name", "Unknown Channel")
        
        # Download original thumbnail
        temp_thumb = f"cache/temp_{videoid}.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(temp_thumb, mode="wb") as f:
                        await f.write(await resp.read())
                else:
                    print(f"Error downloading thumbnail: {resp.status}")
                    # Fallback to a default image if download fails
                    youtube_thumb = Image.open(YOUTUBE_IMG_URL)
        
        # Create ultra-high quality canvas (base background)
        canvas = Image.new('RGBA', (1280, 720), (0, 0, 0, 255))
        
        # Load and process original thumbnail for the main background (behind the card)
        try:
            youtube_thumb_bg = Image.open(temp_thumb).convert("RGBA")
        except:
            youtube_thumb_bg = Image.open(YOUTUBE_IMG_URL).convert("RGBA") # Fallback
        
        # Resize to fit background and apply blur/darken
        youtube_thumb_bg = changeImageSize(1280, 720, youtube_thumb_bg)
        youtube_thumb_bg = ImageEnhance.Brightness(youtube_thumb_bg).enhance(0.5) # Darken
        youtube_thumb_bg = ImageEnhance.Contrast(youtube_thumb_bg).enhance(1.2) # Enhance contrast
        youtube_thumb_bg = youtube_thumb_bg.filter(ImageFilter.GaussianBlur(30)) # Blur heavily
        canvas.paste(youtube_thumb_bg, (0,0), youtube_thumb_bg)
        
        # Select random gradient style for subtle overlay
        gradient_colors = random.choice(generator.gradient_colors)
        gradient_bg_overlay = generator.create_advanced_gradient(
            1280, 720, gradient_colors, random.choice(["diagonal", "holographic"])
        )
        canvas = Image.alpha_composite(canvas, Image.blend(Image.new('RGBA', (1280, 720), (0,0,0,0)), gradient_bg_overlay, 0.2)) # Subtle blend
        
        draw = ImageDraw.Draw(canvas)
        
        # --- PLAYER CARD START ---
        
        card_width = 800
        card_height = 500
        card_x = (1280 - card_width) // 2
        card_y = (720 - card_height) // 2
        card_radius = 40
        
        # Create glassmorphism card as the main player interface
        canvas = generator.create_glassmorphism_card(canvas, card_x, card_y, card_width, card_height, card_radius, blur_radius=40, bg_alpha=120, border_color="#FFFFFF", border_width=2)
        
        # --- Content inside the player card ---
        
        # Load original video thumbnail for inside the card
        try:
            player_thumb = Image.open(temp_thumb).convert("RGBA")
        except:
            player_thumb = Image.open(YOUTUBE_IMG_URL).convert("RGBA") # Fallback

        player_thumb_width = 700
        player_thumb_height = 300 # This will be adjusted to maintain aspect ratio
        
        player_thumb_resized = changeImageSize(player_thumb_width, player_thumb_height, player_thumb)
        
        # Calculate position for player thumb inside the card
        player_thumb_x = card_x + (card_width - player_thumb_resized.size[0]) // 2
        player_thumb_y = card_y + 30 # Slightly down from the top of the card
        
        # Round the corners of the player thumbnail
        mask = Image.new("L", player_thumb_resized.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0,0), player_thumb_resized.size], radius=20, fill=255)
        
        player_thumb_rounded = Image.composite(player_thumb_resized, Image.new("RGBA", player_thumb_resized.size, (0,0,0,0)), mask)
        
        canvas.paste(player_thumb_rounded, (player_thumb_x, player_thumb_y), player_thumb_rounded)
        
        # Load premium fonts with better fallbacks
        try:
            app_font = ImageFont.truetype("AnonXMusic/assets/font4.ttf", 35) # Smaller for card
            title_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 40)
            subtitle_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 28)
            info_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 24)
            small_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 20)
            duration_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 20)
        except:
            # High-quality fallbacks
            from PIL import ImageFont
            try:
                app_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 35)
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 40)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 28)
                info_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
                duration_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
            except:
                app_font = ImageFont.load_default()
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                info_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
                duration_font = ImageFont.load_default()
        
        # Video Title (Truncated)
        display_title = clear(title, 45) # Adjusted max_length for the card
        title_text_x = card_x + 50
        title_text_y = player_thumb_y + player_thumb_resized.size[1] + 20
        draw.text((title_text_x, title_text_y), display_title, fill="#FFFFFF", font=title_font)
        
        # YouTube icon and views/channel
        youtube_icon_size = 25
        # Attempt to load YouTube icon image, otherwise draw a simple one
        try:
            youtube_icon_img = Image.open(generator.icon_paths["youtube"]).convert("RGBA").resize((youtube_icon_size, youtube_icon_size), Image.Resampling.LANCZOS)
            canvas.paste(youtube_icon_img, (title_text_x, title_text_y + 50), youtube_icon_img)
        except Exception as e:
            print(f"Could not load YouTube icon: {e}")
            generator.draw_player_icon(draw, "youtube", title_text_x + youtube_icon_size // 2, title_text_y + 50 + youtube_icon_size // 2, youtube_icon_size, "red")

        channel_text = f"YouTube | {views}"
        draw.text((title_text_x + youtube_icon_size + 10, title_text_y + 50 + (youtube_icon_size - small_font.getbbox(channel_text)[3]) // 2), channel_text, fill="#AAAAAA", font=small_font)
        
        # Progress Bar
        progress_bar_y = title_text_y + 110
        progress_bar_x = card_x + 50
        progress_bar_width = card_width - 100
        progress_bar_height = 8
        
        draw.rounded_rectangle([(progress_bar_x, progress_bar_y), (progress_bar_x + progress_bar_width, progress_bar_y + progress_bar_height)], 
                               radius=4, fill=(255, 255, 255, 50)) # Background
        
        # Current progress (e.g., 60% done)
        current_progress_ratio = 0.45 # Example: 45% progress
        filled_width = int(progress_bar_width * current_progress_ratio)
        
        draw.rounded_rectangle([(progress_bar_x, progress_bar_y), (progress_bar_x + filled_width, progress_bar_y + progress_bar_height)], 
                               radius=4, fill="#FF0000") # Filled with red
        
        # Progress handle (circle)
        handle_size = 12
        handle_x = progress_bar_x + filled_width
        handle_y = progress_bar_y + progress_bar_height // 2
        draw.ellipse([(handle_x - handle_size // 2, handle_y - handle_size // 2), 
                      (handle_x + handle_size // 2, handle_y + handle_size // 2)], 
                     fill="#FF0000", outline="#FFFFFF", width=1)
        
        # Current time and total duration
        current_time_str = "0:00" # Placeholder, actual calculation needed
        if duration and duration != "0:00":
             duration_parts = [int(p) for p in duration.split(':')]
             total_seconds = duration_parts[0] * 60 + duration_parts[1]
             current_seconds = int(total_seconds * current_progress_ratio)
             current_time_str = f"{current_seconds // 60}:{current_seconds % 60:02d}"

        draw.text((progress_bar_x, progress_bar_y + progress_bar_height + 5), current_time_str, fill="#FFFFFF", font=duration_font)
        duration_text_width = duration_font.getbbox(duration)[2] - duration_font.getbbox(duration)[0]
        draw.text((progress_bar_x + progress_bar_width - duration_text_width, progress_bar_y + progress_bar_height + 5), duration, fill="#FFFFFF", font=duration_font)
        
        # Player control buttons (shuffle, prev, play/pause, next, repeat)
        button_y = progress_bar_y + progress_bar_height + 60
        button_size = 35
        
        # Center the buttons
        total_button_width = 5 * (button_size + 30) - 30 # 5 buttons, 30 spacing
        start_x = card_x + (card_width - total_button_width) // 2
        
        buttons_layout = ["shuffle", "previous", "play", "next", "repeat"] # "play" or "pause" dynamically
        
        for i, btn_type in enumerate(buttons_layout):
            btn_x = start_x + i * (button_size + 30) + button_size // 2
            
            # Use play/pause dynamically
            actual_btn_type = btn_type
            if btn_type == "play":
                actual_btn_type = random.choice(["play", "pause"]) # Randomly show play or pause
            
            # Call draw_player_icon (which can load images or draw shapes)
            icon_img = generator.draw_player_icon(draw, actual_btn_type, btn_x, button_y, button_size, color="#FFFFFF", glow_color="#00FFFF")
            if icon_img:
                # If an image was returned, composite it onto the canvas
                canvas.paste(icon_img, (btn_x - button_size // 2, button_y - button_size // 2), icon_img)
        
        # --- PLAYER CARD END ---
        
        # --- SIDE HD FULL VIDEO TEXT (Left) ---
        hd_text = "HD FULL VIDEO"
        try:
            hd_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 40)
        except:
            hd_font = ImageFont.load_default()

        hd_text_size = draw.textbbox((0, 0), hd_text, font=hd_font)
        hd_text_width = hd_text_size[2] - hd_text_size[0]
        hd_text_height = hd_text_size[3] - hd_text_size[1]
        
        # Position vertically centered on the left, rotated
        hd_x = 30 # Distance from left edge
        hd_y = (720 - hd_text_width) // 2
        
        hd_layer = Image.new('RGBA', (hd_text_width + 20, hd_text_height + 20), (0,0,0,0))
        hd_draw = ImageDraw.Draw(hd_layer)
        
        # Apply glow/shadow to HD text
        for d in range(5, 0, -1):
            hd_draw.text((10 + d, 10 + d), hd_text, fill=(0, 0, 0, 100), font=hd_font)
        hd_draw.text((10, 10), hd_text, fill="#FFFFFF", font=hd_font)
        
        hd_layer = hd_layer.rotate(90, expand=True) # Rotate 90 degrees clockwise
        
        canvas.paste(hd_layer, (hd_x, hd_y), hd_layer)

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
        except Exception as fe:
            print(f"Fallback thumbnail generation error: {fe}")
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


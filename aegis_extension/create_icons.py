#!/usr/bin/env python3
"""
Create simple icon files for Aegis Pro Chrome Extension
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple shield icon"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Shield shape (simplified)
    margin = size // 8
    shield_points = [
        (size // 2, margin),  # Top point
        (size - margin, size // 3),  # Right top
        (size - margin, size - margin),  # Right bottom
        (size // 2, size - margin // 2),  # Bottom point
        (margin, size - margin),  # Left bottom
        (margin, size // 3),  # Left top
    ]
    
    # Draw shield background
    draw.polygon(shield_points, fill=(102, 126, 234, 255))  # Blue color
    draw.polygon(shield_points, outline=(255, 255, 255, 255), width=2)
    
    # Draw "A" for Aegis
    font_size = size // 3
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "A"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - size // 8
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save image
    img.save(output_path)
    print(f"Created {output_path}")

def main():
    """Create all required icon sizes"""
    icon_sizes = [16, 32, 48, 128]
    icons_dir = os.path.join(os.path.dirname(__file__), "public", "icons")
    
    # Ensure icons directory exists
    os.makedirs(icons_dir, exist_ok=True)
    
    # Create icons for each size
    for size in icon_sizes:
        output_path = os.path.join(icons_dir, f"icon{size}.png")
        create_icon(size, output_path)
    
    print("All icons created successfully!")

if __name__ == "__main__":
    main()

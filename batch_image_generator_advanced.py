import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import random
from google.colab import files

def draw_decorative_border(draw, width, height, color=(50, 50, 50), thickness=5):
    """Draws decorative border around image"""
    draw.rectangle([thickness, thickness, width-thickness, height-thickness], 
                   outline=color, width=thickness)

def draw_gradient_background(width, height, color1, color2):
    """Creates gradient background"""
    gradient = Image.new('RGB', (width, height))
    pixels = gradient.load()
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        for x in range(width):
            pixels[x, y] = (r, g, b)
    
    return gradient

def draw_stick_figure(draw, x, y, size=60, color=(100, 150, 255)):
    """Draws a simple stick figure"""
    # Head
    draw.ellipse([x-size//4, y-size//2, x+size//4, y-size//4], fill=color, outline=color)
    # Body
    draw.line([x, y-size//4, x, y+size//4], fill=color, width=3)
    # Arms
    draw.line([x-size//3, y, x+size//3, y], fill=color, width=3)
    # Legs
    draw.line([x, y+size//4, x-size//4, y+size//2], fill=color, width=3)
    draw.line([x, y+size//4, x+size//4, y+size//2], fill=color, width=3)

def draw_decorative_elements(draw, width, height, theme_color):
    """Draws decorative circles and shapes"""
    # Top right decorative circles
    colors = [
        (theme_color[0]+30, theme_color[1]+30, theme_color[2]+30),
        (theme_color[0]-20, theme_color[1]-20, theme_color[2]-20)
    ]
    
    for i, color in enumerate(colors):
        x = width - 100 - (i * 60)
        y = 50
        draw.ellipse([x-30, y-30, x+30, y+30], fill=color, outline=color, width=2)
    
    # Bottom left decorative elements
    for i in range(3):
        x = 50 + (i * 50)
        y = height - 80
        draw.ellipse([x-15, y-15, x+15, y+15], fill=colors[i%2], outline=colors[i%2], width=1)

def create_advanced_sensory_images(
    batch_size: int = 50,
    output_dir: str = "sensory_play_advanced",
    image_width: int = 1920,
    image_height: int = 1080
):
    """Creates advanced sensory play images with scenes, characters, and rich content"""
    
    # Validate batch size
    if batch_size > 5000:
        batch_size = 5000
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Define rich slide content with descriptions
    slides = [
        {
            "title": "Sensory Play Activities",
            "subtitle": "Screen-Free Learning Experiences",
            "description": "Sensory play is crucial for child development. It helps children explore their environment,\ndevelop their senses, and build neural pathways. These activities are perfect for ages 1-8.\nEngage your child with fun, educational screen-free play today!",
            "color1": (200, 220, 255),
            "color2": (150, 180, 255),
            "accent_color": (70, 120, 200),
            "emoji": "🎨"
        },
        {
            "title": "Kinetic Sand & Playdough",
            "subtitle": "Tactile Exploration & Fine Motor Skills",
            "description": "Benefits:\n• Develops fine motor skills and hand strength\n• Enhances sensory awareness through touch\n• Promotes creativity and imagination\n• Reduces stress and anxiety\n• Safe, non-toxic, and easy to clean\n\nActivity: Let children mold, stretch, and create shapes!",
            "color1": (255, 240, 200),
            "color2": (255, 200, 150),
            "accent_color": (200, 150, 50),
            "emoji": "🤲"
        },
        {
            "title": "Nature Scavenger Hunt",
            "subtitle": "Outdoor Sensory Exploration",
            "description": "Benefits:\n• Increases observation and focus skills\n• Encourages physical activity and movement\n• Builds appreciation for nature\n• Develops vocabulary about textures and materials\n• Promotes curiosity and discovery\n\nActivity: Collect leaves, rocks, flowers, and different textures!",
            "color1": (200, 255, 200),
            "color2": (150, 220, 150),
            "accent_color": (80, 180, 80),
            "emoji": "🍃"
        },
        {
            "title": "Water Pouring Station",
            "subtitle": "Cause & Effect Learning",
            "description": "Benefits:\n• Teaches cause and effect relationships\n• Develops hand-eye coordination\n• Introduces basic physics concepts (volume, flow)\n• Provides calming, meditative play\n• Improves concentration and patience\n\nSetup: Use cups, funnels, sponges, and bowls with water!",
            "color1": (200, 240, 255),
            "color2": (100, 200, 255),
            "accent_color": (50, 150, 220),
            "emoji": "💧"
        },
        {
            "title": "Blanket Fort Building",
            "subtitle": "Creativity & Spatial Awareness",
            "description": "Benefits:\n• Develops problem-solving and planning skills\n• Encourages creative and imaginative play\n• Builds spatial awareness and understanding\n• Creates a safe, cozy play space\n• Promotes independence and confidence\n\nActivity: Use blankets, pillows, and furniture to build!",
            "color1": (240, 220, 255),
            "color2": (200, 150, 220),
            "accent_color": (160, 80, 200),
            "emoji": "🏠"
        },
        {
            "title": "Rainbow Color Mixing",
            "subtitle": "Scientific Exploration & Art",
            "description": "Benefits:\n• Introduces primary and secondary colors\n• Teaches scientific method through experimentation\n• Develops color recognition and prediction\n• Encourages hypothesis and testing\n• Creates beautiful, visible results\n\nActivity: Mix food coloring with water to create new colors!",
            "color1": (255, 220, 220),
            "color2": (255, 150, 150),
            "accent_color": (220, 80, 80),
            "emoji": "🌈"
        },
        {
            "title": "Sensory Bins",
            "subtitle": "Multi-Sensory Exploration",
            "description": "Benefits:\n• Engages multiple senses simultaneously\n• Provides safe exploration of different materials\n• Develops fine motor skills (pinching, grasping)\n• Encourages imaginative play scenarios\n• Can be themed for learning (letters, numbers)\n\nFill with: Rice, pasta, beans, sand, or kinetic sand!",
            "color1": (255, 245, 200),
            "color2": (255, 220, 100),
            "accent_color": (200, 150, 0),
            "emoji": "🎁"
        },
        {
            "title": "Music & Sound Making",
            "subtitle": "Auditory Sensory Development",
            "description": "Benefits:\n• Develops auditory processing and discrimination\n• Introduces rhythm and patterns\n• Encourages creative expression\n• Helps emotional regulation and mood\n• Makes music accessible and fun\n\nUse: Pots, spoons, bottles, bells, and household items!",
            "color1": (240, 200, 255),
            "color2": (200, 150, 220),
            "accent_color": (160, 80, 200),
            "emoji": "🎵"
        },
        {
            "title": "Bubble Exploration",
            "subtitle": "Visual & Tactile Learning",
            "description": "Benefits:\n• Captivates attention and focus\n• Introduces physics concepts (surface tension)\n• Develops tracking and coordination\n• Provides sensory satisfaction\n• Safe and age-appropriate fun\n\nActivity: Blow bubbles with different wand shapes!",
            "color1": (200, 255, 240),
            "color2": (100, 240, 220),
            "accent_color": (50, 180, 180),
            "emoji": "🫧"
        },
        {
            "title": "Screen-Free Play Benefits",
            "subtitle": "Why Sensory Play Matters",
            "description": "Screen-free play benefits:\n• Improved attention and focus\n• Better social and emotional development\n• Enhanced creativity and problem-solving\n• Healthier physical development\n• Stronger parent-child bonding\n• Better sleep patterns\n\nStart today for a healthier, happier childhood!",
            "color1": (220, 220, 220),
            "color2": (180, 180, 180),
            "accent_color": (100, 100, 100),
            "emoji": "⭐"
        }
    ]
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        emoji_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 100)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        emoji_font = ImageFont.load_default()
    
    print(f"🖼️  Generating {batch_size} advanced images with scenes and characters...")
    print(f"📐 Resolution: {image_width}x{image_height}")
    print(f"📁 Output: {output_dir}\n")
    
    successful_count = 0
    
    for i in range(batch_size):
        try:
            slide = slides[i % len(slides)]
            
            # Create gradient background
            img_pil = draw_gradient_background(
                image_width, image_height,
                slide["color1"], slide["color2"]
            )
            draw = ImageDraw.Draw(img_pil, 'RGBA')
            
            # Draw decorative border
            draw_decorative_border(draw, image_width, image_height, slide["accent_color"], 8)
            
            # Draw decorative elements
            draw_decorative_elements(draw, image_width, image_height, slide["accent_color"])
            
            # Draw large emoji/character on the right side
            emoji_x = image_width - 200
            emoji_y = 150
            draw.text((emoji_x, emoji_y), slide["emoji"], font=emoji_font, fill=(255, 255, 255, 200))
            
            # Draw stick figures at bottom
            stick_fig_y = image_height - 150
            draw_stick_figure(draw, 150, stick_fig_y, size=80, color=slide["accent_color"])
            draw_stick_figure(draw, 350, stick_fig_y, size=80, color=slide["accent_color"])
            draw_stick_figure(draw, 550, stick_fig_y, size=80, color=slide["accent_color"])
            
            # Draw title with shadow effect
            title_bbox = draw.textbbox((0, 0), slide["title"], font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (image_width - title_width) // 2
            title_y = 60
            
            # Shadow
            draw.text((title_x + 2, title_y + 2), slide["title"], font=title_font, 
                     fill=(0, 0, 0, 100))
            # Main text
            draw.text((title_x, title_y), slide["title"], font=title_font, 
                     fill=slide["accent_color"])
            
            # Draw subtitle with background
            subtitle_bbox = draw.textbbox((0, 0), slide["subtitle"], font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (image_width - subtitle_width) // 2
            subtitle_y = title_y + 90
            
            # Subtitle background box
            padding = 15
            draw.rectangle(
                [subtitle_x - padding, subtitle_y - padding,
                 subtitle_x + subtitle_width + padding, subtitle_y + 50 + padding],
                fill=(255, 255, 255, 180),
                outline=slide["accent_color"],
                width=3
            )
            draw.text((subtitle_x, subtitle_y), slide["subtitle"], font=subtitle_font,
                     fill=slide["accent_color"])
            
            # Draw description text with better formatting
            description_y = subtitle_y + 100
            line_height = 50
            max_width = image_width - 200
            
            # Split description into lines
            lines = slide["description"].split('\n')
            for line in lines:
                if line.strip():
                    # Determine color based on content
                    if line.startswith('•'):
                        text_color = (50, 50, 50)
                    else:
                        text_color = slide["accent_color"]
                    
                    draw.text((100, description_y), line, font=text_font, fill=text_color)
                    description_y += line_height
            
            # Add image number at bottom right
            image_num_text = f"#{i+1}/{batch_size}"
            draw.text((image_width - 200, image_height - 40), image_num_text,
                     font=text_font, fill=(100, 100, 100))
            
            # Save image
            filename = f"{output_dir}/sensory_advanced_{i+1:05d}.png"
            img_pil.save(filename, quality=95)
            successful_count += 1
            
            if (i + 1) % 20 == 0 or i == 0:
                print(f"✓ Generated {i+1}/{batch_size}")
        
        except Exception as e:
            print(f"❌ Error on image {i+1}: {e}")
    
    # Calculate statistics
    total_size = sum(os.path.getsize(os.path.join(output_dir, f)) 
                     for f in os.listdir(output_dir) if f.endswith('.png'))
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"\n{'='*70}")
    print(f"✅ ADVANCED BATCH GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"📊 Images created: {successful_count}/{batch_size}")
    print(f"💾 Total size: {total_size_mb:.2f} MB")
    print(f"🖼️  Resolution: {image_width}x{image_height}")
    print(f"🎨 Unique designs: {len(slides)}")
    print(f"✨ Features: Scenes, Characters, Decorative Elements, Rich Text")
    print(f"{'='*70}\n")
    
    return output_dir

# Run the generator
print("="*70)
print("🎨 SENSORY PLAY ADVANCED IMAGE BATCH GENERATOR")
print("="*70 + "\n")

output_folder = create_advanced_sensory_images(
    batch_size=100,  # Change this: 10, 50, 100, 200, 500
    output_dir="sensory_play_advanced"
)

# Zip and download
import shutil
print("📦 Creating ZIP file for download...")
shutil.make_archive('sensory_play_advanced_batch', 'zip', output_folder)
files.download('sensory_play_advanced_batch.zip')
print("✅ ZIP file downloaded! All images ready!")

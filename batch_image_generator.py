import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import sys
from datetime import datetime

def create_batch_sensory_images(
    batch_size: int = 10,
    output_dir: str = "sensory_play_images",
    image_width: int = 1920,
    image_height: int = 1080,
    resolution: str = "1080p"
):
    """
    Generates batch of sensory play activity images.
    
    Args:
        batch_size: Number of images to generate (1-1000, default 10)
        output_dir: Directory to save images
        image_width: Image width in pixels
        image_height: Image height in pixels
        resolution: Preset resolution ("480p", "720p", "1080p", "4k")
    
    Returns:
        Number of images successfully created
    """
    
    # Resolution presets
    resolutions = {
        "480p": (854, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160)
    }
    
    # Apply resolution preset if available
    if resolution in resolutions:
        image_width, image_height = resolutions[resolution]
    
    # Validate batch size
    max_batch_size = 1000
    if batch_size < 1:
        print(f"⚠ Batch size must be at least 1. Setting to 1.")
        batch_size = 1
    elif batch_size > max_batch_size:
        print(f"⚠ Batch size exceeds maximum ({max_batch_size}). Setting to {max_batch_size}.")
        batch_size = max_batch_size
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Sensory play activities with variations
    base_slides = [
        {
            "title": "Sensory Play Ideas",
            "subtitle": "& Screen-Free Activities",
            "bg_color": (230, 245, 255)
        },
        {
            "title": "1. Kinetic Sand & Playdough",
            "subtitle": "Encourages tactile exploration and develops fine motor skills.",
            "bg_color": (235, 255, 235)
        },
        {
            "title": "2. Nature Scavenger Hunt",
            "subtitle": "Engage the senses outdoors by collecting leaves, rocks, and textures.",
            "bg_color": (245, 255, 230)
        },
        {
            "title": "3. Water Pouring Station",
            "subtitle": "Utilize cups, funnels, and sponges for auditory and visual stimulation.",
            "bg_color": (255, 235, 245)
        },
        {
            "title": "4. Blanket Fort Building",
            "subtitle": "Fosters creativity, spatial awareness, and imaginative screen-free play.",
            "bg_color": (255, 250, 230)
        },
        {
            "title": "5. Rainbow Color Mixing",
            "subtitle": "Explore colors through water and food coloring experiments.",
            "bg_color": (245, 235, 255)
        },
        {
            "title": "6. Sensory Bins",
            "subtitle": "Create bins filled with rice, beans, or pasta for tactile exploration.",
            "bg_color": (255, 245, 230)
        },
        {
            "title": "7. Music Making Station",
            "subtitle": "Use household items to create instruments and explore sounds.",
            "bg_color": (230, 255, 245)
        },
        {
            "title": "Enjoy Screen-Free Time!",
            "subtitle": "Thank you for exploring these developmental activities.",
            "bg_color": (240, 240, 240)
        }
    ]
    
    # Load fonts
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "arial.ttf",
            "Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        font_title = None
        font_subtitle = None
        
        for path in font_paths:
            if os.path.exists(path):
                font_title = ImageFont.truetype(path, int(80 * image_height / 1080))
                font_subtitle = ImageFont.truetype(path, int(40 * image_height / 1080))
                break
                
        if font_title is None:
            raise FileNotFoundError("No TrueType font found")
            
    except Exception as e:
        print(f"⚠ Warning: {e}. Using default font.")
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
    
    print(f"🖼️  Generating batch of {batch_size} images...")
    print(f"📐 Resolution: {image_width}x{image_height} ({resolution})")
    print(f"📁 Output directory: {output_dir}\n")
    
    successful_count = 0
    failed_count = 0
    
    # Generate images
    for i in range(batch_size):
        try:
            # Rotate through base slides
            slide = base_slides[i % len(base_slides)]
            
            # Create image
            img_pil = Image.new('RGB', (image_width, image_height), color=slide["bg_color"])
            draw = ImageDraw.Draw(img_pil)
            
            # Calculate text positions
            title_bbox = draw.textbbox((0, 0), slide["title"], font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            subtitle_bbox = draw.textbbox((0, 0), slide["subtitle"], font=font_subtitle)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            
            title_position = ((image_width - title_width) // 2, (image_height // 2) - title_height - 20)
            subtitle_position = ((image_width - subtitle_width) // 2, (image_height // 2) + 20)
            
            # Draw text
            draw.text(title_position, slide["title"], fill=(50, 50, 50), font=font_title)
            draw.text(subtitle_position, slide["subtitle"], fill=(80, 80, 80), font=font_subtitle)
            
            # Add image number watermark
            watermark_text = f"Image {i+1}/{batch_size}"
            watermark_bbox = draw.textbbox((0, 0), watermark_text, font=font_subtitle)
            watermark_width = watermark_bbox[2] - watermark_bbox[0]
            watermark_position = (image_width - watermark_width - 20, image_height - 50)
            draw.text(watermark_position, watermark_text, fill=(150, 150, 150), font=font_subtitle)
            
            # Save image
            filename = f"{output_dir}/sensory_play_{i+1:04d}.png"
            img_pil.save(filename, quality=95)
            successful_count += 1
            
            # Progress indicator
            if (i + 1) % 10 == 0 or i == 0:
                print(f"✓ Generated {i+1}/{batch_size} images")
        
        except Exception as e:
            print(f"❌ Error generating image {i+1}: {e}")
            failed_count += 1
    
    # Summary statistics
    total_size = 0
    for file in os.listdir(output_dir):
        if file.endswith('.png'):
            total_size += os.path.getsize(os.path.join(output_dir, file))
    
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"\n{'='*60}")
    print(f"✅ BATCH GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"📊 Images created: {successful_count}/{batch_size}")
    print(f"❌ Failed: {failed_count}")
    print(f"📁 Location: {os.path.abspath(output_dir)}")
    print(f"💾 Total size: {total_size_mb:.2f} MB")
    print(f"🖼️  Resolution: {image_width}x{image_height}")
    print(f"🎨 Activities: {len(base_slides)} unique designs")
    print(f"{'='*60}")
    
    return successful_count

def create_slideshow_from_batch(
    image_dir: str = "sensory_play_images",
    output_video: str = "sensory_play_slideshow.mp4",
    fps: int = 1,
    duration_per_image: float = 4.0
):
    """
    Creates a slideshow video from batch of generated images.
    """
    
    if not os.path.exists(image_dir):
        print(f"❌ Image directory not found: {image_dir}")
        return False
    
    # Get all PNG images sorted
    images = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])
    
    if not images:
        print(f"❌ No images found in {image_dir}")
        return False
    
    print(f"\n🎬 Creating slideshow video from {len(images)} images...")
    
    # Get image dimensions
    sample_img = Image.open(os.path.join(image_dir, images[0]))
    width, height = sample_img.size
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("❌ Failed to initialize video writer")
        return False
    
    frames_per_image = int(fps * duration_per_image)
    
    # Write frames
    for idx, image_file in enumerate(images):
        img_path = os.path.join(image_dir, image_file)
        img = cv2.imread(img_path)
        
        # Repeat frame for duration
        for _ in range(frames_per_image):
            out.write(img)
        
        if (idx + 1) % 10 == 0:
            print(f"✓ Processed {idx+1}/{len(images)} images")
    
    out.release()
    
    video_size = os.path.getsize(output_video) / (1024 * 1024)
    total_duration = len(images) * duration_per_image
    
    print(f"\n✅ Slideshow created: {output_video}")
    print(f"📊 Duration: {total_duration:.1f} seconds")
    print(f"💾 Size: {video_size:.2f} MB")
    
    return True

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("🖼️  SENSORY PLAY BATCH IMAGE GENERATOR")
        print("=" * 60 + "\n")
        
        # Generate batch of images
        batch_count = 50  # Change this to generate different amounts
        created = create_batch_sensory_images(
            batch_size=batch_count,
            output_dir="sensory_play_images",
            resolution="1080p"  # Options: "480p", "720p", "1080p", "4k"
        )
        
        # Optional: Create slideshow from images
        if created > 0:
            create_slideshow_option = input("\n📹 Create slideshow video from images? (y/n): ").lower()
            if create_slideshow_option == 'y':
                create_slideshow_from_batch(
                    image_dir="sensory_play_images",
                    output_video="sensory_play_slideshow.mp4",
                    fps=1,
                    duration_per_image=4.0
                )
        
        print("\n✨ Done! Download your images from the Files panel.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

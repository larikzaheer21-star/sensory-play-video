import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def create_sensory_play_video(output_filename: str = "sensory_play_activities.mp4"):
    """
    Generates an MP4 video file featuring sensory play ideas and screen-free activities.
    The video maintains a strict 1920x1080 (16:9) resolution and ratio throughout.
    Optimized for Replit environment.
    """
    
    # Define strict video parameters to maintain consistent size and ratio
    WIDTH = 1920
    HEIGHT = 1080
    FPS = 30
    SLIDE_DURATION_SECONDS = 4
    FRAMES_PER_SLIDE = FPS * SLIDE_DURATION_SECONDS
    
    # Define the content for each slide (Title, Subtitle, Background Color in BGR format)
    slides = [
        {
            "title": "Sensory Play Ideas",
            "subtitle": "& Screen-Free Activities",
            "bg_color": (230, 245, 255)  # Light Blue
        },
        {
            "title": "1. Kinetic Sand & Playdough",
            "subtitle": "Encourages tactile exploration and develops fine motor skills.",
            "bg_color": (235, 255, 235)  # Light Green
        },
        {
            "title": "2. Nature Scavenger Hunt",
            "subtitle": "Engage the senses outdoors by collecting leaves, rocks, and textures.",
            "bg_color": (245, 255, 230)  # Pale Yellow-Green
        },
        {
            "title": "3. Water Pouring Station",
            "subtitle": "Utilize cups, funnels, and sponges for auditory and visual stimulation.",
            "bg_color": (255, 235, 245)  # Light Pink
        },
        {
            "title": "4. Blanket Fort Building",
            "subtitle": "Fosters creativity, spatial awareness, and imaginative screen-free play.",
            "bg_color": (255, 250, 230)  # Light Cream
        },
        {
            "title": "Enjoy Screen-Free Time!",
            "subtitle": "Thank you for exploring these developmental activities.",
            "bg_color": (240, 240, 240)  # Light Gray
        }
    ]

    # Initialize the VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, FPS, (WIDTH, HEIGHT))

    if not out.isOpened():
        raise RuntimeError("Failed to initialize the video writer. Please check your OpenCV installation.")

    print(f"Initializing video generation at {WIDTH}x{HEIGHT} ({WIDTH/HEIGHT:.2f} ratio)...")
    print(f"Generating {len(slides)} slides, {SLIDE_DURATION_SECONDS} seconds each...")

    # Attempt to load a standard TrueType font for high-quality text rendering
    try:
        # Common font paths across different operating systems
        font_paths = [
            "arial.ttf", 
            "Arial.ttf", 
            "/System/Library/Fonts/Helvetica.ttc", 
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        ]
        font_title = None
        font_subtitle = None
        
        for path in font_paths:
            if os.path.exists(path):
                font_title = ImageFont.truetype(path, 80)
                font_subtitle = ImageFont.truetype(path, 40)
                print(f"✓ Using font: {path}")
                break
                
        if font_title is None:
            raise FileNotFoundError("No suitable TrueType font found.")
            
    except Exception as e:
        print(f"⚠ Warning: Custom font not found ({e}). Falling back to default PIL font.")
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()

    # Generate frames for each slide
    slide_count = 0
    for slide in slides:
        slide_count += 1
        print(f"Processing slide {slide_count}/{len(slides)}: {slide['title'][:40]}...")
        
        for frame_num in range(FRAMES_PER_SLIDE):
            # Create a new PIL Image with the specified background color
            img_pil = Image.new('RGB', (WIDTH, HEIGHT), color=slide["bg_color"])
            draw = ImageDraw.Draw(img_pil)

            # Calculate text bounding boxes to center the text perfectly
            title_bbox = draw.textbbox((0, 0), slide["title"], font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            subtitle_bbox = draw.textbbox((0, 0), slide["subtitle"], font=font_subtitle)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]

            # Define text positions (centered horizontally, adjusted vertically)
            title_position = ((WIDTH - title_width) // 2, (HEIGHT // 2) - title_height - 20)
            subtitle_position = ((WIDTH - subtitle_width) // 2, (HEIGHT // 2) + 20)

            # Draw text onto the image
            draw.text(title_position, slide["title"], fill=(50, 50, 50), font=font_title)
            draw.text(subtitle_position, slide["subtitle"], fill=(80, 80, 80), font=font_subtitle)

            # Convert PIL Image (RGB) to OpenCV format (BGR)
            frame_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

            # Write the frame to the video file
            out.write(frame_cv)

    # Release the video writer
    out.release()
    print(f"\n✅ Video successfully generated and saved as: {output_filename}")
    print(f"📊 Video specs: {WIDTH}x{HEIGHT} @ {FPS}FPS, Duration: ~{len(slides) * SLIDE_DURATION_SECONDS}s")
    
    # Verify file was created
    if os.path.exists(output_filename):
        file_size = os.path.getsize(output_filename) / (1024 * 1024)
        print(f"📁 File size: {file_size:.2f} MB")
    else:
        print("❌ Error: Video file was not created!")

if __name__ == "__main__":
    try:
        print("🎬 Sensory Play Video Generator")
        print("=" * 50)
        create_sensory_play_video()
        print("=" * 50)
        print("✨ Done! Your video is ready to download.")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        sys.exit(1)

import sys
import os
from PIL import Image, ImageEnhance, ImageOps

def prep_photo(input_path, output_path="source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist.")
        return

    img = Image.open(input_path)
    
    # Try rembg background removal
    try:
        from rembg import remove
        print("Removing background with rembg...")
        img_no_bg = remove(img)
    except Exception as e:
        print(f"rembg notice: ({e}). Using full image with thresholding.")
        img_no_bg = img

    # Convert to RGBA
    img_rgba = img_no_bg.convert("RGBA")
    
    # Create white background
    background = Image.new("RGBA", img_rgba.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(background, img_rgba)
    grayscale = composite.convert("L")
    
    # Increase contrast to make facial outline and features sharp
    enhancer = ImageEnhance.Contrast(grayscale)
    enhanced = enhancer.enhance(2.0)
    
    enhanced.save(output_path)
    print(f"Saved prepped photo to {output_path}")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(input_file)

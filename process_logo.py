
from PIL import Image, ImageDraw, ImageOps

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    
    # Corners
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    
    # Edges
    alpha.paste(255, (rad, 0, w - rad, h))
    alpha.paste(255, (0, rad, rad, h - rad))
    alpha.paste(255, (w - rad, rad, w, h - rad))
    
    im.putalpha(alpha)
    return im

def make_transparent(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    
    # Create a mask for rounded corners
    # macOS icons are usually rounded squares.
    # Radius is typically ~17-18% of the size.
    size = img.size[0]
    radius = int(size * 0.22) # Slightly rounded
    
    img = add_corners(img, radius)
    
    img.save(output_path, "PNG")
    print(f"Saved processed logo to {output_path}")

if __name__ == "__main__":
    make_transparent("logo.png", "logo_clean.png")

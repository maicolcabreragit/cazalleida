import os
from PIL import Image, ImageDraw, ImageFont

def make_logo_transparent_and_keep_colors(logo_path):
    # Load logo
    logo = Image.open(logo_path).convert("RGBA")
    width, height = logo.size
    
    # Background color to remove: (245, 240, 230)
    bg_r, bg_g, bg_b = 245, 240, 230
    tolerance = 20
    
    data = logo.getdata()
    new_data = []
    
    for item in data:
        r, g, b, a = item
        # Calculate distance to background color
        dist = ((r - bg_r)**2 + (g - bg_g)**2 + (b - bg_b)**2)**0.5
        
        if dist < tolerance:
            # Make background fully transparent
            new_data.append((0, 0, 0, 0))
        elif dist < tolerance + 15:
            # Smooth edge transition
            alpha = int(255 * (dist - tolerance) / 15)
            new_data.append((r, g, b, alpha))
        else:
            # Keep original colors (including shading, details, text)
            new_data.append((r, g, b, 255))
            
    logo.putdata(new_data)
    return logo

def create_outro():
    # Dimensions
    width = 3840
    height = 2160
    
    # Base background (Elegant cream color matching the website)
    # Brand cream: #F4EFE3 -> (244, 239, 227)
    bg_color = (244, 239, 227)
    img = Image.new("RGBA", (width, height), bg_color + (255,))
    
    # Create a very subtle radial vignette (lighter in the center)
    mask_w, mask_h = 384, 216
    mask = Image.new("L", (mask_w, mask_h), 0)
    draw_m = ImageDraw.Draw(mask)
    for y in range(mask_h):
        for x in range(mask_w):
            dx = x - mask_w / 2
            dy = y - mask_h / 2
            dist = (dx**2 + dy**2)**0.5
            max_dist = ((mask_w/2)**2 + (mask_h/2)**2)**0.5
            # Center is slightly lighter, edges have natural cream color
            val = int(255 - 25 * (dist / max_dist))
            mask.putpixel((x, y), max(0, val))
            
    vignette = mask.resize((width, height), Image.Resampling.BILINEAR)
    img = Image.composite(img, Image.new("RGBA", (width, height), (236, 230, 214, 255)), vignette)

    draw = ImageDraw.Draw(img)
    
    # 4. Load and make logo transparent
    logo_path = "logo_check_light.png"
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found")
        return
        
    logo = make_logo_transparent_and_keep_colors(logo_path)
    
    # Resize logo (e.g. to 650x650 pixels)
    logo_size = 650
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    # Paste logo in the center (slightly shifted up)
    logo_x = (width - logo_size) // 2
    logo_y = 480
    img.paste(logo, (logo_x, logo_y), logo)
    
    # 5. Load fonts
    font_serif_path = "C:\\Windows\\Fonts\\georgiab.ttf" # Georgia Bold
    font_sans_path = "C:\\Windows\\Fonts\\segoeui.ttf"   # Segoe UI Regular
    font_sans_b_path = "C:\\Windows\\Fonts\\segoeuib.ttf" # Segoe UI Bold
    
    if not os.path.exists(font_serif_path):
        font_serif_path = "arial.ttf"
    if not os.path.exists(font_sans_path):
        font_sans_path = "arial.ttf"
    if not os.path.exists(font_sans_b_path):
        font_sans_b_path = "arial.ttf"
        
    font_title = ImageFont.truetype(font_serif_path, 115)
    font_subtitle = ImageFont.truetype(font_sans_path, 55)
    font_info = ImageFont.truetype(font_sans_b_path, 68)
    
    # Brand Colors for Text (on cream background)
    # Deep Moss Green: #26301F -> (38, 48, 31)
    # Gold: #C79A3E -> (199, 154, 62)
    color_moss = (38, 48, 31, 255)
    color_gold = (199, 154, 62, 255)
    
    # Draw "cazalleida.com"
    title_text = "cazalleida.com"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (width - title_w) // 2
    title_y = logo_y + logo_size + 80
    draw.text((title_x, title_y), title_text, font=font_title, fill=color_moss)
    
    # Draw subtle separator line
    line_y = title_y + 175
    line_w = 400
    draw.line(((width - line_w)//2, line_y, (width + line_w)//2, line_y), fill=(199, 154, 62, 180), width=4)
    
    # Draw Location / Info
    loc_text = "COTO DE GRANYENA DE LES GARRIGUES"
    loc_bbox = draw.textbbox((0, 0), loc_text, font=font_subtitle)
    loc_w = loc_bbox[2] - loc_bbox[0]
    loc_x = (width - loc_w) // 2
    loc_y = line_y + 60
    draw.text((loc_x, loc_y), loc_text, font=font_subtitle, fill=color_gold)
    
    # Draw Phone Number (Updated to +34 699 94 97 37, removed email)
    phone_text = "Tel: +34 699 94 97 37"
    phone_bbox = draw.textbbox((0, 0), phone_text, font=font_info)
    phone_w = phone_bbox[2] - phone_bbox[0]
    phone_x = (width - phone_w) // 2
    phone_y = loc_y + 110
    draw.text((phone_x, phone_y), phone_text, font=font_info, fill=color_moss)
    
    # Save the output image
    os.makedirs("videos", exist_ok=True)
    out_path = "videos/outro.png"
    img.convert("RGB").save(out_path, "PNG")
    print(f"Outro image saved successfully to {out_path}")

if __name__ == "__main__":
    create_outro()

import os
from PIL import Image

src_dir = 'pic'
dest_dir = os.path.join(src_dir, 'optimized')

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

files = [
    'Background.JPG',
    'Bureau.png',
    'EP02.png',
    'EP06.png',
    'Poster.jpg',
    'Residue02.PNG',
    'Weapon.PNG',
    'characters.PNG'
]

print("Starting image optimization...")
for f in files:
    src_path = os.path.join(src_dir, f)
    name_wo_ext = os.path.splitext(f)[0]
    dest_path = os.path.join(dest_dir, f"{name_wo_ext}.jpg")
    
    if not os.path.exists(src_path):
        print(f"Warning: {src_path} does not exist.")
        continue
        
    try:
        with Image.open(src_path) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (0, 0, 0))
                # If RGBA, use alpha channel as mask
                mask = img.split()[3] if img.mode == 'RGBA' else None
                background.paste(img, mask=mask)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
                
            w, h = img.size
            max_size = 1080
            if w > max_size or h > max_size:
                if w > h:
                    new_w = max_size
                    new_h = int(h * (max_size / w))
                else:
                    new_h = max_size
                    new_w = int(w * (max_size / h))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                print(f"Resized {f} from {w}x{h} to {new_w}x{new_h}")
            else:
                print(f"Kept original size for {f}: {w}x{h}")
                
            img.save(dest_path, 'JPEG', quality=85)
            print(f"Saved optimized image to {dest_path} (Size: {os.path.getsize(dest_path)} bytes)")
    except Exception as e:
        print(f"Error processing {f}: {e}")

print("Image optimization finished.")

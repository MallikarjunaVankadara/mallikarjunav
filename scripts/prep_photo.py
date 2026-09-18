from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

INPUT = Path("profile-photo.jpg")
OUTPUT = Path("profile-prepped.png")

if not INPUT.exists():
    raise FileNotFoundError(
        "Upload your photo to the repository root as profile-photo.jpg"
    )

img = Image.open(INPUT).convert("RGB")

img = ImageOps.exif_transpose(img)

width, height = img.size

side = min(width, height)

left = (width - side) // 2
top = (height - side) // 2

img = img.crop(
    (
        left,
        top,
        left + side,
        top + side
    )
)

img = img.resize((700, 700))

img = ImageOps.grayscale(img)

img = ImageEnhance.Contrast(img).enhance(1.8)
img = ImageEnhance.Sharpness(img).enhance(1.3)

img.save(OUTPUT)

print(f"Created {OUTPUT}")
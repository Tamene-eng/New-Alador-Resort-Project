from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory if it doesn't exist
os.makedirs('app/static/images', exist_ok=True)

# Image specs
images = [
    ('your-resort.jpg', 'Alador Resort', (1920, 1080), 'blue'),
    ('Resort_View.jpg', 'Resort View', (800, 600), 'green'),
    ('Relaxing_Spa.jpg', 'Relaxing Spa', (800, 600), 'purple'),
    ('Resort_View_2.jpg', 'Resort View 2', (800, 600), 'teal'),
    ('Culinary_1.jpg', 'Culinary 1', (800, 600), 'orange'),
    ('Culinary_2.jpg', 'Culinary 2', (800, 600), 'pink'),
    ('Culinary_3.jpg', 'Culinary 3', (800, 600), 'brown')
]

colors = {
    'blue': '#4A90E2',
    'green': '#7ED321',
    'purple': '#9013FE',
    'teal': '#50E3C2',
    'orange': '#F5A623',
    'pink': '#D0021B',
    'brown': '#8B572A'
}

for filename, text, size, color_name in images:
    # Create image
    img = Image.new('RGB', size, color=colors[color_name])
    draw = ImageDraw.Draw(img)

    # Try to use a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    # Draw text
    draw.text((x, y), text, fill='white', font=font)

    # Save image
    img.save(f'app/static/images/{filename}')
    print(f'Created {filename}')

print('All placeholder images created!')
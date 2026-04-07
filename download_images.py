import requests
import os

# List of image names from your index.html template
images = [
    'your-resort.jpg',
    'Resort_View.jpg',
    'Relaxing_Spa.jpg',
    'Resort_View_2.jpg',
    'Culinary_1.jpg',
    'Culinary_2.jpg',
    'Culinary_3.jpg'
]

# Create images directory if it doesn't exist
os.makedirs('app/static/images', exist_ok=True)

# Download placeholder images from Lorem Picsum
for img in images:
    url = f'https://picsum.photos/800/600?random={hash(img)}'
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'app/static/images/{img}', 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {img}')
    else:
        print(f'Failed to download {img}')

print('All images downloaded!')
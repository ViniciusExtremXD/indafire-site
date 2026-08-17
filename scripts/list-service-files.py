import os
from PIL import Image

# Let's inspect each image from original site
files = [f for f in os.listdir('images/original_site') if f.startswith('serv') and f.endswith('.jpg')]
files.sort()
print("Found service images:", files)

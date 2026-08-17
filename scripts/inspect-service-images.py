import os
from PIL import Image

image_files = [
    'images/original_site/projeto-simplificado-2028.jpg',
    'images/original_site/banneravcb-830.jpg',
    'images/original_site/serv14-180.jpg',
    'images/original_site/serv15-189.jpg',
    'images/original_site/serv16-192.jpg',
    'images/original_site/serv17-211.jpg',
    'images/original_site/serv18-229.jpg',
    'images/original_site/serv2-195.jpg',
    'images/original_site/serv3-198.jpg',
    'images/original_site/serv4-201.jpg',
    'images/original_site/serv5-204.jpg',
    'images/original_site/serv6-207.jpg',
    'images/original_site/serv7-217.jpg',
    'images/original_site/serv8-220.jpg',
    'images/original_site/serv9-213.jpg',
    'images/original_site/serv10-223.jpg',
    'images/original_site/serv11-226.jpg',
    'images/original_site/serv12-232.jpg',
    'images/original_site/serv13-235.jpg',
    'images/original_site/central-alarme-incendio-02-545.jpg',
    'images/original_site/hidrantes-2008.jpg',
    'images/original_site/fire-sprinkler-in-office-building-blur-background-focus-at-selective-2055.jpg',
    'images/sprinklers.webp',
    'images/facility.webp',
    'images/inspection.webp',
    'images/treinamento_brigada_brasil.jpg'
]

for p in image_files:
    if os.path.exists(p):
        img = Image.open(p)
        print(f"{p} -> {img.size} ({img.format})")
    else:
        print(f"MISSING: {p}")

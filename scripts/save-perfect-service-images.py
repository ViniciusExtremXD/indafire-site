import os
from PIL import Image

os.makedirs('images/services', exist_ok=True)

mapping = [
    ('images/original_site/serv14-180.jpg', 'images/services/projeto-tecnico-ppci.jpg'),
    ('images/original_site/serv15-189.jpg', 'images/services/processo-simplificado-pts.jpg'),
    ('images/original_site/serv16-192.jpg', 'images/services/avcb-clcb-regularizacao.jpg'),
    ('images/original_site/serv3-198.jpg', 'images/services/recarga-inmetro-extintores.jpg'),
    ('images/original_site/serv4-201.jpg', 'images/services/teste-hidrostatico-mangueiras.jpg'),
    ('images/original_site/serv6-207.jpg', 'images/services/redes-hidrantes-bombas.jpg'),
    ('images/original_site/fire-sprinkler-in-office-building-blur-background-focus-at-selective-2055.jpg', 'images/services/sistemas-sprinklers.jpg'),
    ('images/original_site/serv7-217.jpg', 'images/services/iluminacao-emergencia.jpg'),
    ('images/original_site/serv17-211.jpg', 'images/services/alarmes-deteccao-incendio.jpg'),
    ('images/original_site/serv13-235.jpg', 'images/services/caixa-dagua-reservatorio-rti.jpg'),
    ('images/original_site/serv18-229.jpg', 'images/services/locacao-equipamentos-extintores.jpg'),
    ('images/original_site/serv12-232.jpg', 'images/services/bombeiros-civis-eventos.jpg'),
    ('images/original_site/serv11-226.jpg', 'images/services/treinamento-brigada-incendio.jpg'),
    ('images/original_site/serv5-204.jpg', 'images/services/laudos-vistorias-tecnicas.jpg'),
    ('images/original_site/serv10-223.jpg', 'images/services/sinalizacao-fotoluminescente.jpg'),
]

for src, dst in mapping:
    if os.path.exists(src):
        img = Image.open(src)
        img.save(dst, 'JPEG', quality=95)
        print(f"OK: {dst} ({img.size}) from {src}")
    else:
        print(f"MISSING: {src}")

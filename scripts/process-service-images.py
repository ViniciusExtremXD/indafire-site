import os
from PIL import Image

os.makedirs('images/services', exist_ok=True)

services_mapping = [
    {
        'id': 'projeto-tecnico',
        'src': 'images/original_site/serv14-180.jpg',
        'dst': 'images/services/projeto-tecnico-ppci.jpg'
    },
    {
        'id': 'pts',
        'src': 'images/original_site/serv15-189.jpg',
        'dst': 'images/services/processo-simplificado-pts.jpg'
    },
    {
        'id': 'avcb-clcb',
        'src': 'images/original_site/serv16-192.jpg',
        'dst': 'images/services/avcb-clcb-regularizacao.jpg'
    },
    {
        'id': 'recarga-inmetro',
        'src': 'images/original_site/serv17-211.jpg',
        'dst': 'images/services/recarga-inmetro-extintores.jpg'
    },
    {
        'id': 'teste-hidrostatico',
        'src': 'images/original_site/serv18-229.jpg',
        'dst': 'images/services/teste-hidrostatico-mangueiras.jpg'
    },
    {
        'id': 'sistemas-hidrantes',
        'src': 'images/original_site/serv2-195.jpg',
        'dst': 'images/services/redes-hidrantes-bombas.jpg'
    },
    {
        'id': 'sprinklers',
        'src': 'images/original_site/serv3-198.jpg',
        'dst': 'images/services/sistemas-sprinklers.jpg'
    },
    {
        'id': 'iluminacao-emergencia',
        'src': 'images/original_site/serv4-201.jpg',
        'dst': 'images/services/iluminacao-emergencia.jpg'
    },
    {
        'id': 'alarmes-deteccao',
        'src': 'images/original_site/serv5-204.jpg',
        'dst': 'images/services/alarmes-deteccao-incendio.jpg'
    },
    {
        'id': 'caixa-dagua',
        'src': 'images/original_site/serv6-207.jpg',
        'dst': 'images/services/caixa-dagua-reservatorio-rti.jpg'
    },
    {
        'id': 'locacao-equipamentos',
        'src': 'images/original_site/serv7-217.jpg',
        'dst': 'images/services/locacao-equipamentos-extintores.jpg'
    },
    {
        'id': 'equipe-eventos',
        'src': 'images/original_site/serv8-220.jpg',
        'dst': 'images/services/bombeiros-civis-eventos.jpg'
    },
    {
        'id': 'treinamento-brigada',
        'src': 'images/original_site/serv9-213.jpg',
        'dst': 'images/services/treinamento-brigada-incendio.jpg'
    },
    {
        'id': 'laudos-vistorias',
        'src': 'images/original_site/serv10-223.jpg',
        'dst': 'images/services/laudos-vistorias-tecnicas.jpg'
    },
    {
        'id': 'instalacoes-gas',
        'src': 'images/original_site/serv11-226.jpg',
        'dst': 'images/services/instalacoes-redes-gas.jpg'
    },
    {
        'id': 'pressurizacao-escadas',
        'src': 'images/original_site/serv12-232.jpg',
        'dst': 'images/services/pressurizacao-escadas-fumaca.jpg'
    },
    {
        'id': 'portas-corta-fogo',
        'src': 'images/original_site/serv13-235.jpg',
        'dst': 'images/services/portas-corta-fogo.jpg'
    }
]

for item in services_mapping:
    src = item['src']
    dst = item['dst']
    if os.path.exists(src):
        img = Image.open(src)
        img.save(dst, 'JPEG', quality=95)
        print(f"Saved {dst} ({img.size})")
    else:
        print(f"ERROR: {src} not found")

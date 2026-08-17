import os

services_map = {
    'serv14-180.jpg': 'Projeto Técnico (PPCI) / Plantas e Engenharia',
    'serv15-189.jpg': 'Processo Técnico Simplificado (PTS) / Certificado Bombeiros',
    'serv16-192.jpg': 'AVCB / CLCB Regularização',
    'serv17-211.jpg': 'Recarga Inmetro Extintores',
    'serv18-229.jpg': 'Teste Hidrostático',
    'serv2-195.jpg': 'Sistemas Hidráulicos / Hidrantes',
    'serv3-198.jpg': 'Sprinklers',
    'serv4-201.jpg': 'Iluminação de Emergência',
    'serv5-204.jpg': 'Alarmes e Detecção',
    'serv6-207.jpg': 'Caixa d’Água / RTI Reservatório',
    'serv7-217.jpg': 'Locação de Extintores e Equipamentos',
    'serv8-220.jpg': 'Bombeiros Civis e Brigada de Eventos',
    'serv9-213.jpg': 'Treinamento de Brigada',
    'serv10-223.jpg': 'Laudos e Vistorias Técnicas',
    'serv11-226.jpg': 'Instalações de Gás GLP / GN',
    'serv12-232.jpg': 'Pressurização de Escadas',
    'serv13-235.jpg': 'Portas Corta-Fogo'
}

for filename, desc in services_map.items():
    path = os.path.join('images/original_site', filename)
    exists = os.path.exists(path)
    print(f"[{'OK' if exists else 'MISSING'}] {filename}: {desc}")

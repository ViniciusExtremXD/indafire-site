import os

files = [f for f in os.listdir('images/original_site') if (f.startswith('serv') or 'hidrante' in f or 'sprinkler' in f or 'avcb' in f or 'bombeiro' in f or 'inmetro' in f or 'alarme' in f) and (f.endswith('.jpg') or f.endswith('.png') or f.endswith('.webp'))]
files.sort()

html = ['<!DOCTYPE html><html><head><style>body{font-family:sans-serif;background:#111;color:#fff;padding:20px;} .grid{display:grid;grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));gap:20px;} .card{background:#222;padding:10px;border-radius:8px;text-align:center;} img{max-width:100%;height:140px;object-fit:cover;border-radius:4px;}</style></head><body><h1>Galeria de Imagens de Serviços</h1><div class="grid">']

for f in files:
    html.append(f'<div class="card"><img src="images/original_site/{f}"><p style="font-size:12px;word-break:break-all;">{f}</p></div>')

html.append('</div></body></html>')

with open('preview-service-gallery.html', 'w', encoding='utf-8') as out:
    out.write('\n'.join(html))

print(f"Generated preview-service-gallery.html with {len(files)} images!")

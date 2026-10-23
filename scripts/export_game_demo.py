"""Exporta la isla como un HTML autónomo, sin servidor ni recursos externos."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
import django
django.setup()
from django.template.loader import render_to_string

html = render_to_string('academy/game.html')
css = (ROOT / 'static/game.css').read_text(encoding='utf-8')
js = (ROOT / 'static/game.bundle.js').read_text(encoding='utf-8')
# Escape closing script delimiters while preserving the bundled JavaScript.
js = js.replace('</script', '<\\/script')
html = html.replace('<link rel="stylesheet" href="/static/game.css">', '<style>' + css + '</style>')
html = html.replace('<script src="/static/game.bundle.js" defer></script>', '<script>' + js + '</script>')
html = html.replace('href="/"', 'href="http://127.0.0.1:8000/"')
html = html.replace('href="/tema/8/"', 'href="http://127.0.0.1:8000/tema/8/"')
# Course links inside the compiled script use escaped double quotes.
html = html.replace('href=\\"/tema/8/\\"', 'href=\\"http://127.0.0.1:8000/tema/8/\\"')
html = html.replace('Volver al curso ↗', 'Curso Django local ↗')
out = ROOT / 'demo/isla_django.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding='utf-8')
print(out)

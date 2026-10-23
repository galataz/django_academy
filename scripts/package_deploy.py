"""Package this public academy after collectstatic; never copies a local venv.
Run from any directory: python scripts/package_deploy.py --output ../deploy.zip
The nested layout requires the startup command documented in lesson 68.
"""
import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = ('manage.py', 'requirements.txt', 'config', 'academy', 'UTIL_LIB',
           'repoGenerico', 'templates', 'static', 'staticfiles')
EXCLUDE = {'__pycache__', '.git', '.venv', 'venv', 'node_modules', '.pytest_cache'}

def package(output):
    manifest = ROOT / 'staticfiles/staticfiles.json'
    if not manifest.is_file():
        raise SystemExit('Primero ejecuta collectstatic con el backend manifest de producción.')
    files = []
    for entry in INCLUDE:
        source = ROOT / entry
        if not source.exists():
            raise SystemExit(f'Falta un componente requerido: {entry}')
        for path in ([source] if source.is_file() else sorted(source.rglob('*'))):
            relative = path.relative_to(ROOT)
            if any(part in EXCLUDE for part in relative.parts):
                continue
            if path.is_symlink():
                raise SystemExit(f'No se empaquetan enlaces simbólicos: {relative}')
            if not path.is_file() or path.suffix in {'.pyc', '.sqlite3'} or path.name.startswith('.env'):
                continue
            if path.resolve() == output.resolve():
                raise SystemExit('El ZIP de salida no puede estar dentro del contenido incluido.')
            files.append((path, 'SensorHub/' + relative.as_posix()))
    # x refuses to overwrite a previous release.
    with ZipFile(output, 'x', compression=ZIP_DEFLATED) as archive:
        archive.write(ROOT / 'requirements.txt', 'requirements.txt')
        for source, target in files:
            archive.write(source, target)
    print(f'Creado {output.resolve()} con {len(files) + 1} archivos.')
    print('Arranque: gunicorn --chdir SensorHub config.wsgi:application --bind 0.0.0.0:8000')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT.parent / 'deploy.zip')
    package(parser.parse_args().output)

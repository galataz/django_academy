const STORAGE = 'django-professional-course-v2';
let state = { done: [], notes: {} };
try {
    const stored = JSON.parse(localStorage.getItem(STORAGE) || 'null');
    if (stored && Array.isArray(stored.done) && stored.notes && typeof stored.notes === 'object') state = stored;
} catch {}
const total = Number(document.body.dataset.total) || 1;
state.done = [...new Set(state.done.filter(id => Number.isInteger(id) && id >= 1 && id <= total))];
function saveState() {
    try { localStorage.setItem(STORAGE, JSON.stringify(state)); return true; }
    catch { return false; }
}
if (document.querySelector('#progress-percent')) {
    const percent = Math.round(state.done.length / total * 100);
    document.querySelector('#progress-percent').textContent = percent + '%';
    document.querySelector('#progress-count').textContent = state.done.length;
    document.querySelector('#progress-bar').value = percent;
    const order = JSON.parse(document.querySelector('#course-order').textContent);
    const next = order.find(id => !state.done.includes(id)) || order[order.length - 1];
    document.querySelector('#continue-course').href = '/tema/' + next + '/';
}
document.querySelectorAll('.card').forEach(card => {
    if (state.done.includes(Number(card.dataset.lesson))) card.querySelector('.completion-label').textContent = '✓ Completado';
});
const form = document.querySelector('#study-form');
if (form) {
    const id = Number(form.dataset.lesson);
    document.querySelector('#note').value = typeof state.notes[id] === 'string' ? state.notes[id] : '';
    form.addEventListener('submit', event => {
        event.preventDefault();
        state.notes[id] = document.querySelector('#note').value;
        document.querySelector('#status').textContent = saveState() ? 'Nota guardada en este navegador.' : 'No se pudo guardar. Copia tu nota.';
    });
}
const completed = document.querySelector('#complete');
if (completed) {
    const id = Number(completed.dataset.lesson);
    if (state.done.includes(id)) completed.textContent = '✓ Tema completado';
    completed.addEventListener('click', () => {
        if (!state.done.includes(id)) state.done.push(id);
        if (saveState()) {
            completed.textContent = '✓ Tema completado';
            document.querySelector('#completion-status').textContent = 'Progreso guardado.';
        } else document.querySelector('#completion-status').textContent = 'No se pudo guardar el progreso.';
    });
}
document.querySelector('.copy-code')?.addEventListener('click', async () => {
    const code = document.querySelector('#lesson-code').textContent;
    try { await navigator.clipboard.writeText(code); document.querySelector('#copy-status').textContent = 'Código copiado.'; }
    catch {
        const selection = window.getSelection();
        const range = document.createRange(); range.selectNodeContents(document.querySelector('#lesson-code'));
        selection.removeAllRanges(); selection.addRange(range);
        document.querySelector('#copy-status').textContent = 'Código seleccionado. Pulsa Ctrl+C para copiar.';
    }
});
document.querySelector('#export-notes')?.addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], {type: 'application/json;charset=utf-8'});
    const url = URL.createObjectURL(blob); const anchor = document.createElement('a');
    anchor.href = url; anchor.download = 'mi-cuaderno-django.json'; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
});
const selector = document.querySelector('#role-selector');
if (selector) {
    function renderRole() {
        const role = selector.value;
        const permissions = [['Consultar mediciones', role !== 'none'], ['Configurar umbrales', ['supervisor','admin'].includes(role)], ['Administrar catálogo', role === 'admin']];
        const output = document.querySelector('#role-output'); output.replaceChildren();
        permissions.forEach(([name, allowed]) => {
            const row = document.createElement('div'); row.className = 'capability' + (allowed ? '' : ' denied');
            const label = document.createElement('span'); label.textContent = name;
            const value = document.createElement('b'); value.textContent = allowed ? 'Permitido' : 'Denegado';
            row.append(label,value); output.append(row);
        });
    }
    selector.addEventListener('change', renderRole); renderRole();
}
document.querySelector('#conversion-form')?.addEventListener('submit', async event => {
    event.preventDefault(); const target = document.querySelector('#conversion-result');
    try {
        const response = await fetch('/api/laboratorio/temperatura/', {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({celsius: Number(document.querySelector('#celsius').value)})});
        const data = await response.json(); if (!response.ok) throw new Error(JSON.stringify(data));
        target.textContent = data.celsius + ' °C = ' + data.fahrenheit + ' °F';
    } catch (error) { target.textContent = 'Error: ' + error.message; }
});
// Exploración accesible: SVG local y controles nativos, sin librerías ni red.
document.querySelectorAll('.visual-lab').forEach(lab => {
    const controls = lab.querySelector('.map-controls');
    const nodes = [...lab.querySelectorAll('.visual-node')];
    const buttons = [...lab.querySelectorAll('.map-step')];
    const feedback = lab.querySelector('.map-feedback');
    controls.hidden = false;
    function resetMap() {
        nodes.forEach(node => node.classList.remove('is-active', 'is-muted'));
        buttons.forEach(button => button.setAttribute('aria-pressed', 'false'));
        feedback.textContent = 'Vista completa. Selecciona una pieza para destacar su responsabilidad.';
    }
    buttons.forEach(button => button.addEventListener('click', () => {
        const selected = 'node-' + button.dataset.node;
        nodes.forEach(node => {
            node.classList.toggle('is-active', node.id === selected);
            node.classList.toggle('is-muted', node.id !== selected);
        });
        buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        feedback.textContent = button.textContent.trim() + ': ' + button.dataset.detail;
    }));
    lab.querySelector('.map-reset').addEventListener('click', resetMap);
});

// Configurator: comparisons only. Never sends configuration or credentials.
const deployLab = document.querySelector('#laboratorio-entornos');
if (deployLab) {
    function renderDeployment() {
        const prod = document.querySelector('#deploy-env').value === 'prod';
        const asgi = document.querySelector('#deploy-server').value === 'asgi';
        const auth = document.querySelector('#deploy-auth').value;
        const nested = document.querySelector('#deploy-layout').value === 'nested';
        const values = [
            ['Configuración', 'config.settings.' + (prod ? 'production' : 'development')],
            ['Valores', prod ? 'Variables de entorno de App Service; secretos separados' : '.env cargado antes de base.py; fuera de Git'],
            ['DEBUG', prod ? 'False' : 'True'],
            ['Paquete', nested ? 'requirements.txt en raíz + SensorHub/ con proyecto, requirements.txt y staticfiles/' : 'manage.py y requirements.txt directamente en raíz'],
            ['Estáticos', prod ? (nested ? 'Preconstruidos; DISABLE_COLLECTSTATIC=true. Build de dependencias activado.' : 'Elegir collectstatic remoto o preconstruido y verificar el manifiesto.') : 'runserver sirve las fuentes durante desarrollo'],
            ['Arranque', prod ? (asgi ? (nested ? 'cd SensorHub && ' : '') + 'daphne -b 0.0.0.0 -p 8000 config.asgi:application' : 'gunicorn ' + (nested ? '--chdir SensorHub ' : '') + 'config.wsgi:application --bind 0.0.0.0:8000') : (asgi ? 'daphne -b 127.0.0.1 -p 8000 config.asgi:application (requiere Daphne y routing)' : 'python manage.py runserver')],
            ['Identidad', auth === 'msal' ? 'Django gestiona MSAL. App Service Authentication desactivado.' : auth === 'easy' ? (prod ? 'App Service Authentication activado con proveedor Microsoft.' : 'Easy Auth vive en Azure. Prueba en un App Service DEV; no está en runserver.') : 'Lectura pública. Sin proveedor ni callback de login.'],
            ['Retorno', auth === 'msal' ? (prod ? 'https://tu-host/aad/callback' : 'http://localhost:8000/aad/callback') : auth === 'easy' ? 'https://tu-app-azure/.auth/login/aad/callback' : 'No aplica'],
            ['Verificación', prod ? 'Build, logs, /health/, /ready/, estáticos y caso funcional' : 'check, test y petición local']
        ];
        const output = document.querySelector('#deploy-result'); output.replaceChildren();
        const list = document.createElement('dl');
        for (const [label, value] of values) {
            const row = document.createElement('div');
            const term = document.createElement('dt'); term.textContent = label;
            const desc = document.createElement('dd'); desc.textContent = value;
            row.append(term, desc); list.append(row);
        }
        output.append(list);
    }
    deployLab.querySelectorAll('select').forEach(select => select.addEventListener('change', renderDeployment));
    renderDeployment();
}

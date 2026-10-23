/* Autoevaluación y referencias locales: nunca se envían a un servidor. */
(() => {
    const KEY = 'django-professional-journey-v1';
    const NOTE_KEY = 'django-professional-course-v2';
    let notebook = { evidence: {}, checkpoints: {} };
    const object = value => value && typeof value === 'object' && !Array.isArray(value);
    try {
        const stored = JSON.parse(localStorage.getItem(KEY) || 'null');
        if (object(stored)) {
            if (object(stored.evidence)) notebook.evidence = stored.evidence;
            if (object(stored.checkpoints)) notebook.checkpoints = stored.checkpoints;
        }
    } catch {}
    function save() {
        try { localStorage.setItem(KEY, JSON.stringify(notebook)); return true; }
        catch { return false; }
    }
    function doneLessons() {
        try {
            const stored = JSON.parse(localStorage.getItem(NOTE_KEY) || 'null');
            return new Set(Array.isArray(stored?.done) ? stored.done.filter(Number.isInteger) : []);
        } catch { return new Set(); }
    }
    const stages = JSON.parse(document.querySelector('#journey-stages')?.textContent || '[]');
    function refreshProgress() {
        const done = doneLessons();
        for (const stage of stages) {
            const count = stage.lessons.filter(id => done.has(id)).length;
            document.querySelectorAll('[data-stage-progress]').forEach(element => {
                if (element.dataset.stageProgress === stage.slug) {
                    element.textContent = count ? `${count}/${stage.lessons.length} temas leídos · abrir etapa →` : 'Abrir etapa →';
                }
            });
        }
        document.querySelectorAll('[data-topic]').forEach(link => {
            const completed = done.has(Number(link.dataset.topic));
            link.classList.toggle('topic-complete', completed);
            link.querySelector('.topic-state').textContent = completed ? '✓ Tema leído' : 'Abrir →';
        });
        const resume = document.querySelector('#resume-journey');
        if (resume && done.size) {
            const next = stages.find(stage => stage.lessons.some(id => !done.has(id)));
            resume.hidden = false;
            resume.href = next ? `/ruta/${next.slug}/#temas` : '/ruta/entregar/#entrega';
            resume.textContent = next ? `Continuar: ${next.title} →` : 'Temas principales leídos: revisar mi entrega →';
        }
    }
    refreshProgress();
    window.addEventListener('storage', refreshProgress);
    document.querySelector('#complete')?.addEventListener('click', refreshProgress);
    document.querySelectorAll('.checkpoint-form').forEach(form => {
        const key = form.dataset.stage;
        const stored = notebook.checkpoints[key];
        const boxes = [...form.querySelectorAll('input[type=checkbox]')];
        boxes.forEach((box, index) => { box.checked = Array.isArray(stored) && stored[index] === true; });
        form.addEventListener('change', () => {
            notebook.checkpoints[key] = boxes.map(box => box.checked);
            form.querySelector('.checkpoint-status').textContent = save()
                ? 'Autoevaluación guardada en este navegador. Las evidencias se verifican por separado.'
                : 'No se pudo guardar. Conserva una copia de tu autoevaluación.';
        });
    });
    const forms = [...document.querySelectorAll('.evidence-form')];
    const fields = ['status', 'owner', 'evidence'];
    function capture(form) {
        const values = {};
        fields.forEach(field => { values[field] = form.elements.namedItem(field).value; });
        notebook.evidence[form.dataset.control] = values;
    }
    forms.forEach(form => {
        const values = notebook.evidence[form.dataset.control];
        if (object(values)) fields.forEach(field => {
            const input = form.elements.namedItem(field);
            if (typeof values[field] === 'string') input.value = values[field];
        });
        form.addEventListener('submit', event => {
            event.preventDefault(); capture(form);
            form.querySelector('.evidence-feedback').textContent = save()
                ? 'Respuesta guardada. Conserva la prueba y la aprobación referenciadas en tu expediente.'
                : 'No se pudo guardar. Descarga una copia antes de salir.';
        });
    });
    document.querySelector('#export-evidence')?.addEventListener('click', () => {
        forms.forEach(capture);
        const saved = save();
        const lines = ['# Mi matriz de aceptación · borrador didáctico', '',
            'Autoevaluación del autor de las respuestas. No certifica cumplimiento ni sustituye la aceptación del cliente.', '',
            'Completar por requisito: documento y versión, obligatoriedad, responsable, implementación, evidencia, prueba, brecha, fecha y decisión autorizada.', ''];
        forms.forEach(form => {
            const values = notebook.evidence[form.dataset.control];
            const select = form.elements.namedItem('status');
            lines.push(`## ${form.dataset.title}`, '', `Estado: ${select.selectedOptions[0]?.textContent || 'Por evaluar'}`,
                `Responsable: ${values.owner || 'Por definir'}`, '', values.evidence || 'Evidencia, prueba y siguiente acción: pendientes.', '');
        });
        const url = URL.createObjectURL(new Blob([lines.join('\n')], { type: 'text/markdown;charset=utf-8' }));
        const anchor = document.createElement('a');
        anchor.href = url; anchor.download = 'mi-matriz-aceptacion.md'; anchor.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        document.querySelector('#evidence-status').textContent = saved ? 'Matriz descargada; respuestas guardadas en este navegador.' : 'Matriz descargada; el navegador no permitió guardar las respuestas.';
    });
})();

let _faltas = {}   // { alumnoId: horas } del módulo activo
let _fases  = {}   // { alumnoId: 'pendiente'|'superada'|'no_superada'|'exenta' }
let _matri  = {}   // { alumnoId: {convocatorias, pendiente} }

async function loadAlumnos() {
  const mid = document.getElementById('alumnos-mod-sel').value
  if (!mid) return
  _alumnos = await window.api.getAlumnos(mid)
  // Faltas de asistencia por alumno (art. 3.3 de la Orden 201/2024)
  _faltas = {}
  try {
    const cfg = await window.api.getAllConfig()
    const pref = `faltas_${mid}_`
    for (const [k, v] of Object.entries(cfg)) {
      if (k.startsWith(pref) && String(v).trim() !== '') _faltas[Number(k.slice(pref.length))] = parseFloat(v)
    }
  } catch { /* sin faltas registradas */ }
  // Estado de la fase de formación en empresa (Orden 201/2024, art. 12)
  _fases = {}
  try {
    const filas = await window.api.getFaseEmpresa(parseInt(mid))
    filas.forEach(f => { _fases[Number(f.alumno_id)] = f.estado })
  } catch { /* base antigua sin la tabla */ }
  // Convocatorias gastadas y módulos que se arrastran de otro curso
  _matri = {}
  try {
    const filas = await window.api.getMatriculas(parseInt(mid))
    filas.forEach(f => { _matri[Number(f.alumno_id)] = { convocatorias: f.convocatorias, pendiente: f.pendiente } })
  } catch { /* base antigua sin la tabla */ }
  renderAlumnosTable()
}

/** Máximo de convocatorias ordinarias: 4 en grado D, 2 en grado E (art. 8.2). */
function _maxConvocatorias(mid) {
  const data = _getModData(mid)
  const nivel = String(data?.modulo?.ciclo_nivel || '').toUpperCase()
  return nivel === 'CE' ? 2 : 4
}

async function updateMatricula(alumnoId, campo, valor) {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  if (!mid) return
  const actual = _matri[alumnoId] || { convocatorias: 0, pendiente: 0 }
  const nuevo = { ...actual, [campo]: campo === 'pendiente' ? (valor ? 1 : 0) : (parseInt(valor, 10) || 0) }
  const tope = _maxConvocatorias(mid)
  if (campo === 'convocatorias' && nuevo.convocatorias > tope) {
    alert(`En esta enseñanza el máximo son ${tope} convocatorias ordinarias (Orden 201/2024, art. 8.2).\n` +
          'Agotadas, hace falta una convocatoria extraordinaria concedida por la dirección (art. 9).')
  }
  try {
    await window.api.setMatricula({ alumnoId, ...nuevo })
    _matri[alumnoId] = nuevo
    showSaved()
    renderAlumnosTable()
  } catch (e) {
    alert('No se ha podido guardar: ' + (e && e.message ? e.message : e))
  }
}

/** ¿El módulo activo tiene fase de formación en empresa? */
function _moduloTieneFase(mid) {
  const data = _getModData(mid)
  return moduloConFaseEmpresa(data?.modulo)
}

/** Estado de la fase de empresa de un alumno. */
async function updateFaseEmpresa(alumnoId, estado) {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  if (!mid) return
  let motivo = null
  if (estado === 'exenta') {
    motivo = prompt('Exención de la fase de empresa (art. 22): ¿en qué se basa?\n' +
                    'Por ejemplo: experiencia laboral acreditada de un año.', '')
    if (motivo === null) { renderAlumnosTable(); return }
  }
  try {
    await window.api.setFaseEmpresa({ alumnoId, estado, motivo })
    _fases[alumnoId] = estado
    showSaved()
    renderAlumnosTable()
  } catch (e) {
    alert('No se ha podido guardar: ' + (e && e.message ? e.message : e))
  }
}

function renderAlumnosTable() {
  const tbody = document.getElementById('alumnos-tbody')
  if (!_alumnos.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" style="padding:0">
          <div class="empty-state" style="margin:0">
            <div style="font-weight:700;color:var(--text);margin-bottom:6px">Todavía no hay alumnado en este módulo</div>
            <div style="margin-bottom:12px">Importa una lista o añade el primer alumno para empezar a trabajar.</div>
            <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
              <button class="btn btn-ghost btn-sm" onclick="importAlumnos()">📋 Importar lista</button>
              <button class="btn btn-primary btn-sm" onclick="addAlumno()">＋ Añadir alumno</button>
            </div>
          </div>
        </td>
      </tr>`
    document.getElementById('alumnos-footer').textContent = 'Consejo: puedes importar apellidos y nombre en una sola línea por alumno.'
    return
  }
  tbody.innerHTML = _alumnos.map(a => `
    <tr>
      <td><input value="${a.num||''}" style="width:36px" onblur="updateAlumno(${a.id},'num',this.value)"/></td>
      <td><input value="${esc(a.apellidos||'')}" onblur="updateAlumno(${a.id},'apellidos',this.value)"/></td>
      <td><input value="${esc(a.nombre||'')}" onblur="updateAlumno(${a.id},'nombre',this.value)"/></td>
      <td><input value="${esc(a.email||'')}" onblur="updateAlumno(${a.id},'email',this.value)"/></td>
      <td>${_celdaFaltas(a)}</td>
      <td>${_celdaFase(a)}</td>
      <td>${_celdaMatricula(a)}</td>
      <td>
        <select onchange="updateAlumno(${a.id},'estado',this.value)">
          <option ${a.estado==='Activo'?'selected':''}>Activo</option>
          <option ${a.estado==='Pendiente'?'selected':''}>Pendiente</option>
          <option ${a.estado==='Renuncia'?'selected':''}>Renuncia</option>
          <option ${a.estado==='Baja'?'selected':''}>Baja</option>
        </select>
      </td>
      <td><button class="btn btn-ghost btn-sm" onclick="removeAlumno(${a.id})" aria-label="Eliminar alumno" style="padding:3px 8px">✕</button></td>
    </tr>
  `).join('')
  const activos = _alumnos.filter(a => a.estado === 'Activo').length
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  const enRiesgo = _aplicaEvaluacionContinua(mid)
    ? _alumnos.filter(a => _porcentajeFalta(mid, a.id) > 25).length : 0
  document.getElementById('alumnos-footer').textContent =
    `${_alumnos.length} alumnos/as · ${activos} activos · ${_alumnos.length - activos} fuera de activo` +
    (enRiesgo ? ` · ⚠ ${enRiesgo} por debajo del 75 % de asistencia` : '') +
    (_moduloTieneFase(mid)
      ? ` · fase de empresa: ${_alumnos.filter(a => ['superada', 'exenta'].includes(_fases[a.id])).length} resuelta(s)`
      : '')
}

/**
 * Celda de la fase de formación en empresa. Solo tiene sentido en los módulos
 * que la tienen: en el resto se deja en blanco para no ensuciar la tabla.
 */
function _celdaFase(a) {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  if (!_moduloTieneFase(mid)) return '<span style="color:var(--text3);font-size:11px">—</span>'
  const est = _fases[a.id] || 'pendiente'
  const opciones = [
    ['pendiente',   'Pendiente'],
    ['superada',    'Superada'],
    ['no_superada', 'No superada'],
    ['exenta',      'Exenta'],
  ].map(([v, t]) => `<option value="${v}"${est === v ? ' selected' : ''}>${t}</option>`).join('')
  const color = est === 'superada' || est === 'exenta' ? 'var(--green)'
    : est === 'no_superada' ? 'var(--red)' : 'var(--text2)'
  return `<select onchange="updateFaseEmpresa(${a.id},this.value)"
      title="Fase de formación en empresa. Con todo lo del centro alcanzado y esta fase pendiente, el módulo queda «superado parcial» (Orden 201/2024, art. 12)."
      style="width:104px;font-size:11px;color:${color}">${opciones}</select>`
}

/**
 * Convocatorias gastadas y arrastre del módulo de otro curso.
 * El recuento lo lleva la secretaría del centro, pero tenerlo a la vista evita
 * evaluar a quien ya no tiene convocatorias (art. 8.2) y recordar quién viene con
 * el módulo pendiente, que se evalúa en las sesiones de este curso (art. 19).
 */
function _celdaMatricula(a) {
  const mid  = parseInt(document.getElementById('alumnos-mod-sel').value)
  const m    = _matri[a.id] || { convocatorias: 0, pendiente: 0 }
  const tope = _maxConvocatorias(mid)
  const agotadas = m.convocatorias >= tope
  return `<div style="display:flex;align-items:center;gap:5px;white-space:nowrap">
    <input type="number" min="0" max="9" value="${m.convocatorias || 0}"
      title="Convocatorias ordinarias ya consumidas. Máximo ${tope} en esta enseñanza (art. 8.2). La renuncia y la anulación no cuentan."
      style="width:44px;${agotadas ? 'color:var(--red);font-weight:700' : ''}"
      onblur="updateMatricula(${a.id},'convocatorias',this.value)"/>
    <span style="font-size:10px;color:${agotadas ? 'var(--red)' : 'var(--text3)'}">/${tope}${agotadas ? ' ⚠' : ''}</span>
    <label title="Arrastra este módulo de un curso anterior: se evalúa en las sesiones ordinarias del curso en el que está matriculado (art. 19)"
           style="display:inline-flex;align-items:center;gap:3px;font-size:10px;color:var(--text3);cursor:pointer">
      <input type="checkbox" ${m.pendiente ? 'checked' : ''}
        onchange="updateMatricula(${a.id},'pendiente',this.checked)"
        style="accent-color:var(--accent);width:12px;height:12px"/>pend.
    </label>
  </div>`
}

/** Porcentaje de horas faltadas sobre las horas del módulo. */
function _porcentajeFalta(mid, alumnoId) {
  const horas = _horasModulo(mid)
  const f = _faltas[alumnoId]
  if (!horas || f == null) return 0
  return (f / horas) * 100
}

/** Celda de faltas con el aviso del 75 % de asistencia. */
function _celdaFaltas(a) {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  const aplica = _aplicaEvaluacionContinua(mid)
  const pct = _porcentajeFalta(mid, a.id)
  const pierde = aplica && pct > 25
  const etiqueta = _faltas[a.id] == null ? ''
    : `<span title="${pct.toFixed(1)} % de las horas del módulo"
             style="font-size:10px;font-weight:700;margin-left:4px;color:${pierde ? 'var(--red)' : 'var(--text3)'}">
         ${pct.toFixed(0)}%${pierde ? ' ⚠' : ''}
       </span>`
  const ayuda = aplica
    ? 'Horas de falta. Por encima del 25 % de las horas del módulo se pierde el derecho a la evaluación continua (Orden 201/2024, art. 3.3).'
    : 'Horas de falta. En grado básico no se aplica la pérdida de evaluación continua (art. 3.4).'
  return `<input type="number" min="0" step="1" value="${_faltas[a.id] ?? ''}" placeholder="—"
      title="${ayuda}" style="width:52px" onblur="updateFaltas(${a.id},this.value)"/>${etiqueta}`
}

function updateAlumno(id, field, val) {
  clearTimeout(_updateTimers[id+field])
  _updateTimers[id+field] = setTimeout(async () => {
    const a = _alumnos.find(x => x.id === id)
    if (!a) return

    const oldVal = a[field]  // guardar para rollback en caso de error

    try {
      // Validar campo y calcular el nuevo valor antes de modificar el objeto
      let newVal
      switch(field) {
        case 'num':
          if (!validators.moduleNumber(val)) { alert('Número de alumno inválido (1-999)'); return }
          newVal = parseInt(val) || null
          break
        case 'apellidos':
        case 'nombre':
          if (!validators.text(val, 100)) { alert(`${field} debe tener máximo 100 caracteres`); return }
          newVal = val
          break
        case 'email':
          if (!validators.email(val)) { alert('Email inválido'); return }
          newVal = val
          break
        case 'telefono':
          if (!validators.phone(val)) { alert('Teléfono inválido'); return }
          newVal = val
          break
        case 'estado':
          // «Renuncia» es la renuncia a convocatoria del art. 11 de la Orden
          // 201/2024, que en actas se refleja como «RC» (art. 25.9).
          if (!['Activo', 'Pendiente', 'Renuncia', 'Baja'].includes(val)) { alert('Estado inválido'); return }
          newVal = val
          break
        default:
          newVal = val
      }

      // Aplicar el cambio al objeto en memoria
      a[field] = newVal

      // Validar el objeto completo antes de guardar
      if (!validators.alumno(a)) {
        a[field] = oldVal  // rollback
        alert('Datos de alumno inválidos. Revisa todos los campos.')
        return
      }

      await window.api.saveAlumno(a)
      // ✅ Guardado con éxito — newVal ya es la verdad
    } catch(e) {
      a[field] = oldVal       // rollback: restaurar valor original en memoria
      renderAlumnosTable()    // re-renderizar con el valor antiguo
      alert('Error: ' + validators.sanitizeErrorMessage(e, 'updateAlumno'))
      console.error(e)
    }
  }, 400)
}

/**
 * Horas de falta del alumno en el módulo, con el porcentaje sobre las horas de
 * aula y el aviso del 75 % (Orden 201/2024, art. 3.3: por debajo de ese
 * porcentaje se pierde el derecho a la evaluación continua en grado medio,
 * superior y cursos de especialización; art. 3.4: no aplica en grado básico).
 */
async function updateFaltas(alumnoId, horas) {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  if (!mid) return
  const h = String(horas).trim() === '' ? null : parseFloat(horas)
  if (h !== null && (isNaN(h) || h < 0)) { alert('Horas de falta inválidas.'); return }
  try {
    await window.api.setConfig(`faltas_${mid}_${alumnoId}`, h === null ? '' : String(h))
    showSaved()
    renderAlumnosTable()
  } catch (e) {
    alert('No se han podido guardar las faltas: ' + (e && e.message ? e.message : e))
  }
}

/** Horas lectivas del módulo sobre las que se calcula el porcentaje de falta. */
function _horasModulo(mid) {
  const data = _getModData(mid)
  return parseInt(data?.modulo?.horas_aula, 10) ||
         parseInt(data?.modulo?.total_horas, 10) ||
         (_modulos.find(m => m.id == mid)?.horas || 0)
}

/** ¿Este módulo puede perder la evaluación continua? En grado básico, no. */
function _aplicaEvaluacionContinua(mid) {
  const data = _getModData(mid)
  const nivel = String(data?.modulo?.ciclo_nivel || '').toUpperCase()
  return nivel !== 'CFGB'
}

async function addAlumno() {
  const mid = document.getElementById('alumnos-mod-sel').value
  if (!mid) { alert('Selecciona un módulo primero.'); return }

  // Rate limiting: prevent spam
  if (!rateLimiters.database.check('addAlumno')) {
    alert('Demasiadas solicitudes. Espera un momento.')
    return
  }

  try {
    const nextNum = _alumnos.length ? Math.max(..._alumnos.map(a=>a.num||0)) + 1 : 1

    // Validate new alumno object
    const newAlumno = {
      modulo_id: parseInt(mid),
      num: nextNum,
      estado: 'Activo',
      apellidos: '',
      nombre: '',
      email: '',
      telefono: '',
      observaciones: ''
    }

    if (!validators.alumno(newAlumno)) {
      alert('Error: No se pudo crear alumno con datos inválidos.')
      return
    }

    const id = await window.api.saveAlumno(newAlumno)
    _alumnos.push({ id, ...newAlumno })
    renderAlumnosTable()
    document.getElementById('alumnos-footer').textContent = `${_alumnos.length} alumnos/as · ${_alumnos.filter(a => a.estado === 'Activo').length} activos · nuevo alumno añadido`
    setTimeout(() => {
      const rows = document.getElementById('alumnos-tbody').querySelectorAll('tr')
      const last = rows[rows.length-1]
      last?.querySelectorAll('input')[1]?.focus()
    }, 50)
  } catch(e) {
    alert('Error al guardar alumno: ' + validators.sanitizeErrorMessage(e, 'addAlumno'))
    console.error(e)
  }
}

function importAlumnos() {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  if (!mid) { alert('Selecciona un módulo primero.'); return }
  document.getElementById('import-alumnos-txt').value = ''
  document.getElementById('dlg-import-alumnos').showModal()
}

async function confirmImportAlumnos() {
  const mid = parseInt(document.getElementById('alumnos-mod-sel').value)
  const txt = document.getElementById('import-alumnos-txt').value
  if (!txt.trim()) return

  // Rate limiting for bulk operations
  if (!rateLimiters.database.check('importAlumnos')) {
    alert('Demasiadas solicitudes. Espera un momento.')
    return
  }

  document.getElementById('dlg-import-alumnos').close()
  try {
    const lines = txt.trim().split('\n').filter(Boolean)
    const maxNum = _alumnos.reduce((m, a) => Math.max(m, a.num || 0), 0)
    let imported = 0
    let skipped  = 0
    for (let i = 0; i < lines.length; i++) {
      const parts = lines[i].split(',').map(s => s.trim())
      const apellidos = parts[0] || ''
      const nombre = parts[1] || ''

      // Detectar duplicado: mismo apellidos+nombre ya en el módulo
      const isDuplicate = _alumnos.some(a =>
        a.apellidos.toLowerCase() === apellidos.toLowerCase() &&
        a.nombre.toLowerCase()    === nombre.toLowerCase()
      )
      if (isDuplicate) { skipped++; continue }

      // Con el máximo, no con el recuento: si se ha dado de baja a alguien de
      // en medio, contar filas repite un número de lista que ya existe, y ese
      // número es el que identifica al alumnado en la corrección anónima.
      const num = maxNum + imported + 1

      // Validate each imported alumno
      const alumnoData = {
        modulo_id: mid,
        num,
        apellidos,
        nombre,
        estado: 'Activo',
        email: '',
        telefono: '',
        observaciones: ''
      }

      if (!validators.alumno(alumnoData)) {
        console.warn(`Alumno ${i+1} inválido:`, alumnoData)
        continue
      }

      const id = await window.api.saveAlumno(alumnoData)
      _alumnos.push({ id, ...alumnoData })
      imported++
    }
    renderAlumnosTable()
    const msg = skipped > 0
      ? `Se importaron ${imported} de ${lines.length} alumnos. ${skipped} omitidos por duplicado.`
      : `Se importaron ${imported} de ${lines.length} alumnos correctamente.`
    alert(msg)
  } catch(e) {
    alert('Error al importar: ' + validators.sanitizeErrorMessage(e, 'confirmImportAlumnos'))
    console.error(e)
  }
}

async function removeAlumno(id) {
  if (!confirm('¿Eliminar este alumno y todas sus notas?')) return
  await window.api.deleteAlumno(id)
  _alumnos = _alumnos.filter(a => a.id !== id)
  renderAlumnosTable()
}

// ── Enter en tabla de alumnos mueve al siguiente campo ──────────
document.addEventListener('keydown', function(e) {
  const el = e.target
  if (e.key !== 'Enter') return
  const td = el.closest('td')
  if (!td || td.closest('#alumnos-tbody') === null) return
  // Tab al siguiente input de la misma fila
  const row = el.closest('tr')
  const inputs = Array.from(row.querySelectorAll('input,select'))
  const i = inputs.indexOf(el)
  if (i >= 0 && i < inputs.length - 1) {
    inputs[i + 1].focus()
    if (inputs[i + 1].select) inputs[i + 1].select()
    e.preventDefault()
  }
})

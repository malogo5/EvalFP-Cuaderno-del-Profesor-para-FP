async function loadAlumnos() {
  const mid = document.getElementById('alumnos-mod-sel').value
  if (!mid) return
  _alumnos = await window.api.getAlumnos(mid)
  renderAlumnosTable()
}

function renderAlumnosTable() {
  const tbody = document.getElementById('alumnos-tbody')
  const mod = _modulos.find(m => m.id == document.getElementById('alumnos-mod-sel').value)
  if (!_alumnos.length) {
    tbody.innerHTML = '<tr><td colspan="6" style="color:var(--text2);text-align:center;padding:20px">Sin alumnos. Añade el primero.</td></tr>'
    document.getElementById('alumnos-footer').textContent = ''
    return
  }
  tbody.innerHTML = _alumnos.map(a => `
    <tr>
      <td><input value="${a.num||''}" style="width:36px" onblur="updateAlumno(${a.id},'num',this.value)"/></td>
      <td><input value="${esc(a.apellidos||'')}" onblur="updateAlumno(${a.id},'apellidos',this.value)"/></td>
      <td><input value="${esc(a.nombre||'')}" onblur="updateAlumno(${a.id},'nombre',this.value)"/></td>
      <td><input value="${esc(a.email||'')}" onblur="updateAlumno(${a.id},'email',this.value)"/></td>
      <td>
        <select onchange="updateAlumno(${a.id},'estado',this.value)">
          <option ${a.estado==='Activo'?'selected':''}>Activo</option>
          <option ${a.estado==='Pendiente'?'selected':''}>Pendiente</option>
          <option ${a.estado==='Baja'?'selected':''}>Baja</option>
        </select>
      </td>
      <td><button class="btn btn-ghost btn-sm" onclick="removeAlumno(${a.id})" aria-label="Eliminar alumno" style="padding:3px 8px">✕</button></td>
    </tr>
  `).join('')
  const activos = _alumnos.filter(a => a.estado === 'Activo').length
  document.getElementById('alumnos-footer').textContent =
    `${_alumnos.length} alumnos/as · ${activos} activos`
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
          if (!['Activo', 'Pendiente', 'Baja'].includes(val)) { alert('Estado inválido'); return }
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

      const num = _alumnos.length + imported + 1

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

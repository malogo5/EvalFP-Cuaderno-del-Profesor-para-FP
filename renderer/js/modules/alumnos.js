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
    tbody.innerHTML = '<tr><td colspan="7" style="color:var(--text2);text-align:center;padding:20px">Sin alumnos. Añade el primero.</td></tr>'
    document.getElementById('alumnos-footer').textContent = ''
    return
  }
  tbody.innerHTML = _alumnos.map(a => `
    <tr>
      <td><input value="${a.num||''}" style="width:36px" onblur="updateAlumno(${a.id},'num',this.value)"/></td>
      <td><input value="${esc(a.apellidos||'')}" onblur="updateAlumno(${a.id},'apellidos',this.value)"/></td>
      <td><input value="${esc(a.nombre||'')}" onblur="updateAlumno(${a.id},'nombre',this.value)"/></td>
      <td><input value="${esc(a.nia||'')}" onblur="updateAlumno(${a.id},'nia',this.value)"/></td>
      <td><input value="${esc(a.email||'')}" onblur="updateAlumno(${a.id},'email',this.value)"/></td>
      <td>
        <select onchange="updateAlumno(${a.id},'estado',this.value)">
          <option ${a.estado==='Activo'?'selected':''}>Activo</option>
          <option ${a.estado==='Pendiente'?'selected':''}>Pendiente</option>
          <option ${a.estado==='Baja'?'selected':''}>Baja</option>
        </select>
      </td>
      <td><button class="btn btn-ghost btn-sm" onclick="removeAlumno(${a.id})" style="padding:3px 8px">✕</button></td>
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
    a[field] = field === 'num' ? (parseInt(val)||null) : val
    await window.api.saveAlumno(a)
  }, 400)
}

async function addAlumno() {
  const mid = document.getElementById('alumnos-mod-sel').value
  if (!mid) { alert('Selecciona un módulo primero.'); return }
  try {
    const nextNum = _alumnos.length ? Math.max(..._alumnos.map(a=>a.num||0)) + 1 : 1
    const id = await window.api.saveAlumno({ modulo_id: parseInt(mid), num: nextNum, estado: 'Activo' })
    _alumnos.push({ id, modulo_id: parseInt(mid), num: nextNum, estado: 'Activo',
      apellidos:'', nombre:'', nia:'', email:'', telefono:'', observaciones:'' })
    renderAlumnosTable()
    setTimeout(() => {
      const rows = document.getElementById('alumnos-tbody').querySelectorAll('tr')
      const last = rows[rows.length-1]
      last?.querySelectorAll('input')[1]?.focus()
    }, 50)
  } catch(e) {
    alert('Error al guardar alumno: ' + e.message)
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
  document.getElementById('dlg-import-alumnos').close()
  try {
    const lines = txt.trim().split('\n').filter(Boolean)
    for (let i = 0; i < lines.length; i++) {
      const parts = lines[i].split(',').map(s => s.trim())
      const apellidos = parts[0] || ''
      const nombre = parts[1] || ''
      const num = _alumnos.length + i + 1
      const id = await window.api.saveAlumno({ modulo_id: mid, num, apellidos, nombre, estado:'Activo' })
      _alumnos.push({ id, modulo_id: mid, num, apellidos, nombre, estado:'Activo',
        nia:'', email:'', telefono:'', observaciones:'' })
    }
    renderAlumnosTable()
  } catch(e) {
    alert('Error al importar: ' + e.message)
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

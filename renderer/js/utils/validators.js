/**
 * Input Validation Framework for EvalFP
 */

'use strict'

const validators = {
  /**
   * Email validation — campo opcional
   */
  email: (value) => {
    if (value === null || value === undefined) return true
    if (typeof value !== 'string') return false
    const trimmed = value.trim()
    if (trimmed.length === 0) return true   // campo opcional
    if (trimmed.length > 255) return false
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed)
  },

  /**
   * Teléfono — campo opcional (acepta vacío)
   */
  phone: (value) => {
    if (value === null || value === undefined) return true
    if (typeof value !== 'string') return false
    const trimmed = value.trim()
    if (trimmed.length === 0) return true   // campo opcional
    if (trimmed.length > 20) return false
    return /^(\+34|0034|34)?[69]\d{8}$|^\d+$/.test(trimmed.replace(/[\s\-()]/g, ''))
  },

  /**
   * Fecha YYYY-MM-DD — campo opcional
   */
  date: (value) => {
    if (value === null || value === undefined) return true
    if (typeof value !== 'string') return false
    const trimmed = value.trim()
    if (trimmed.length === 0) return true
    if (!/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) return false
    const d = new Date(trimmed)
    return d instanceof Date && !isNaN(d.getTime())
  },

  /**
   * NIA — campo opcional (8 dígitos + letra opcional)
   */
  nia: (value) => {
    if (value === null || value === undefined) return true
    if (typeof value !== 'string') return false
    const trimmed = value.trim().toUpperCase()
    if (trimmed.length === 0) return true   // campo opcional
    if (trimmed.length > 9) return false
    return /^\d{8}[A-Z]?$/.test(trimmed)
  },

  /**
   * Texto libre — solo bloquea XSS (<script>, tags HTML)
   * Permite em dash, puntuación, acentos, etc.
   */
  text: (value, maxLength = 255) => {
    if (value === null || value === undefined) return true
    if (typeof value !== 'string') return false
    const trimmed = value.trim()
    if (trimmed.length > maxLength) return false
    // Solo rechazar etiquetas HTML/script (XSS básico)
    return !/<[^>]*>|<script/i.test(trimmed)
  },

  /**
   * Rango numérico
   */
  numberRange: (value, min = 0, max = 100) => {
    if (value === null || value === undefined || value === '') return true
    const num = parseFloat(value)
    if (isNaN(num)) return false
    return num >= min && num <= max
  },

  /**
   * Entero positivo
   */
  integer: (value) => {
    if (value === null || value === undefined || value === '') return true
    const num = parseInt(value, 10)
    return Number.isInteger(num) && num > 0
  },

  /**
   * Número de alumno (1-999)
   */
  moduleNumber: (value) => {
    if (value === null || value === undefined || value === '') return true
    const num = parseInt(String(value).trim(), 10)
    return !isNaN(num) && num > 0 && num <= 999
  },

  activityName:  (value) => validators.text(value, 100),
  description:   (value) => validators.text(value, 500),

  /**
   * Objeto alumno completo
   */
  alumno: (alumno) => {
    if (!alumno || typeof alumno !== 'object') return false
    const { modulo_id, num, apellidos, nombre, fecha_nacim,
            email, telefono, estado, observaciones, id } = alumno

    if (id !== undefined && !validators.integer(id)) return false
    if (!validators.integer(modulo_id)) return false
    if (!validators.moduleNumber(num)) return false
    if (!validators.text(apellidos, 100)) return false
    if (!validators.text(nombre, 100)) return false
    if (!validators.date(fecha_nacim)) return false
    if (!validators.email(email)) return false
    if (!validators.phone(telefono)) return false
    // Estados válidos de la app
    if (estado && !['Activo', 'Pendiente', 'Baja'].includes(estado)) return false
    if (!validators.description(observaciones)) return false
    return true
  },

  /**
   * Objeto actividad completo
   */
  actividad: (actividad) => {
    if (!actividad || typeof actividad !== 'object') return false
    const { modulo_id, descripcion, peso, nota_max, id } = actividad
    if (id !== undefined && !validators.integer(id)) return false
    if (!validators.integer(modulo_id)) return false
    if (!validators.description(descripcion)) return false
    if (!validators.numberRange(peso, 0, 100)) return false
    if (!validators.numberRange(nota_max, 0, 20)) return false
    return true
  },

  nota:        (value) => validators.numberRange(value, 0, 10),
  ponderacion: (value) => validators.numberRange(value, 0, 100),

  /**
   * API Key (mínimo 10 chars)
   */
  apiKey: (value) => {
    if (!value || typeof value !== 'string') return false
    const trimmed = value.trim()
    return trimmed.length >= 10 && trimmed.length <= 500
  },

  provider: (value) => ['auto', 'claude', 'openai', 'demo'].includes(value),

  /**
   * Mensaje de error amigable (oculta detalles técnicos)
   */
  sanitizeErrorMessage: (error, context = '') => {
    const msg = (error?.message || String(error)).toLowerCase()
    if (msg.includes('sql') || msg.includes('database')) return 'Error de base de datos. Inténtalo de nuevo.'
    if (msg.includes('permission') || msg.includes('eacces')) return 'Sin permisos para realizar esta operación.'
    if (msg.includes('enoent') || msg.includes('not found')) return 'Archivo no encontrado.'
    if (msg.includes('network') || msg.includes('timeout')) return 'Error de red. Comprueba la conexión.'
    if (/<|>|script/i.test(msg)) return 'Entrada no válida.'
    return 'Ha ocurrido un error. Inténtalo de nuevo.'
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = validators
}

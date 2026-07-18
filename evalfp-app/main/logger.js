'use strict'
const winston = require('winston')
const path = require('path')
const os = require('os')

// Directorio para logs (misma ubicación que backups)
const logsDir = path.join(os.homedir(), 'Documents', 'EvalFP', 'logs')

// Crear directorio si no existe
const fs = require('fs')
fs.mkdirSync(logsDir, { recursive: true })

// Formato personalizado
const customFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json()
)

// Logger instance
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: customFormat,
  defaultMeta: { service: 'EvalFP' },
  transports: [
    // Error file (solo errores)
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 7, // 7 días
    }),
    // Combined file (todo)
    new winston.transports.File({
      filename: path.join(logsDir, 'combined.log'),
      maxsize: 5242880, // 5MB
      maxFiles: 30, // 30 días
    }),
  ],
})

// Agregar consola en desarrollo
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.printf(({ level, message, timestamp, ...meta }) => {
        const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : ''
        return `${timestamp} [${level}]: ${message} ${metaStr}`
      })
    ),
  }))
}

// Métodos de conveniencia
logger.logError = (message, error = {}) => {
  logger.error(message, {
    errorMessage: error.message,
    errorStack: error.stack,
    ...error,
  })
}

logger.logEvent = (event, data = {}) => {
  logger.info(`EVENT: ${event}`, { event, ...data })
}

module.exports = logger

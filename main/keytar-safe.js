'use strict'

/**
 * Safe Keytar Wrapper
 * 
 * This module safely wraps the keytar native module.
 * If keytar fails to load (common on macOS without native build),
 * it provides a stub that uses database storage instead.
 */

class KeytarStub {
  constructor(available = false) {
    this.available = available
    this.instance = null
  }

  async initialize() {
    try {
      // Try to load the real keytar module
      this.instance = require('keytar')
      this.available = true
      return true
    } catch (err) {
      // Keytar not available - use stub mode
      this.available = false
      return false
    }
  }

  async getPassword(service, account) {
    if (this.instance && this.available) {
      try {
        return await this.instance.getPassword(service, account)
      } catch (err) {
        console.warn(`Keytar getPassword failed: ${err.message}`)
        return null
      }
    }
    return null
  }

  async setPassword(service, account, password) {
    if (this.instance && this.available) {
      try {
        return await this.instance.setPassword(service, account, password)
      } catch (err) {
        console.warn(`Keytar setPassword failed: ${err.message}`)
        return false
      }
    }
    return false
  }

  async deletePassword(service, account) {
    if (this.instance && this.available) {
      try {
        return await this.instance.deletePassword(service, account)
      } catch (err) {
        console.warn(`Keytar deletePassword failed: ${err.message}`)
        return false
      }
    }
    return false
  }

  isAvailable() {
    return this.available && !!this.instance
  }
}

module.exports = new KeytarStub()

/**
 * Rate Limiting Module for EvalFP
 * Prevents abuse of API calls and Python script execution
 */

'use strict'

class RateLimiter {
  constructor(limit = 10, windowMs = 60000) {
    this.limit = limit
    this.windowMs = windowMs
    this.requests = new Map()
  }

  check(key) {
    const now = Date.now()
    const windowStart = now - this.windowMs
    
    // Clean old entries
    for (const [k, times] of this.requests.entries()) {
      const recent = times.filter(t => t > windowStart)
      if (recent.length === 0) {
        this.requests.delete(k)
      } else {
        this.requests.set(k, recent)
      }
    }

    // Check limit for this key
    const times = this.requests.get(key) || []
    if (times.length >= this.limit) {
      return false
    }

    // Record this request
    times.push(now)
    this.requests.set(key, times)
    return true
  }

  reset(key) {
    this.requests.delete(key)
  }

  resetAll() {
    this.requests.clear()
  }
}

// Define rate limiters for different operations
const rateLimiters = {
  // Database operations: 20 per minute
  database: new RateLimiter(20, 60000),
  
  // API key saves: 5 per minute (sensitive)
  apiKeys: new RateLimiter(5, 60000),
  
  // Python script execution: 10 per minute (resource intensive)
  pythonScripts: new RateLimiter(10, 60000),
  
  // PDF export: 3 per minute (very resource intensive)
  pdfExport: new RateLimiter(3, 60000),
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { RateLimiter, rateLimiters }
}

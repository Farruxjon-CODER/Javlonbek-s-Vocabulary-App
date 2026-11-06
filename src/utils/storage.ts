/**
 * Centralized LocalStorage abstraction
 * All localStorage access goes through this module
 */

const PREFIX = 'javlonbek_lc_'
const LEGACY_PREFIX = 'lexiflow_'

function getKey(key: string): string {
  return `${PREFIX}${key}`
}

function getLegacyKey(key: string): string {
  return `${LEGACY_PREFIX}${key}`
}

export function getItem<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(getKey(key)) ?? localStorage.getItem(getLegacyKey(key))
    if (raw === null) return fallback
    return JSON.parse(raw) as T
  } catch {
    return fallback
  }
}

export function setItem<T>(key: string, value: T): void {
  try {
    localStorage.setItem(getKey(key), JSON.stringify(value))
  } catch (e) {
    console.warn('LocalStorage write failed:', e)
  }
}

export function removeItem(key: string): void {
  localStorage.removeItem(getKey(key))
  localStorage.removeItem(getLegacyKey(key))
}

export function clearAll(): void {
  const keys = Object.keys(localStorage).filter(
    k => k.startsWith(PREFIX) || k.startsWith(LEGACY_PREFIX)
  )
  keys.forEach(k => localStorage.removeItem(k))
  localStorage.clear()
}

// Storage keys enum
export const STORAGE_KEYS = {
  PROGRESS: 'progress',
  FAVORITES: 'favorites',
  SETTINGS: 'settings',
  DAILY_STATS: 'daily_stats',
  STREAK: 'streak',
  QUIZ_HISTORY: 'quiz_history',
  LAST_ACTIVE: 'last_active',
  DAILY_GOAL: 'daily_goal',
  THEME: 'theme'
} as const

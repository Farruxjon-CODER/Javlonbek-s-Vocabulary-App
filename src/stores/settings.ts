import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserSettings } from '@/types'
import { getItem, setItem, STORAGE_KEYS } from '@/utils/storage'

const DEFAULT_SETTINGS: UserSettings = {
  dailyGoal: 20,
  theme: 'system',
  showDefinitions: true,
  showExamples: true,
  flashcardAutoFlip: false,
  quizQuestionCount: 20
}

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<UserSettings>(
    getItem(STORAGE_KEYS.SETTINGS, { ...DEFAULT_SETTINGS })
  )

  function saveSettings() {
    setItem(STORAGE_KEYS.SETTINGS, settings.value)
  }

  function updateSettings(partial: Partial<UserSettings>) {
    Object.assign(settings.value, partial)
    saveSettings()
  }

  function setDailyGoal(goal: number) {
    settings.value.dailyGoal = goal
    saveSettings()
  }

  const isDarkMode = computed(() => {
    if (settings.value.theme === 'dark') return true
    if (settings.value.theme === 'light') return false
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return false
  })

  function toggleTheme() {
    const next = isDarkMode.value ? 'light' : 'dark'
    updateSettings({ theme: next })
  }

  function resetToInitial() {
    settings.value = { ...DEFAULT_SETTINGS }
  }

  return {
    settings,
    isDarkMode,
    updateSettings,
    setDailyGoal,
    toggleTheme,
    saveSettings,
    resetToInitial
  }
})

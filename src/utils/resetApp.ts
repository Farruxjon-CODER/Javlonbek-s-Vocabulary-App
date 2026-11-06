import { useProgressStore } from '@/stores/progress'
import { useStatsStore } from '@/stores/stats'
import { useSettingsStore } from '@/stores/settings'
import { useWordsStore } from '@/stores/words'
import { clearAll } from '@/utils/storage'

export function resetAppData(): void {
  const progressStore = useProgressStore()
  const statsStore = useStatsStore()
  const settingsStore = useSettingsStore()
  const wordsStore = useWordsStore()

  // Reset all Pinia store state to clean defaults
  progressStore.resetToInitial()
  statsStore.resetToInitial()
  settingsStore.resetToInitial()
  wordsStore.resetFilters()

  // Completely wipe all localStorage
  clearAll()
  localStorage.clear()

  // Refresh page
  window.location.reload()
}

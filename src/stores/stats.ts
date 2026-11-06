import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { DailyStats, QuizResult } from '@/types'
import { getItem, setItem, STORAGE_KEYS } from '@/utils/storage'
import { useSettingsStore } from '@/stores/settings'
import { useAuthStore } from '@/stores/auth'
import { saveUserData } from '@/firebase/userService'

export const useStatsStore = defineStore('stats', () => {
  const dailyStatsHistory = ref<DailyStats[]>(
    getItem(STORAGE_KEYS.DAILY_STATS, [])
  )

  const quizHistory = ref<QuizResult[]>(
    getItem(STORAGE_KEYS.QUIZ_HISTORY, [])
  )

  const streak = ref<{ current: number; lastDate: string }>(
    getItem(STORAGE_KEYS.STREAK, { current: 0, lastDate: '' })
  )

  let syncTimer: any = null

  function syncStatsToCloud() {
    if (typeof window === 'undefined') return
    clearTimeout(syncTimer)
    syncTimer = setTimeout(() => {
      const authStore = useAuthStore()
      if (authStore.user?.uid) {
        saveUserData(authStore.user.uid, {
          stats: {
            streak: streak.value,
            dailyStatsHistory: dailyStatsHistory.value,
            quizHistory: quizHistory.value
          }
        })
      }
    }, 2000) // 2 soniya debounce
  }

  function saveDailyStats() {
    setItem(STORAGE_KEYS.DAILY_STATS, dailyStatsHistory.value)
    syncStatsToCloud()
  }

  function saveQuizHistory() {
    setItem(STORAGE_KEYS.QUIZ_HISTORY, quizHistory.value)
    syncStatsToCloud()
  }

  function saveStreak() {
    setItem(STORAGE_KEYS.STREAK, streak.value)
    syncStatsToCloud()
  }

  function setStatsData(data: any) {
    if (data && typeof data === 'object') {
      if (data.streak) streak.value = data.streak
      if (Array.isArray(data.dailyStatsHistory)) dailyStatsHistory.value = data.dailyStatsHistory
      if (Array.isArray(data.quizHistory)) quizHistory.value = data.quizHistory

      setItem(STORAGE_KEYS.STREAK, streak.value)
      setItem(STORAGE_KEYS.DAILY_STATS, dailyStatsHistory.value)
      setItem(STORAGE_KEYS.QUIZ_HISTORY, quizHistory.value)
    }
  }

  function getTodayEntry(): DailyStats {
    const today = new Date().toISOString().split('T')[0]
    let entry = dailyStatsHistory.value.find(d => d.date === today)
    if (!entry) {
      entry = { date: today, wordsLearned: 0, wordsReviewed: 0, quizScore: 0, quizTotal: 0 }
      dailyStatsHistory.value.push(entry)
    }
    return entry
  }

  const todayStats = computed(() => {
    const today = new Date().toISOString().split('T')[0]
    const existing = dailyStatsHistory.value.find(d => d.date === today)
    return existing || { date: today, wordsLearned: 0, wordsReviewed: 0, quizScore: 0, quizTotal: 0 }
  })

  const dailyGoalProgress = computed(() => {
    const settingsStore = useSettingsStore()
    return Math.min(todayStats.value.wordsLearned, settingsStore.settings.dailyGoal)
  })

  const isDailyGoalComplete = computed(() => {
    const settingsStore = useSettingsStore()
    return dailyGoalProgress.value >= settingsStore.settings.dailyGoal
  })

  const weeklyActivity = computed(() => {
    const days: { date: string; label: string; wordsLearned: number }[] = []
    for (let i = 6; i >= 0; i--) {
      const d = new Date()
      d.setDate(d.getDate() - i)
      const dateStr = d.toISOString().split('T')[0]
      const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      const entry = dailyStatsHistory.value.find(s => s.date === dateStr)
      days.push({
        date: dateStr,
        label: dayNames[d.getDay()],
        wordsLearned: entry ? entry.wordsLearned : 0
      })
    }
    return days
  })

  const totalQuizAccuracy = computed(() => {
    if (quizHistory.value.length === 0) return 0
    const totalCorrect = quizHistory.value.reduce((sum, q) => sum + q.correct, 0)
    const totalQuestions = quizHistory.value.reduce((sum, q) => sum + q.total, 0)
    return totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 0
  })

  function incrementTodayLearned() {
    const entry = getTodayEntry()
    entry.wordsLearned++
    saveDailyStats()
  }

  function incrementTodayReviewed() {
    const entry = getTodayEntry()
    entry.wordsReviewed++
    saveDailyStats()
  }

  function addQuizResult(result: QuizResult) {
    quizHistory.value.push(result)
    saveQuizHistory()

    const entry = getTodayEntry()
    entry.quizScore += result.correct
    entry.quizTotal += result.total
    saveDailyStats()
  }

  function updateStreak() {
    const today = new Date().toISOString().split('T')[0]
    if (streak.value.lastDate === today) return

    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    const yesterdayStr = yesterday.toISOString().split('T')[0]

    if (streak.value.lastDate === yesterdayStr) {
      streak.value.current++
    } else if (streak.value.lastDate !== today) {
      streak.value.current = 1
    }

    streak.value.lastDate = today
    saveStreak()
  }

  function resetToInitial() {
    dailyStatsHistory.value = []
    quizHistory.value = []
    streak.value = { current: 0, lastDate: '' }
  }

  function resetAll() {
    resetToInitial()
  }

  return {
    dailyStatsHistory,
    quizHistory,
    streak,
    todayStats,
    dailyGoalProgress,
    isDailyGoalComplete,
    weeklyActivity,
    totalQuizAccuracy,
    incrementTodayLearned,
    incrementTodayReviewed,
    addQuizResult,
    updateStreak,
    setStatsData,
    resetToInitial,
    resetAll
  }
})

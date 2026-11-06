import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { WordProgress, WordStatus, ReviewAction } from '@/types'
import { getItem, setItem, clearAll, STORAGE_KEYS } from '@/utils/storage'
import { useWordsStore } from '@/stores/words'
import { useStatsStore } from '@/stores/stats'
import { useSettingsStore } from '@/stores/settings'
import { useGamificationStore } from '@/stores/gamification'

export const useProgressStore = defineStore('progress', () => {
  const progressMap = ref<Record<number, WordProgress>>(
    getItem(STORAGE_KEYS.PROGRESS, {})
  )

  function saveProgress() {
    setItem(STORAGE_KEYS.PROGRESS, progressMap.value)
  }

  function getProgress(wordId: number): WordProgress {
    if (!progressMap.value[wordId]) {
      progressMap.value[wordId] = {
        wordId,
        status: 'new',
        correct: 0,
        incorrect: 0,
        lastReviewed: null,
        nextReview: null,
        interval: 0,
        favorite: false
      }
    }
    return progressMap.value[wordId]
  }

  function getWordStatus(wordId: number): WordStatus {
    const p = progressMap.value[wordId]
    return p ? p.status : 'new'
  }

  function isFavorite(wordId: number): boolean {
    const p = progressMap.value[wordId]
    return p ? p.favorite : false
  }

  const learnedWords = computed(() => {
    const wordsStore = useWordsStore()
    return wordsStore.words.filter(w => {
      const p = progressMap.value[w.id]
      return p && (p.status === 'learning' || p.status === 'mastered')
    })
  })

  const masteredWords = computed(() => {
    const wordsStore = useWordsStore()
    return wordsStore.words.filter(w => {
      const p = progressMap.value[w.id]
      return p && p.status === 'mastered'
    })
  })

  const newWords = computed(() => {
    const wordsStore = useWordsStore()
    return wordsStore.words.filter(w => {
      const p = progressMap.value[w.id]
      return !p || p.status === 'new'
    })
  })

  const favoriteWords = computed(() => {
    const wordsStore = useWordsStore()
    return wordsStore.words.filter(w => {
      const p = progressMap.value[w.id]
      return p && p.favorite
    })
  })

  const reviewDueWords = computed(() => {
    const wordsStore = useWordsStore()
    const now = new Date().toISOString().split('T')[0]
    return wordsStore.words.filter(w => {
      const p = progressMap.value[w.id]
      if (!p || p.status === 'new') return false
      if (!p.nextReview) return true
      return p.nextReview <= now
    })
  })

  const cefrDistribution = computed(() => {
    const wordsStore = useWordsStore()
    const dist: Record<string, { total: number; learned: number; mastered: number }> = {}
    for (const w of wordsStore.words) {
      const level = w.cefr || 'Unknown'
      if (!dist[level]) dist[level] = { total: 0, learned: 0, mastered: 0 }
      dist[level].total++
      const p = progressMap.value[w.id]
      if (p) {
        if (p.status === 'learning' || p.status === 'mastered') dist[level].learned++
        if (p.status === 'mastered') dist[level].mastered++
      }
    }
    return dist
  })

  function markLearned(wordId: number) {
    const statsStore = useStatsStore()
    const p = getProgress(wordId)
    if (p.status === 'new') {
      p.status = 'learning'
      statsStore.incrementTodayLearned()
      statsStore.updateStreak()
      useGamificationStore().addCoins(5, "So'z o'rganildi (+5 Coin)")
    }
    saveProgress()
  }

  function markMastered(wordId: number) {
    const statsStore = useStatsStore()
    const p = getProgress(wordId)
    if (p.status === 'mastered') {
      saveProgress()
      return
    }

    const wasNew = p.status === 'new'
    p.status = 'mastered'
    if (wasNew) {
      statsStore.incrementTodayLearned()
    }
    statsStore.updateStreak()
    useGamificationStore().addCoins(15, "So'z mukammal o'zlashtirildi (+15 Coin)")
    saveProgress()
  }

  function markNew(wordId: number) {
    const p = getProgress(wordId)
    p.status = 'new'
    p.correct = 0
    p.incorrect = 0
    p.lastReviewed = null
    p.nextReview = null
    p.interval = 0
    saveProgress()
  }

  function toggleFavorite(wordId: number) {
    const p = getProgress(wordId)
    p.favorite = !p.favorite
    saveProgress()
  }

  function processReview(wordId: number, action: ReviewAction) {
    const statsStore = useStatsStore()
    const p = getProgress(wordId)
    const now = new Date()
    p.lastReviewed = now.toISOString().split('T')[0]

    let newInterval: number

    switch (action.type) {
      case 'again':
        newInterval = 1
        p.incorrect++
        p.status = 'learning'
        break
      case 'hard':
        newInterval = Math.max(1, p.interval)
        p.correct++
        p.status = 'learning'
        break
      case 'good':
        newInterval = Math.max(2, p.interval * 2)
        p.correct++
        if (p.correct >= 5) p.status = 'mastered'
        else p.status = 'learning'
        break
      case 'easy':
        newInterval = Math.max(4, Math.floor(p.interval * 2.5))
        p.correct++
        if (p.correct >= 3) p.status = 'mastered'
        else p.status = 'learning'
        break
    }

    p.interval = newInterval
    const nextDate = new Date(now)
    nextDate.setDate(nextDate.getDate() + newInterval)
    p.nextReview = nextDate.toISOString().split('T')[0]

    statsStore.incrementTodayReviewed()
    statsStore.updateStreak()
    useGamificationStore().addCoins(15, "So'z mukammal o'zlashtirildi (+15 Coin)")
    saveProgress()
  }

  function resetToInitial() {
    progressMap.value = {}
  }

  function resetAllData() {
    resetToInitial()
    useStatsStore().resetToInitial()
    useSettingsStore().resetToInitial()
    useWordsStore().resetFilters()
    clearAll()
  }

  return {
    progressMap,
    learnedWords,
    masteredWords,
    newWords,
    favoriteWords,
    reviewDueWords,
    cefrDistribution,
    getProgress,
    getWordStatus,
    isFavorite,
    markLearned,
    markMastered,
    markNew,
    toggleFavorite,
    processReview,
    saveProgress,
    resetToInitial,
    resetAllData
  }
})

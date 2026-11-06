import { ref, computed } from 'vue'
import type { VocabularyWord, FlashcardSession } from '@/types'
import { useWordsStore } from '@/stores/words'
import { useProgressStore } from '@/stores/progress'
import { shuffle } from '@/utils/shuffle'

export function useFlashcards() {
  const wordsStore = useWordsStore()
  const progressStore = useProgressStore()
  const session = ref<FlashcardSession | null>(null)

  function startSession(wordList?: VocabularyWord[], shouldShuffle = false) {
    const pool = wordList || wordsStore.filteredWords
    if (pool.length === 0) return

    const cardWords = shouldShuffle
      ? shuffle(pool)
      : [...pool].sort((a, b) => (a.orderIndex ?? 0) - (b.orderIndex ?? 0))

    session.value = {
      words: cardWords,
      currentIndex: 0,
      isFlipped: false,
      known: [],
      learning: [],
      again: []
    }
  }

  const currentWord = computed(() => {
    if (!session.value) return null
    return session.value.words[session.value.currentIndex] || null
  })

  const progress = computed(() => {
    if (!session.value) return { current: 0, total: 0, percent: 0 }
    const total = session.value.words.length
    const current = session.value.currentIndex + 1
    return { current, total, percent: Math.round((current / total) * 100) }
  })

  const isSessionComplete = computed(() => {
    if (!session.value) return false
    return session.value.currentIndex >= session.value.words.length
  })

  function flip() {
    if (session.value) {
      session.value.isFlipped = !session.value.isFlipped
    }
  }

  function nextCard() {
    if (session.value && session.value.currentIndex < session.value.words.length - 1) {
      session.value.currentIndex++
      session.value.isFlipped = false
    } else if (session.value) {
      session.value.currentIndex = session.value.words.length
    }
  }

  function prevCard() {
    if (session.value && session.value.currentIndex > 0) {
      session.value.currentIndex--
      session.value.isFlipped = false
    }
  }

  function markKnown() {
    if (!session.value || !currentWord.value) return
    session.value.known.push(currentWord.value.id)
    progressStore.markLearned(currentWord.value.id)
    nextCard()
  }

  function markLearning() {
    if (!session.value || !currentWord.value) return
    session.value.learning.push(currentWord.value.id)
    nextCard()
  }

  function markAgain() {
    if (!session.value || !currentWord.value) return
    session.value.again.push(currentWord.value.id)
    nextCard()
  }

  function endSession() {
    session.value = null
  }

  const sessionStats = computed(() => {
    if (!session.value) return null
    return {
      total: session.value.words.length,
      known: session.value.known.length,
      learning: session.value.learning.length,
      again: session.value.again.length,
      accuracy: session.value.words.length > 0
        ? Math.round((session.value.known.length / session.value.words.length) * 100)
        : 0
    }
  })

  return {
    session,
    currentWord,
    progress,
    isSessionComplete,
    sessionStats,
    startSession,
    flip,
    nextCard,
    prevCard,
    markKnown,
    markLearning,
    markAgain,
    endSession
  }
}

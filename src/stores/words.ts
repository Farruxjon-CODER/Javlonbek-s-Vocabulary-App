import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { VocabularyWord, WordStatus, CEFRLevel } from '@/types'
import { APP_VERSION } from '@/config/app'
import { useProgressStore } from '@/stores/progress'

export const useWordsStore = defineStore('words', () => {
  const words = ref<VocabularyWord[]>([])
  const isLoaded = ref(false)
  const isLoading = ref(false)

  const searchQuery = ref('')
  const filterCEFR = ref<CEFRLevel | 'all'>('all')
  const filterPOS = ref<string>('all')
  const filterStatus = ref<WordStatus | 'all'>('all')

  const totalWords = computed(() => words.value.length)

  const uniquePOSTags = computed(() => {
    const tags = new Set<string>()
    for (const w of words.value) {
      if (w.pos) {
        const parts = w.pos.split(/[,;]\s*/).map(s => s.trim()).filter(Boolean)
        parts.forEach(p => tags.add(p))
      }
    }
    return Array.from(tags).sort()
  })

  const wordMapById = computed(() => {
    const map = new Map<number, VocabularyWord>()
    for (const w of words.value) {
      map.set(w.id, w)
    }
    return map
  })

  const wordMapByKey = computed(() => {
    const map = new Map<string, VocabularyWord>()
    for (const w of words.value) {
      map.set(`${w.word.toLowerCase()}|${w.pos.toLowerCase()}`, w)
    }
    return map
  })

  const filteredWords = computed(() => {
    const progressStore = useProgressStore()
    let result = words.value

    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim()
      result = result.filter(w =>
        w.word.toLowerCase().includes(q) ||
        (w.pos && w.pos.toLowerCase().includes(q)) ||
        (w.cefr && w.cefr.toLowerCase() === q) ||
        (w.meaningUz && w.meaningUz.toLowerCase().includes(q)) ||
        (w.definition && w.definition.toLowerCase().includes(q)) ||
        (w.example && w.example.toLowerCase().includes(q)) ||
        (w.exampleUz && w.exampleUz.toLowerCase().includes(q)) ||
        (w.senses && w.senses.some(s =>
          s.definition.toLowerCase().includes(q) ||
          (s.meaningUz && s.meaningUz.toLowerCase().includes(q)) ||
          (s.example && s.example.toLowerCase().includes(q))
        ))
      )
    }

    if (filterCEFR.value !== 'all') {
      result = result.filter(w => w.cefr === filterCEFR.value)
    }

    if (filterPOS.value !== 'all') {
      result = result.filter(w => {
        const parts = w.pos.split(/[,;]\s*/).map(s => s.trim())
        return parts.includes(filterPOS.value)
      })
    }

    if (filterStatus.value !== 'all') {
      result = result.filter(w => {
        const p = progressStore.progressMap[w.id]
        if (filterStatus.value === 'new') return !p || p.status === 'new'
        return p && p.status === filterStatus.value
      })
    }

    return result
  })

  async function loadVocabulary() {
    if (isLoaded.value || isLoading.value) return
    isLoading.value = true
    try {
      const response = await fetch(`/data/vocabulary.json?v=${APP_VERSION}`, {
        cache: 'no-cache'
      })
      if (!response.ok) {
        throw new Error(`Failed to load vocabulary: ${response.status}`)
      }
      const data: VocabularyWord[] = await response.json()
      data.sort((a, b) => (a.orderIndex ?? 0) - (b.orderIndex ?? 0))
      words.value = data
      isLoaded.value = true
    } catch (error) {
      console.error('Failed to load vocabulary:', error)
    } finally {
      isLoading.value = false
    }
  }

  function resetFilters() {
    searchQuery.value = ''
    filterCEFR.value = 'all'
    filterPOS.value = 'all'
    filterStatus.value = 'all'
  }

  return {
    words,
    isLoaded,
    isLoading,
    searchQuery,
    filterCEFR,
    filterPOS,
    filterStatus,
    totalWords,
    uniquePOSTags,
    wordMapById,
    wordMapByKey,
    filteredWords,
    loadVocabulary,
    resetFilters
  }
})

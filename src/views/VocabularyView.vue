<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { VocabularyWord } from '@/types'
import { useWordsStore } from '@/stores/words'
import WordCard from '@/components/WordCard.vue'
import WordDetailModal from '@/components/WordDetailModal.vue'
import EmptyState from '@/components/EmptyState.vue'
import { Search, SlidersHorizontal, BookOpen } from 'lucide-vue-next'

const wordsStore = useWordsStore()
const route = useRoute()

const selectedWord = ref<VocabularyWord | null>(null)
const selectedIndex = ref(0)
const showFilters = ref(false)

// Pagination
const page = ref(1)
const perPage = 24

const paginatedWords = computed(() => {
  const start = (page.value - 1) * perPage
  return wordsStore.filteredWords.slice(start, start + perPage)
})

const totalPages = computed(() => Math.ceil(wordsStore.filteredWords.length / perPage))

// Debounced search
let searchTimeout: ReturnType<typeof setTimeout>
function onSearch(e: Event) {
  const value = (e.target as HTMLInputElement).value
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    wordsStore.searchQuery = value
    page.value = 1
  }, 200)
}

function selectWord(word: VocabularyWord) {
  selectedWord.value = word
  selectedIndex.value = wordsStore.filteredWords.findIndex(w => w.id === word.id)
}

function navigateWord(direction: 'prev' | 'next') {
  const words = wordsStore.filteredWords
  if (direction === 'prev' && selectedIndex.value > 0) {
    selectedIndex.value--
  } else if (direction === 'next' && selectedIndex.value < words.length - 1) {
    selectedIndex.value++
  }
  selectedWord.value = words[selectedIndex.value]
}

// Handle deep link from command palette
onMounted(() => {
  if (route.query.word) {
    const wordId = parseInt(route.query.word as string)
    const word = wordsStore.words.find(w => w.id === wordId)
    if (word) selectWord(word)
  }
})

const cefrLevels = ['all', 'A1', 'A2', 'B1', 'B2']
const statusOptions = [
  { value: 'all', label: 'All' },
  { value: 'new', label: 'New' },
  { value: 'learning', label: 'Learning' },
  { value: 'mastered', label: 'Mastered' }
]

const topPOSTags = computed(() => {
  const main = ['n.', 'v.', 'adj.', 'adv.', 'prep.', 'pron.', 'conj.', 'det.']
  return main.filter(p => wordsStore.uniquePOSTags.includes(p))
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Vocabulary</h1>
      <p class="text-sm text-surface-500">Browse and search {{ wordsStore.totalWords.toLocaleString() }} Oxford 5000 words</p>
    </div>

    <!-- Search & Filters -->
    <div class="mb-6 space-y-4">
      <!-- Search bar -->
      <div class="relative">
        <Search :size="18" class="absolute left-4 top-1/2 -translate-y-1/2 text-surface-400" />
        <input
          type="text"
          :placeholder="`Search ${wordsStore.totalWords.toLocaleString()} words...`"
          :value="wordsStore.searchQuery"
          @input="onSearch"
          class="w-full pl-11 pr-4 py-3 bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 rounded-xl text-sm text-surface-900 dark:text-white placeholder:text-surface-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-400 transition-all"
        />
        <button
          @click="showFilters = !showFilters"
          class="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
          :class="showFilters ? 'text-primary-500' : 'text-surface-400'"
        >
          <SlidersHorizontal :size="18" />
        </button>
      </div>

      <!-- Filters Panel -->
      <div v-if="showFilters" class="bg-white dark:bg-surface-900 rounded-xl border border-surface-200 dark:border-surface-800 p-4 space-y-4">
        <!-- CEFR -->
        <div>
          <label class="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-2 block">CEFR Level</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="level in cefrLevels"
              :key="level"
              @click="wordsStore.filterCEFR = level as any; page = 1"
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
              :class="wordsStore.filterCEFR === level
                ? 'bg-primary-100 dark:bg-primary-500/20 text-primary-700 dark:text-primary-400'
                : 'bg-surface-100 dark:bg-surface-800 text-surface-500 hover:bg-surface-200 dark:hover:bg-surface-700'"
            >
              {{ level === 'all' ? 'All Levels' : level }}
            </button>
          </div>
        </div>

        <!-- POS -->
        <div>
          <label class="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-2 block">Part of Speech</label>
          <div class="flex flex-wrap gap-2">
            <button
              @click="wordsStore.filterPOS = 'all'; page = 1"
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
              :class="wordsStore.filterPOS === 'all'
                ? 'bg-primary-100 dark:bg-primary-500/20 text-primary-700 dark:text-primary-400'
                : 'bg-surface-100 dark:bg-surface-800 text-surface-500 hover:bg-surface-200 dark:hover:bg-surface-700'"
            >
              All
            </button>
            <button
              v-for="pos in topPOSTags"
              :key="pos"
              @click="wordsStore.filterPOS = pos; page = 1"
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
              :class="wordsStore.filterPOS === pos
                ? 'bg-primary-100 dark:bg-primary-500/20 text-primary-700 dark:text-primary-400'
                : 'bg-surface-100 dark:bg-surface-800 text-surface-500 hover:bg-surface-200 dark:hover:bg-surface-700'"
            >
              {{ pos }}
            </button>
          </div>
        </div>

        <!-- Status -->
        <div>
          <label class="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-2 block">Status</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="opt in statusOptions"
              :key="opt.value"
              @click="wordsStore.filterStatus = opt.value as any; page = 1"
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
              :class="wordsStore.filterStatus === opt.value
                ? 'bg-primary-100 dark:bg-primary-500/20 text-primary-700 dark:text-primary-400'
                : 'bg-surface-100 dark:bg-surface-800 text-surface-500 hover:bg-surface-200 dark:hover:bg-surface-700'"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Results count -->
      <p class="text-xs text-surface-400">
        Showing {{ paginatedWords.length }} of {{ wordsStore.filteredWords.length }} words
      </p>
    </div>

    <!-- Word Grid -->
    <div v-if="paginatedWords.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
      <WordCard
        v-for="word in paginatedWords"
        :key="word.id"
        :word="word"
        @click="selectWord"
      />
    </div>

    <!-- Empty State -->
    <EmptyState
      v-else
      title="No words found"
      description="Try another spelling or remove some filters."
      :icon="BookOpen"
    />

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-center gap-2">
      <button
        @click="page = Math.max(1, page - 1)"
        :disabled="page === 1"
        class="px-3 py-2 rounded-lg text-sm font-medium bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 text-surface-600 dark:text-surface-400 hover:bg-surface-50 dark:hover:bg-surface-800 disabled:opacity-30 transition-colors"
      >
        Previous
      </button>

      <template v-for="p in totalPages" :key="p">
        <button
          v-if="p === 1 || p === totalPages || (p >= page - 2 && p <= page + 2)"
          @click="page = p"
          class="w-9 h-9 rounded-lg text-sm font-medium transition-colors"
          :class="page === p
            ? 'bg-primary-600 text-white'
            : 'bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 text-surface-600 dark:text-surface-400 hover:bg-surface-50 dark:hover:bg-surface-800'"
        >
          {{ p }}
        </button>
        <span
          v-else-if="p === page - 3 || p === page + 3"
          class="text-surface-400"
        >
          ...
        </span>
      </template>

      <button
        @click="page = Math.min(totalPages, page + 1)"
        :disabled="page === totalPages"
        class="px-3 py-2 rounded-lg text-sm font-medium bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 text-surface-600 dark:text-surface-400 hover:bg-surface-50 dark:hover:bg-surface-800 disabled:opacity-30 transition-colors"
      >
        Next
      </button>
    </div>

    <!-- Word Detail Modal -->
    <WordDetailModal
      v-if="selectedWord"
      :word="selectedWord"
      :words="wordsStore.filteredWords"
      :current-index="selectedIndex"
      @close="selectedWord = null"
      @navigate="navigateWord"
    />
  </div>
</template>

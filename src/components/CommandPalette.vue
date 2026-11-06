<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWordsStore } from '@/stores/words'
import { Search, ArrowRight } from 'lucide-vue-next'

const emit = defineEmits<{ close: [] }>()
const router = useRouter()
const wordsStore = useWordsStore()

const query = ref('')
const inputRef = ref<HTMLInputElement>()

onMounted(() => {
  setTimeout(() => inputRef.value?.focus(), 50)
})

const pages = [
  { label: 'Dashboard', path: '/', keywords: 'home' },
  { label: 'Vocabulary', path: '/vocabulary', keywords: 'words dictionary' },
  { label: 'Flashcards', path: '/flashcards', keywords: 'cards practice' },
  { label: 'Smart Review', path: '/review', keywords: 'spaced repetition' },
  { label: 'Quiz', path: '/quiz', keywords: 'test' },
  { label: 'Progress', path: '/progress', keywords: 'stats analytics' },
  { label: 'Favorites', path: '/favorites', keywords: 'saved starred' },
  { label: 'Settings', path: '/settings', keywords: 'preferences theme' },
]

const searchResults = computed(() => {
  if (!query.value.trim()) return { words: [], pages: pages.slice(0, 4) }

  const q = query.value.toLowerCase().trim()

  const matchedPages = pages.filter(p =>
    p.label.toLowerCase().includes(q) || p.keywords.includes(q)
  )

  const matchedWords = wordsStore.words
    .filter(w => w.word.toLowerCase().includes(q))
    .slice(0, 8)

  return { words: matchedWords, pages: matchedPages }
})

function navigateTo(path: string) {
  router.push(path)
  emit('close')
}

function goToWord(wordId: number) {
  router.push({ path: '/vocabulary', query: { word: wordId.toString() } })
  emit('close')
}

function handleOverlayClick(e: MouseEvent) {
  if ((e.target as HTMLElement).classList.contains('modal-overlay')) {
    emit('close')
  }
}
</script>

<template>
  <div
    class="modal-overlay fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] flex items-start justify-center pt-[15vh]"
    @click="handleOverlayClick"
  >
    <div class="modal-content w-full max-w-lg mx-4 bg-white dark:bg-surface-900 rounded-2xl shadow-2xl border border-surface-200 dark:border-surface-700 overflow-hidden">
      <!-- Search Input -->
      <div class="flex items-center gap-3 px-5 py-4 border-b border-surface-200 dark:border-surface-800">
        <Search :size="20" class="text-surface-400 shrink-0" />
        <input
          ref="inputRef"
          v-model="query"
          type="text"
          placeholder="Search words, pages, actions..."
          class="flex-1 bg-transparent border-none outline-none text-surface-900 dark:text-white placeholder:text-surface-400 text-sm"
          @keydown.escape="emit('close')"
        />
        <kbd class="px-2 py-0.5 bg-surface-100 dark:bg-surface-800 rounded text-xs text-surface-400 font-mono">Esc</kbd>
      </div>

      <!-- Results -->
      <div class="max-h-80 overflow-y-auto p-2">
        <!-- Pages -->
        <div v-if="searchResults.pages.length" class="mb-2">
          <p class="px-3 py-1.5 text-[11px] font-semibold text-surface-400 uppercase tracking-wider">Pages</p>
          <button
            v-for="page in searchResults.pages"
            :key="page.path"
            @click="navigateTo(page.path)"
            class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors text-left"
          >
            <ArrowRight :size="16" class="text-surface-400" />
            <span class="text-sm text-surface-700 dark:text-surface-300">{{ page.label }}</span>
          </button>
        </div>

        <!-- Words -->
        <div v-if="searchResults.words.length" class="mb-2">
          <p class="px-3 py-1.5 text-[11px] font-semibold text-surface-400 uppercase tracking-wider">Words</p>
          <button
            v-for="word in searchResults.words"
            :key="word.id"
            @click="goToWord(word.id)"
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors text-left"
          >
            <div class="flex items-center gap-3">
              <span class="text-sm font-medium text-surface-900 dark:text-white">{{ word.word }}</span>
              <span class="text-xs text-surface-400">{{ word.pos }}</span>
            </div>
            <span class="text-xs px-2 py-0.5 rounded-full bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400 font-medium">{{ word.cefr }}</span>
          </button>
        </div>

        <!-- No results -->
        <div v-if="query && !searchResults.words.length && !searchResults.pages.length" class="py-8 text-center">
          <p class="text-sm text-surface-500">No results found</p>
          <p class="text-xs text-surface-400 mt-1">Try a different search term</p>
        </div>
      </div>
    </div>
  </div>
</template>

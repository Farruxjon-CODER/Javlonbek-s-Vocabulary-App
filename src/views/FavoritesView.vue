<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { VocabularyWord } from '@/types'
import { useProgressStore } from '@/stores/progress'
import { useToastStore } from '@/stores/toast'
import WordCard from '@/components/WordCard.vue'
import WordDetailModal from '@/components/WordDetailModal.vue'
import EmptyState from '@/components/EmptyState.vue'
import { Heart, Search, Layers, Trash2 } from 'lucide-vue-next'

const progressStore = useProgressStore()
const router = useRouter()

const searchQuery = ref('')
const selectedWord = ref<VocabularyWord | null>(null)
const selectedIndex = ref(0)

const filteredFavorites = computed(() => {
  const favs = progressStore.favoriteWords
  if (!searchQuery.value.trim()) return favs
  const q = searchQuery.value.toLowerCase()
  return favs.filter(w => w.word.toLowerCase().includes(q))
})

const toastStore = useToastStore()

function selectWord(word: VocabularyWord) {
  selectedWord.value = word
  selectedIndex.value = filteredFavorites.value.findIndex(w => w.id === word.id)
}

function navigateWord(direction: 'prev' | 'next') {
  const words = filteredFavorites.value
  if (direction === 'prev' && selectedIndex.value > 0) {
    selectedIndex.value--
  } else if (direction === 'next' && selectedIndex.value < words.length - 1) {
    selectedIndex.value++
  }
  selectedWord.value = words[selectedIndex.value]
}

function clearAll() {
  if (confirm('Remove all favorites?')) {
    progressStore.favoriteWords.forEach(w => progressStore.toggleFavorite(w.id))
    toastStore.addToast('All favorites cleared', 'info')
  }
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Favorites</h1>
        <p class="text-sm text-surface-500">{{ progressStore.favoriteWords.length }} saved words</p>
      </div>

      <div v-if="progressStore.favoriteWords.length" class="flex items-center gap-2">
        <button
          @click="router.push('/flashcards')"
          class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium rounded-xl transition-colors"
        >
          <Layers :size="14" class="inline -mt-0.5 mr-1" />
          Practice
        </button>
        <button
          @click="clearAll"
          class="px-4 py-2 bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400 text-sm font-medium rounded-xl hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors"
        >
          <Trash2 :size="14" class="inline -mt-0.5 mr-1" />
          Clear
        </button>
      </div>
    </div>

    <!-- Search -->
    <div v-if="progressStore.favoriteWords.length" class="mb-6">
      <div class="relative">
        <Search :size="18" class="absolute left-4 top-1/2 -translate-y-1/2 text-surface-400" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search favorites..."
          class="w-full pl-11 pr-4 py-3 bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 rounded-xl text-sm text-surface-900 dark:text-white placeholder:text-surface-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-400 transition-all"
        />
      </div>
    </div>

    <!-- Grid -->
    <div v-if="filteredFavorites.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <WordCard
        v-for="word in filteredFavorites"
        :key="word.id"
        :word="word"
        @click="selectWord"
      />
    </div>

    <!-- Empty State -->
    <EmptyState
      v-else-if="progressStore.favoriteWords.length === 0"
      title="No favorite words yet"
      description="Your vocabulary collection is empty. Star words you want to revisit."
      :icon="Heart"
      action-label="Explore Vocabulary"
      @action="router.push('/vocabulary')"
    />

    <EmptyState
      v-else
      title="No matching favorites"
      description="Try a different search term."
      :icon="Search"
    />

    <!-- Modal -->
    <WordDetailModal
      v-if="selectedWord"
      :word="selectedWord"
      :words="filteredFavorites"
      :current-index="selectedIndex"
      @close="selectedWord = null"
      @navigate="navigateWord"
    />
  </div>
</template>

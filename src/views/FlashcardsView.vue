<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useWordsStore } from '@/stores/words'
import { useProgressStore } from '@/stores/progress'
import { useToastStore } from '@/stores/toast'
import { useFlashcards } from '@/composables/useFlashcards'
import CEFRBadge from '@/components/CEFRBadge.vue'
import POSBadge from '@/components/POSBadge.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import EmptyState from '@/components/EmptyState.vue'
import {
  Star,
  ChevronLeft,
  ChevronRight,
  RotateCcw,
  Check,
  BookOpen,
  RefreshCw,
  Layers,
  Trophy
} from 'lucide-vue-next'

const wordsStore = useWordsStore()
const progressStore = useProgressStore()
const toastStore = useToastStore()
const {
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
} = useFlashcards()

const isStarted = ref(false)
const cefrFilter = ref<string>('all')

function begin() {
  let pool = wordsStore.words
  if (cefrFilter.value !== 'all') {
    pool = pool.filter(w => w.cefr === cefrFilter.value)
  }
  startSession(pool)
  isStarted.value = true
}

function restart() {
  endSession()
  isStarted.value = false
}

function handleFavorite() {
  if (currentWord.value) {
    progressStore.toggleFavorite(currentWord.value.id)
    toastStore.addToast(
      progressStore.isFavorite(currentWord.value.id) ? '⭐ Added to favorites' : 'Removed from favorites',
      'info'
    )
  }
}

// Keyboard shortcuts
function handleKeyDown(e: KeyboardEvent) {
  if (!isStarted.value || isSessionComplete.value) return
  const target = e.target as HTMLElement
  if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') return

  switch (e.key) {
    case ' ':
      e.preventDefault()
      flip()
      break
    case 'ArrowLeft':
      prevCard()
      break
    case 'ArrowRight':
      nextCard()
      break
    case 'f':
    case 'F':
      handleFavorite()
      break
    case 'k':
    case 'K':
      if (!e.ctrlKey) markKnown()
      break
  }
}

onMounted(() => window.addEventListener('keydown', handleKeyDown))
onUnmounted(() => window.removeEventListener('keydown', handleKeyDown))
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Flashcards</h1>
      <p class="text-sm text-surface-500">Swipe through words and test your knowledge</p>
    </div>

    <!-- Start Screen -->
    <div v-if="!isStarted" class="space-y-6">
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-8 border border-surface-200 dark:border-surface-800 text-center">
        <div class="w-16 h-16 rounded-2xl bg-primary-50 dark:bg-primary-500/10 flex items-center justify-center mx-auto mb-4">
          <Layers :size="28" class="text-primary-500" />
        </div>
        <h2 class="text-xl font-bold text-surface-900 dark:text-white mb-2">Ready to practice?</h2>
        <p class="text-sm text-surface-500 mb-6">Choose a CEFR level or practice all words</p>

        <div class="flex flex-wrap justify-center gap-2 mb-6">
          <button
            v-for="level in ['all', 'A1', 'A2', 'B1', 'B2']"
            :key="level"
            @click="cefrFilter = level"
            class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
            :class="cefrFilter === level
              ? 'bg-primary-600 text-white'
              : 'bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400 hover:bg-surface-200 dark:hover:bg-surface-700'"
          >
            {{ level === 'all' ? 'All Levels' : level }}
          </button>
        </div>

        <button
          @click="begin"
          class="px-8 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-colors shadow-lg shadow-primary-500/20"
        >
          Start Flashcards
        </button>

        <div class="mt-4 text-xs text-surface-400">
          <kbd class="px-1.5 py-0.5 bg-surface-100 dark:bg-surface-800 rounded font-mono">Space</kbd> flip &nbsp;
          <kbd class="px-1.5 py-0.5 bg-surface-100 dark:bg-surface-800 rounded font-mono">←→</kbd> navigate &nbsp;
          <kbd class="px-1.5 py-0.5 bg-surface-100 dark:bg-surface-800 rounded font-mono">F</kbd> favorite &nbsp;
          <kbd class="px-1.5 py-0.5 bg-surface-100 dark:bg-surface-800 rounded font-mono">K</kbd> know it
        </div>
      </div>
    </div>

    <!-- Session Complete -->
    <div v-else-if="isSessionComplete && sessionStats" class="space-y-6">
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-8 border border-surface-200 dark:border-surface-800 text-center">
        <div class="w-16 h-16 rounded-2xl bg-emerald-50 dark:bg-emerald-500/10 flex items-center justify-center mx-auto mb-4">
          <Trophy :size="28" class="text-emerald-500" />
        </div>
        <h2 class="text-2xl font-bold text-surface-900 dark:text-white mb-2">Session Complete! 🎉</h2>
        <p class="text-sm text-surface-500 mb-8">Great work! Here's your summary.</p>

        <div class="grid grid-cols-3 gap-4 mb-8">
          <div class="p-4 bg-emerald-50 dark:bg-emerald-500/10 rounded-xl">
            <p class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{{ sessionStats.known }}</p>
            <p class="text-xs text-emerald-600/60 dark:text-emerald-400/60">Known</p>
          </div>
          <div class="p-4 bg-amber-50 dark:bg-amber-500/10 rounded-xl">
            <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ sessionStats.learning }}</p>
            <p class="text-xs text-amber-600/60 dark:text-amber-400/60">Learning</p>
          </div>
          <div class="p-4 bg-rose-50 dark:bg-rose-500/10 rounded-xl">
            <p class="text-2xl font-bold text-rose-600 dark:text-rose-400">{{ sessionStats.again }}</p>
            <p class="text-xs text-rose-600/60 dark:text-rose-400/60">Review Again</p>
          </div>
        </div>

        <p class="text-4xl font-bold text-surface-900 dark:text-white mb-1">{{ sessionStats.accuracy }}%</p>
        <p class="text-sm text-surface-400 mb-8">Accuracy</p>

        <div class="flex justify-center gap-3">
          <button
            @click="restart"
            class="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-xl transition-colors"
          >
            <RefreshCw :size="16" class="inline -mt-0.5 mr-1" />
            Practice Again
          </button>
        </div>
      </div>
    </div>

    <!-- Active Flashcard -->
    <div v-else-if="session && currentWord" class="space-y-6">
      <!-- Progress -->
      <div class="flex items-center gap-4">
        <ProgressBar :value="progress.current" :max="progress.total" size="sm" class="flex-1" />
        <span class="text-sm text-surface-500 tabular-nums">{{ progress.current }} / {{ progress.total }}</span>
      </div>

      <!-- Card -->
      <div
        class="flashcard-container cursor-pointer select-none"
        @click="flip"
      >
        <div class="flashcard-inner w-full h-72 sm:h-80" :class="{ flipped: session.isFlipped }">
          <!-- Front -->
          <div class="flashcard-front w-full h-full bg-white dark:bg-surface-900 rounded-2xl border border-surface-200 dark:border-surface-800 shadow-lg flex flex-col items-center justify-center p-8">
            <div class="flex items-center gap-2 mb-4">
              <CEFRBadge :level="currentWord.cefr" />
              <POSBadge :pos="currentWord.pos" />
            </div>
            <h2 class="text-4xl sm:text-5xl font-bold text-surface-900 dark:text-white mb-4">
              {{ currentWord.word }}
            </h2>
            <p class="text-sm text-surface-400">Tap to flip</p>
          </div>

          <!-- Back -->
          <div class="flashcard-back w-full h-full bg-white dark:bg-surface-900 rounded-2xl border border-surface-200 dark:border-surface-800 shadow-lg flex flex-col items-center justify-center p-6 sm:p-8 text-center overflow-y-auto">
            <h2 class="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-white mb-2">
              {{ currentWord.word }}
            </h2>

            <!-- Uzbek Meaning -->
            <div v-if="currentWord.meaningUz" class="mb-3 px-3 py-1 bg-primary-50 dark:bg-primary-500/10 rounded-full">
              <span class="text-base font-bold text-primary-600 dark:text-primary-400">
                {{ currentWord.meaningUz }}
              </span>
            </div>

            <!-- English Definition -->
            <p v-if="currentWord.definition" class="text-sm text-surface-700 dark:text-surface-300 mb-3 max-w-md leading-relaxed">
              {{ currentWord.definition }}
            </p>

            <!-- Example Sentence -->
            <div v-if="currentWord.example" class="pt-2 border-t border-surface-100 dark:border-surface-800/80 max-w-md">
              <p class="text-xs text-surface-600 dark:text-surface-400 italic">
                "{{ currentWord.example }}"
              </p>
              <p v-if="currentWord.exampleUz" class="text-[11px] text-surface-500 dark:text-surface-400 mt-1">
                {{ currentWord.exampleUz }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Controls -->
      <div class="flex items-center justify-between">
        <button
          @click="prevCard"
          class="p-3 rounded-xl bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 hover:bg-surface-50 dark:hover:bg-surface-800 transition-colors disabled:opacity-30"
          :disabled="progress.current <= 1"
          aria-label="Previous card"
        >
          <ChevronLeft :size="20" class="text-surface-500" />
        </button>

        <div class="flex items-center gap-2">
          <button
            @click="markAgain"
            class="px-4 py-2.5 rounded-xl text-sm font-medium bg-rose-50 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400 hover:bg-rose-100 dark:hover:bg-rose-500/20 transition-colors"
          >
            <RotateCcw :size="14" class="inline -mt-0.5 mr-1" />
            Again
          </button>
          <button
            @click="markLearning"
            class="px-4 py-2.5 rounded-xl text-sm font-medium bg-amber-50 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400 hover:bg-amber-100 dark:hover:bg-amber-500/20 transition-colors"
          >
            <BookOpen :size="14" class="inline -mt-0.5 mr-1" />
            Still learning
          </button>
          <button
            @click="markKnown"
            class="px-4 py-2.5 rounded-xl text-sm font-medium bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-100 dark:hover:bg-emerald-500/20 transition-colors"
          >
            <Check :size="14" class="inline -mt-0.5 mr-1" />
            Know it
          </button>
        </div>

        <button
          @click="handleFavorite"
          class="p-3 rounded-xl bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 hover:bg-surface-50 dark:hover:bg-surface-800 transition-colors"
          aria-label="Toggle favorite"
        >
          <Star
            :size="20"
            :class="progressStore.isFavorite(currentWord.id)
              ? 'fill-amber-400 text-amber-400'
              : 'text-surface-300 dark:text-surface-600'"
          />
        </button>
      </div>
    </div>
  </div>
</template>

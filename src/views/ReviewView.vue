<script setup lang="ts">
import { ref, computed } from 'vue'
import { useProgressStore } from '@/stores/progress'
import { useToastStore } from '@/stores/toast'
import CEFRBadge from '@/components/CEFRBadge.vue'
import POSBadge from '@/components/POSBadge.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import EmptyState from '@/components/EmptyState.vue'
import { Brain, RotateCcw, Check, Zap, Inbox } from 'lucide-vue-next'

const progressStore = useProgressStore()
const toastStore = useToastStore()

const isStarted = ref(false)
const currentIndex = ref(0)
const showAnswer = ref(false)

const reviewWords = computed(() => progressStore.reviewDueWords)

const currentWord = computed(() => {
  if (currentIndex.value >= reviewWords.value.length) return null
  return reviewWords.value[currentIndex.value]
})

const isComplete = computed(() => {
  return isStarted.value && currentIndex.value >= reviewWords.value.length
})

function start() {
  currentIndex.value = 0
  showAnswer.value = false
  isStarted.value = true
}

function reveal() {
  showAnswer.value = true
}

function respond(type: 'again' | 'hard' | 'good' | 'easy') {
  if (!currentWord.value) return
  progressStore.processReview(currentWord.value.id, { type })

  const msgs = { again: 'Will review again soon', hard: 'Marked as hard', good: 'Good progress!', easy: 'Easy! 🎉' }
  toastStore.addToast(msgs[type], type === 'easy' || type === 'good' ? 'success' : 'info')

  currentIndex.value++
  showAnswer.value = false
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Smart Review</h1>
      <p class="text-sm text-surface-500">Spaced repetition to reinforce your learning</p>
    </div>

    <!-- Not started -->
    <div v-if="!isStarted" class="space-y-6">
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-8 border border-surface-200 dark:border-surface-800 text-center">
        <div class="w-16 h-16 rounded-2xl bg-violet-50 dark:bg-violet-500/10 flex items-center justify-center mx-auto mb-4">
          <Brain :size="28" class="text-violet-500" />
        </div>
        <h2 class="text-xl font-bold text-surface-900 dark:text-white mb-2">Spaced Repetition</h2>
        <p class="text-sm text-surface-500 mb-6">Review words that are due based on your learning history</p>

        <div class="grid grid-cols-3 gap-4 mb-6 max-w-xs mx-auto">
          <div class="p-3 bg-violet-50 dark:bg-violet-500/10 rounded-xl">
            <p class="text-xl font-bold text-violet-600 dark:text-violet-400">{{ reviewWords.length }}</p>
            <p class="text-[10px] text-violet-600/60">Due</p>
          </div>
          <div class="p-3 bg-amber-50 dark:bg-amber-500/10 rounded-xl">
            <p class="text-xl font-bold text-amber-600 dark:text-amber-400">{{ progressStore.learnedWords.length }}</p>
            <p class="text-[10px] text-amber-600/60">Learning</p>
          </div>
          <div class="p-3 bg-emerald-50 dark:bg-emerald-500/10 rounded-xl">
            <p class="text-xl font-bold text-emerald-600 dark:text-emerald-400">{{ progressStore.masteredWords.length }}</p>
            <p class="text-[10px] text-emerald-600/60">Mastered</p>
          </div>
        </div>

        <button
          v-if="reviewWords.length > 0"
          @click="start"
          class="px-8 py-3 bg-violet-600 hover:bg-violet-700 text-white font-semibold rounded-xl transition-colors shadow-lg shadow-violet-500/20"
        >
          Start Review ({{ reviewWords.length }} words)
        </button>

        <EmptyState
          v-else
          title="You're all caught up!"
          description="No words are due for review. Learn new words or check back later."
          :icon="Inbox"
        />
      </div>
    </div>

    <!-- Complete -->
    <div v-else-if="isComplete" class="space-y-6">
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-8 border border-surface-200 dark:border-surface-800 text-center">
        <div class="w-16 h-16 rounded-2xl bg-emerald-50 dark:bg-emerald-500/10 flex items-center justify-center mx-auto mb-4">
          <Check :size="28" class="text-emerald-500" />
        </div>
        <h2 class="text-2xl font-bold text-surface-900 dark:text-white mb-2">Review Complete! 🎉</h2>
        <p class="text-sm text-surface-500 mb-6">You've reviewed all due words. Great work!</p>

        <button
          @click="isStarted = false"
          class="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-xl transition-colors"
        >
          Back to Review
        </button>
      </div>
    </div>

    <!-- Active Review -->
    <div v-else-if="currentWord" class="space-y-6">
      <div class="flex items-center gap-4">
        <ProgressBar :value="currentIndex + 1" :max="reviewWords.length" size="sm" color="bg-violet-500" class="flex-1" />
        <span class="text-sm text-surface-500 tabular-nums">{{ currentIndex + 1 }} / {{ reviewWords.length }}</span>
      </div>

      <div class="bg-white dark:bg-surface-900 rounded-2xl border border-surface-200 dark:border-surface-800 shadow-lg p-8 text-center min-h-[280px] flex flex-col items-center justify-center">
        <div class="flex items-center gap-2 mb-4">
          <CEFRBadge :level="currentWord.cefr" />
          <POSBadge :pos="currentWord.pos" />
        </div>
        <h2 class="text-4xl font-bold text-surface-900 dark:text-white mb-4">{{ currentWord.word }}</h2>

        <div v-if="!showAnswer">
          <button
            @click="reveal"
            class="px-6 py-2.5 bg-violet-600 hover:bg-violet-700 text-white font-medium rounded-xl transition-colors"
          >
            Show Answer
          </button>
        </div>

        <div v-else class="w-full mt-4">
          <div v-if="currentWord.meaningUz" class="text-xl font-bold text-primary-600 dark:text-primary-400 mb-1">
            {{ currentWord.meaningUz }}
          </div>
          <div v-if="currentWord.definition" class="text-sm text-surface-600 dark:text-surface-400 mb-3 max-w-lg mx-auto leading-relaxed">
            {{ currentWord.definition }}
          </div>
          <div v-if="currentWord.example" class="p-3 bg-surface-50 dark:bg-surface-800/60 rounded-xl text-left max-w-lg mx-auto text-xs text-surface-600 dark:text-surface-300">
            <p class="italic text-surface-700 dark:text-surface-200">"{{ currentWord.example }}"</p>
            <p v-if="currentWord.exampleUz" class="text-surface-500 dark:text-surface-400 mt-1">{{ currentWord.exampleUz }}</p>
          </div>

          <div class="flex flex-wrap items-center justify-center gap-2 mt-6">
            <button
              @click="respond('again')"
              class="px-4 py-2.5 rounded-xl text-sm font-medium bg-rose-50 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400 hover:bg-rose-100 transition-colors"
            >
              <RotateCcw :size="14" class="inline -mt-0.5 mr-1" />
              Again
            </button>
            <button
              @click="respond('hard')"
              class="px-4 py-2.5 rounded-xl text-sm font-medium bg-orange-50 dark:bg-orange-500/10 text-orange-600 dark:text-orange-400 hover:bg-orange-100 transition-colors"
            >
              Hard
            </button>
            <button
              @click="respond('good')"
              class="px-4 py-2.5 rounded-xl text-sm font-medium bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-100 transition-colors"
            >
              <Check :size="14" class="inline -mt-0.5 mr-1" />
              Good
            </button>
            <button
              @click="respond('easy')"
              class="px-4 py-2.5 rounded-xl text-sm font-medium bg-sky-50 dark:bg-sky-500/10 text-sky-600 dark:text-sky-400 hover:bg-sky-100 transition-colors"
            >
              <Zap :size="14" class="inline -mt-0.5 mr-1" />
              Easy
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

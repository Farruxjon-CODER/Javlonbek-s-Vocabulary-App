<script setup lang="ts">
import type { VocabularyWord } from '@/types'
import { useProgressStore } from '@/stores/progress'
import CEFRBadge from './CEFRBadge.vue'
import POSBadge from './POSBadge.vue'
import { Star, Check, BookOpen } from 'lucide-vue-next'

const props = defineProps<{
  word: VocabularyWord
}>()

const emit = defineEmits<{
  click: [word: VocabularyWord]
}>()

const progressStore = useProgressStore()

function toast(msg: string, type: 'success' | 'info' = 'success') {
  if (typeof window !== 'undefined' && (window as any).__lexiflow_toast) {
    (window as any).__lexiflow_toast(msg, type)
  }
}

function handleFavorite(e: Event) {
  e.stopPropagation()
  progressStore.toggleFavorite(props.word.id)
  toast(progressStore.isFavorite(props.word.id) ? '⭐ Added to favorites' : 'Removed from favorites', 'info')
}

function handleLearn(e: Event) {
  e.stopPropagation()
  const status = progressStore.getWordStatus(props.word.id)
  if (status === 'new') {
    progressStore.markLearned(props.word.id)
    toast('✓ Word marked as learned')
  } else if (status === 'learning') {
    progressStore.markMastered(props.word.id)
    toast('🎉 Word mastered!')
  } else {
    progressStore.markNew(props.word.id)
    toast('Reset to new', 'info')
  }
}
</script>

<template>
  <div
    @click="emit('click', word)"
    class="group bg-white dark:bg-surface-900 rounded-2xl p-5 border border-surface-200 dark:border-surface-800 hover:border-primary-300 dark:hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all duration-200 cursor-pointer"
    role="button"
    tabindex="0"
    :aria-label="`Word: ${word.word}`"
  >
    <div class="flex items-start justify-between mb-3">
      <h3 class="text-lg font-bold text-surface-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
        {{ word.word }}
      </h3>
      <button
        @click="handleFavorite"
        class="p-1.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
        :aria-label="progressStore.isFavorite(word.id) ? 'Remove from favorites' : 'Add to favorites'"
      >
        <Star
          :size="18"
          :class="progressStore.isFavorite(word.id)
            ? 'fill-amber-400 text-amber-400'
            : 'text-surface-300 dark:text-surface-600'"
        />
      </button>
    </div>

    <div class="flex items-center gap-2 mb-3">
      <POSBadge :pos="word.pos" />
      <CEFRBadge :level="word.cefr" />
    </div>

    <!-- Uzbek Meaning -->
    <div v-if="word.meaningUz" class="mb-1.5">
      <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">
        {{ word.meaningUz }}
      </span>
    </div>

    <!-- English Definition -->
    <p v-if="word.definition" class="text-xs text-surface-600 dark:text-surface-400 line-clamp-2 mb-4 leading-relaxed">
      {{ word.definition }}
    </p>

    <div class="flex items-center justify-between">
      <div class="flex items-center gap-1.5">
        <span
          class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium"
          :class="{
            'bg-surface-100 dark:bg-surface-800 text-surface-500': progressStore.getWordStatus(word.id) === 'new',
            'bg-amber-50 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400': progressStore.getWordStatus(word.id) === 'learning',
            'bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400': progressStore.getWordStatus(word.id) === 'mastered',
          }"
        >
          <Check v-if="progressStore.getWordStatus(word.id) === 'mastered'" :size="12" />
          <BookOpen v-else-if="progressStore.getWordStatus(word.id) === 'learning'" :size="12" />
          {{ progressStore.getWordStatus(word.id) === 'new' ? 'New' : progressStore.getWordStatus(word.id) === 'learning' ? 'Learning' : 'Mastered' }}
        </span>
      </div>

      <button
        @click="handleLearn"
        class="px-3 py-1.5 text-xs font-medium rounded-lg transition-colors"
        :class="{
          'bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400 hover:bg-primary-100 dark:hover:bg-primary-500/20': progressStore.getWordStatus(word.id) === 'new',
          'bg-amber-50 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400 hover:bg-amber-100': progressStore.getWordStatus(word.id) === 'learning',
          'bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-100': progressStore.getWordStatus(word.id) === 'mastered',
        }"
      >
        {{ progressStore.getWordStatus(word.id) === 'new' ? 'Learn' : progressStore.getWordStatus(word.id) === 'learning' ? 'Master' : 'Reset' }}
      </button>
    </div>
  </div>
</template>

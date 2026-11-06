<script setup lang="ts">
import { computed } from 'vue'
import type { VocabularyWord } from '@/types'
import { useProgressStore } from '@/stores/progress'
import CEFRBadge from './CEFRBadge.vue'
import POSBadge from './POSBadge.vue'
import { X, Star, Check, BookOpen, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-vue-next'

const props = defineProps<{
  word: VocabularyWord
  words?: VocabularyWord[]
  currentIndex?: number
}>()

const emit = defineEmits<{
  close: []
  navigate: [direction: 'prev' | 'next']
}>()

const progressStore = useProgressStore()

const status = computed(() => progressStore.getWordStatus(props.word.id))
const isFav = computed(() => progressStore.isFavorite(props.word.id))

function toast(msg: string, type: 'success' | 'info' = 'success') {
  if (typeof window !== 'undefined' && (window as any).__lexiflow_toast) {
    (window as any).__lexiflow_toast(msg, type)
  }
}

function handleLearn() {
  if (status.value === 'new') {
    progressStore.markLearned(props.word.id)
    toast('✓ Word marked as learned')
  } else if (status.value === 'learning') {
    progressStore.markMastered(props.word.id)
    toast('🎉 Word mastered!')
  }
}

function handleReset() {
  progressStore.markNew(props.word.id)
  toast('Word reset', 'info')
}

function handleFavorite() {
  progressStore.toggleFavorite(props.word.id)
  toast(progressStore.isFavorite(props.word.id) ? '⭐ Added to favorites' : 'Removed from favorites', 'info')
}
</script>

<template>
  <div
    class="modal-overlay fixed inset-0 bg-black/50 backdrop-blur-sm z-[80] flex items-center justify-center p-4"
    @click.self="emit('close')"
  >
    <div class="modal-content w-full max-w-lg bg-white dark:bg-surface-900 rounded-2xl shadow-2xl border border-surface-200 dark:border-surface-700 overflow-hidden">
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-surface-200 dark:border-surface-800">
        <div class="flex items-center gap-3">
          <CEFRBadge :level="word.cefr" />
          <POSBadge :pos="word.pos" />
        </div>
        <button
          @click="emit('close')"
          class="p-2 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
          aria-label="Close"
        >
          <X :size="20" class="text-surface-400" />
        </button>
      </div>

      <!-- Content -->
      <div class="p-6">
        <h2 class="text-3xl font-bold text-surface-900 dark:text-white mb-2">{{ word.word }}</h2>

        <!-- Status -->
        <div class="flex items-center gap-2 mb-6">
          <span
            class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium"
            :class="{
              'bg-surface-100 dark:bg-surface-800 text-surface-500': status === 'new',
              'bg-amber-50 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400': status === 'learning',
              'bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400': status === 'mastered',
            }"
          >
            <Check v-if="status === 'mastered'" :size="14" />
            <BookOpen v-else-if="status === 'learning'" :size="14" />
            {{ status === 'new' ? 'Not learned' : status === 'learning' ? 'Learning' : 'Mastered' }}
          </span>
        </div>

        <!-- Uzbek Meaning (Primary) -->
        <div v-if="word.meaningUz" class="mb-4 p-3 bg-primary-50/50 dark:bg-primary-500/10 rounded-xl border border-primary-500/20">
          <p class="text-xs font-semibold text-primary-600 dark:text-primary-400 uppercase tracking-wider mb-0.5">O‘zbekcha ma’nosi</p>
          <p class="text-base font-bold text-surface-900 dark:text-white">{{ word.meaningUz }}</p>
        </div>

        <!-- English Definition -->
        <div v-if="word.definition" class="mb-4">
          <p class="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-1">English Definition</p>
          <p class="text-surface-700 dark:text-surface-300 leading-relaxed">{{ word.definition }}</p>
        </div>

        <!-- Examples Block (Cambridge Dictionary) -->
        <div v-if="(word.examples && word.examples.length) || word.example" class="mb-4 p-4 bg-surface-50 dark:bg-surface-800/40 rounded-xl space-y-3">
          <p class="text-xs font-semibold text-surface-400 uppercase tracking-wider">
            {{ (word.examples && word.examples.length > 1) ? 'Examples' : 'Example' }}
          </p>

          <!-- Multiple Examples List -->
          <div v-if="word.examples && word.examples.length" class="space-y-3">
            <div
              v-for="(ex, idx) in word.examples"
              :key="idx"
              class="border-b last:border-b-0 border-surface-200/60 dark:border-surface-700/60 pb-2.5 last:pb-0 space-y-1"
            >
              <p class="text-surface-800 dark:text-surface-200 italic text-sm leading-relaxed">
                "{{ ex.en }}"
              </p>
              <p v-if="ex.uz" class="text-xs text-surface-500 dark:text-surface-400">
                {{ ex.uz }}
              </p>
            </div>
          </div>

          <!-- Fallback single example -->
          <div v-else-if="word.example" class="space-y-1">
            <p class="text-surface-800 dark:text-surface-200 italic text-sm leading-relaxed">
              "{{ word.example }}"
            </p>
            <p v-if="word.exampleUz" class="text-xs text-surface-500 dark:text-surface-400">
              {{ word.exampleUz }}
            </p>
          </div>

          <!-- Cambridge Dictionary Source -->
          <div v-if="word.source" class="text-xs text-surface-400 dark:text-surface-500 italic text-right pt-1">
            Manba: {{ word.source }}
          </div>
        </div>

        <!-- Multiple Senses -->
        <div v-if="word.senses && word.senses.length > 0" class="mb-6 space-y-3">
          <p class="text-xs font-semibold text-surface-400 uppercase tracking-wider">Multiple Senses / Qo‘shimcha ma’nolari</p>
          <div
            v-for="(sense, idx) in word.senses"
            :key="idx"
            class="p-3.5 bg-surface-50 dark:bg-surface-800/60 rounded-xl border border-surface-200/80 dark:border-surface-700/80 space-y-1.5"
          >
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300">
                Sense {{ idx + 1 }}
              </span>
              <span class="text-xs font-semibold text-primary-600 dark:text-primary-400">
                {{ sense.meaningUz }}
              </span>
            </div>
            <p class="text-xs text-surface-700 dark:text-surface-300 leading-relaxed">{{ sense.definition }}</p>
            <div v-if="sense.example" class="pt-1 border-t border-surface-200/60 dark:border-surface-700/60">
              <p class="text-xs text-surface-600 dark:text-surface-400 italic">"{{ sense.example }}"</p>
              <p v-if="sense.exampleUz" class="text-[11px] text-surface-500 mt-0.5">{{ sense.exampleUz }}</p>
            </div>
          </div>
        </div>

        <!-- Progress info -->
        <div class="mb-6 p-4 bg-surface-50 dark:bg-surface-800/50 rounded-xl">
          <div class="grid grid-cols-3 gap-4 text-center">
            <div>
              <p class="text-xl font-bold text-surface-900 dark:text-white">{{ progressStore.getProgress(word.id).correct }}</p>
              <p class="text-xs text-surface-400">Correct</p>
            </div>
            <div>
              <p class="text-xl font-bold text-surface-900 dark:text-white">{{ progressStore.getProgress(word.id).incorrect }}</p>
              <p class="text-xs text-surface-400">Incorrect</p>
            </div>
            <div>
              <p class="text-xl font-bold text-surface-900 dark:text-white">{{ progressStore.getProgress(word.id).interval }}d</p>
              <p class="text-xs text-surface-400">Interval</p>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex flex-wrap gap-2">
          <button
            v-if="status !== 'mastered'"
            @click="handleLearn"
            class="flex-1 px-4 py-2.5 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium rounded-xl transition-colors shadow-sm"
          >
            {{ status === 'new' ? 'Mark as Learned' : 'Mark as Mastered' }}
          </button>

          <button
            @click="handleFavorite"
            class="px-4 py-2.5 rounded-xl text-sm font-medium transition-colors border"
            :class="isFav
              ? 'bg-amber-50 dark:bg-amber-500/10 border-amber-200 dark:border-amber-500/20 text-amber-600 dark:text-amber-400'
              : 'bg-white dark:bg-surface-800 border-surface-200 dark:border-surface-700 text-surface-600 dark:text-surface-400 hover:border-amber-300'"
          >
            <Star :size="16" :class="isFav ? 'fill-amber-400' : ''" class="inline -mt-0.5 mr-1" />
            {{ isFav ? 'Favorited' : 'Favorite' }}
          </button>

          <button
            v-if="status !== 'new'"
            @click="handleReset"
            class="px-4 py-2.5 rounded-xl text-sm font-medium bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400 hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors"
          >
            <RotateCcw :size="14" class="inline -mt-0.5 mr-1" />
            Reset
          </button>
        </div>
      </div>

      <!-- Navigation -->
      <div v-if="words && words.length > 1" class="flex items-center justify-between px-6 py-3 border-t border-surface-200 dark:border-surface-800">
        <button
          @click="emit('navigate', 'prev')"
          :disabled="currentIndex === 0"
          class="flex items-center gap-1 px-3 py-1.5 text-sm text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 disabled:opacity-30 transition-colors"
        >
          <ChevronLeft :size="16" />
          Previous
        </button>
        <span class="text-xs text-surface-400">{{ (currentIndex || 0) + 1 }} / {{ words.length }}</span>
        <button
          @click="emit('navigate', 'next')"
          :disabled="currentIndex === words.length - 1"
          class="flex items-center gap-1 px-3 py-1.5 text-sm text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 disabled:opacity-30 transition-colors"
        >
          Next
          <ChevronRight :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>

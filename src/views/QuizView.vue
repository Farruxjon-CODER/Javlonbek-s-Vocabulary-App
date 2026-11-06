<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuiz } from '@/composables/useQuiz'
import type { QuizMode } from '@/types'
import ProgressBar from '@/components/ProgressBar.vue'
import EmptyState from '@/components/EmptyState.vue'
import {
  HelpCircle,
  CheckCircle2,
  XCircle,
  Trophy,
  RefreshCw,
  ArrowRight,
  LayoutDashboard
} from 'lucide-vue-next'

const router = useRouter()
const {
  currentQuestion,
  selectedAnswer,
  showResult,
  isQuizComplete,
  progress,
  quizResult,
  generateQuiz,
  selectAnswer,
  nextQuestion,
  resetQuiz
} = useQuiz()

const isStarted = ref(false)
const selectedMode = ref<QuizMode>('mixed')
const selectedCount = ref(20)

const modes = [
  { value: 'word-to-meaning' as QuizMode, label: 'Word → Meaning', desc: 'Identify word meaning' },
  { value: 'word-to-pos' as QuizMode, label: 'Word → POS', desc: 'Identify the part of speech' },
  { value: 'word-to-cefr' as QuizMode, label: 'Word → CEFR', desc: 'Identify the CEFR level' },
  { value: 'mixed' as QuizMode, label: 'Mixed', desc: 'Random mix of question types' },
]

const counts = [10, 20, 30]

function start() {
  generateQuiz(selectedMode.value, selectedCount.value)
  isStarted.value = true
}

function retry() {
  resetQuiz()
  isStarted.value = false
}

function getScoreColor(pct: number) {
  if (pct >= 80) return 'text-emerald-500'
  if (pct >= 60) return 'text-amber-500'
  return 'text-rose-500'
}

function getScoreMessage(pct: number) {
  if (pct >= 90) return 'Outstanding! 🌟'
  if (pct >= 80) return 'Great work! 🎉'
  if (pct >= 70) return 'Good job! 👍'
  if (pct >= 50) return 'Keep practicing! 💪'
  return 'Room for improvement 📚'
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Quiz</h1>
      <p class="text-sm text-surface-500">Test your vocabulary knowledge</p>
    </div>

    <!-- Setup Screen -->
    <div v-if="!isStarted" class="space-y-6">
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-8 border border-surface-200 dark:border-surface-800">
        <div class="text-center mb-8">
          <div class="w-16 h-16 rounded-2xl bg-primary-50 dark:bg-primary-500/10 flex items-center justify-center mx-auto mb-4">
            <HelpCircle :size="28" class="text-primary-500" />
          </div>
          <h2 class="text-xl font-bold text-surface-900 dark:text-white mb-2">Choose Quiz Mode</h2>
          <p class="text-sm text-surface-500">Select the type and number of questions</p>
        </div>

        <!-- Mode -->
        <div class="mb-6">
          <label class="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-3 block">Quiz Mode</label>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              v-for="mode in modes"
              :key="mode.value"
              @click="selectedMode = mode.value"
              class="p-4 rounded-xl border-2 text-left transition-all"
              :class="selectedMode === mode.value
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-500/10'
                : 'border-surface-200 dark:border-surface-800 hover:border-surface-300 dark:hover:border-surface-700'"
            >
              <p class="font-semibold text-sm text-surface-900 dark:text-white">{{ mode.label }}</p>
              <p class="text-xs text-surface-500 mt-0.5">{{ mode.desc }}</p>
            </button>
          </div>
        </div>

        <!-- Count -->
        <div class="mb-8">
          <label class="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-3 block">Questions</label>
          <div class="flex gap-3">
            <button
              v-for="count in counts"
              :key="count"
              @click="selectedCount = count"
              class="px-6 py-2.5 rounded-xl text-sm font-medium transition-colors"
              :class="selectedCount === count
                ? 'bg-primary-600 text-white'
                : 'bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400 hover:bg-surface-200 dark:hover:bg-surface-700'"
            >
              {{ count }}
            </button>
          </div>
        </div>

        <button
          @click="start"
          class="w-full py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-colors shadow-lg shadow-primary-500/20"
        >
          Start Quiz
        </button>
      </div>
    </div>

    <!-- Quiz Complete -->
    <div v-else-if="isQuizComplete && quizResult" class="space-y-6">
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-8 border border-surface-200 dark:border-surface-800 text-center">
        <div class="w-16 h-16 rounded-2xl bg-primary-50 dark:bg-primary-500/10 flex items-center justify-center mx-auto mb-4">
          <Trophy :size="28" class="text-primary-500" />
        </div>

        <p :class="getScoreColor(Math.round((quizResult.correct / quizResult.total) * 100))"
           class="text-6xl font-bold mb-2">
          {{ Math.round((quizResult.correct / quizResult.total) * 100) }}%
        </p>
        <p class="text-lg text-surface-600 dark:text-surface-400 mb-1">
          {{ quizResult.correct }} / {{ quizResult.total }} correct
        </p>
        <p class="text-sm text-surface-500 mb-8">
          {{ getScoreMessage(Math.round((quizResult.correct / quizResult.total) * 100)) }}
        </p>

        <div class="flex flex-wrap justify-center gap-3">
          <button
            @click="retry"
            class="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-xl transition-colors"
          >
            <RefreshCw :size="16" class="inline -mt-0.5 mr-1" />
            Retry
          </button>
          <button
            @click="router.push('/')"
            class="px-6 py-2.5 bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400 font-medium rounded-xl hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors"
          >
            <LayoutDashboard :size="16" class="inline -mt-0.5 mr-1" />
            Dashboard
          </button>
        </div>
      </div>
    </div>

    <!-- Active Quiz -->
    <div v-else-if="currentQuestion" class="space-y-6">
      <div class="flex items-center gap-4">
        <ProgressBar :value="progress.current" :max="progress.total" size="sm" class="flex-1" />
        <span class="text-sm text-surface-500 tabular-nums">{{ progress.current }} / {{ progress.total }}</span>
      </div>

      <div class="bg-white dark:bg-surface-900 rounded-2xl border border-surface-200 dark:border-surface-800 shadow-lg overflow-hidden">
        <!-- Question -->
        <div class="p-8 text-center border-b border-surface-200 dark:border-surface-800">
          <p class="text-sm text-surface-400 mb-3">{{ currentQuestion.type === 'word-to-pos' ? 'Part of Speech' : 'CEFR Level' }}</p>
          <h2 class="text-2xl font-bold text-surface-900 dark:text-white">{{ currentQuestion.question }}</h2>
        </div>

        <!-- Options -->
        <div class="p-6 space-y-3">
          <button
            v-for="(option, i) in currentQuestion.options"
            :key="i"
            @click="selectAnswer(i)"
            :disabled="showResult"
            class="w-full p-4 rounded-xl border-2 text-left transition-all font-medium"
            :class="{
              'border-surface-200 dark:border-surface-800 hover:border-primary-300 dark:hover:border-primary-500/30 hover:bg-primary-50 dark:hover:bg-primary-500/5': !showResult,
              'border-emerald-500 bg-emerald-50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400': showResult && i === currentQuestion.correctIndex,
              'border-rose-500 bg-rose-50 dark:bg-rose-500/10 text-rose-700 dark:text-rose-400': showResult && i === selectedAnswer && i !== currentQuestion.correctIndex,
              'border-surface-200 dark:border-surface-800 opacity-50': showResult && i !== currentQuestion.correctIndex && i !== selectedAnswer,
            }"
          >
            <div class="flex items-center justify-between">
              <span>{{ option }}</span>
              <CheckCircle2 v-if="showResult && i === currentQuestion.correctIndex" :size="20" class="text-emerald-500" />
              <XCircle v-if="showResult && i === selectedAnswer && i !== currentQuestion.correctIndex" :size="20" class="text-rose-500" />
            </div>
          </button>
        </div>

        <!-- Next Button -->
        <div v-if="showResult" class="px-6 pb-6">
          <button
            @click="nextQuestion"
            class="w-full py-3 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-xl transition-colors"
          >
            {{ progress.current < progress.total ? 'Next Question' : 'See Results' }}
            <ArrowRight :size="16" class="inline -mt-0.5 ml-1" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

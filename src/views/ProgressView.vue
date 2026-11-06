<script setup lang="ts">
import { computed } from 'vue'
import { useWordsStore } from '@/stores/words'
import { useProgressStore } from '@/stores/progress'
import { useStatsStore } from '@/stores/stats'
import { useSettingsStore } from '@/stores/settings'
import StatCard from '@/components/StatCard.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import CEFRBadge from '@/components/CEFRBadge.vue'
import {
  BookOpen,
  GraduationCap,
  Star,
  Brain,
  Target,
  TrendingUp,
  BarChart3,
  Flame
} from 'lucide-vue-next'

const wordsStore = useWordsStore()
const progressStore = useProgressStore()
const statsStore = useStatsStore()
const settingsStore = useSettingsStore()

const overallProgress = computed(() => {
  if (wordsStore.totalWords === 0) return 0
  return Math.round((progressStore.learnedWords.length / wordsStore.totalWords) * 100)
})

const masteryProgress = computed(() => {
  if (wordsStore.totalWords === 0) return 0
  return Math.round((progressStore.masteredWords.length / wordsStore.totalWords) * 100)
})

const totalWordsLearned = computed(() => {
  return statsStore.dailyStatsHistory.reduce((sum, d) => sum + d.wordsLearned, 0)
})

const totalQuizzes = computed(() => statsStore.quizHistory.length)

// CEFR Stacked Bar Chart Metrics
const cefrChartData = computed(() => {
  return ['A1', 'A2', 'B1', 'B2'].map(level => {
    const data = progressStore.cefrDistribution[level] || { total: 0, learned: 0, mastered: 0 }
    const total = data.total || 1
    const mastered = data.mastered || 0
    const learning = Math.max(0, (data.learned || 0) - mastered)
    const newWords = Math.max(0, total - (mastered + learning))

    return {
      level,
      total: data.total || 0,
      mastered,
      learning,
      newWords,
      masteredPct: Math.round((mastered / total) * 100),
      learningPct: Math.round((learning / total) * 100),
      newPct: Math.max(0, 100 - Math.round((mastered / total) * 100) - Math.round((learning / total) * 100))
    }
  })
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Progress</h1>
      <p class="text-sm text-surface-500">Track your learning journey</p>
    </div>

    <!-- Overview Stats -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
      <StatCard
        title="Total Words"
        :value="wordsStore.totalWords"
        :icon="BookOpen"
        color="bg-primary-50 dark:bg-primary-500/10 text-primary-500"
      />
      <StatCard
        title="Learned"
        :value="progressStore.learnedWords.length"
        :subtitle="`${overallProgress}% of all words`"
        :icon="GraduationCap"
        color="bg-amber-50 dark:bg-amber-500/10 text-amber-500"
      />
      <StatCard
        title="Mastered"
        :value="progressStore.masteredWords.length"
        :subtitle="`${masteryProgress}% mastery`"
        :icon="Star"
        color="bg-emerald-50 dark:bg-emerald-500/10 text-emerald-500"
      />
      <StatCard
        title="Review Due"
        :value="progressStore.reviewDueWords.length"
        :icon="Brain"
        color="bg-violet-50 dark:bg-violet-500/10 text-violet-500"
      />
    </div>

    <!-- Overall Progress -->
    <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800 mb-8">
      <h3 class="font-semibold text-surface-900 dark:text-white mb-5 flex items-center gap-2">
        <TrendingUp :size="18" class="text-primary-500" />
        Overall Progress
      </h3>

      <div class="space-y-4">
        <div>
          <div class="flex justify-between mb-1.5">
            <span class="text-sm text-surface-600 dark:text-surface-400">Words Learned</span>
            <span class="text-sm font-medium text-surface-900 dark:text-white">{{ progressStore.learnedWords.length }} / {{ wordsStore.totalWords }}</span>
          </div>
          <ProgressBar :value="progressStore.learnedWords.length" :max="wordsStore.totalWords" color="bg-amber-500" size="md" />
        </div>

        <div>
          <div class="flex justify-between mb-1.5">
            <span class="text-sm text-surface-600 dark:text-surface-400">Words Mastered</span>
            <span class="text-sm font-medium text-surface-900 dark:text-white">{{ progressStore.masteredWords.length }} / {{ wordsStore.totalWords }}</span>
          </div>
          <ProgressBar :value="progressStore.masteredWords.length" :max="wordsStore.totalWords" color="bg-emerald-500" size="md" />
        </div>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      <!-- CEFR Stacked Bar Chart -->
      <div class="bg-white dark:bg-surface-900 rounded-3xl p-6 border border-surface-200 dark:border-surface-800 shadow-sm">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
          <h3 class="font-bold text-base text-surface-900 dark:text-white flex items-center gap-2">
            <BarChart3 :size="18" class="text-primary-600 dark:text-primary-400" />
            CEFR Stacked Bar Chart
          </h3>

          <!-- Strict Color Legend -->
          <div class="flex items-center gap-3 text-xs">
            <div class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full bg-[#22c55e]"></span>
              <span class="text-surface-600 dark:text-surface-400 font-medium">Mastered</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full bg-[#eab308]"></span>
              <span class="text-surface-600 dark:text-surface-400 font-medium">Learning</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full bg-[#9ca3af]"></span>
              <span class="text-surface-600 dark:text-surface-400 font-medium">New</span>
            </div>
          </div>
        </div>

        <!-- Stacked Bars per Level -->
        <div class="space-y-5">
          <div v-for="item in cefrChartData" :key="item.level" class="group">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <CEFRBadge :level="item.level" />
                <span class="text-xs font-semibold text-surface-700 dark:text-surface-300">
                  {{ item.level }} Darajasi
                </span>
              </div>
              <div class="text-xs text-surface-400 tabular-nums">
                <span class="text-emerald-600 dark:text-emerald-400 font-medium">{{ item.mastered }}M</span> •
                <span class="text-amber-600 dark:text-amber-400 font-medium">{{ item.learning }}L</span> •
                <span class="text-surface-400">{{ item.newWords }}N</span>
                <span class="ml-1 text-surface-500 font-semibold">({{ item.total }} ta)</span>
              </div>
            </div>

            <!-- Stacked Bar Track -->
            <div class="w-full h-4 rounded-full overflow-hidden flex bg-surface-100 dark:bg-surface-800 p-0.5 gap-0.5 border border-surface-200 dark:border-surface-700/60 shadow-inner">
              <!-- Mastered Segment (Green #22c55e) -->
              <div
                v-if="item.mastered > 0"
                class="h-full rounded-sm bg-[#22c55e] transition-all duration-500 relative group/seg cursor-pointer"
                :style="{ width: `${item.masteredPct}%` }"
                :title="`Mastered: ${item.mastered} ta (${item.masteredPct}%)`"
              ></div>

              <!-- Learning Segment (Yellow #eab308) -->
              <div
                v-if="item.learning > 0"
                class="h-full rounded-sm bg-[#eab308] transition-all duration-500 relative group/seg cursor-pointer"
                :style="{ width: `${item.learningPct}%` }"
                :title="`Learning: ${item.learning} ta (${item.learningPct}%)`"
              ></div>

              <!-- New Words Segment (Gray #9ca3af) -->
              <div
                v-if="item.newWords > 0"
                class="h-full rounded-sm bg-[#9ca3af] transition-all duration-500 relative group/seg cursor-pointer"
                :style="{ width: `${item.newPct}%` }"
                :title="`New: ${item.newWords} ta (${item.newPct}%)`"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
        <h3 class="font-semibold text-surface-900 dark:text-white mb-5 flex items-center gap-2">
          <Target :size="18" class="text-primary-500" />
          Learning Stats
        </h3>

        <div class="space-y-4">
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Current Streak</span>
            <span class="font-semibold text-surface-900 dark:text-white flex items-center gap-1">
              <Flame :size="16" class="text-orange-500" />
              {{ statsStore.streak.current }} {{ statsStore.streak.current === 1 ? 'day' : 'days' }}
            </span>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Total Words Reviewed</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ totalWordsLearned }}</span>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Quizzes Taken</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ totalQuizzes }}</span>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Quiz Accuracy</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ statsStore.totalQuizAccuracy }}%</span>
          </div>
          <div class="flex items-center justify-between py-3">
            <span class="text-sm text-surface-600 dark:text-surface-400">Favorites</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ progressStore.favoriteWords.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Weekly Activity -->
    <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
      <h3 class="font-semibold text-surface-900 dark:text-white mb-5">Weekly Activity</h3>

      <div class="flex items-end justify-between gap-2 h-32">
        <div
          v-for="day in statsStore.weeklyActivity"
          :key="day.date"
          class="flex-1 flex flex-col items-center gap-2"
        >
          <span class="text-xs font-medium text-surface-900 dark:text-white tabular-nums">{{ day.wordsLearned }}</span>
          <div class="w-full flex items-end justify-center h-20">
            <div
              class="w-full max-w-[32px] rounded-t-lg transition-all duration-300"
              :class="day.wordsLearned > 0 ? 'bg-primary-500' : 'bg-surface-200 dark:bg-surface-800'"
              :style="{ height: `${Math.max(day.wordsLearned > 0 ? 16 : 4, Math.min((day.wordsLearned / Math.max(settingsStore.settings.dailyGoal, 1)) * 80, 80))}px` }"
            />
          </div>
          <span class="text-xs text-surface-400">{{ day.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

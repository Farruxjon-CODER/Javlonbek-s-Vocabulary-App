<script setup lang="ts">
import { computed } from 'vue'
import apexchart from 'vue3-apexcharts'
import { useWordsStore } from '@/stores/words'
import { useProgressStore } from '@/stores/progress'
import { useStatsStore } from '@/stores/stats'
import { useSettingsStore } from '@/stores/settings'
import StatCard from '@/components/StatCard.vue'
import ProgressBar from '@/components/ProgressBar.vue'
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

// ApexCharts Stacked Bar Series
// Ranglar ketma-ketligi: Mastered (#22c55e), Learning (#eab308), New (#9ca3af)
const chartSeries = computed(() => [
  {
    name: 'Mastered (O‘zlashtirilgan)',
    data: ['A1', 'A2', 'B1', 'B2'].map(level => {
      const data = progressStore.cefrDistribution[level]
      return data?.mastered || 0
    })
  },
  {
    name: 'Learning (O‘rganilayotgan)',
    data: ['A1', 'A2', 'B1', 'B2'].map(level => {
      const data = progressStore.cefrDistribution[level]
      const mastered = data?.mastered || 0
      const learned = data?.learned || 0
      return Math.max(0, learned - mastered)
    })
  },
  {
    name: 'New (Yangi so‘zlar)',
    data: ['A1', 'A2', 'B1', 'B2'].map(level => {
      const data = progressStore.cefrDistribution[level]
      const total = data?.total || 0
      const learned = data?.learned || 0
      return Math.max(0, total - learned)
    })
  }
])

// ApexCharts Options (Stacked Bar Chart, qat'iy ranglar bilan)
const chartOptions = computed(() => ({
  chart: {
    type: 'bar',
    stacked: true,
    toolbar: { show: false },
    fontFamily: 'inherit',
    background: 'transparent',
    animations: {
      enabled: true,
      speed: 600
    }
  },
  // Qat'iy talab qilingan ranglar: Yashil (#22c55e), Sariq (#eab308), Kulrang (#9ca3af)
  colors: ['#22c55e', '#eab308', '#9ca3af'],
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 6,
      columnWidth: '45%',
      dataLabels: {
        total: {
          enabled: true,
          style: {
            fontSize: '11px',
            fontWeight: 700,
            color: settingsStore.isDarkMode ? '#e2e8f0' : '#1e293b'
          }
        }
      }
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    width: 1,
    colors: [settingsStore.isDarkMode ? '#0f172a' : '#ffffff']
  },
  xaxis: {
    categories: ['A1', 'A2', 'B1', 'B2'],
    labels: {
      style: {
        colors: settingsStore.isDarkMode ? '#94a3b8' : '#64748b',
        fontSize: '12px',
        fontWeight: 700
      }
    },
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: {
    title: {
      text: "So'zlar soni",
      style: {
        color: settingsStore.isDarkMode ? '#94a3b8' : '#64748b',
        fontSize: '11px',
        fontWeight: 500
      }
    },
    labels: {
      style: {
        colors: settingsStore.isDarkMode ? '#94a3b8' : '#64748b',
        fontSize: '11px'
      }
    }
  },
  grid: {
    borderColor: settingsStore.isDarkMode ? '#334155' : '#f1f5f9',
    strokeDashArray: 4
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    fontSize: '12px',
    labels: {
      colors: settingsStore.isDarkMode ? '#cbd5e1' : '#475569'
    },
    markers: {
      radius: 12
    }
  },
  tooltip: {
    theme: settingsStore.isDarkMode ? 'dark' : 'light',
    y: {
      formatter: (val: number) => `${val} ta so‘z`
    }
  }
}))
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Progress</h1>
      <p class="text-sm text-surface-500">O‘rganish natijalari va darajangiz statistikasi</p>
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
        Umumiy O‘zlashtirish Progressi
      </h3>

      <div class="space-y-4">
        <div>
          <div class="flex justify-between mb-1.5">
            <span class="text-sm text-surface-600 dark:text-surface-400">O‘rganilgan so‘zlar</span>
            <span class="text-sm font-medium text-surface-900 dark:text-white">{{ progressStore.learnedWords.length }} / {{ wordsStore.totalWords }}</span>
          </div>
          <ProgressBar :value="progressStore.learnedWords.length" :max="wordsStore.totalWords" color="bg-amber-500" size="md" />
        </div>

        <div>
          <div class="flex justify-between mb-1.5">
            <span class="text-sm text-surface-600 dark:text-surface-400">To‘liq o‘zlashtirilgan (Mastered)</span>
            <span class="text-sm font-medium text-surface-900 dark:text-white">{{ progressStore.masteredWords.length }} / {{ wordsStore.totalWords }}</span>
          </div>
          <ProgressBar :value="progressStore.masteredWords.length" :max="wordsStore.totalWords" color="bg-emerald-500" size="md" />
        </div>
      </div>
    </div>

    <!-- Two Column Layout: CEFR Stacked Bar Chart & Quick Stats -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- CEFR Stacked Bar Chart Box -->
      <div class="bg-white dark:bg-surface-900 rounded-3xl p-6 border border-surface-200 dark:border-surface-800 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
            <h3 class="font-bold text-base text-surface-900 dark:text-white flex items-center gap-2">
              <BarChart3 :size="18" class="text-primary-600 dark:text-primary-400" />
              CEFR Progress (Stacked Bar Chart)
            </h3>

            <!-- Ranglar tushuntirishi (Legend) -->
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

          <!-- ApexCharts Komponenti -->
          <div class="w-full min-h-[320px]">
            <apexchart
              type="bar"
              height="320"
              :options="chartOptions"
              :series="chartSeries"
            />
          </div>
        </div>

        <p class="text-xs text-surface-400 mt-4 text-center">
          X o‘qi: A1, A2, B1, B2 darajalari • Y o‘qi: Har bir darajadagi so‘zlar soni
        </p>
      </div>

      <!-- Learning Stats -->
      <div class="bg-white dark:bg-surface-900 rounded-3xl p-6 border border-surface-200 dark:border-surface-800 shadow-sm">
        <h3 class="font-semibold text-surface-900 dark:text-white mb-5 flex items-center gap-2">
          <Target :size="18" class="text-primary-500" />
          O‘rganish Ko‘rsatkichlari
        </h3>

        <div class="space-y-4">
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Joriy Streak</span>
            <span class="font-semibold text-surface-900 dark:text-white flex items-center gap-1">
              <Flame :size="16" class="text-orange-500" />
              {{ statsStore.streak.current }} {{ statsStore.streak.current === 1 ? 'kun' : 'kun' }}
            </span>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Takrorlangan so‘zlar</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ totalWordsLearned }}</span>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Yechilgan testlar</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ totalQuizzes }}</span>
          </div>
          <div class="flex items-center justify-between py-3 border-b border-surface-100 dark:border-surface-800">
            <span class="text-sm text-surface-600 dark:text-surface-400">Test aniqligi</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ statsStore.totalQuizAccuracy }}%</span>
          </div>
          <div class="flex items-center justify-between py-3">
            <span class="text-sm text-surface-600 dark:text-surface-400">Sevimlilar soni</span>
            <span class="font-semibold text-surface-900 dark:text-white">{{ progressStore.favoriteWords.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Weekly Activity -->
    <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
      <h3 class="font-semibold text-primary-600 dark:text-primary-400 mb-5">Haftalik Faollik (Weekly Activity)</h3>

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
              :style="{ height: `${Math.max(day.wordsLearned > 0 ? 16 : 4, Math.min((day.wordsLearned / 20) * 80, 80))}px` }"
            />
          </div>
          <span class="text-xs text-surface-400">{{ day.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

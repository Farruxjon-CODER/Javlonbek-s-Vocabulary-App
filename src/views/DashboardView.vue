<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useWordsStore } from '@/stores/words'
import { useProgressStore } from '@/stores/progress'
import { useStatsStore } from '@/stores/stats'
import { useSettingsStore } from '@/stores/settings'
import { useGamificationStore } from '@/stores/gamification'
import { useAuthStore } from '@/stores/auth'
import StatCard from '@/components/StatCard.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import CEFRBadge from '@/components/CEFRBadge.vue'
import {
  BookOpen,
  GraduationCap,
  Target,
  Flame,
  Star,
  Brain,
  Sparkles,
  TrendingUp,
  CheckCircle2,
  Trophy,
  Coins,
  Award,
  Crown,
  Medal
} from 'lucide-vue-next'

const wordsStore = useWordsStore()
const progressStore = useProgressStore()
const statsStore = useStatsStore()
const settingsStore = useSettingsStore()
const gamificationStore = useGamificationStore()
const authStore = useAuthStore()
const router = useRouter()

const goalOptions = [10, 20, 30, 50]

const learnedCount = computed(() => progressStore.learnedWords.length)
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Informational Banner Poster -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-primary-600 to-primary-900 p-8 sm:p-12 mb-8 text-white shadow-xl shadow-primary-600/25">
      <div class="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/3" />
      <div class="absolute bottom-0 left-0 w-64 h-64 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/3" />

      <div class="relative z-10 flex flex-col md:flex-row justify-between items-center gap-8">
        <!-- Chap tomon (Sarlavha va Tavsif) -->
        <div class="flex-1 text-center md:text-left">
          <div class="inline-flex items-center gap-2 mb-3 px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm border border-white/15">
            <Sparkles :size="18" class="text-purple-200" />
            <span class="text-xs font-semibold tracking-wide text-purple-100 uppercase">Javlonbek's LC</span>
          </div>

          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight mb-3 text-white leading-tight">
            Welcome to Javlonbek's LC
          </h1>
          <p class="text-base sm:text-lg text-purple-100 max-w-xl leading-relaxed">
            One word a day, one step closer to your goal <br class="hidden sm:inline" />
            (Har kuni bir so'z, maqsadlaringiz sari qo'yilgan bir qadam)
          </p>
        </div>

        <!-- O'ng tomon (Imzo rasmi) -->
        <div class="shrink-0 flex items-center justify-center">
          <img
            src="/signature_variant2_white_outline.png"
            alt="Signature"
            class="w-52 sm:w-64 md:w-80 object-contain opacity-95 hover:opacity-100 transition-opacity duration-300"
          />
        </div>
      </div>
    </div>

    <!-- Leaderboard (Peshqadamlar) & Streak Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- Leaderboard (2 Cols) -->
      <div class="lg:col-span-2 bg-white dark:bg-surface-900 rounded-3xl p-6 border border-surface-200 dark:border-surface-800 shadow-sm">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center text-amber-500 shadow-xs">
              <Trophy :size="20" />
            </div>
            <div>
              <h2 class="font-bold text-lg text-surface-900 dark:text-white flex items-center gap-2">
                Leaderboard (Peshqadamlar)
              </h2>
              <p class="text-xs text-surface-400">Yig‘ilgan Coinlar va o‘zlashtirilgan so‘zlar reytingi</p>
            </div>
          </div>

          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400 text-xs font-semibold self-start sm:self-auto">
            <Award :size="16" />
            <span>Sizning o'rningiz: #{{ gamificationStore.currentUserRank }}</span>
          </div>
        </div>

        <!-- Leaderboard Table / Cards -->
        <div class="space-y-2.5">
          <div
            v-for="(u, index) in gamificationStore.leaderboard.slice(0, 5)"
            :key="u.id"
            class="flex items-center justify-between p-3 sm:px-4 rounded-2xl transition-all duration-200"
            :class="u.isCurrentUser
              ? 'bg-primary-50/80 dark:bg-primary-500/15 border-2 border-primary-500 shadow-sm'
              : 'bg-surface-50 dark:bg-surface-800/40 hover:bg-surface-100 dark:hover:bg-surface-800/80 border border-surface-100 dark:border-surface-800/50'"
          >
            <div class="flex items-center gap-3 min-w-0">
              <!-- Rank Badge -->
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0"
                :class="[
                  index === 0 ? 'bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400 shadow-xs' :
                  index === 1 ? 'bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300' :
                  index === 2 ? 'bg-amber-900/10 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300' :
                  'text-surface-400 bg-surface-100 dark:bg-surface-800'
                ]"
              >
                <Crown v-if="index === 0" :size="15" class="text-amber-500" />
                <span v-else>{{ index + 1 }}</span>
              </div>

              <!-- Avatar -->
              <img
                :src="u.avatar"
                :alt="u.name"
                class="w-10 h-10 rounded-full object-cover shrink-0 border border-surface-200 dark:border-surface-700 shadow-xs"
              />

              <div class="min-w-0">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold text-surface-900 dark:text-white truncate">
                    {{ u.name }}
                  </span>
                  <span
                    v-if="u.badge"
                    class="px-2 py-0.5 rounded-md text-[10px] font-semibold tracking-wide shrink-0"
                    :class="u.isCurrentUser
                      ? 'bg-primary-600 text-white'
                      : 'bg-surface-200 dark:bg-surface-700 text-surface-700 dark:text-surface-300'"
                  >
                    {{ u.badge }}
                  </span>
                </div>
                <p class="text-xs text-surface-400 truncate">
                  {{ u.wordsLearned }} ta so‘z • {{ u.accuracy }}% aniqlik
                </p>
              </div>
            </div>

            <!-- Coin Balance -->
            <div class="flex items-center gap-1.5 shrink-0 pl-2">
              <span class="text-sm font-bold text-amber-600 dark:text-amber-400 tabular-nums">
                🪙 {{ u.coins }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Streak & Gamification Stats (1 Col) -->
      <div class="bg-white dark:bg-surface-900 rounded-3xl p-6 border border-surface-200 dark:border-surface-800 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-4">
            <div class="w-10 h-10 rounded-2xl bg-orange-50 dark:bg-orange-500/10 flex items-center justify-center text-orange-500">
              <Flame :size="20" />
            </div>
            <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-orange-100 dark:bg-orange-500/20 text-orange-700 dark:text-orange-400">
              Active Streak
            </span>
          </div>

          <h3 class="text-base font-bold text-surface-900 dark:text-white">Kunlik Davomiylik</h3>
          <p class="text-xs text-surface-400 mb-4">Har kuni uzluksiz so‘z o‘rganing</p>

          <div class="flex items-baseline gap-2 mb-3">
            <span class="text-5xl font-black text-primary-600 dark:text-primary-400">{{ statsStore.streak.current }}</span>
            <span class="text-sm font-medium text-surface-400">kun</span>
          </div>

          <p class="text-xs text-surface-400">
            {{ statsStore.streak.current > 0 ? '🔥 Zo‘r ketmoqdasiz! Har kuni davom eting.' : '🚀 Streakni boshlash uchun bugun 1 ta so‘z o‘rganing!' }}
          </p>
        </div>

        <!-- Coin Balance Card -->
        <div class="mt-6 p-4 rounded-2xl bg-gradient-to-br from-amber-500/10 to-primary-500/10 border border-amber-500/20">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-medium text-surface-600 dark:text-surface-400">Sizning balansingiz</span>
            <span class="text-xs font-bold text-amber-600 dark:text-amber-400 flex items-center gap-1">
              <Coins :size="14" /> +10 har bir to‘g‘ri testga
            </span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-3xl font-black text-amber-500">🪙 {{ gamificationStore.coins }}</span>
            <span class="text-xs text-surface-400">Coin</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
      <StatCard
        title="Total Words"
        :value="wordsStore.totalWords"
        :icon="BookOpen"
        color="bg-primary-50 dark:bg-primary-500/10 text-primary-500"
      />
      <StatCard
        title="Learned"
        :value="learnedCount"
        :subtitle="`${wordsStore.totalWords ? Math.round((learnedCount / wordsStore.totalWords) * 100) : 0}% complete`"
        :icon="GraduationCap"
        color="bg-emerald-50 dark:bg-emerald-500/10 text-emerald-500"
      />
      <StatCard
        title="Favorites"
        :value="progressStore.favoriteWords.length"
        :icon="Star"
        color="bg-amber-50 dark:bg-amber-500/10 text-amber-500"
      />
      <StatCard
        title="Review Due"
        :value="progressStore.reviewDueWords.length"
        :icon="Brain"
        color="bg-violet-50 dark:bg-violet-500/10 text-violet-500"
      />
    </div>

    <!-- CEFR Distribution -->
    <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800 mb-8">
      <h3 class="font-semibold text-primary-600 dark:text-primary-400 mb-5 flex items-center gap-2">
        <TrendingUp :size="18" class="text-primary-600 dark:text-primary-400" />
        CEFR Progress
      </h3>

      <div class="space-y-4">
        <div v-for="level in ['A1', 'A2', 'B1', 'B2']" :key="level" class="flex items-center gap-4">
          <CEFRBadge :level="level" />
          <div class="flex-1">
            <ProgressBar
              :value="progressStore.cefrDistribution[level]?.learned || 0"
              :max="progressStore.cefrDistribution[level]?.total || 1"
              size="sm"
              :color="level === 'A1' ? 'bg-emerald-500' : level === 'A2' ? 'bg-sky-500' : level === 'B1' ? 'bg-amber-500' : 'bg-rose-500'"
            />
          </div>
          <span class="text-sm text-surface-500 tabular-nums w-20 text-right">
            {{ progressStore.cefrDistribution[level]?.learned || 0 }} / {{ progressStore.cefrDistribution[level]?.total || 0 }}
          </span>
        </div>
      </div>
    </div>

    <!-- Weekly Activity -->
    <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
      <h3 class="font-semibold text-primary-600 dark:text-primary-400 mb-5">Weekly Activity</h3>

      <div class="flex items-end justify-between gap-2 h-32">
        <div
          v-for="day in statsStore.weeklyActivity"
          :key="day.date"
          class="flex-1 flex flex-col items-center gap-2"
        >
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

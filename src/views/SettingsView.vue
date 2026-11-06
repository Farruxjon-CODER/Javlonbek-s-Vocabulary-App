<script setup lang="ts">
import { ref } from 'vue'
import { useWordsStore } from '@/stores/words'
import { useSettingsStore } from '@/stores/settings'
import { useToastStore } from '@/stores/toast'
import { resetAppData } from '@/utils/resetApp'
import { Sun, Moon, Monitor, Trash2, Info, AlertTriangle } from 'lucide-vue-next'

const wordsStore = useWordsStore()
const settingsStore = useSettingsStore()
const toastStore = useToastStore()
const showConfirmReset = ref(false)

const themes = [
  { value: 'light' as const, label: 'Light', icon: Sun },
  { value: 'dark' as const, label: 'Dark', icon: Moon },
  { value: 'system' as const, label: 'System', icon: Monitor },
]

const goalOptions = [10, 20, 30, 50]

function setTheme(theme: 'light' | 'dark' | 'system') {
  settingsStore.updateSettings({ theme })
  toastStore.addToast(`Theme set to ${theme}`, 'info')
}

function handleResetClick() {
  showConfirmReset.value = true
}

function confirmReset() {
  resetAppData()
}

function cancelReset() {
  showConfirmReset.value = false
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-surface-900 dark:text-white mb-1">Settings</h1>
      <p class="text-sm text-surface-500">Customize your learning experience</p>
    </div>

    <div class="space-y-6">
      <!-- Theme -->
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
        <h3 class="font-semibold text-surface-900 dark:text-white mb-4">Appearance</h3>
        <div class="flex gap-3">
          <button
            v-for="theme in themes"
            :key="theme.value"
            @click="setTheme(theme.value)"
            class="flex-1 flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all"
            :class="settingsStore.settings.theme === theme.value
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-500/10'
              : 'border-surface-200 dark:border-surface-800 hover:border-surface-300 dark:hover:border-surface-700'"
          >
            <component :is="theme.icon" :size="22" :class="settingsStore.settings.theme === theme.value ? 'text-primary-500' : 'text-surface-400'" />
            <span class="text-sm font-medium" :class="settingsStore.settings.theme === theme.value ? 'text-primary-600 dark:text-primary-400' : 'text-surface-600 dark:text-surface-400'">{{ theme.label }}</span>
          </button>
        </div>
      </div>

      <!-- Daily Goal -->
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
        <h3 class="font-semibold text-surface-900 dark:text-white mb-4">Daily Goal</h3>
        <p class="text-sm text-surface-500 mb-4">How many words do you want to learn each day?</p>
        <div class="flex gap-3">
          <button
            v-for="goal in goalOptions"
            :key="goal"
            @click="settingsStore.setDailyGoal(goal)"
            class="flex-1 py-3 rounded-xl text-sm font-semibold transition-colors"
            :class="settingsStore.settings.dailyGoal === goal
              ? 'bg-primary-600 text-white'
              : 'bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400 hover:bg-surface-200 dark:hover:bg-surface-700'"
          >
            {{ goal }} words
          </button>
        </div>
      </div>

      <!-- Keyboard Shortcuts -->
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
        <h3 class="font-semibold text-surface-900 dark:text-white mb-4">Keyboard Shortcuts</h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between py-2">
            <span class="text-sm text-surface-600 dark:text-surface-400">Global Search</span>
            <kbd class="px-2 py-1 bg-surface-100 dark:bg-surface-800 rounded text-xs font-mono text-surface-500">Ctrl + K</kbd>
          </div>
          <div class="flex items-center justify-between py-2">
            <span class="text-sm text-surface-600 dark:text-surface-400">Flip Flashcard</span>
            <kbd class="px-2 py-1 bg-surface-100 dark:bg-surface-800 rounded text-xs font-mono text-surface-500">Space</kbd>
          </div>
          <div class="flex items-center justify-between py-2">
            <span class="text-sm text-surface-600 dark:text-surface-400">Previous / Next</span>
            <div class="flex gap-1">
              <kbd class="px-2 py-1 bg-surface-100 dark:bg-surface-800 rounded text-xs font-mono text-surface-500">←</kbd>
              <kbd class="px-2 py-1 bg-surface-100 dark:bg-surface-800 rounded text-xs font-mono text-surface-500">→</kbd>
            </div>
          </div>
          <div class="flex items-center justify-between py-2">
            <span class="text-sm text-surface-600 dark:text-surface-400">Toggle Favorite</span>
            <kbd class="px-2 py-1 bg-surface-100 dark:bg-surface-800 rounded text-xs font-mono text-surface-500">F</kbd>
          </div>
          <div class="flex items-center justify-between py-2">
            <span class="text-sm text-surface-600 dark:text-surface-400">Mark Known</span>
            <kbd class="px-2 py-1 bg-surface-100 dark:bg-surface-800 rounded text-xs font-mono text-surface-500">K</kbd>
          </div>
          <div class="flex items-center justify-between py-2">
            <span class="text-sm text-surface-600 dark:text-surface-400">Close Modal</span>
            <kbd class="px-2 py-1 bg-surface-100 dark:bg-surface-800 rounded text-xs font-mono text-surface-500">Esc</kbd>
          </div>
        </div>
      </div>

      <!-- About -->
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-surface-200 dark:border-surface-800">
        <h3 class="font-semibold text-surface-900 dark:text-white mb-4 flex items-center gap-2">
          <Info :size="18" class="text-primary-500" />
          About
        </h3>
        <div class="space-y-2 text-sm text-surface-600 dark:text-surface-400">
          <p><strong class="text-surface-900 dark:text-white">Javlonbek's LC</strong> — Master the Oxford 5000 IELTS vocabulary, one word at a time.</p>
          <p>Dataset: American Oxford 5000 by CEFR level (A1–B2) curated for IELTS preparation</p>
          <p>Total words: {{ wordsStore.totalWords.toLocaleString() }} (Fully enriched with definitions, Uzbek meanings & examples)</p>
          <p>All data is stored locally in your browser. No account required.</p>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="bg-white dark:bg-surface-900 rounded-2xl p-6 border border-rose-200 dark:border-rose-500/20">
        <h3 class="font-semibold text-rose-600 dark:text-rose-400 mb-2">Danger Zone</h3>
        <p class="text-sm text-surface-500 mb-4">Barcha o‘zlashtirilgan so‘zlar, streak, sevimlilar va statistika o‘chiriladi.</p>

        <button
          type="button"
          @click="handleResetClick"
          class="px-4 py-2.5 bg-rose-600 hover:bg-rose-700 text-white text-sm font-medium rounded-xl transition-colors flex items-center gap-2"
        >
          <Trash2 :size="15" />
          Barcha ma'lumotlarni o'chirish
        </button>
      </div>
    </div>

    <div
      v-if="showConfirmReset"
      class="fixed inset-0 z-[90] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      @click.self="cancelReset"
    >
      <div class="w-full max-w-md bg-white dark:bg-surface-900 rounded-2xl border border-rose-200 dark:border-rose-500/30 p-6 shadow-2xl">
        <div class="flex items-start gap-3 mb-4">
          <div class="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-500/10 flex items-center justify-center shrink-0">
            <AlertTriangle :size="20" class="text-rose-600 dark:text-rose-400" />
          </div>
          <div>
            <h2 class="text-base font-semibold text-rose-700 dark:text-rose-300">Ma'lumotlarni o'chirish</h2>
            <p class="text-sm text-surface-600 dark:text-surface-400 mt-1">
              Rostdan ham barcha ma'lumotlarni va o'zlashtirilgan so'zlarni o'chirmoqchimisiz? Bu jarayonni orqaga qaytarib bo'lmaydi.
            </p>
          </div>
        </div>
        <div class="flex items-center justify-end gap-2">
          <button
            type="button"
            @click="cancelReset"
            class="px-4 py-2 bg-surface-200 dark:bg-surface-800 text-surface-700 dark:text-surface-300 hover:bg-surface-300 dark:hover:bg-surface-700 text-sm font-medium rounded-lg transition-colors"
          >
            Bekor qilish
          </button>
          <button
            type="button"
            @click="confirmReset"
            class="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-sm font-semibold rounded-lg transition-colors"
          >
            Ha, o'chirish
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

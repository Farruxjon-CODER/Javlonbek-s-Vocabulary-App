<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'

const props = defineProps<{
  title: string
  value: string | number
  subtitle?: string
  icon?: Component
  color?: string
  trend?: 'up' | 'down' | 'neutral'
}>()
</script>

<template>
  <div class="bg-white dark:bg-surface-900 rounded-2xl p-5 border border-surface-200 dark:border-surface-800 hover:border-surface-300 dark:hover:border-surface-700 transition-colors">
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-surface-500 dark:text-surface-400">{{ title }}</p>
        <p class="mt-1.5 text-2xl font-bold text-surface-900 dark:text-white">{{ value }}</p>
        <p v-if="subtitle" class="mt-1 text-xs text-surface-400">{{ subtitle }}</p>
      </div>
      <div
        v-if="icon"
        class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
        :class="color || 'bg-primary-50 dark:bg-primary-500/10 text-primary-500'"
      >
        <component :is="icon" :size="20" />
      </div>
    </div>
  </div>
</template>

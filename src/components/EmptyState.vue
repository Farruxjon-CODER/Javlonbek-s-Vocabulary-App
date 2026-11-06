<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  title: string
  description?: string
  icon?: Component
  actionLabel?: string
}>()

defineEmits<{ action: [] }>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-6 text-center">
    <div
      v-if="icon"
      class="w-16 h-16 rounded-2xl bg-surface-100 dark:bg-surface-800 flex items-center justify-center mb-4"
    >
      <component :is="icon" :size="28" class="text-surface-400" />
    </div>
    <h3 class="text-lg font-semibold text-surface-700 dark:text-surface-300">{{ title }}</h3>
    <p v-if="description" class="mt-2 text-sm text-surface-500 max-w-sm">{{ description }}</p>
    <button
      v-if="actionLabel"
      @click="$emit('action')"
      class="mt-6 px-5 py-2.5 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium rounded-xl transition-colors shadow-sm shadow-primary-500/20"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>

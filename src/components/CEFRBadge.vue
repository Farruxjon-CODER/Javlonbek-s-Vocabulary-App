<script setup lang="ts">
defineProps<{ level: string }>()

const colors: Record<string, string> = {
  A1: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 ring-emerald-500/20',
  A2: 'bg-sky-50 text-sky-700 dark:bg-sky-500/10 dark:text-sky-400 ring-sky-500/20',
  B1: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400 ring-amber-500/20',
  B2: 'bg-rose-50 text-rose-700 dark:bg-rose-500/10 dark:text-rose-400 ring-rose-500/20',
}
</script>

<template>
  <span
    class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold ring-1 ring-inset"
    :class="colors[level] || 'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400 ring-surface-500/20'"
  >
    {{ level }}
  </span>
</template>

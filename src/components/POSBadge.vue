<script setup lang="ts">
defineProps<{ pos: string }>()
</script>

<template>
  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400">
    {{ pos }}
  </span>
</template>

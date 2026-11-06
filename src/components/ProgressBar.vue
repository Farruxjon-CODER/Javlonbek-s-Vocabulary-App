<script setup lang="ts">
defineProps<{
  value: number
  max: number
  color?: string
  showLabel?: boolean
  size?: 'sm' | 'md' | 'lg'
}>()
</script>

<template>
  <div class="w-full">
    <div
      v-if="showLabel"
      class="flex justify-between items-center mb-1.5"
    >
      <slot name="label" />
      <span class="text-xs font-medium text-surface-500">{{ value }} / {{ max }}</span>
    </div>
    <div
      class="w-full rounded-full overflow-hidden bg-surface-200 dark:bg-surface-800"
      :class="{
        'h-1.5': size === 'sm',
        'h-2.5': size === 'md' || !size,
        'h-4': size === 'lg'
      }"
    >
      <div
        class="h-full rounded-full transition-all duration-500 ease-out"
        :class="color || 'bg-primary-500'"
        :style="{ width: `${max > 0 ? Math.min((value / max) * 100, 100) : 0}%` }"
      />
    </div>
  </div>
</template>

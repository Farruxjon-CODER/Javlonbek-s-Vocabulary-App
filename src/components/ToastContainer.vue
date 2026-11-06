<script setup lang="ts">
import { ref, reactive } from 'vue'
import { CheckCircle, AlertCircle, Info, X } from 'lucide-vue-next'

export interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info'
}

const toasts = reactive<Toast[]>([])
let nextId = 0

function addToast(message: string, type: Toast['type'] = 'success') {
  const id = nextId++
  toasts.push({ id, message, type })
  setTimeout(() => removeToast(id), 3000)
}

function removeToast(id: number) {
  const idx = toasts.findIndex(t => t.id === id)
  if (idx !== -1) toasts.splice(idx, 1)
}

// Expose globally
defineExpose({ addToast })

// Make available via provide/inject or event bus
if (typeof window !== 'undefined') {
  (window as any).__lexiflow_toast = addToast
}
</script>

<template>
  <div class="fixed top-4 right-4 z-[200] space-y-2 max-w-sm" aria-live="polite">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg border backdrop-blur-sm"
        :class="{
          'bg-success-50 dark:bg-success-500/10 border-success-500/20 text-success-600 dark:text-success-500': toast.type === 'success',
          'bg-error-50 dark:bg-error-500/10 border-error-500/20 text-error-600 dark:text-error-500': toast.type === 'error',
          'bg-primary-50 dark:bg-primary-500/10 border-primary-500/20 text-primary-600 dark:text-primary-400': toast.type === 'info'
        }"
      >
        <CheckCircle v-if="toast.type === 'success'" :size="18" />
        <AlertCircle v-else-if="toast.type === 'error'" :size="18" />
        <Info v-else :size="18" />
        <span class="text-sm font-medium flex-1">{{ toast.message }}</span>
        <button @click="removeToast(toast.id)" class="opacity-60 hover:opacity-100 transition-opacity">
          <X :size="14" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

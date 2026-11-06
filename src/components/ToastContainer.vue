<script setup lang="ts">
import { useToastStore } from '@/stores/toast'
import { CheckCircle, AlertCircle, Info, X } from 'lucide-vue-next'

const toastStore = useToastStore()

// Global fallback bridge
if (typeof window !== 'undefined') {
  ;(window as any).__lexiflow_toast = toastStore.addToast
}
</script>

<template>
  <div
    class="fixed top-5 right-5 z-[200] flex flex-col gap-2 max-w-sm pointer-events-none select-none"
    aria-live="polite"
  >
    <TransitionGroup
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform translate-y-[-12px] opacity-0 scale-95"
      enter-to-class="transform translate-y-0 opacity-100 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100 scale-100"
      leave-to-class="transform translate-x-4 opacity-0 scale-95"
    >
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-2xl shadow-xl border backdrop-blur-md transition-all duration-200"
        :class="{
          'bg-emerald-50/95 dark:bg-emerald-950/80 border-emerald-500/30 text-emerald-700 dark:text-emerald-300 shadow-emerald-500/10': toast.type === 'success',
          'bg-rose-50/95 dark:bg-rose-950/80 border-rose-500/30 text-rose-700 dark:text-rose-300 shadow-rose-500/10': toast.type === 'error',
          'bg-primary-50/95 dark:bg-primary-950/80 border-primary-500/30 text-primary-700 dark:text-primary-300 shadow-primary-500/10': toast.type === 'info'
        }"
      >
        <!-- Icon -->
        <CheckCircle v-if="toast.type === 'success'" :size="18" class="text-emerald-500 shrink-0" />
        <AlertCircle v-else-if="toast.type === 'error'" :size="18" class="text-rose-500 shrink-0" />
        <Info v-else :size="18" class="text-primary-500 shrink-0" />

        <!-- Message -->
        <span class="text-xs sm:text-sm font-semibold flex-1 leading-snug">
          {{ toast.message }}
        </span>

        <!-- Close Button -->
        <button
          type="button"
          @click="toastStore.removeToast(toast.id)"
          class="p-1 rounded-lg opacity-60 hover:opacity-100 hover:bg-black/5 dark:hover:bg-white/10 transition-all cursor-pointer shrink-0"
          title="Yopish"
          aria-label="Yopish"
        >
          <X :size="14" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

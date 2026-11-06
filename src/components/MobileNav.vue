<script setup lang="ts">
import { useRoute } from 'vue-router'
import {
  LayoutDashboard,
  BookOpen,
  Layers,
  HelpCircle,
  BarChart3
} from 'lucide-vue-next'

const route = useRoute()

const navItems = [
  { path: '/', label: 'Home', icon: LayoutDashboard },
  { path: '/vocabulary', label: 'Words', icon: BookOpen },
  { path: '/flashcards', label: 'Cards', icon: Layers },
  { path: '/quiz', label: 'Quiz', icon: HelpCircle },
  { path: '/progress', label: 'Progress', icon: BarChart3 },
]

function isActive(path: string) {
  return route.path === path
}
</script>

<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white/95 dark:bg-surface-900/95 backdrop-blur-md border-t border-surface-200 dark:border-surface-800 z-50 safe-area-bottom">
    <div class="grid grid-cols-5 items-center px-2 py-1">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center justify-center py-2 px-1 rounded-xl text-xs font-medium transition-all"
        :class="isActive(item.path)
          ? 'text-primary-600 dark:text-primary-400 font-semibold'
          : 'text-surface-400 dark:text-surface-500 hover:text-surface-700 dark:hover:text-surface-300'"
      >
        <component
          :is="item.icon"
          :size="22"
          :stroke-width="isActive(item.path) ? 2.5 : 1.7"
          class="transition-transform"
          :class="isActive(item.path) ? 'scale-110' : ''"
        />
        <span class="mt-0.5 truncate w-full text-center leading-none">{{ item.label }}</span>
      </router-link>
    </div>
  </nav>
</template>

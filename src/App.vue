<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useWordsStore } from '@/stores/words'
import { useSettingsStore } from '@/stores/settings'
import { useSidebar } from '@/composables/useSidebar'
import { useAuthStore } from '@/stores/auth'
import { useGamificationStore } from '@/stores/gamification'
import AppSidebar from '@/components/AppSidebar.vue'
import MobileNav from '@/components/MobileNav.vue'
import CommandPalette from '@/components/CommandPalette.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'
import { Search, Sun, Moon, Settings, Menu } from 'lucide-vue-next'

const route = useRoute()
const wordsStore = useWordsStore()
const settingsStore = useSettingsStore()
const { isSidebarOpen, toggleMobile, closeMobile } = useSidebar()
const authStore = useAuthStore()
const gamificationStore = useGamificationStore()
const showCommandPalette = ref(false)

watch(() => route.path, () => {
  closeMobile()
})

function applyTheme(theme: 'light' | 'dark' | 'system') {
  const root = document.documentElement
  let isDark = false
  if (theme === 'system') {
    isDark = typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  } else {
    isDark = theme === 'dark'
  }

  if (isDark) {
    root.classList.add('dark')
    root.setAttribute('data-theme', 'dark')
  } else {
    root.classList.remove('dark')
    root.setAttribute('data-theme', 'light')
  }
}

let mediaQuery: MediaQueryList | null = null
let mediaListener: ((e: MediaQueryListEvent) => void) | null = null

onMounted(() => {
  authStore.initAuth()
  wordsStore.loadVocabulary()
  applyTheme(settingsStore.settings.theme)

  if (typeof window !== 'undefined' && window.matchMedia) {
    mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaListener = () => {
      if (settingsStore.settings.theme === 'system') {
        applyTheme('system')
      }
    }
    mediaQuery.addEventListener('change', mediaListener)
  }
})

onUnmounted(() => {
  if (mediaQuery && mediaListener) {
    mediaQuery.removeEventListener('change', mediaListener)
  }
})

watch(() => settingsStore.settings.theme, (theme) => {
  applyTheme(theme)
}, { immediate: true })

useKeyboardShortcuts([
  {
    key: 'k',
    ctrl: true,
    handler: () => { showCommandPalette.value = !showCommandPalette.value },
    description: 'Toggle command palette'
  },
  {
    key: 'Escape',
    handler: () => { showCommandPalette.value = false },
    description: 'Close command palette'
  }
])
</script>

<template>
  <div class="min-h-screen bg-surface-50 dark:bg-surface-950 text-surface-900 dark:text-surface-100 transition-colors duration-200">
    <!-- Sidebar (Desktop Fixed & Mobile Drawer) -->
    <AppSidebar v-if="route.name !== 'login'" />

    <!-- Mobile Top Header Bar -->
    <header v-if="route.name !== 'login'" class="lg:hidden sticky top-0 z-30 bg-white/90 dark:bg-surface-900/90 backdrop-blur-md border-b border-surface-200 dark:border-surface-800 px-3 sm:px-4 py-2.5 flex items-center justify-between transition-colors">
      <div class="flex items-center gap-2 min-w-0">
        <!-- Hamburger Menu Button (Mobile) -->
        <button
          type="button"
          @click="toggleMobile"
          class="p-2 -ml-1 rounded-xl text-surface-600 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors cursor-pointer"
          title="Menyu"
          aria-label="Toggle mobile menu"
        >
          <Menu :size="20" />
        </button>

        <router-link to="/" class="flex items-center gap-2 min-w-0">
          <div class="w-8 h-8 bg-white dark:bg-surface-800 rounded-lg shadow-sm border border-surface-200 dark:border-surface-700 overflow-hidden flex items-center justify-center shrink-0">
            <img
              src="/LC logo_2.jpg"
              alt="Javlonbek's LC Logo"
              class="w-full h-full object-cover scale-110"
            />
          </div>
          <div class="min-w-0">
            <span class="font-bold text-xs sm:text-sm text-surface-900 dark:text-white leading-tight block truncate">Javlonbek's LC</span>
            <span class="text-[9px] sm:text-[10px] text-surface-400 font-medium tracking-wider uppercase block truncate">Oxford 5000</span>
          </div>
        </router-link>
      </div>

      <div class="flex items-center gap-2">
        <!-- Coin Badge -->
        <div class="flex items-center gap-1 px-2.5 py-1 bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/20 rounded-xl text-xs font-bold text-amber-600 dark:text-amber-400 shadow-xs">
          <span>🪙</span>
          <span class="tabular-nums">{{ gamificationStore.coins }}</span>
        </div>

        <!-- User Avatar -->
        <img
          v-if="authStore.user?.photoURL"
          :src="authStore.user.photoURL"
          :alt="authStore.user.displayName || 'Avatar'"
          class="w-7 h-7 rounded-full object-cover border border-surface-200 dark:border-surface-700"
        />
        <!-- Quick Search -->
        <button
          @click="showCommandPalette = true"
          class="p-2 rounded-xl text-surface-500 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
          title="Search (Ctrl+K)"
          aria-label="Search"
        >
          <Search :size="18" />
        </button>

        <!-- Quick Theme Toggle (hidden on /settings) -->
        <button
          v-if="route.path !== '/settings'"
          @click="settingsStore.toggleTheme()"
          class="p-2 rounded-xl text-surface-500 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
          :title="settingsStore.isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
          :aria-label="settingsStore.isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        >
          <Sun v-if="settingsStore.isDarkMode" :size="18" class="text-amber-500 animate-in fade-in duration-200" />
          <Moon v-else :size="18" class="text-primary-600 animate-in fade-in duration-200" />
        </button>

        <!-- Settings Link -->
        <router-link
          to="/settings"
          class="p-2 rounded-xl transition-colors"
          :class="route.path === '/settings'
            ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-500/10 shadow-xs'
            : 'text-surface-500 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800'"
          title="Settings"
          aria-label="Settings"
        >
          <Settings :size="18" />
        </router-link>
      </div>
    </header>

    <!-- Main Content (Dynamic margin based on sidebar state) -->
    <main
      class="min-h-screen pb-20 lg:pb-0 transition-all duration-300 ease-in-out"
      :class="route.name === 'login' ? '' : (isSidebarOpen ? 'lg:ml-64' : 'lg:ml-20')"
    >
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Mobile Nav -->
    <MobileNav v-if="route.name !== 'login'" class="lg:hidden" />

    <!-- Command Palette -->
    <CommandPalette
      v-if="showCommandPalette"
      @close="showCommandPalette = false"
    />

    <!-- Toast -->
    <ToastContainer />
  </div>
</template>

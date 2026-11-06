<script setup lang="ts">
import { useRoute } from 'vue-router'
import {
  LayoutDashboard,
  BookOpen,
  Layers,
  Brain,
  HelpCircle,
  BarChart3,
  Heart,
  Settings,
  Sun,
  Moon,
  Menu,
  LogOut,
  Coins
} from 'lucide-vue-next'
import { useSettingsStore } from '@/stores/settings'
import { useSidebar } from '@/composables/useSidebar'
import { useAuthStore } from '@/stores/auth'
import { useGamificationStore } from '@/stores/gamification'

const route = useRoute()
const settingsStore = useSettingsStore()
const { isSidebarOpen, toggleSidebar } = useSidebar()
const authStore = useAuthStore()
const gamificationStore = useGamificationStore()

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/vocabulary', label: 'Vocabulary', icon: BookOpen },
  { path: '/flashcards', label: 'Flashcards', icon: Layers },
  { path: '/review', label: 'Smart Review', icon: Brain },
  { path: '/quiz', label: 'Quiz', icon: HelpCircle },
  { path: '/progress', label: 'Progress', icon: BarChart3 },
  { path: '/favorites', label: 'Favorites', icon: Heart },
]

function isActive(path: string) {
  return route.path === path
}
</script>

<template>
  <aside
    class="fixed left-0 top-0 bottom-0 bg-white dark:bg-surface-900 border-r border-surface-200 dark:border-surface-800 flex flex-col z-40 transition-all duration-300 ease-in-out select-none"
    :class="isSidebarOpen ? 'w-64' : 'w-20'"
  >
    <!-- Header / Logo & Collapse Toggle -->
    <div
      class="p-4 border-b border-surface-200 dark:border-surface-800 shrink-0 flex items-center transition-all duration-300"
      :class="isSidebarOpen ? 'justify-between px-5' : 'flex-col gap-3 justify-center px-2'"
    >
      <router-link
        to="/"
        class="flex items-center gap-3 group min-w-0"
        :title="isSidebarOpen ? undefined : 'Javlonbek\'s LC'"
      >
        <div class="w-10 h-10 bg-white dark:bg-surface-800 rounded-xl shadow-sm border border-surface-200 dark:border-surface-700 overflow-hidden flex items-center justify-center shrink-0">
          <img
            src="/LC logo_2.jpg"
            alt="Javlonbek's LC Logo"
            class="w-full h-full object-cover scale-110 group-hover:scale-125 transition-transform duration-300"
          />
        </div>
        <div v-show="isSidebarOpen" class="min-w-0 overflow-hidden transition-all duration-200">
          <h1 class="text-base font-bold text-primary-600 dark:text-primary-400 group-hover:text-primary-700 transition-colors truncate">
            Javlonbek's LC
          </h1>
          <p class="text-[10px] font-medium text-surface-400 tracking-wider uppercase truncate">
            Oxford 5000 IELTS
          </p>
        </div>
      </router-link>

      <!-- Desktop Collapse Toggle Button (hidden on mobile, visible on lg+) -->
      <button
        type="button"
        @click="toggleSidebar"
        class="hidden lg:flex items-center justify-center w-8 h-8 rounded-lg text-surface-500 hover:text-surface-900 dark:text-surface-400 dark:hover:text-white hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors cursor-pointer shrink-0"
        :title="isSidebarOpen ? 'Menyuni yig‘ish (Collapse)' : 'Menyuni ochish (Expand)'"
        :aria-label="isSidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'"
      >
        <Menu :size="20" />
      </button>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 min-h-0 p-3 space-y-1 overflow-y-auto overflow-x-hidden">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center rounded-xl text-sm font-medium transition-all duration-200"
        :class="[
          isSidebarOpen ? 'gap-3 px-3.5 py-2.5' : 'justify-center p-2.5',
          isActive(item.path)
            ? 'bg-primary-50 dark:bg-primary-500/15 text-primary-600 dark:text-primary-400 font-semibold shadow-xs'
            : 'text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 hover:text-surface-900 dark:hover:text-white'
        ]"
        :title="isSidebarOpen ? '' : item.label"
      >
        <component
          :is="item.icon"
          :size="20"
          :class="isActive(item.path) ? 'text-primary-600 dark:text-primary-400' : ''"
          class="shrink-0"
        />
        <span v-show="isSidebarOpen" class="truncate transition-opacity duration-200">
          {{ item.label }}
        </span>
      </router-link>
    </nav>

    <!-- Settings & Theme Toggle -->
    <div
      class="p-3 border-t border-surface-200 dark:border-surface-800 space-y-1 shrink-0 overflow-hidden transition-all duration-300"
    >
      <router-link
        to="/settings"
        class="flex items-center rounded-xl text-sm font-medium transition-all duration-200"
        :class="[
          isSidebarOpen ? 'gap-3 px-3.5 py-2.5' : 'justify-center p-2.5',
          isActive('/settings')
            ? 'bg-primary-50 dark:bg-primary-500/15 text-primary-600 dark:text-primary-400 font-semibold'
            : 'text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800'
        ]"
        :title="isSidebarOpen ? '' : 'Settings'"
      >
        <Settings :size="20" class="shrink-0" />
        <span v-show="isSidebarOpen" class="truncate transition-opacity duration-200">
          Settings
        </span>
      </router-link>

      <!-- Theme Toggle Switch -->
      <button
        type="button"
        @click="settingsStore.toggleTheme()"
        class="w-full flex items-center rounded-xl text-sm font-medium text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors group cursor-pointer"
        :class="isSidebarOpen ? 'justify-between px-3.5 py-2' : 'justify-center p-2.5'"
        :title="settingsStore.isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        :aria-label="settingsStore.isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
      >
        <div class="flex items-center gap-3">
          <Sun v-if="settingsStore.isDarkMode" :size="20" class="text-amber-500 transition-transform duration-200 group-hover:rotate-45 shrink-0" />
          <Moon v-else :size="20" class="text-primary-600 transition-transform duration-200 group-hover:-rotate-12 shrink-0" />
          <span v-show="isSidebarOpen" class="truncate transition-opacity duration-200">
            {{ settingsStore.isDarkMode ? 'Light Mode' : 'Dark Mode' }}
          </span>
        </div>

        <!-- Capsule Toggle (shown only when expanded) -->
        <div
          v-show="isSidebarOpen"
          class="w-9 h-5 rounded-full p-0.5 transition-colors duration-200 flex items-center shrink-0"
          :class="settingsStore.isDarkMode ? 'bg-primary-600' : 'bg-surface-300 dark:bg-surface-700'"
        >
          <div
            class="w-4 h-4 rounded-full bg-white transition-transform duration-200 shadow-sm"
            :class="settingsStore.isDarkMode ? 'translate-x-4' : 'translate-x-0'"
          ></div>
        </div>
      </button>

      <!-- User Profile, Coins & Logout -->
      <div class="mt-2 pt-2 border-t border-surface-200 dark:border-surface-800">
        <div
          class="flex items-center rounded-xl p-2 transition-all duration-200"
          :class="isSidebarOpen ? 'justify-between gap-2 bg-surface-50 dark:bg-surface-800/60' : 'justify-center'"
        >
          <!-- User Info & Avatar -->
          <div class="flex items-center gap-2.5 min-w-0">
            <img
              v-if="authStore.user?.photoURL"
              :src="authStore.user.photoURL"
              :alt="authStore.user.displayName || 'Avatar'"
              class="w-8 h-8 rounded-full object-cover shrink-0 border border-primary-500/30 shadow-xs"
            />
            <div
              v-else
              class="w-8 h-8 rounded-full bg-primary-600 text-white font-bold text-xs flex items-center justify-center shrink-0 shadow-xs"
            >
              {{ authStore.userInitials }}
            </div>

            <div v-show="isSidebarOpen" class="min-w-0 overflow-hidden">
              <p class="text-xs font-bold text-surface-900 dark:text-white truncate">
                {{ authStore.user?.displayName || "Javlonbek's Learner" }}
              </p>
              <div class="flex items-center gap-1 text-[11px] font-semibold text-amber-600 dark:text-amber-400">
                <span>🪙</span>
                <span class="tabular-nums">{{ gamificationStore.coins }} Coins</span>
              </div>
            </div>
          </div>

          <!-- Logout Button -->
          <button
            v-show="isSidebarOpen"
            type="button"
            @click="authStore.logout()"
            class="p-1.5 rounded-lg text-surface-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-500/10 transition-colors shrink-0"
            title="Tizimdan chiqish (Logout)"
            aria-label="Logout"
          >
            <LogOut :size="16" />
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>

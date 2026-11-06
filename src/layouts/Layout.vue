<script setup lang="ts">
import { useSidebar } from '@/composables/useSidebar'
import AppSidebar from '@/components/AppSidebar.vue'
import MobileNav from '@/components/MobileNav.vue'

const { isSidebarOpen } = useSidebar()
</script>

<template>
  <div class="min-h-screen bg-surface-50 dark:bg-surface-950 text-surface-900 dark:text-surface-100 transition-colors duration-200">
    <!-- Collapsible Desktop Sidebar -->
    <AppSidebar class="hidden lg:flex" />

    <!-- Main Content Area (Expands automatically when sidebar collapses) -->
    <main
      class="min-h-screen pb-20 lg:pb-0 transition-all duration-300 ease-in-out"
      :class="isSidebarOpen ? 'lg:ml-64' : 'lg:ml-20'"
    >
      <slot />
    </main>

    <!-- Mobile Bottom Navigation -->
    <MobileNav class="lg:hidden" />
  </div>
</template>


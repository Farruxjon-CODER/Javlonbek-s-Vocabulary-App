import { ref } from 'vue'

// Read persisted desktop state from localStorage (default: true)
const isSidebarOpen = ref(
  typeof window !== 'undefined'
    ? localStorage.getItem('javlonbek_lc_sidebar_open') !== 'false'
    : true
)

// Mobile drawer state
const isMobileOpen = ref(false)

export function useSidebar() {
  function toggleSidebar() {
    isSidebarOpen.value = !isSidebarOpen.value
    if (typeof window !== 'undefined') {
      localStorage.setItem('javlonbek_lc_sidebar_open', String(isSidebarOpen.value))
    }
  }

  function setSidebar(open: boolean) {
    isSidebarOpen.value = open
    if (typeof window !== 'undefined') {
      localStorage.setItem('javlonbek_lc_sidebar_open', String(open))
    }
  }

  function toggleMobile() {
    isMobileOpen.value = !isMobileOpen.value
  }

  function openMobile() {
    isMobileOpen.value = true
  }

  function closeMobile() {
    isMobileOpen.value = false
  }

  return {
    isSidebarOpen,
    isMobileOpen,
    toggleSidebar,
    setSidebar,
    toggleMobile,
    openMobile,
    closeMobile
  }
}

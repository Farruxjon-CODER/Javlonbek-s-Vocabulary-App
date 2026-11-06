import { ref } from 'vue'

// Read persisted state from localStorage (default: true)
const isSidebarOpen = ref(
  typeof window !== 'undefined'
    ? localStorage.getItem('javlonbek_lc_sidebar_open') !== 'false'
    : true
)

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

  return {
    isSidebarOpen,
    toggleSidebar,
    setSidebar
  }
}

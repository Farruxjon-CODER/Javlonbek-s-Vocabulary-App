import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { firebaseAuth, type AuthUser, isFirebaseConfigured } from '@/config/firebase'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(firebaseAuth.getCurrentUser())
  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)
  const userInitials = computed(() => {
    if (!user.value?.displayName) return 'JS'
    return user.value.displayName
      .split(' ')
      .map(part => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  })

  // Listen to Auth State Changes
  firebaseAuth.onAuthStateChanged((newUser) => {
    user.value = newUser
  })

  async function loginWithGoogle(): Promise<boolean> {
    loading.value = true
    error.value = null
    try {
      const loggedUser = await firebaseAuth.signInWithGoogle()
      user.value = loggedUser
      return true
    } catch (err: any) {
      error.value = err.message || 'Google orqali tizimga kirishda xatolik yuz berdi'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<void> {
    loading.value = true
    try {
      await firebaseAuth.signOut()
      user.value = null
    } catch (err: any) {
      console.error('Logout failed', err)
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    loading,
    error,
    userInitials,
    isFirebaseConfigured,
    loginWithGoogle,
    logout
  }
})


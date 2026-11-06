import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged
} from 'firebase/auth'
import { auth } from '@/firebase/config'
import { fetchUserData, saveUserData } from '@/firebase/userService'
import { useGamificationStore } from '@/stores/gamification'
import { useProgressStore } from '@/stores/progress'
import { useStatsStore } from '@/stores/stats'

export interface UserInfo {
  uid: string
  email: string | null
  displayName: string | null
  photoURL: string | null
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<UserInfo | null>(null)
  const loading = ref<boolean>(true)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const userInitials = computed(() => {
    if (!user.value?.displayName) return 'JS'
    return user.value.displayName
      .split(' ')
      .map((part) => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  })

  /**
   * Foydalanuvchi ma'lumotlarini Firestore bazasi bilan sinxronizatsiya qilish
   * (Circular dependency bo'lmasligi uchun store'lar chaqiruvi ichida xavfsiz o'qiladi)
   */
  async function syncUserDataWithCloud(u: UserInfo): Promise<void> {
    try {
      const cloudData = await fetchUserData(u.uid)
      const gamificationStore = useGamificationStore()
      const progressStore = useProgressStore()
      const statsStore = useStatsStore()

      if (cloudData) {
        // Agar foydalanuvchi bazada bo'lsa: mavjud tangalar va progressni tiklash
        if (typeof cloudData.coins === 'number') {
          gamificationStore.setCoins(cloudData.coins)
        }
        if (cloudData.progress) {
          progressStore.setProgressData(cloudData.progress)
        }
        if (cloudData.stats) {
          statsStore.setStatsData(cloudData.stats)
        }

        // Oxirgi kirish vaqti va profil ma'lumotlarini yangilash
        await saveUserData(u.uid, {
          displayName: u.displayName,
          email: u.email,
          photoURL: u.photoURL,
          lastLoginAt: new Date().toISOString()
        })
      } else {
        // Agar foydalanuvchi birinchi marta kirayotgan bo'lsa: yangi doc yaratish
        await saveUserData(u.uid, {
          uid: u.uid,
          displayName: u.displayName,
          email: u.email,
          photoURL: u.photoURL,
          coins: gamificationStore.coins || 0,
          progress: progressStore.progressMap || {},
          stats: {
            streak: statsStore.streak,
            dailyStatsHistory: [],
            quizHistory: []
          },
          createdAt: new Date().toISOString(),
          lastLoginAt: new Date().toISOString()
        })
      }
    } catch (err) {
      console.warn('Foydalanuvchi ma\'lumotlarini sinxronlashda xatolik:', err)
    }
  }

  // Actions
  async function loginWithGoogle(): Promise<boolean> {
    loading.value = true
    try {
      const provider = new GoogleAuthProvider()
      const result = await signInWithPopup(auth, provider)
      const u = result.user

      user.value = {
        uid: u.uid,
        email: u.email,
        displayName: u.displayName,
        photoURL: u.photoURL
      }

      if (typeof window !== 'undefined') {
        localStorage.setItem('javlonbek_lc_auth_user', JSON.stringify(user.value))
      }

      // Firestore Cloud Save bilan sinxronlash
      await syncUserDataWithCloud(user.value)

      return true
    } catch (error) {
      console.error('Google orqali tizimga kirishda xatolik:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<void> {
    loading.value = true
    try {
      await signOut(auth)
      user.value = null

      if (typeof window !== 'undefined') {
        localStorage.removeItem('javlonbek_lc_auth_user')
      }
    } catch (error) {
      console.error('Tizimdan chiqishda xatolik:', error)
    } finally {
      loading.value = false
    }
  }

  function initAuth(): Promise<UserInfo | null> {
    loading.value = true
    return new Promise((resolve) => {
      onAuthStateChanged(auth, async (currentUser) => {
        if (currentUser) {
          user.value = {
            uid: currentUser.uid,
            email: currentUser.email,
            displayName: currentUser.displayName,
            photoURL: currentUser.photoURL
          }
          if (typeof window !== 'undefined') {
            localStorage.setItem('javlonbek_lc_auth_user', JSON.stringify(user.value))
          }

          // Sahifa yangilanganda ham Firestore dan ma'lumotlarni yuklab olish
          await syncUserDataWithCloud(user.value)
        } else {
          user.value = null
          if (typeof window !== 'undefined') {
            localStorage.removeItem('javlonbek_lc_auth_user')
          }
        }
        loading.value = false
        resolve(user.value)
      })
    })
  }

  return {
    user,
    loading,
    isAuthenticated,
    userInitials,
    loginWithGoogle,
    logout,
    initAuth
  }
})

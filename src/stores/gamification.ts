import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useToastStore } from '@/stores/toast'
import { useAuthStore } from '@/stores/auth'
import { saveUserData } from '@/firebase/userService'

const STORAGE_KEY = 'javlonbek_lc_coins'

export const useGamificationStore = defineStore('gamification', () => {
  // State: coins (default: 0 yoki localStorage dan tiklangan qiymat)
  const initialCoins = typeof window !== 'undefined'
    ? parseInt(localStorage.getItem(STORAGE_KEY) || '0', 10)
    : 0

  const coins = ref<number>(isNaN(initialCoins) ? 0 : initialCoins)

  // Debounced Firestore sync (har safar tanga o'zgarganda ortiqcha so'rov bo'lmasligi uchun)
  let syncTimer: any = null
  function syncCoinsToCloud(amount: number) {
    if (typeof window === 'undefined') return
    clearTimeout(syncTimer)
    syncTimer = setTimeout(() => {
      const authStore = useAuthStore()
      if (authStore.user?.uid) {
        saveUserData(authStore.user.uid, { coins: amount })
      }
    }, 1000)
  }

  // localStorage va Cloud bilan avtomatik sinxronizatsiya
  watch(
    coins,
    (newCoins) => {
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, String(newCoins))
      }
      syncCoinsToCloud(newCoins)
    },
    { immediate: false }
  )

  // Actions
  function setCoins(amount: number) {
    coins.value = amount
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, String(amount))
    }
  }

  function addCoins(amount: number, reason?: string) {
    if (amount <= 0) return
    coins.value += amount

    // Pinia Toast Store orqali bildirishnoma chiqarish
    const toastStore = useToastStore()
    const msg = reason ? `+${amount} Coins: ${reason}` : `+${amount} Coins qo‘shildi! 🎉`
    toastStore.addToast(msg, 'success')
  }

  function spendCoins(amount: number): boolean {
    if (coins.value >= amount) {
      coins.value -= amount
      return true
    }
    return false
  }

  return {
    coins,
    setCoins,
    addCoins,
    spendCoins
  }
})

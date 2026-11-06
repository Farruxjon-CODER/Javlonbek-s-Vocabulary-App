import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useAuthStore } from './auth'

export interface LeaderboardUser {
  id: string
  name: string
  avatar: string
  coins: number
  wordsLearned: number
  accuracy: number
  isCurrentUser?: boolean
  badge?: string
}

export const useGamificationStore = defineStore('gamification', () => {
  const authStore = useAuthStore()

  // Storage key based on user UID
  const storageKey = computed(() => {
    return authStore.user?.uid
      ? `javlonbek_lc_coins_${authStore.user.uid}`
      : 'javlonbek_lc_coins_guest'
  })

  // Read initial coins from storage (default: 150)
  const initialCoins = typeof window !== 'undefined'
    ? parseInt(localStorage.getItem(storageKey.value) || '150', 10)
    : 150

  const coins = ref<number>(isNaN(initialCoins) ? 150 : initialCoins)

  // Watch user change to load their specific coins
  watch(() => authStore.user?.uid, (newUid) => {
    if (typeof window !== 'undefined') {
      const key = newUid ? `javlonbek_lc_coins_${newUid}` : 'javlonbek_lc_coins_guest'
      const saved = localStorage.getItem(key)
      coins.value = saved ? parseInt(saved, 10) : 150
    }
  })

  // Watch coins change to persist
  watch(coins, (newCoins) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(storageKey.value, String(newCoins))
    }
  })

  function addCoins(amount: number, reason?: string) {
    if (amount <= 0) return
    coins.value += amount

    // Trigger visual toast
    if (typeof window !== 'undefined' && (window as any).__lexiflow_toast) {
      const msg = reason ? `+${amount} Coins: ${reason}` : `+${amount} Coins qo‘shildi! 🎉`
      ;(window as any).__lexiflow_toast(msg, 'success')
    }
  }

  function spendCoins(amount: number): boolean {
    if (coins.value >= amount) {
      coins.value -= amount
      return true
    }
    return false
  }

  // Pre-configured dynamic leaderboard with active user positioning
  const mockLeaderboard = ref<LeaderboardUser[]>([
    {
      id: 'mentor-1',
      name: "Javlonbek O'rinov",
      avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=256&q=80',
      coins: 620,
      wordsLearned: 1850,
      accuracy: 98,
      badge: '👑 Mentor / Top 1'
    },
    {
      id: 'student-2',
      name: 'Malika Karimova',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=256&q=80',
      coins: 480,
      wordsLearned: 1420,
      accuracy: 94,
      badge: '🥈 IELTS 8.0'
    },
    {
      id: 'student-3',
      name: 'Bekzod Aliyev',
      avatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=256&q=80',
      coins: 390,
      wordsLearned: 1150,
      accuracy: 91,
      badge: '🥉 Vocab Master'
    },
    {
      id: 'student-5',
      name: 'Shahzod Rustamov',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=256&q=80',
      coins: 270,
      wordsLearned: 820,
      accuracy: 86
    },
    {
      id: 'student-6',
      name: 'Diyora Umarova',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=256&q=80',
      coins: 210,
      wordsLearned: 640,
      accuracy: 84
    },
    {
      id: 'student-7',
      name: 'Azizbek Toshmatov',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=256&q=80',
      coins: 160,
      wordsLearned: 450,
      accuracy: 80
    }
  ])

  // Full Leaderboard including the current logged-in user
  const leaderboard = computed(() => {
    const currentUser: LeaderboardUser = {
      id: authStore.user?.uid || 'current_user',
      name: authStore.user?.displayName || "Siz (You)",
      avatar: authStore.user?.photoURL || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80',
      coins: coins.value,
      wordsLearned: 380, // will reflect progress store
      accuracy: 88,
      isCurrentUser: true,
      badge: '⭐ You'
    }

    const list = [...mockLeaderboard.value, currentUser]
    // Sort descending by coins
    return list.sort((a, b) => b.coins - a.coins)
  })

  const currentUserRank = computed(() => {
    const idx = leaderboard.value.findIndex(u => u.isCurrentUser)
    return idx >= 0 ? idx + 1 : 4
  })

  return {
    coins,
    leaderboard,
    currentUserRank,
    addCoins,
    spendCoins
  }
})


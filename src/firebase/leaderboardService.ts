import { collection, query, orderBy, limit, getDocs } from 'firebase/firestore'
import { db } from '@/firebase/config'

export interface LeaderboardUser {
  id: string
  name: string
  coins: number
  avatar: string
}

/**
 * Firestore'dagi 'users' kolleksiyasidan eng ko'p tanga to'plagan foydalanuvchilar ro'yxatini olish
 * @param limitCount Qaytariladigan foydalanuvchilar soni (default: 10)
 */
export async function fetchTopUsers(limitCount = 10): Promise<LeaderboardUser[]> {
  try {
    const usersRef = collection(db, 'users')
    const q = query(usersRef, orderBy('coins', 'desc'), limit(limitCount))
    const querySnapshot = await getDocs(q)

    const topUsers: LeaderboardUser[] = []

    querySnapshot.forEach((docSnap: any) => {
      const data = typeof docSnap.data === 'function' ? docSnap.data() : docSnap
      topUsers.push({
        id: docSnap.id || data.uid || '',
        name: data.displayName || "O'quvchi",
        coins: Number(data.coins) || 0,
        avatar: data.photoURL || ''
      })
    })

    return topUsers
  } catch (error) {
    console.error('Leaderboard ma\'lumotlarini olishda xatolik:', error)
    return []
  }
}


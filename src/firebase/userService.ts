import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore'
import { db } from '@/firebase/config'

export interface UserDataDoc {
  uid?: string
  displayName?: string | null
  email?: string | null
  photoURL?: string | null
  coins?: number
  progress?: Record<number, any>
  stats?: Record<string, any>
  createdAt?: string
  lastLoginAt?: string
  updatedAt?: string
}

/**
 * Foydalanuvchi ma'lumotlarini Firestore bazasidan olish
 * @param uid Foydalanuvchining unikal ID si
 */
export async function fetchUserData(uid: string): Promise<UserDataDoc | null> {
  try {
    const userDocRef = doc(db, 'users', uid)
    const docSnap = await getDoc(userDocRef)

    if (docSnap && typeof docSnap.exists === 'function' ? docSnap.exists() : docSnap?.data) {
      return (typeof docSnap.data === 'function' ? docSnap.data() : docSnap) as UserDataDoc
    }
    return null
  } catch (error) {
    console.error('Firestore dan ma\'lumot o‘qishda xatolik:', error)
    return null
  }
}

/**
 * Foydalanuvchi ma'lumotlarini Firestore bazasiga saqlash / yangilash (Merge)
 * @param uid Foydalanuvchining unikal ID si
 * @param data Saqlanadigan qisman yoki to'liq ma'lumot
 */
export async function saveUserData(uid: string, data: Partial<UserDataDoc>): Promise<void> {
  try {
    const userDocRef = doc(db, 'users', uid)
    const payload = {
      ...data,
      updatedAt: new Date().toISOString()
    }
    await setDoc(userDocRef, payload, { merge: true })
  } catch (error) {
    console.error('Firestore ga ma\'lumot yozishda xatolik:', error)
  }
}


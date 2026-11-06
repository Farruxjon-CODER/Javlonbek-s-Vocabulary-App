/**
 * Firebase Initialization & Configuration
 *
 * To connect real Firebase:
 * 1. Run: npm install firebase
 * 2. Create a .env file in project root with:
 *    VITE_FIREBASE_API_KEY=your_api_key
 *    VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
 *    VITE_FIREBASE_PROJECT_ID=your_project_id
 *    VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
 *    VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
 *    VITE_FIREBASE_APP_ID=your_app_id
 */

export interface AuthUser {
  uid: string
  email: string | null
  displayName: string | null
  photoURL: string | null
}

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || '',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || '',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || '',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || '',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || ''
}

export const isFirebaseConfigured = Boolean(
  firebaseConfig.apiKey &&
  firebaseConfig.apiKey !== '' &&
  !firebaseConfig.apiKey.includes('your_')
)

/**
 * Firebase Services Adapter with Demo/Offline Fallback
 */
class FirebaseAuthService {
  private listeners: ((user: AuthUser | null) => void)[] = []
  private currentUser: AuthUser | null = null

  constructor() {
    // Restore cached user from localStorage
    if (typeof window !== 'undefined') {
      try {
        const cached = localStorage.getItem('javlonbek_lc_auth_user')
        if (cached) {
          this.currentUser = JSON.parse(cached)
        }
      } catch (e) {
        console.error('Failed to parse cached auth user', e)
      }
    }
  }

  getCurrentUser(): AuthUser | null {
    return this.currentUser
  }

  async signInWithGoogle(): Promise<AuthUser> {
    if (isFirebaseConfigured) {
      try {
        const { initializeApp, getApps } = await import('firebase/app')
        const { getAuth, GoogleAuthProvider, signInWithPopup } = await import('firebase/auth')

        const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig)
        const auth = getAuth(app)
        const provider = new GoogleAuthProvider()
        provider.addScope('profile')
        provider.addScope('email')

        const credential = await signInWithPopup(auth, provider)
        const u = credential.user
        const authUser: AuthUser = {
          uid: u.uid,
          email: u.email,
          displayName: u.displayName,
          photoURL: u.photoURL
        }

        this.setUser(authUser)
        return authUser
      } catch (err: any) {
        console.warn('Real Firebase sign-in failed or cancelled:', err)
        throw err
      }
    }

    // Interactive Demo / Offline Google Account selection fallback
    const mockEmail = `learner.${Math.floor(1000 + Math.random() * 9000)}@gmail.com`
    const mockUser: AuthUser = {
      uid: `google_user_${Date.now()}`,
      email: mockEmail,
      displayName: "Javlonbek's Student",
      photoURL: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80"
    }

    this.setUser(mockUser)
    return mockUser
  }

  async signOut(): Promise<void> {
    if (isFirebaseConfigured) {
      try {
        const { getApps } = await import('firebase/app')
        const { getAuth, signOut } = await import('firebase/auth')
        if (getApps().length) {
          await signOut(getAuth())
        }
      } catch (err) {
        console.error('Firebase signOut error', err)
      }
    }

    this.setUser(null)
  }

  onAuthStateChanged(callback: (user: AuthUser | null) => void): () => void {
    this.listeners.push(callback)
    callback(this.currentUser)
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback)
    }
  }

  private setUser(user: AuthUser | null) {
    this.currentUser = user
    if (typeof window !== 'undefined') {
      if (user) {
        localStorage.setItem('javlonbek_lc_auth_user', JSON.stringify(user))
      } else {
        localStorage.removeItem('javlonbek_lc_auth_user')
      }
    }
    this.listeners.forEach(cb => cb(user))
  }
}

export const firebaseAuth = new FirebaseAuthService()


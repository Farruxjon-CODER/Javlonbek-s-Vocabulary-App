declare module 'firebase/app' {
  export interface FirebaseApp { name: string; options: any }
  export function initializeApp(options: any, name?: string): FirebaseApp
  export function getApps(): FirebaseApp[]
}

declare module 'firebase/auth' {
  export interface User {
    uid: string
    email: string | null
    displayName: string | null
    photoURL: string | null
  }
  export interface UserCredential {
    user: User
  }
  export interface Auth {
    currentUser: User | null
  }
  export class GoogleAuthProvider {
    addScope(scope: string): void
  }
  export function getAuth(app?: any): Auth
  export function signInWithPopup(auth: Auth, provider: any): Promise<UserCredential>
  export function signOut(auth: Auth): Promise<void>
  export function onAuthStateChanged(auth: Auth, callback: (user: User | null) => void): () => void
}

declare module 'firebase/firestore' {
  export interface Firestore {
    [key: string]: any
  }
  export function getFirestore(app?: any): Firestore
  export function doc(db: Firestore, path: string, ...pathSegments: string[]): any
  export function setDoc(docRef: any, data: any, options?: any): Promise<void>
  export function getDoc(docRef: any): Promise<any>
}


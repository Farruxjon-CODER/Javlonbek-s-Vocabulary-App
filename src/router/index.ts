import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true }
    },
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue')
    },
    {
      path: '/vocabulary',
      name: 'vocabulary',
      component: () => import('@/views/VocabularyView.vue')
    },
    {
      path: '/flashcards',
      name: 'flashcards',
      component: () => import('@/views/FlashcardsView.vue')
    },
    {
      path: '/review',
      name: 'review',
      component: () => import('@/views/ReviewView.vue')
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: () => import('@/views/QuizView.vue')
    },
    {
      path: '/progress',
      name: 'progress',
      component: () => import('@/views/ProgressView.vue')
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('@/views/FavoritesView.vue')
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

// Global Navigation Guard for Authentication
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  // Agar Firebase auth hali tekshirilayotgan bo'lsa, kutamiz
  if (authStore.loading) {
    await authStore.initAuth()
  }

  // Agar sahifa /login bo'lmasa va foydalanuvchi tizimga kirmagan bo'lsa
  if (to.path !== '/login' && !authStore.isAuthenticated) {
    return next('/login')
  }

  // Agar tizimga kirgan foydalanuvchi /login sahifasiga bormoqchi bo'lsa
  if (to.path === '/login' && authStore.isAuthenticated) {
    return next('/')
  }

  return next()
})

export default router

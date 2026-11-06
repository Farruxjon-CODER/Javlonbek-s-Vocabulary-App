import { createRouter, createWebHistory } from 'vue-router'

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
router.beforeEach((to, _from, next) => {
  const cachedUser = typeof window !== 'undefined' ? localStorage.getItem('javlonbek_lc_auth_user') : null
  const isAuthenticated = Boolean(cachedUser)

  if (!to.meta.public && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Sparkles, CheckCircle2, ShieldCheck, ArrowRight, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isLoggingIn = ref(false)

async function handleGoogleLogin() {
  isLoggingIn.value = true
  const success = await authStore.loginWithGoogle()
  isLoggingIn.value = false

  if (success) {
    const redirectPath = (route.query.redirect as string) || '/'
    router.replace(redirectPath)
  }
}
</script>

<template>
  <div class="min-h-screen bg-surface-50 dark:bg-surface-950 flex flex-col justify-center items-center px-4 py-12 relative overflow-hidden select-none">
    <!-- Ambient Background Gradients -->
    <div class="absolute -top-32 -left-32 w-96 h-96 bg-primary-600/15 dark:bg-primary-600/25 rounded-full blur-3xl pointer-events-none" />
    <div class="absolute -bottom-32 -right-32 w-96 h-96 bg-primary-800/15 dark:bg-primary-500/20 rounded-full blur-3xl pointer-events-none" />

    <div class="w-full max-w-md relative z-10">
      <!-- Main Brand Card -->
      <div class="bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-800 rounded-3xl p-8 sm:p-10 shadow-2xl shadow-primary-900/10 dark:shadow-black/40">
        <!-- Logo and App Title -->
        <div class="flex flex-col items-center text-center mb-8">
          <div class="w-16 h-16 bg-white dark:bg-surface-800 rounded-2xl shadow-md border border-surface-200 dark:border-surface-700 overflow-hidden flex items-center justify-center mb-4">
            <img
              src="/LC logo_2.jpg"
              alt="Javlonbek's LC Logo"
              class="w-full h-full object-cover scale-110"
            />
          </div>

          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <Sparkles :size="14" />
            <span>IELTS & Oxford 3000 SaaS</span>
          </div>

          <h1 class="text-2xl sm:text-3xl font-extrabold text-surface-900 dark:text-white tracking-tight">
            Javlonbek's LC
          </h1>
          <p class="text-sm text-surface-500 dark:text-surface-400 mt-1 max-w-xs">
            Har kuni bir so‘z, IELTS va maqsadlaringiz sari qo‘yilgan bir qadam.
          </p>
        </div>

        <!-- Features summary -->
        <div class="space-y-2.5 mb-8 bg-surface-50 dark:bg-surface-800/50 p-4 rounded-2xl border border-surface-100 dark:border-surface-800">
          <div class="flex items-center gap-2.5 text-xs text-surface-700 dark:text-surface-300">
            <CheckCircle2 :size="16" class="text-emerald-500 shrink-0" />
            <span>3,000+ Saralangan Oxford va IELTS so‘zlari</span>
          </div>
          <div class="flex items-center gap-2.5 text-xs text-surface-700 dark:text-surface-300">
            <CheckCircle2 :size="16" class="text-emerald-500 shrink-0" />
            <span>100% Rasmiy Cambridge Dictionary ta’riflari</span>
          </div>
          <div class="flex items-center gap-2.5 text-xs text-surface-700 dark:text-surface-300">
            <CheckCircle2 :size="16" class="text-emerald-500 shrink-0" />
            <span>Spaced Repetition & Gamified Coin reytingi</span>
          </div>
        </div>

        <!-- Error Alert -->
        <div v-if="authStore.error" class="mb-6 p-3.5 rounded-xl bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-800 text-rose-600 dark:text-rose-400 text-xs text-center font-medium">
          {{ authStore.error }}
        </div>

        <!-- Google Sign-In Button -->
        <button
          type="button"
          @click="handleGoogleLogin"
          :disabled="isLoggingIn"
          class="w-full h-13 flex items-center justify-center gap-3.5 px-6 py-3.5 rounded-2xl bg-white hover:bg-surface-50 dark:bg-surface-800 dark:hover:bg-surface-700/80 text-surface-800 dark:text-white font-semibold border border-surface-300 dark:border-surface-700 shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer group disabled:opacity-60 disabled:cursor-not-allowed"
        >
          <!-- Google "G" Colorful SVG Icon -->
          <svg v-if="!isLoggingIn" class="w-5 h-5 shrink-0" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
          </svg>
          <Loader2 v-else class="w-5 h-5 animate-spin text-primary-600 dark:text-primary-400" />

          <span class="text-sm">
            {{ isLoggingIn ? 'Kirilmoqda...' : 'Continue with Google' }}
          </span>

          <ArrowRight v-if="!isLoggingIn" :size="16" class="text-surface-400 group-hover:translate-x-1 transition-transform" />
        </button>

        <!-- Secure Footer info -->
        <div class="mt-8 pt-6 border-t border-surface-100 dark:border-surface-800 flex items-center justify-center gap-2 text-xs text-surface-400">
          <ShieldCheck :size="16" class="text-emerald-500" />
          <span>Xavfsiz va tezkor Google OAuth 2.0</span>
        </div>
      </div>
    </div>
  </div>
</template>


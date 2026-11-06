import { ref, computed } from 'vue'
import type { VocabularyWord, QuizQuestion, QuizResult, QuizAnswer, QuizMode } from '@/types'
import { useWordsStore } from '@/stores/words'
import { useStatsStore } from '@/stores/stats'
import { useGamificationStore } from '@/stores/gamification'
import { shuffle } from '@/utils/shuffle'

export function useQuiz() {
  const wordsStore = useWordsStore()
  const statsStore = useStatsStore()

  const questions = ref<QuizQuestion[]>([])
  const currentIndex = ref(0)
  const answers = ref<QuizAnswer[]>([])
  const selectedAnswer = ref<number | null>(null)
  const showResult = ref(false)
  const isQuizComplete = ref(false)
  const quizMode = ref<QuizMode>('mixed')

  const currentQuestion = computed(() => questions.value[currentIndex.value] || null)

  const progress = computed(() => ({
    current: currentIndex.value + 1,
    total: questions.value.length,
    percent: questions.value.length > 0
      ? Math.round(((currentIndex.value + 1) / questions.value.length) * 100)
      : 0
  }))

  const quizResult = computed<QuizResult | null>(() => {
    if (!isQuizComplete.value) return null
    const correct = answers.value.filter(a => a.isCorrect).length
    return {
      mode: quizMode.value,
      total: answers.value.length,
      correct,
      incorrect: answers.value.length - correct,
      timestamp: new Date().toISOString(),
      answers: answers.value
    }
  })

  function generateQuiz(mode: QuizMode, count: number) {
    quizMode.value = mode
    currentIndex.value = 0
    answers.value = []
    selectedAnswer.value = null
    showResult.value = false
    isQuizComplete.value = false

    const pool = wordsStore.words.filter(w => w.pos && w.cefr)
    if (pool.length < 4) return

    const selected = shuffle(pool).slice(0, Math.min(count, pool.length))

    questions.value = selected.map((word, i) => {
      const actualMode = mode === 'mixed'
        ? (['word-to-meaning', 'word-to-pos', 'word-to-cefr'] as QuizMode[])[Math.floor(Math.random() * 3)]
        : mode

      return generateQuestion(word, actualMode, i, pool)
    })
  }

  function generateQuestion(
    word: VocabularyWord,
    mode: QuizMode,
    id: number,
    pool: VocabularyWord[]
  ): QuizQuestion {
    let question = ''
    let correctAnswer = ''
    let optionPool: string[] = []

    switch (mode) {
      case 'word-to-meaning': {
        question = `What does "${word.word}" mean?`
        correctAnswer = word.meaningUz || word.definition || ''
        const candidates = pool
          .filter(w => w.id !== word.id && (w.meaningUz || w.definition))
          .map(w => (w.meaningUz || w.definition || ''))
          .filter(m => m && m !== correctAnswer)
        optionPool = [...new Set(candidates)]
        break
      }
      case 'word-to-pos': {
        question = `What is the part of speech of "${word.word}"?`
        const primaryPOS = word.pos.split(/[,;]\s*/)[0].trim()
        correctAnswer = primaryPOS
        const allPOS = [...new Set(pool.map(w => w.pos.split(/[,;]\s*/)[0].trim()).filter(Boolean))]
        optionPool = allPOS.filter(p => p !== correctAnswer)
        break
      }
      case 'word-to-cefr': {
        question = `What is the CEFR level of "${word.word}"?`
        correctAnswer = word.cefr
        optionPool = ['A1', 'A2', 'B1', 'B2'].filter(c => c !== correctAnswer)
        break
      }
    }

    const shuffledOptions = shuffle(optionPool).slice(0, 3)
    const allOptions = shuffle([...shuffledOptions, correctAnswer])
    const correctIndex = allOptions.indexOf(correctAnswer)

    return {
      id,
      word,
      type: mode,
      question,
      options: allOptions,
      correctIndex
    }
  }

  function selectAnswer(index: number) {
    if (showResult.value) return
    selectedAnswer.value = index
    showResult.value = true

    const q = currentQuestion.value
    if (!q) return

    answers.value.push({
      questionId: q.id,
      wordId: q.word.id,
      selectedIndex: index,
      correctIndex: q.correctIndex,
      isCorrect: index === q.correctIndex
    })
  }

  function nextQuestion() {
    // Double-trigger (qayta-qayta bosib tanga olish) ning oldini olish
    if (isQuizComplete.value) return

    if (currentIndex.value < questions.value.length - 1) {
      currentIndex.value++
      selectedAnswer.value = null
      showResult.value = false
    } else {
      isQuizComplete.value = true
      if (quizResult.value) {
        statsStore.addQuizResult(quizResult.value)
        const correctAnswersCount = quizResult.value.correct
        if (correctAnswersCount > 0) {
          const gamificationStore = useGamificationStore()
          gamificationStore.addCoins(
            correctAnswersCount * 10,
            'Testni muvaffaqiyatli yakunladingiz!'
          )
        }
      }
    }
  }

  function resetQuiz() {
    questions.value = []
    currentIndex.value = 0
    answers.value = []
    selectedAnswer.value = null
    showResult.value = false
    isQuizComplete.value = false
  }

  return {
    questions,
    currentIndex,
    currentQuestion,
    selectedAnswer,
    showResult,
    isQuizComplete,
    progress,
    quizResult,
    quizMode,
    generateQuiz,
    selectAnswer,
    nextQuestion,
    resetQuiz
  }
}

export interface WordExample {
  en: string
  uz?: string
}

export interface WordSense {
  definition: string
  meaningUz: string
  example?: string
  exampleUz?: string
  examples?: WordExample[]
}

export interface VocabularyWord {
  id: number
  orderIndex: number
  word: string
  pos: string
  cefr: string
  definition: string
  meaningUz?: string
  example?: string
  exampleUz?: string
  examples?: WordExample[]
  senses?: WordSense[]
  column?: number
  row?: number
  source?: string
}

export type CEFRLevel = 'A1' | 'A2' | 'B1' | 'B2'

export type WordStatus = 'new' | 'learning' | 'mastered'

export interface WordProgress {
  wordId: number
  status: WordStatus
  correct: number
  incorrect: number
  lastReviewed: string | null
  nextReview: string | null
  interval: number
  favorite: boolean
}

export interface DailyStats {
  date: string
  wordsLearned: number
  wordsReviewed: number
  quizScore: number
  quizTotal: number
}

export interface UserSettings {
  dailyGoal: number
  theme: 'light' | 'dark' | 'system'
  showDefinitions: boolean
  showExamples: boolean
  flashcardAutoFlip: boolean
  quizQuestionCount: number
}

export interface QuizQuestion {
  id: number
  word: VocabularyWord
  type: QuizMode
  question: string
  options: string[]
  correctIndex: number
}

export type QuizMode = 'word-to-pos' | 'word-to-cefr' | 'word-to-meaning' | 'mixed'

export interface QuizResult {
  mode: QuizMode
  total: number
  correct: number
  incorrect: number
  timestamp: string
  answers: QuizAnswer[]
}

export interface QuizAnswer {
  questionId: number
  wordId: number
  selectedIndex: number
  correctIndex: number
  isCorrect: boolean
}

export interface FlashcardSession {
  words: VocabularyWord[]
  currentIndex: number
  isFlipped: boolean
  known: number[]
  learning: number[]
  again: number[]
}

export interface ReviewAction {
  type: 'again' | 'hard' | 'good' | 'easy'
}

export type SortOption = 'alphabetical' | 'cefr' | 'status'
export type FilterPOS = string | 'all'
export type FilterCEFR = CEFRLevel | 'all'
